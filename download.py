from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import parse_table, to_json

path = 'C:\Program Files (x86)\Selenium\chromedriver.exe'
driver = webdriver.Chrome(path)
url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=fc15GG-KNts4sTUfTXSuaSBE.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=&value=&isDescending=false'

term = "Form W-2"
start_year = 2000
end_year = 2021

driver.get(url)
search = driver.find_element_by_id("searchFor")
search.clear()
search.send_keys(term)
search.send_keys(Keys.RETURN)
res = parse_table(driver.page_source)

links = []
for rec in res:
    if rec['form_number'] == term and start_year <= rec['year'] <= end_year + 1:
        links.append(rec['link'])

print(links)
