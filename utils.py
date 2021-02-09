import json
import os

import requests
from bs4 import BeautifulSoup
from urllib import parse


base_url = 'https://apps.irs.gov'


def get_page(search_term=''):
    value = parse.quote(search_term)
    url = f'{base_url}/app/picklist/list/priorFormPublication.html?value={value}&criteria=formNumber&submitSearch=Find'
    html_page = requests.get(url).content
    page_size_link = get_largest_page_size_link(html_page)
    if page_size_link:
        html_page = requests.get(page_size_link).content
    return html_page


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


def get_next_link(page):
    soup = BeautifulSoup(page, 'lxml')
    pagination = soup.find('div', {'class': 'paginationBottom'})
    if not pagination:
        return
    links = pagination.find_all('a', href=True)
    next_link = f'{base_url}{links[-1]["href"]}' if links and 'Next' in links[-1].text else None
    return next_link


def get_largest_page_size_link(html_page):
    soup = BeautifulSoup(html_page, 'lxml')
    page_size = soup.find('th', {'class': 'NumResultsDisplayed'})
    if not page_size:
        return
    links = page_size.find_all('a', href=True)
    page_size_link = f'{base_url}{links[-1]["href"]}' if links and '200' in links[-1].text else None
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
