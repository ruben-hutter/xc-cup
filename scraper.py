import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def get_flights(date, take_off_site):
    ranked_flights = {}
    base_url = f'https://www.xcontest.org/switzerland/en/flights/daily-score-pg/#filter[date]={date}@filter[country]=CH@filter[detail_glider_catg]=FAI3'
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(base_url)
        max_list_id = get_max_list_id(wait)
        count = 1
        for i in range(0, max_list_id+100, 100):
            print(f'Processing first flights {i+1}-{i+100}...')
            if i != 0:
                url = f'{base_url}@flights[start]={i}'
                driver.get(url)
                time.sleep(2) # TODO: refactor without sleep
            flights_table = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'XClist'))
            )
            flights_table_body = flights_table.find_element(By.TAG_NAME, 'tbody')
            flights = flights_table_body.find_elements(By.TAG_NAME, 'tr')
            for flight in flights:
                count = save_relevant_flights(flight, take_off_site, ranked_flights, count)
        return ranked_flights

    except TimeoutException as e:
        print('TimeoutException:', e)
        driver.quit()
        sys.exit(1)

    finally:
        driver.quit()


def save_relevant_flights(flight, take_off_site, ranked_flights, rank):
    cells = flight.find_elements(By.TAG_NAME, 'td')
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
    if pilot_name in ranked_flights:
        print(f'Pilot {pilot_name} already ranked')
    if launch_site == take_off_site and pilot_name not in ranked_flights:
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


def get_max_list_id(wait):
    xc_pager = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'XCpager'))
    )
    pager_links = xc_pager.find_elements(By.TAG_NAME, 'a')
    last_link = pager_links[-1]
    href_value = last_link.get_attribute('href')
    return int(href_value.split('=')[-1])


def export_flights(flights, date, take_off_site):
    print('Exporting flights to CSV...')
    with open(f'output/{date}_{take_off_site}.csv', 'w') as f:
        f.write('Rank,Take off time,Pilot name,Take off site,Distance (km),Route Type,Points,Avg speed (km/h),Glider\n')
        for pilot_name, flight in flights.items():
            f.write(f"{flight['rank']},{flight['take_off_time']},{pilot_name},{flight['distance']},{flight['route_type']},{flight['points']},{flight['avg_speed']},{flight['glider']}\n")
    print('Export complete!')


def get_date_and_take_off_site(event_id):
    # event_id in csv are integers from 1 to n
    event_id = int(event_id)
    with open('data/events.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if i == event_id - 1:
                print(f'Event found: {row[1]}, {row[2]}')
                return row[1], row[2]
    return None, None


def main():
    if len(sys.argv) != 2:
        print('Usage: python scraper.py <event_id>')
        sys.exit(1)
    event_id = sys.argv[1]
    date, take_off_site = get_date_and_take_off_site(event_id)
    if date is None or take_off_site is None:
        print('Event not found')
        sys.exit(1)

    flights = get_flights(date, take_off_site)
    # TODO: compare pilots with competing pilots
    export_flights(flights, date, take_off_site)
    # TODO: create nice pdf with the data


if __name__ == '__main__':
    main()
