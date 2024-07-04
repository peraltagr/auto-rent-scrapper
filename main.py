from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
import time

website = "https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos?regionslug=san-jose-provincia,heredia-provincia&q=f_rent.200000-300000|f_currency.CRC"

def scrape_all_apartments(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    scroll_pause_time = 2
    all_apartments_data = []

    try:
        while True:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.d3-ad-tile')))
            
            advertisements_tiles = driver.find_elements(By.CSS_SELECTOR, 'div.d3-ad-tile')

            for ad in advertisements_tiles:
                apartment_data = {}

                try:
                    price_element = ad.find_element(By.CLASS_NAME, 'd3-ad-tile__price')
                    apartment_data["price"] = price_element.text.strip()
                except:
                    apartment_data["price"] = "Price not found"

                try:
                    location_element = ad.find_element(By.CLASS_NAME, 'd3-ad-tile__location')
                    apartment_data["location"] = location_element.text.strip()
                except:
                    apartment_data["location"] = "Location not found"

                try:
                    ad_url_element = ad.find_element(By.TAG_NAME, "a")
                    apartment_data["ad_url"] = ad_url_element.get_attribute("href")
                except:
                    apartment_data["ad_url"] = "URL not found"

                all_apartments_data.append(apartment_data)

            next_page_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.d3-pagination__arrow--next')))
            if next_page_element:
                next_page_element.click()
                time.sleep(scroll_pause_time)
            else:
                break

    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")

    finally:
        driver.quit()

    return all_apartments_data

apartments_data = scrape_all_apartments(website)

def export_to_csv(apartments_data):
    current_date = datetime.now().strftime("%d-%m-%y")
    filename = f"apartments_data_{current_date}.csv"

    fields = ['price', 'location', 'ad_url']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for apartment in apartments_data:
            writer.writerow(apartment)

export_to_csv(apartments_data)
