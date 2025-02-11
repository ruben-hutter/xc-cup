import csv
import sys
import time
import datetime
import argparse
import logging

from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 10
OUTPUT_DIR = Path("output")
DATA_DIR = Path("data")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

year = datetime.datetime.now().year
event_id = 0
date = ""
take_off_site = ""
participants = None

def get_flights():
    """
    Fetches flights from XContest and returns a dictionary of relevant flights
    """
    global participants

    participants = get_participants()
    if not participants:
        logger.error("No participants found for event")
        sys.exit(1)
    base_url = (
        f"https://www.xcontest.org/"
        f"{f'{year}/' if year != datetime.datetime.now().year else ''}"
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
                count = save_relevant_flights(flight, ranked_flights, count)

            prev_flights_table_id = flights_table_id

        return ranked_flights

    except TimeoutException as e:
        logger.exception(e)
        sys.exit(1)

    finally:
        driver.quit()


def _get_flights(driver, prev_flights_table_id):
    while True:
        flights_table = WebDriverWait(driver, TIMEOUT).until(
            lambda d: d.find_element(By.CLASS_NAME, "XClist"),
            "flights_table not found"
        )
        if flights_table.id != prev_flights_table_id:
            break
        time.sleep(0.2)

    flights_table_body = WebDriverWait(flights_table, TIMEOUT).until(
        lambda t: t.find_element(By.TAG_NAME, "tbody"),
        "flights_table_body not found"
    )
    flights = WebDriverWait(flights_table_body, TIMEOUT).until(
        lambda t: t.find_elements(By.TAG_NAME, "tr"),
        "flights not found"
    )
    return flights, flights_table.id


def save_relevant_flights(flight, ranked_flights, rank):
    cells = WebDriverWait(flight, TIMEOUT).until(
        lambda f: f.find_elements(By.TAG_NAME, "td"),
        "cells not found"
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
            "glider": glider
        }
        return rank + 1
    return rank


def get_participants():
    # TODO: maybe get participants from `swissleague.ch`
    participants = set()
    participants_file = DATA_DIR / str(year) / "participants" / f"{event_id}.csv"

    check_file_exists_and_not_empty(participants_file)

    with participants_file.open(newline="") as f:
        logger.debug(f"Reading participants from {participants_file}")
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            participants.add(row[0])

    return participants


def get_max_list_id(driver):
    xc_pager = WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.CLASS_NAME, "XCpager"),
        "XCpager not found"
    )
    pager_links = xc_pager.find_elements(By.TAG_NAME, "a")
    last_link = pager_links[-1]
    href_value = last_link.get_attribute("href")
    if href_value is None:
        return 0
    return int(href_value.split("=")[-1])


def export_flights(flights):
    global take_off_site

    logger.info("Exporting flights to CSV...")
    assert take_off_site is not None
    take_off_site = take_off_site.replace(" ", "_").lower()

    # create output folder if it doesn't exist
    output_path = OUTPUT_DIR / str(year)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{date}_{take_off_site}.csv"
    with file_path.open("w", newline="") as f:
        writer = csv.writer(f)
        header = [
            "Rank", "Take off time", "Pilot name", "Take off site",
            "Distance (km)", "Route Type", "Points", "Avg speed (km/h)", "Glider"
        ]
        writer.writerow(header)
        for pilot_name, flight in flights.items():
            writer.writerow([
                flight["rank"], flight["take_off_time"], pilot_name,
                take_off_site, flight["distance"], flight["route_type"],
                flight["points"], flight["avg_speed"], flight["glider"]
            ])
    logger.info("Export complete!")


def get_date_and_take_off_site():
    # event_id in csv are integers from 1 to n
    events_file = DATA_DIR / str(year) / "events.csv"

    check_file_exists_and_not_empty(events_file)

    with events_file.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if i == event_id - 1:
                logger.info(f"Event found: {row[1]}, {row[2]}")
                return row[1], row[2]

    return None, None

def check_file_exists_and_not_empty(file_path):
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)

    if file_path.stat().st_size == 0:
        logger.error(f"File is empty: {file_path}")
        sys.exit(1)


def export_to_pdf():
    logger.info("Exporting to PDF...")
    output_path = OUTPUT_DIR / str(year)
    pdf_file = output_path / f"{date}_{take_off_site}.pdf"
    csv_file = output_path / f"{date}_{take_off_site}.csv"

    if not csv_file.exists():
        logger.error(f"CSV file not found: {csv_file}")
        sys.exit(1)

    # TODO: logic to convert CSV to PDF
    logger.info(f"PDF file saved to {pdf_file}")


def args_parser():
    parser = argparse.ArgumentParser(description="Create XC Cup ranking for an event")
    parser.add_argument("event_id", type=int, help="event id as in events.csv")
    parser.add_argument("-y", "--year", type=int, help="year")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode")
    parser.add_argument("--pdf", action="store_true", help="export to PDF")
    return parser.parse_args()


def main():
    global event_id, year, date, take_off_site

    args = args_parser()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    event_id = args.event_id

    if args.year:
        if args.year < 2024 or args.year > datetime.datetime.now().year:
            logger.error("Invalid year")
            sys.exit(1)
        year = args.year

    date, take_off_site = get_date_and_take_off_site()
    if date is None or take_off_site is None:
        logger.error("Event not found")
        sys.exit(1)

    flights = get_flights()
    export_flights(flights)
    if args.pdf:
        export_to_pdf()


if __name__ == "__main__":
    main()

