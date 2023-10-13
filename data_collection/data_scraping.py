### import libraries

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np

### request html code
### english language and germany. otherwise no parameter

url = 'https://www.stepstone.de/jobs/in-germany?radius=30'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}

response = requests.get(url, headers=headers)

## status print
print("the get request:", response)

### parse response with beautiful soup

soup = bs(response.content, 'html.parser')

### status print

print("created the beautiful soup for:", soup.title)

### job block, displayed on landing page for each job offer
jobs = soup.find_all('article', class_='res-j5y1mq')

job_titles, companies, locations, descriptions = [],[],[],[]

for job in jobs:
    job_title = job.find('div', class_='res-nehv70').text
    job_titles.append(job_title)
    
    company = job.find('span', class_='res-btchsq')
    companies.append(company.text)
    
    location = company.find_next('span', class_='res-btchsq')
    locations.append(location.text)
    
    description = job.find('div', class_='res-1d1eotm')
    descriptions.append(description.text)
    
df_new=pd.DataFrame(list(zip(job_titles, companies, locations, descriptions)), columns=['job_titles', 'companies', 'locations', 'descriptions'])

### save dataframe into .csv    
old_df = pd.read_csv('jobs.csv')
jobs = pd.concat([old_df, df_new], ignore_index=True)
jobs.to_csv('./jobs.csv')

### status print
print("the new file has", len(jobs), "entries")
                     
                     
                     
                     
                     
                     
                     
                     