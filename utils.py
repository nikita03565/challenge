import asyncio
import json
import os
import sys
from urllib import parse

import aiofiles
import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
from bs4 import BeautifulSoup

base_url = 'https://apps.irs.gov'


async def get_safe(url, session):
    try:
        async with session.get(url) as response:
            return await response.read()
    except ClientConnectionError:
        sys.exit(f'Failed to load {url} because of connection')


async def get_page(search_term, session):
    value = parse.quote(search_term)
    url = f'{base_url}/app/picklist/list/priorFormPublication.html?value={value}&criteria=formNumber&submitSearch=Find'
    html_page = await get_safe(url, session)
    page_size_link = get_largest_page_size_link(html_page)
    if page_size_link:
        html_page = await get_safe(page_size_link, session)
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


def get_dict_data(data):
    min_year = min(f['year'] for f in data)
    max_record = max(data, key=lambda f: f['year'])
    return {
        'form_number': data[0]['form_number'],
        'form_title': max_record['form_title'],
        'min_year': min_year,
        'max_year': max_record['year']
    }


async def fetch_document(pdf_data, session):
    url = pdf_data['link']
    try:
        async with session.get(url) as response:
            if response.status == 200:
                print(f'Downloaded file {url}')
                r = await response.read()
                filename = f'{pdf_data["form_number"]}/{pdf_data["form_number"]} - {pdf_data["year"]}.pdf'
                return r, filename
            print(f'File {url} was not found')
    except ClientConnectionError:
        sys.exit(f'Failed to download file from {url} because of connection')


async def fetch_documents(pdf_data, session):
    tasks = [asyncio.create_task(fetch_document(data, session)) for data in pdf_data]
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
                    print(f'Saved file {filename}')
    except (OSError, PermissionError):
        sys.exit('Failed to save documents on disc')


def get_all_found_names(data):
    return set(d['form_number'] for d in data)


def filter_none(lst):
    return [item for item in lst if item is not None]
