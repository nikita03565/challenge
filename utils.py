import asyncio
import json
import os
import sys
from urllib import parse

import aiofiles
import aiohttp
import requests
from aiohttp.client_exceptions import ClientConnectionError
from bs4 import BeautifulSoup
from requests.exceptions import BaseHTTPError, ConnectionError

base_url = 'https://apps.irs.gov'


def get_safe(url):
    try:
        return requests.get(url)
    except (BaseHTTPError, ConnectionError):
        sys.exit(f'Failed to access {url}')


def get_page(search_term=''):
    value = parse.quote(search_term)
    url = f'{base_url}/app/picklist/list/priorFormPublication.html?value={value}&criteria=formNumber&submitSearch=Find'
    html_page = get_safe(url).content
    page_size_link = get_largest_page_size_link(html_page)
    if page_size_link:
        html_page = get_safe(page_size_link).content
    return html_page


def pretty_print(data):
    print(json.dumps(data, sort_keys=True, indent=4, default=str))


def parse_table(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'class': 'picklist-dataTable'})
    if not table:
        return []
    res = []
    rows = table.find_all('tr')
    for row in rows[1:]:  # skipping header
        ds = row.find_all('td')
        if len(ds) == 3:
            res.append({
                'form_number': ds[0].text.strip(), 'form_title': ds[1].text.strip(), 'year': int(ds[2].text),
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
        'form_title': max_record['form_title'],
        'min_year': min_year,
        'max_year': max_record['year']
    }


async def fetch_document(pdf_data, session):
    try:
        async with session.get(pdf_data['link']) as response:
            if response.status == 200:
                r = await response.read()
                filename = f'{pdf_data["form_number"]}/{pdf_data["form_number"]} - {pdf_data["year"]}.pdf'
                return r, filename
            print(f'File {pdf_data["link"]} was not found')
    except ClientConnectionError:
        sys.exit(f'Failed to download file from {pdf_data["link"]} because of connection')


async def fetch_documents(pdf_data, session):
    tasks = []
    for data in pdf_data:
        task = asyncio.create_task(fetch_document(data, session))
        tasks.append(task)
    return await asyncio.gather(*tasks)


async def download_pdfs(data):
    if not data:
        return
    dir_name = data[0]['form_number']
    try:
        os.makedirs(dir_name, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            result = await fetch_documents(data, session)
            for res in result:
                if res is not None:
                    content, filename = res
                    f = await aiofiles.open(filename, mode='wb')
                    await f.write(content)
                    await f.close()
    except (OSError, PermissionError):
        sys.exit('Failed to save documents on disc')
