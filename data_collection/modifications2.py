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
job_titles, companies, locations, anouncement_date, vollzeit, contract_type = [],[],[],[],[],[]
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
    # I added to choose first element
    # location_elements = location_elements[0] I am creating if

    if location_elements:
        # if Sei einer der ersten Bewerber then skip to next element
        if "Sei einer der ersten Bewerber" in location_elements[0]:
            location_text = location_elements[1]
        else:
            location_text = location_elements[0]
    else:
        location_text = 'No info about location'
    

#  this is html :<a class="listing-content-provider-1ukm0vf" data-genesis-element="BASE" href="#location"><span class="listing-content-provider-uxgcen" data-genesis-element="ICON_CONTAINER"><svg aria-hidden="true" role="img" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 20 20" aria-labelledby="MapMarkerIcon-4"><title id="MapMarkerIcon-4">Map marker icon</title><path fill="currentColor" d="M9.998 9.833c.417 0 .77-.146 1.062-.437.292-.292.438-.646.438-1.063 0-.417-.146-.77-.438-1.062a1.444 1.444 0 00-1.062-.438c-.417 0-.77.146-1.062.438a1.444 1.444 0 00-.438 1.062c0 .417.146.771.438 1.063.291.291.645.437 1.062.437zm0 6.542c1.708-1.514 2.99-2.955 3.844-4.323.854-1.368 1.281-2.552 1.281-3.552 0-1.583-.493-2.861-1.479-3.833-.986-.973-2.201-1.459-3.646-1.459-1.445 0-2.66.486-3.646 1.459-.986.972-1.479 2.25-1.479 3.833 0 1 .427 2.184 1.281 3.552.855 1.368 2.136 2.809 3.844 4.323zm0 1.458a.967.967 0 01-.604-.187c-1.972-1.805-3.44-3.462-4.406-4.969C4.023 11.17 3.54 9.778 3.54 8.5c0-2.028.646-3.639 1.937-4.833 1.292-1.195 2.799-1.792 4.521-1.792s3.229.597 4.521 1.792c1.291 1.194 1.937 2.805 1.937 4.833 0 1.278-.483 2.67-1.448 4.177-.965 1.507-2.434 3.164-4.406 4.969a.732.732 0 01-.281.146 1.266 1.266 0 01-.323.041z"></path></svg></span><span class="listing-content-provider-1whr5zf" data-genesis-element="TEXT">Köln, Hamburg</span></a>

# I added .encode('iso-8859-1').decode('utf-8')
    # location_elements_list = [location.text.encode('iso-8859-1').decode('utf-8', errors='replace') for location in location_elements]
    location_elements_list = [location.text for location in location_text]
    locations.append(location_elements_list)
    
    benefit = job_soup.find('h4', class_='listing-company-content-provider-1nsjzge listingHeaderColor')
    
    description_title_elements = job_soup.find_all('h4', class_='listing-content-provider-1t9vh2w listingHeaderColor')
    description_title_list = [element.text for element in description_title_elements]
    description_titles.append(description_title_list)
    description_elements = job_soup.find_all('span', class_='listing-content-provider-14ydav7')
    description_list = [element.text for element in description_elements]
    descriptions.append(description_list)
    
    #############################################################################  anouncment_date
    
    anouncment_date_elements = job_soup.find_all('span', class_='listing-content-provider-1whr5zf')
    # I added to choose first element
    # location_elements = location_elements[0] I am creating if

    anouncment_date_text = anouncment_date_elements[-1]
    anouncment_date_elements_list = [anouncment.text for anouncment in anouncment_date_text]
    anouncement_date.append(anouncment_date_elements_list)

    #############################################################################  vollzeit
    
    vollzeit_elements = job_soup.find_all('span', class_='listing-content-provider-1whr5zf')
    # I added to choose first element
    # location_elements = location_elements[0] I am creating if

    vollzeit_text = vollzeit_elements[-2]
    vollzeit_elements_list = [vollzeit.text for vollzeit in vollzeit_text]
    vollzeit.append(vollzeit_elements_list)

    ############################################################################# contract_type

    contract_type_elements = job_soup.find_all('span', class_='listing-content-provider-1whr5zf')
    # I added to choose first element
    # location_elements = location_elements[0] I am creating if

    contract_type_text = contract_type_elements[-2]
    contract_type_elements_list = [contract_type.text for contract_type in contract_type_text]
    contract_type.append(contract_type_elements_list)

    #############################################################################
    
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



df_new=pd.DataFrame(list(zip(job_titles, companies, locations, anouncement_date, vollzeit, contract_type, description_titles, descriptions, benefits)), columns=['job_titles', 'companies', 'locations', 'anouncement_date', 'vollzeit', 'contract_type' , 'description_titles', 'descriptions', 'benefits'])

df_new['time_of_scraping'] = pd.Series([dt_string] * len(df_new))

### save dataframe into .csv    
old_df = pd.read_csv('jobs.csv')
jobs = pd.concat([old_df, df_new], ignore_index=True)
jobs.to_csv('./jobs.csv')

## when initialized: #df_new.to_csv('./jobs.csv')

### status print
print("the new file has", len(jobs), "entries")

