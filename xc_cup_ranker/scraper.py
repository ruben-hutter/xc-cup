import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from xc_cup_ranker.config import CURRENT_YEAR, TIMEOUT
from xc_cup_ranker.participants import get_participants
from xc_cup_ranker.utils import logger


def get_flights(
    year: int, event_id: int, date: str, take_off_site: str
) -> dict[str, dict]:
    """
    Fetches flights from XContest and returns a dictionary of relevant flights
    :param year: Year of the event
    :param event_id: ID of the event
    :param date: Date of the event
    :param take_off_site: Take off site of the event
    :return: Dictionary of relevant flights
    """
    participants = get_participants(year, event_id)

    base_url = (
        f"https://www.xcontest.org/"
        f"{f'{year}/' if year != CURRENT_YEAR else ''}"
        f"switzerland/en/flights/daily-score-pg/"
        f"#filter[date]={date}@filter[country]=CH@filter[detail_glider_catg]=FAI3"
    )

    driver = webdriver.Firefox()

    try:
        driver.get(base_url)
        max_list_id = get_max_list_id(driver)
        count = 1
        prev_flights_table_id = ""
        ranked_flights = {}

        for i in range(0, max_list_id + 100, 100):
            logger.info(f"Processing first flights {i + 1}-{i + 100}...")
            if i != 0:
                url = f"{base_url}@flights[start]={i}"
                driver.get(url)
            flights, flights_table_id = _get_flights(driver, prev_flights_table_id)
            for flight in flights:
                count = save_relevant_flights(
                    flight, ranked_flights, count, take_off_site, participants
                )

            prev_flights_table_id = flights_table_id

        return ranked_flights

    except TimeoutException as e:
        logger.exception(e)
        sys.exit(1)

    finally:
        driver.quit()


def _get_flights(
    driver: WebDriver, prev_flights_table_id: str
) -> tuple[list[WebElement], str]:
    while True:
        flights_table = WebDriverWait(driver, TIMEOUT).until(
            lambda d: d.find_element(By.CLASS_NAME, "XClist"), "flights_table not found"
        )
        if flights_table.id != prev_flights_table_id:
            break
        time.sleep(0.2)

    flights_table_body = WebDriverWait(flights_table, TIMEOUT).until(
        lambda t: t.find_element(By.TAG_NAME, "tbody"), "flights_table_body not found"
    )
    flights = WebDriverWait(flights_table_body, TIMEOUT).until(
        lambda t: t.find_elements(By.TAG_NAME, "tr"), "flights not found"
    )
    return flights, flights_table.id


def save_relevant_flights(
    flight: WebElement,
    ranked_flights: dict[str, dict],
    rank: int,
    take_off_site: str,
    participants: set,
) -> int:
    cells = WebDriverWait(flight, TIMEOUT).until(
        lambda f: f.find_elements(By.TAG_NAME, "td"), "cells not found"
    )
    take_off_time = cells[1].text.splitlines()[0]
    pilot_name = cells[2].text
    launch_site = cells[3].text.splitlines()[1]
    route_type = (
        cells[4]
        .find_element(By.CSS_SELECTOR, "div:nth-child(1)")
        .get_attribute("title")
    )
    distance = cells[5].text.split()[0]
    points = cells[6].text.split()[0]
    avg_speed = cells[7].text
    glider = (
        cells[8]
        .find_element(By.CSS_SELECTOR, "div:nth-child(1)")
        .get_attribute("title")
    )

    if (
        launch_site == take_off_site
        and pilot_name not in ranked_flights
        and pilot_name in participants
    ):
        ranked_flights[pilot_name] = {
            "rank": rank,
            "take_off_time": take_off_time,
            "route_type": route_type,
            "distance": distance,
            "points": points,
            "avg_speed": avg_speed,
            "glider": glider,
        }
        return rank + 1
    return rank


def get_max_list_id(driver: WebDriver) -> int:
    xc_pager = WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.CLASS_NAME, "XCpager"), "XCpager not found"
    )
    pager_links = xc_pager.find_elements(By.TAG_NAME, "a")
    last_link = pager_links[-1]
    href_value = last_link.get_attribute("href")
    if href_value is None:
        return 0
    return int(href_value.split("=")[-1])
