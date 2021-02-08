from bs4 import BeautifulSoup


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


def to_json(data, term):
    filtered = [d for d in data if d['form_number'] == term]
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
