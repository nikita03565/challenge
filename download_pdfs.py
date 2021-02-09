import sys

import requests

from utils import parse_table, get_next_link, get_page, download_pdfs


def execute():
    print('Started...')
    try:
        term, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    except (ValueError, IndexError) as e:
        sys.exit(f'Invalid input: {e.args}')
    page = get_page(term)
    result = []
    while True:
        result.extend(parse_table(page))
        next_link = get_next_link(page)
        if next_link is None:
            break
        page = requests.get(next_link).content
    filtered = [rec for rec in result if rec['form_number'].lower() == term.lower() and start <= rec['year'] <= end]
    download_pdfs(filtered)
    print('Done!')


if __name__ == '__main__':
    execute()
