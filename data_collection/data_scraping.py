### import libraries

from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
import pandas as pd
import numpy as np

import datetime

import json

### get current time

now = datetime.datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("the scraping starts at:", dt_string)

######################################################################

### request html code
### english language, data and germany. otherwise no parameter, sorted by publish date

url = 'https://www.stepstone.de/jobs/data/in-germany?radius=30&sort=2&action=sort_publish'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}

response = requests.get(url, headers=headers)

## status print
print("the get request:", response)

### parse response with beautiful soup

soup = bs(response.content, 'html.parser')

### status print

print("created the beautiful soup for:", soup.title)

## find and extract links to job offers

job_offer_links = []
links = soup.find_all("a", class_="res-y456gn")
base_url = 'https://www.stepstone.de'

for link in links:
    job_url = link.get('href')
    complete_job_url = urljoin(base_url, job_url)
    job_offer_links.append(complete_job_url)
    
print(len(job_offer_links), "new job offers found.")
###############################################################################

## parse and scrape from each job offer page
job_titles, companies, locations = [],[],[]
description_titles, descriptions, benefits = [],[],[]

for job_link in job_offer_links:
    print("scraping following job post:", job_link)
    job_response = requests.get(job_link, headers = headers)
    print("request status:", job_response.status_code)
    
    job_soup = bs(job_response.text, 'html.parser')
    
    job_title = job_soup.find('span', class_='listing-content-provider-bewwo')
    job_titles.append(job_title.text)
    
    company = job_soup.find('a', class_='listing-content-provider-zw6cpm')
    
    location_elements = job_soup.find_all('span', class_='listing-content-provider-1whr5zf')
    location_elements_list = [location.text for location in location_elements]
    locations.append(location_elements_list)
    
    benefit = job_soup.find('h4', class_='listing-company-content-provider-1nsjzge listingHeaderColor')
    
    description_title_elements = job_soup.find_all('h4', class_='listing-content-provider-1t9vh2w listingHeaderColor')
    description_title_list = [element.text for element in description_title_elements]
    description_titles.append(description_title_list)
    description_elements = job_soup.find_all('span', class_='listing-content-provider-14ydav7')
    description_list = [element.text for element in description_elements]
    descriptions.append(description_list)
    
    
    if company:
        companies.append(company.text)
    else:
        companies.append('not available')
        
    if benefit:
        benefit_elements = job_soup.find_all('span', class_='listing-company-content-provider-1mvot2o')
        benefit_list = [element.text for element in benefit_elements]
        benefits.append(benefit_list)
    else:
        benefits.append('not available')

#############################################################################



df_new=pd.DataFrame(list(zip(job_titles, companies, locations, description_titles, descriptions, benefits)), columns=['job_titles', 'companies', 'locations', 'description_titles', 'descriptions', 'benefits'])

df_new['time_of_scraping'] = pd.Series([dt_string] * len(df_new))

### save dataframe into .csv    
#old_df = pd.read_csv('jobs.csv', index_col=None)
#old_df = old_df.drop(['Unnamed: 0'], axis=1)
#jobs = pd.concat([old_df, df_new], ignore_index=True)
#jobs.to_csv('./jobs.csv')

## when initialized: #
df_new.to_csv('./jobs.csv', index=False)

### status print
print("the new file has", len(df_new), "entries")




                     
                     
                     
                     
                     
                     
                     
                     