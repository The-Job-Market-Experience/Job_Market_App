#!/usr/bin/env python
# coding: utf-8

# In[21]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from time import sleep
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
driver = webdriver.Chrome()
driver.get("https://www.welcometothejungle.com/en/jobs")
sleep(5)
box=driver.find_element(By.ID,"search-query-field")
box.send_keys("data")
box.send_keys(Keys.ENTER)
box2=driver.find_element(By.ID,"search-location-field")
box2.clear()
box2.send_keys("germany")
# right click and copy full xpath
driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]").click()
sleep(2)
soup=BeautifulSoup(driver.page_source,"html.parser")
# here we landed to our destination page , so we have added code to get html
total_pages=int(soup.find("ul",class_="sc-faUjhM hwjokg").find_all("li")[-2].text)
page=0
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
            company = job.find('span', class_= 'sc-ERObt gTCEVh sc-6i2fyx-3 eijbZE wui-text').text.replace(' ','')
        except:
            company="not found"
        
        try:
            job_title = job.find('div', class_='sc-bXCLTC hlqow9-0 helNZg').text.replace(' ','')
        except:
            job_title="not found"
            
        try:
            contract_type = job.find('i', class_= 'sc-fUBkdm bizICt  wui-icon-font')
        except:
            contract_type="not found"
            
        try:
            location = job.find('span', class_= 'sc-68sumg-2 hCLwRn').text.replace(' ','')
        except:
            location="not found"
            
        try:
            remote_hybrid = job.find('div', class_= 'sc-dQEtJz cJTvEr').text.replace(' ','')
        except:
            remote_hybrid="not found"
            
        try:
            salary = job.find('i', class_= 'sc-fUBkdm kdzpUA  wui-icon-font')
        except:
            salary="not found"
        
        try:
            link = job.find('a', class_= 'sc-6i2fyx-0 gIvJqh')['href'] # get only link
        except:
            link="not found"
        
        try:
            time_tag = job.find('time')['datetime'].replace(' ','')
        except:
            time_tag="not found"


        # Sample data to be written into the CSV
        dict1={'Company Name': company, 
             'Job Title': job_title,
             'Contract Type': contract_type,
             'Location': location,
             'Attendance': remote_hybrid,
             'Salary': salary,
             'Publish Date': time_tag
            }

        data_to_append.append(dict1)
        # Function to append data to a CSV file


    # code to click on next page
    
    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div/div[2]/div/div[2]/nav/ul/li[4]/a").click()
    sleep(2)
    
def append_to_csv(data, file_name):
    # Specify the header of your CSV
    header = ['Company Name', 'Job Title', 'Contract Type','Location','Attendance','Salary','Publish Date']

    # Check if the file exists to determine whether to write headers or not
    try:
        with open(file_name, 'r', newline='') as file:
            empty = len(file.read()) == 0
    except FileNotFoundError:
        empty = True

    # Open the CSV file in append mode, if it doesn't exist, write the header
    with open(file_name, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header) #writer = csv.DictWriter(file, fieldnames=header)

        # Write header if the file is empty
        if empty:
            writer.writeheader()

        # Append data to the CSV
        for row in data:
            writer.writerow(row)

# Call the function to append data to the CSV
append_to_csv(data_to_append, 'job_postings.csv')


# In[ ]:




