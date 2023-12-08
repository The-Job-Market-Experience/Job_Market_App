#!/usr/bin/env python
# coding: utf-8

import csv
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



# arrive at first destination page

### for windows user:
# driver = webdriver.Chrome(ChromeDriverManager().install())

### for unix users:
driver = webdriver.Chrome()
driver.get("https://www.welcometothejungle.com/en/jobs")


# wait till element appears then cookie concent
wait = WebDriverWait(driver, 15)
wait.until(EC.visibility_of_element_located((By.ID, "axeptio_btn_dismiss"))).click()


# enter filter detail "data"
filter_detail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-query-field")))

filter_detail.clear()
filter_detail.send_keys("data")
filter_detail.send_keys(Keys.ENTER)



# fill in the value "Germany" and hit Enter as before
filter_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="search-location-field"]')))
filter_location.click()

# execute JavaScript to clear the input field
driver.execute_script('document.getElementById("search-location-field").value = "";')

filter_location.send_keys("Germany")
filter_location.send_keys(Keys.RETURN)




sleep(2)
soup=BeautifulSoup(driver.page_source,"html.parser")
# here we landed to our destination page , so we have added code to get html
total_pages=int(soup.find("ul",class_="sc-faUjhM hwjokg").find_all("li")[-2].text)
page=0

# an empty list to store job data
data_to_append=[]

while page<total_pages:
    page+=1
    soup=BeautifulSoup(driver.page_source,"html.parser")

    # apply for loop to find all job postings:
    jobs = soup.find_all('li', class_='sc-bXCLTC kkKAOM ais-Hits-list-item')

    # search within job entries company, job title, etc.
    # .text to only get text output
    # .replace to avoid white space
    for job in jobs:
        try:
            job_title = job.find('div', class_='sc-bXCLTC hlqow9-0 helNZg').text
        except AttributeError:
            job_title = None
        
        try:
            company = job.find('span', class_='sc-ERObt gTCEVh sc-6i2fyx-3 eijbZE wui-text').text
        except AttributeError:
            company = None
        
        try:
            publish_date = job.find('time')['datetime']
        except (AttributeError, TypeError):
            publish_date = None       
    
        try:
            location = job.find('span', class_='sc-68sumg-2 hCLwRn').text 
        except AttributeError:
            location = None
                   
        try:
            contract_type = job.find('div', class_='sc-dQEtJz cJTvEr').text 
        except AttributeError:
            contract_type = None
                      
        try:
            work_mode = job.find('i', attrs={'name': 'remote'}).find_next('span').text
        except AttributeError:
            work_mode = None
            
        try:
            salary_range = job.find('i', attrs={'name': 'salary'}).find_next('span').text
        except AttributeError:
            salary_range = None
        

        # data to be written into the CSV
        job_data={
                'job_title': job_title,
                'company': company, 
                'publish_date': publish_date,
                'location': location,
                'contract_type': contract_type,
                'employment_status': None,  # Empty field for employment status
                'work_mode': work_mode,
                'description_title': None,  # Empty field for description title
                'description': None,  # Empty field for description
                'salary_range': salary_range,
                'benefits': None  # Empty field for benefits
            }
      
        
        # Function to append data to a CSV file
        data_to_append.append(job_data)
        


    # code to click on next page
    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div/div[2]/div/div[2]/nav/ul/li[4]/a").click()
    sleep(2)
    
def append_to_csv(data, file_name):
    # Specify the header of your CSV
    header = ['job_title', 'company', 'publish_date', 'location', 'contract_type', 'employment_status', 
              'work_mode', 'description_title', 'description', 'salary_range', 'benefits']

    # Check if the file exists to determine whether to write headers or not
    try:
        with open(file_name, 'r', newline='') as file:
            empty = len(file.read()) == 0
    except FileNotFoundError:
        empty = True

    # Open the CSV file in append mode, if it doesn't exist, write the header
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=';')

        # Write header if the file is empty
        if empty:
            writer.writeheader()

        # Append data to the CSV
        for row in data:
            writer.writerow(row)

# Call the function to append data to the CSV
append_to_csv(data_to_append, 'WttJ_jobs.csv')





