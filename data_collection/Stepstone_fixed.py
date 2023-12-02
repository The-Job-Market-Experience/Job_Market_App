# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:37:23 2023

@author: pedro
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from time import sleep

from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
import pandas as pd

import datetime

# arrive at first destination page
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.stepstone.de/candidate/login")


# wait till element appears then cookie concent
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.ID, "ccmgt_explicit_accept"))).click()


# our StepStone login credentials
username = "jobmarket096@gmail.com"
password = "kadfvkpi/()le457"

# Fill in login credentials
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lpca-login-registration-components-1gjafhs"))) # id = "stepstone-form-element-45"
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lpca-login-registration-components-1mjl559"))) # id = "stepstone-form-element-49"
# insert cedentials
username_field.send_keys(username)
password_field.send_keys(password)
#login
login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lpca-login-registration-components-lgbo0i")))
login_button.click()

sleep(5)
# enter filter detail "data"
filter_detail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-at="searchbar-keyword-input"]')))

filter_detail.clear()
filter_detail.send_keys("data")
filter_detail.send_keys(Keys.ENTER)

sleep(5)
# enter location filter
filter_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-at="searchbar-location-input"]')))

filter_location.clear()
filter_location.send_keys("Germany")
filter_location.send_keys(Keys.ENTER)


sleep(2)
# select drop down button
sorting_dropdown_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-at="sorting-dropdown-button"]')))
# click on the sorting dropdown button
sorting_dropdown_button.click()

# sort via datum (replace with the actual selector)
date_sorting = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'date')))
date_sorting.click()



### get current time

now = datetime.datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("the scraping starts at:", dt_string)
t0 = time.time()

######################################################################

### request html code
### english language, data and germany. otherwise no parameter, sorted by publish date

url = 'https://www.stepstone.de/jobs/data/in-germany?radius=30&sort=2&action=sort_publish&page='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

data = [] # data is stored in a list of rows where each row is a dictionary
max_jobs = 1000 # maximum number of rows we wish to retrieve
page = 1

# loop to handle the job pagination from the website
while(len(data) < max_jobs):
    page += 1
    response = requests.get(url + str(page), headers=headers)
    ### status print
    print("the get request:", response)
    
    ### soup for current page
    soup=bs(response.content,"html.parser")
    ### status print
    print("created the beautiful soup for:", soup.title)
    
    jobs = soup.select("a.res-y456gn")
    if len(jobs) == 0:
        break
    
    base_url = 'https://www.stepstone.de'
    
    for job in jobs: # loop to handle all jobs in the same page
        job_link = urljoin(base_url, job.get('href'))
        row = {}
        
        #get soup for the job page
        print("scraping job #", len(data), ':', job_link)
        driver.get(job_link)
        job_soup = bs(driver.page_source, 'html.parser')
        
        # these parameters are taken directly from some spans that cannot be seen in the browser
        row['job_title'] = job_soup.find('span', {"itemprop": "title"}).text
        row['company'] = job_soup.find('span', {"itemprop": "name"}).text
        row['date'] = job_soup.find('span', {"itemprop": "datePosted"}).text
        
        # salary, location, contract and work type are taken using the parent components
        salary_div = job_soup.find('div', class_="at-listing__list-icons_salary")
        if salary_div:
            row['salary_range'] = salary_div.find('strong').text
        
        location_li = job_soup.find('li', class_="at-listing__list-icons_location")
        if location_li:
            row['location'] = location_li.find('span', {"data-genesis-element": "TEXT"}).text
        
        contract_li = job_soup.find('li', class_="at-listing__list-icons_contract-type")
        if contract_li:
            row['contract_type'] = contract_li.find('span', {"data-genesis-element": "TEXT"}).text
        
        work_li = job_soup.find('li', class_="at-listing__list-icons_work-type")
        if work_li:
            row['work_type'] = work_li.find('span', {"data-genesis-element": "TEXT"}).text
        
        #benefit and descriptions taken in the same way as before
        benefit = job_soup.find('h4', class_='listing-company-content-provider-1nsjzge listingHeaderColor')
        if benefit:
            benefit_elements = job_soup.find_all('span', class_='listing-company-content-provider-1mvot2o')
            row['benefits'] = [element.text for element in benefit_elements]
        
        description_title_elements = job_soup.find_all('h4', class_='listing-content-provider-1t9vh2w listingHeaderColor')
        row['description_title'] = [element.text for element in description_title_elements]
        description_elements = job_soup.find_all('span', class_='listing-content-provider-14ydav7')
        row['description'] = [element.text for element in description_elements]
        
        data.append(row)


driver.quit()

print(len(data), 'jobs taken')
print('finished at page', page)
print('time taken:', time.time() -t0)

df = pd.DataFrame(data)
# SEPARATOR SET AS ; BECAUSE SOME FIELDS CONTAIN COMMAS
df.to_csv('../elasticsearch/jobs_stepstone.csv', index=False, sep = ';')