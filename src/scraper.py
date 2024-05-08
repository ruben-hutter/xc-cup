import sys
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
            print(f'Processing first {i} flights...')
            if i != 0:
                # skip reloading the first page
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
    take_off_time = cells[1].text
    pilot_name = cells[2].text
    launch_site = cells[3].text.splitlines()[1]
    # TODO: get route_type from cells[4]
    distance = cells[5].text
    points = cells[6].text
    avg_speed = cells[7].text
    # TODO: get glider from cells[8]
    if launch_site == take_off_site and pilot_name not in ranked_flights:
        ranked_flights[pilot_name] = {
            'rank': rank,
            'take_off_time': take_off_time,
            'distance': distance,
            'points': points,
            'avg_speed': avg_speed
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


def export_flights(flights):
    print('Exporting flights to CSV...')
    with open('../output/flights.csv', 'w') as f:
        f.write('Rank,Take off time,Pilot name,Take off site,Distance,Points,Avg speed\n')
        for pilot_name, flight in flights.items():
            f.write(f"{flight['rank']},{flight['take_off_time']},{pilot_name},{flight['distance']},{flight['points']},{flight['avg_speed']}\n")
    print('Export complete!')


def main():
    if len(sys.argv) != 3:
        print('Usage: python scraper.py <date> <take-off site>')
        sys.exit(1)
    date = sys.argv[1]
    take_off_site = sys.argv[2]

    flights = get_flights(date, take_off_site)
    export_flights(flights)


if __name__ == '__main__':
    main()
