# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:45:46 2023

@author: pedro
"""

import requests
from bs4 import BeautifulSoup as bs

url_api = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Product%20Management&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=0'

url = 'https://www.linkedin.com/jobs/search?position=1&pageNum=0'

response = requests.get(url)
 
soup = bs(response.content, "html.parser")


job_titles = soup.find_all('h3', class_='base-search-card__title')


for job in job_titles:
    print(job.text.strip())
    