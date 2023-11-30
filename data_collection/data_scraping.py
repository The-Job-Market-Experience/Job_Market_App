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
job_titles, companies, locations, announcement_dates, work_types, contract_types = [],[],[],[],[],[]
description_titles, descriptions, benefits = [],[],[]

for job_link in job_offer_links:
    print("scraping following job post:", job_link)
    job_response = requests.get(job_link, headers = headers)
    print("request status:", job_response.status_code)
    
    if job_response.status_code == 200:
        job_soup = bs(job_response.text, 'html.parser')
        
        job_title = job_soup.find('span', class_='listing-content-provider-bewwo')
        job_titles.append(job_title.text)
        
        company = job_soup.find('a', class_='listing-content-provider-zw6cpm')
        
        ################################
        
        location_li = job_soup.find('li', class_='listing-content-provider-l3w8lv at-listing__list-icons_location js-map-offermetadata-link data-map-offermetadata-trigger')
        if location_li:
            location = location_li.find('span', class_='listing-content-provider-1whr5zf')
            locations.append(location.text)
        else:
            locations.append('not available')
            
        ###################################
            
        date_li = job_soup.find('li', class_='listing-content-provider-l3w8lv at-listing__list-icons_date')
        if date_li:
            announcement_date = date_li.find('span', class_='listing-content-provider-1whr5zf')
            announcement_dates.append(announcement_date.text)
        else:
            announcement_dates.append('not available')
            
        ###########################
        
        contract_type_li = job_soup.find('li', class_='listing-content-provider-l3w8lv at-listing__list-icons_contract-type')
        if contract_type_li:
            contract_type = contract_type_li.find('span', class_='listing-content-provider-1whr5zf')
            contract_types.append(contract_type.text)
        else:
            contract_types.append('not available')
            
        ###################################
        
        work_type_li = job_soup.find('li', class_='listing-content-provider-l3w8lv at-listing__list-icons_work-type')
        if work_type_li:
            work_type = work_type_li.find('span', class_='listing-content-provider-1whr5zf')
            work_types.append(work_type.text)
        else:
            work_types.append('not available')
            
        ###################################
        
    
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
    
    else:
        print('ERROR: There is an issue with the request')

#############################################################################


df_new=pd.DataFrame(list(zip(job_titles, companies, locations,announcement_dates, work_types, contract_types, description_titles, descriptions, benefits)), columns=['job_titles', 'companies', 'locations', 'announcement_dates', 'work_types', 'contract_types', 'description_titles', 'descriptions', 'benefits'])

df_new['time_of_scraping'] = pd.to_datetime(pd.Series([dt_string] * len(df_new)))

###############################################################################
## dealing with time of posting

# Extract the number and unit of time from 'anouncement_date'
extracted_data = df_new['announcement_dates'].str.extract(r'vor (\d+) (\w+)', expand=False)
# Assign the results of extraction to new columns
df_new['quantity'] = pd.to_numeric(extracted_data[0], errors='coerce')
df_new['unit'] = extracted_data[1]
# Check for NaN values in the 'quantity' column and replace them with zeros
df_new['quantity'].fillna(0, inplace=True)
# Convert time units to hours
df_new['quantity_in_hours'] = df_new.apply(
    lambda row: row['quantity'] if row['unit'] in ['Stunde', 'Stunden'] else row['quantity'] * 24 if row['unit'] in ['Tag', 'Tage'] else row['quantity'] * 7 * 24 if row['unit'] in ['Wochen', 'Woche'] else 0,
    axis=1
)
# Apply the time difference to obtain 'posting_time'
df_new['posting_time'] = df_new.apply(lambda row: row['time_of_scraping'] - datetime.timedelta(hours=row['quantity_in_hours']), axis=1)

###################################################################################
### save dataframe into .csv    
#old_df = pd.read_csv('listings.csv', index_col=None)
#df_new = pd.concat([old_df, df_new], ignore_index=True)
#df_new.to_csv('./listings.csv', index=False)

## when initializing 
df_new.to_csv('./listings.csv', index=False)

### status print
print("the new file has", len(df_new), "entries")




                     
                     
                     
                     
                     
                     
                     
                     