import os
import csv
import sys
import time
import datetime
import argparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

year = datetime.datetime.now().year
event_id = 0
date = ''
take_off_site = ''
participants = None

timeout = 10

def get_flights():
    ranked_flights = {}
    global participants
    participants = get_participants()
    base_url = f'https://www.xcontest.org/switzerland/en/flights/daily-score-pg/#filter[date]={date}@filter[country]=CH@filter[detail_glider_catg]=FAI3'
    driver = webdriver.Firefox()

    try:
        driver.get(base_url)
        max_list_id = get_max_list_id(driver)
        count = 1
        prev_flights_table_id = ''
        for i in range(0, max_list_id + 100, 100):
            print(f'Processing first flights {i + 1}-{i + 100}...')
            if i != 0:
                url = f'{base_url}@flights[start]={i}'
                driver.get(url)
            flights, flights_table_id = _get_flights(driver, prev_flights_table_id)
            for flight in flights:
                count = save_relevant_flights(flight, ranked_flights, count)

            prev_flights_table_id = flights_table_id
        return ranked_flights

    except TimeoutException as e:
        print('TimeoutException:', e)
        driver.quit()
        sys.exit(1)

    finally:
        driver.quit()


def _get_flights(driver, prev_flights_table_id):
    while True:
        flights_table = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.CLASS_NAME, 'XClist'),
            message='flights_table not found'
        )
        if flights_table.id != prev_flights_table_id:
            break
        time.sleep(0.2)
    flights_table_body = WebDriverWait(flights_table, timeout).until(
        lambda t: t.find_element(By.TAG_NAME, 'tbody'),
        'flights_table_body not found'
    )
    flights = WebDriverWait(flights_table_body, timeout).until(
        lambda t: t.find_elements(By.TAG_NAME, 'tr'),
        'flights not found'
    )
    return flights, flights_table.id


def save_relevant_flights(flight, ranked_flights, rank):
    cells = WebDriverWait(flight, timeout).until(
        lambda f: f.find_elements(By.TAG_NAME, 'td'),
        'cells not found'
    )
    take_off_time = cells[1].text.splitlines()[0]
    pilot_name = cells[2].text
    launch_site = cells[3].text.splitlines()[1]
    route_type = (
        cells[4]
        .find_element(By.CSS_SELECTOR, 'div:nth-child(1)')
        .get_attribute('title')
    )
    distance = cells[5].text.split()[0]
    points = cells[6].text.split()[0]
    avg_speed = cells[7].text
    glider = (
        cells[8]
        .find_element(By.CSS_SELECTOR, 'div:nth-child(1)')
        .get_attribute('title')
    )
    if (
            launch_site == take_off_site
            and pilot_name not in ranked_flights
            and pilot_name in participants
    ):
        ranked_flights[pilot_name] = {
            'rank': rank,
            'take_off_time': take_off_time,
            'route_type': route_type,
            'distance': distance,
            'points': points,
            'avg_speed': avg_speed,
            'glider': glider
        }
        return rank + 1
    return rank


def get_participants():
    # TODO: maybe change to txt file
    participants = set()
    with open(f'data/{year}/participants/{event_id}.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            participants.add(row[0])
    return participants


def get_max_list_id(driver):
    xc_pager = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(By.CLASS_NAME, 'XCpager'),
        'XCpager not found'
    )
    pager_links = xc_pager.find_elements(By.TAG_NAME, 'a')
    last_link = pager_links[-1]
    href_value = last_link.get_attribute('href')
    if href_value is None:
        return 0
    return int(href_value.split('=')[-1])


def export_flights(flights):
    print('Exporting flights to CSV...')
    # create output folder if it doesn't exist
    try:
        os.makedirs(f'output/{year}')
    except FileExistsError:
        pass

    with open(f'output/{year}/{date}_{take_off_site}.csv', 'w') as f:
        f.write('Rank,Take off time,Pilot name,Take off site,Distance (km),Route Type,Points,Avg speed (km/h),Glider\n')
        for pilot_name, flight in flights.items():
            f.write(
                f"{flight['rank']},{flight['take_off_time']},{pilot_name},{flight['distance']},{flight['route_type']},{flight['points']},{flight['avg_speed']},{flight['glider']}\n"
            )
    print('Export complete!')


def get_date_and_take_off_site():
    # event_id in csv are integers from 1 to n
    with open(f'data/{year}/events.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if i == event_id - 1:
                print(f'Event found: {row[1]}, {row[2]}')
                return row[1], row[2]
    return None, None


def args_parser():
    parser = argparse.ArgumentParser(description='Scrape XContest for flights')
    parser.add_argument('event_id', type=int, help='Event ID')
    parser.add_argument('--year', type=int, help='Year')
    args = parser.parse_args()
    return args


def main():
    args = args_parser()
    # save event_id as integer
    global event_id
    event_id = int(args.event_id)
    if args.year:
        global year
        year = args.year

    global date
    global take_off_site
    date, take_off_site = get_date_and_take_off_site()
    if date is None or take_off_site is None:
        print('Event not found')
        sys.exit(1)

    flights = get_flights()
    export_flights(flights)
    # TODO: create nice pdf with the data


if __name__ == '__main__':
    main()
