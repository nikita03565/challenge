from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

from utils import parse_table, to_json, get_next_link, pretty_print

driver = webdriver.Chrome()
url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=fc15GG-KNts4sTUfTXSuaSBE.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=&value=&isDescending=false'

search_terms = sys.argv[1:]
# search_terms = "Form W-2", "Form 1095-C"

driver.get(url)

res_json = []
for term in search_terms:
    res = []
    search = driver.find_element_by_id("searchFor")
    search.clear()
    search.send_keys(term)
    search.send_keys(Keys.RETURN)
    while True:
        res.extend(parse_table(driver.page_source))
        next_link = get_next_link(driver)
        if next_link is None:
            break
        driver.get(next_link)
    data = to_json(res, term)
    if data is not None:
        res_json.append(data)

pretty_print(res_json)
driver.close()


