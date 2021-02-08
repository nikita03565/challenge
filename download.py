import os
import sys

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import parse_table

path = 'C:\Program Files (x86)\Selenium\chromedriver.exe'
driver = webdriver.Chrome(path)
url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=fc15GG-KNts4sTUfTXSuaSBE.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=&value=&isDescending=false'

# term = "Form W-2"
# start_year = 2000
# end_year = 2021
try:
    term, start_year, end_year = sys.argv[1:]
    start_year = int(start_year)
    end_year = int(end_year)
except ValueError as e:
    sys.exit('Invalid input')

driver.get(url)
search = driver.find_element_by_id('searchFor')
search.clear()
search.send_keys(term)
search.send_keys(Keys.RETURN)
res = parse_table(driver.page_source)
filtered = [rec for rec in res if rec['form_number'].lower() == term.lower() and start_year <= rec['year'] <= end_year]

os.makedirs(filtered[0]['form_number'], exist_ok=True)
for f in filtered:
    r = requests.get(f['link'])
    with open(f'{term}/{f["form_number"]} - {f["year"]}.pdf', 'wb') as f:
        f.write(r.content)

driver.close()
print('done')
