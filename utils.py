import json
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_driver(search_term=None, driver_instance=None):
    if driver_instance is None:
        driver = webdriver.Chrome()
        url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'
        driver.get(url)
    else:
        driver = driver_instance
    if search_term is None:
        return driver
    search = driver.find_element_by_id('searchFor')
    search.clear()
    search.send_keys(search_term)
    search.send_keys(Keys.RETURN)
    page_size_link = get_largest_page_size_link(driver)
    if page_size_link:
        driver.get(page_size_link)
    return driver


def pretty_print(data):
    print(json.dumps(data, sort_keys=True, indent=4, default=str))


def parse_table(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'class': 'picklist-dataTable'})
    header, *rows = table.find_all('tr')
    res = []
    for row in rows:
        ds = row.find_all('td')
        res.append({
            'form_number': ds[0].text.strip(), 'title': ds[1].text.strip(), 'year': int(ds[2].text),
            'link': ds[0].a['href']
        })
    return res


def get_next_link(driver):
    pagination = driver.find_elements_by_class_name('paginationBottom')
    if not pagination:
        return
    pagination_links = pagination[0].find_elements_by_tag_name('a')
    next_link = pagination_links[-1].get_attribute('href') if pagination_links and 'Next' in pagination_links[-1].text else None
    return next_link


def get_largest_page_size_link(driver):
    page_size = driver.find_elements_by_class_name('NumResultsDisplayed')
    if not page_size:
        return
    page_size_links = page_size[0].find_elements_by_tag_name('a')
    page_size_link = page_size_links[-1].get_attribute('href') if page_size_links and '200' in page_size_links[-1].text else None
    return page_size_link


def get_dict_data(data, term):
    filtered = [d for d in data if d['form_number'].lower() == term.lower()]
    if not filtered:
        return None
    min_year = min(f['year'] for f in filtered)
    max_record = max(filtered, key=lambda f: f['year'])
    return {
        'form_number': filtered[0]['form_number'],
        'title': max_record['title'],
        'min_year': min_year,
        'max_year': max_record['year']
    }


def download_pdfs(data):
    if not data:
        return
    dir_name = data[0]['form_number']
    os.makedirs(dir_name, exist_ok=True)
    for pdf_info in data:
        r = requests.get(pdf_info['link'])
        with open(f'{dir_name}/{pdf_info["form_number"]} - {pdf_info["year"]}.pdf', 'wb') as file:
            file.write(r.content)
