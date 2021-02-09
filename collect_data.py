import sys

from utils import parse_table, get_dict_data, get_next_link, pretty_print, get_page, get_safe


def execute():
    print('Started...')
    search_terms = sys.argv[1:]
    result = []
    for term in search_terms:
        res = []
        page = get_page(term)
        while True:
            res.extend(parse_table(page))
            next_link = get_next_link(page)
            if next_link is None:
                break
            page = get_safe(next_link).content
        data = get_dict_data(res, term)
        if data is not None:
            result.append(data)
    print('Done!')
    pretty_print(result)


if __name__ == '__main__':
    execute()
