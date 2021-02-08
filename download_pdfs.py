import sys

from utils import parse_table, get_next_link, get_driver, download_pdfs


def execute():
    try:
        term, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    except (ValueError, IndexError) as e:
        sys.exit(f'Invalid input: {e.args}')
    driver = get_driver(term)
    result = []
    while True:
        result.extend(parse_table(driver.page_source))
        next_link = get_next_link(driver)
        if next_link is None:
            break
        driver.get(next_link)
    filtered = [rec for rec in result if rec['form_number'].lower() == term.lower() and start <= rec['year'] <= end]
    download_pdfs(filtered)
    driver.close()
    print('done')


if __name__ == '__main__':
    execute()
