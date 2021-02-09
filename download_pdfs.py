import sys

from utils import parse_table, get_next_link, get_page, download_pdfs, get_safe


def get_args():
    try:
        return sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    except (ValueError, IndexError) as e:
        if isinstance(e, IndexError):
            sys.exit('Invalid input: Not enough arguments, 3 must be given.')
        sys.exit('Invalid input: Year argument is not a valid integer.')


def execute():
    print('Started...')
    term, start, end = get_args()
    page = get_page(term)
    result = []
    while True:
        result.extend(parse_table(page))
        next_link = get_next_link(page)
        if next_link is None:
            break
        page = get_safe(next_link).content
    filtered = [rec for rec in result if rec['form_number'].lower() == term.lower() and start <= rec['year'] <= end]
    download_pdfs(filtered)
    print('Done!')


if __name__ == '__main__':
    execute()
