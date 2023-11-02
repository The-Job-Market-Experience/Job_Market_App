from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging

import http.client
http.client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


url = 'https://www.stepstone.de/jobs/in-germany?radius=30&action=facet_selected%3bskills%3b673826&fsk=673826'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}

response = requests.get(url, headers=headers)

#print(response.text)

soup = bs(response.content, 'html.parser')

print(soup.find('time'))