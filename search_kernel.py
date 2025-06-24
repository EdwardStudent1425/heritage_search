import requests
from bs4 import BeautifulSoup
import selenium
import csv
import os

# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import undetected_chromedriver as uc

import time




def sites_list_func(filename='available_sites.txt'):
    '''
    forms a list of available sites to pass it as an argument.
    '''
    if filename:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            sites = [line.strip() for line in file if line.strip()]
            print(sites)
            return sites


def kernel(query: str, sites_list):
    '''
    manages the search on different websites
    '''
    if not isinstance(query, str):
        return None
    url = ''
    for site in sites_list:
        # holodomor victims
        if site == 'https://victimsholodomor.org.ua/people-search/easytable/25-peoples-new.html':
            continue
            url = site

            options = FirefoxOptions()
            # options.headless = True  # вмикай, якщо хочеш запускати у фоні
            options.set_preference("general.useragent.override", 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

            driver = webdriver.Firefox() 
            # driver = webdriver.Firefox(
            #     # service=FirefoxService(GeckoDriverManager().install()),
            #     options=options
            # )

            driver.get(url)
            
            search_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "etsearch"))
            )
            search_input.clear()
            search_input.send_keys(query)
            search_input.submit()    

            #time to download a result
            time.sleep(3)
            print(driver.page_source)  

            # parse the data
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # parse a table
            table = soup.find('table')

            # headers for csv
            headers = []

            thead = table.find('thead')
            tr = thead.find('tr')
            td_list = tr.find_all('td')
            for td in td_list:
                headers.append(td.get_text(strip=True))

            # data for each header in csv
            data = []

            tbody = table.find('tbody')
            tr_list = tbody.find_all('tr')
            for tr in tr_list:
                td_list = tr.find_all('td')
                for td in td_list:
                    a_data = td.find('a')
                    data.append(a_data.get_text(strip=True))

            driver.quit()
            # results
            print(headers)
            print(data)
        elif site == 'https://martyrology.org.ua/':
            query_list = query.split(" ")
            surname = query_list[0] if len(query_list) > 0 else ""
            name = query_list[1] if len(query_list) > 1 else ""
            patronymic_name = query_list[2] if len(query_list) > 2 else ""

            url = 'https://martyrology.org.ua/result'

            page = 1
            all_cards = []

            while True:
                params = {
                    'SearchForm[surnameUA]': surname,
                    'SearchForm[nameUA]': name,
                    'SearchForm[patronymicUA]': patronymic_name,
                    'SearchForm[surnameRU]': '',
                    'SearchForm[birthRegion]': '',
                    'SearchForm[militaryUnit]': '',
                    'SearchForm[burialRegion]': '',
                    'SearchForm[burialCity]': '',
                    'SearchForm[burialVillage]': '',
                    'SearchForm[burialPlace]': '',
                    'page': page,
                    'per-page': 25
                }

                response = requests.get(url=url, params=params, verify=False, timeout=100)
                print(f"Page {page}: Status {response.status_code}")
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table')
                if not table:
                    break  # Більше сторінок немає

                tbody = table.find('tbody')
                tr_list = tbody.find_all('tr')
                if not tr_list:
                    break  # Більше рядків немає
                


                for tr in tr_list:
                    if not tr:
                        print("Stopped: No rows found on this page")
                        break
                    card = []
                    td_list = tr.find_all('td')
                    for td in td_list:
                        text = td.get_text(strip=True)
                        card.append(text if text else '-')
                    all_cards.append(card)

                print(f"Page {page} rows: {len(tr_list)}")
                page += 1  # Переходимо на наступну сторінку

            return all_cards



            

listok = sites_list_func('available_sites.txt')
query = 'Мельник Іван'
kernel(query, listok)