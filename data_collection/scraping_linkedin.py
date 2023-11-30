# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:45:46 2023

@author: pedro
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

data = []
max_jobs = 10 #Number of jobs to be retrieved

def parse_job(job):
    entry = {}
    
    entry['title'] = job.find('h3').text.strip()
    entry['company'] = job.find('h4').text.strip()
    entry['location'] = job.find('span', class_='job-search-card__location').text.strip()
    entry['published'] = job.find('time').attrs['datetime']
    
    job_url = job.find('a').attrs['href']
    job_response = requests.get(job_url)
    job_soup = bs(job_response.content, "html.parser")
    
    summary_div = job_soup.find('div', class_='show-more-less-html__markup')
    if (summary_div):
        entry['summary'] = summary_div.text.strip()
    
    extra_info = job_soup.find('ul', class_='description__job-criteria-list')
    if (extra_info):
        info_params = extra_info.find_all('h3')
        info_values = extra_info.find_all('span')
        for param, value in zip(info_params, info_values):
            entry[param.text.strip()] = value.text.strip()
    
    data.append(entry)  



base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location=Germany&position=1&pageNum=0&start='
index = 0

import time
 
t0 = time.time()

while index < max_jobs:
    url = base_url + str(index)
    response = requests.get(url)
    soup = bs(response.content, "html.parser")
    print("Getting job #{} ...".format(index+1))
    index += 25
    job_titles = soup.select('li > div.base-card.relative')
    
    for job in job_titles:
        parse_job(job)

   
#print(data[0])    
print("elements retrieved", len(data))
print("time taken", time.time() -t0)

df = pd.DataFrame(data)
df.to_csv('../elasticsearch/jobs_linkedin.csv', index=False)