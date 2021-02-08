from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

from utils import parse_table, to_json

path = 'C:\Program Files (x86)\Selenium\chromedriver.exe'
driver = webdriver.Chrome(path)
url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=fc15GG-KNts4sTUfTXSuaSBE.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=&value=&isDescending=false'

search_terms = sys.argv[1:]
# search_terms = "Form W-2", "Form 1095-C"

driver.get(url)

for term in search_terms:  # TODO листать страницы
    search = driver.find_element_by_id("searchFor")
    search.clear()
    search.send_keys(term)
    search.send_keys(Keys.RETURN)
    res = parse_table(driver.page_source)
    print(to_json(res, term))

driver.close()


