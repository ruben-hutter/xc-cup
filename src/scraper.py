import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def get_flights(date, take_off_site):
    date = '2024-04-06' # TODO: just for testing
    base_url = f'https://www.xcontest.org/switzerland/en/flights/daily-score-pg/#filter[date]={date}@filter[country]=CH@filter[detail_glider_catg]=FAI3'
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(base_url)
        max_list_id = get_max_list_id(wait)
        for i in range(0, max_list_id+100, 100):
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
                print(flight.find_element(By.XPATH, 'td[3]').text)
    except TimeoutException as e:
        print('TimeoutException:', e)
        driver.quit()
        sys.exit(1)

    driver.quit()


def get_max_list_id(wait):
    xc_pager = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'XCpager'))
    )
    pager_links = xc_pager.find_elements(By.TAG_NAME, 'a')
    last_link = pager_links[-1]
    href_value = last_link.get_attribute('href')
    return int(href_value.split('=')[-1])


def main():
    if len(sys.argv) != 3:
        print('Usage: python scraper.py <date> <take-off site>')
        sys.exit(1)
    date = sys.argv[1]
    take_off_site = sys.argv[2]

    get_flights(date, take_off_site)


if __name__ == '__main__':
    main()
