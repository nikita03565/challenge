import sys

from utils import parse_table, get_dict_data, get_next_link, pretty_print, get_driver


def execute():
    driver = get_driver()
    search_terms = sys.argv[1:]
    result = []
    for term in search_terms:
        res = []
        driver = get_driver(term, driver)
        while True:
            res.extend(parse_table(driver.page_source))
            next_link = get_next_link(driver)
            if next_link is None:
                break
            driver.get(next_link)
        data = get_dict_data(res, term)
        if data is not None:
            result.append(data)

    pretty_print(result)
    driver.close()


if __name__ == '__main__':
    execute()
