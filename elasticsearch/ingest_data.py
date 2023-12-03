#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv
import os
import pandas as pd

# Connection to the cluster
es = Elasticsearch(hosts = "http://@localhost:9200")
print(es.ping())

# path to .csv file
file_path = os.path.join(os.path.dirname(__file__), 'jobs_stepstone.csv')
print(file_path)

# Delete the index if it already exists
if es.indices.exists(index='jobs_stepstone'):
    es.indices.delete(index='jobs_stepstone')

with open(file_path, newline="", encoding='utf-8') as f:
    reader = csv.DictReader(f,  delimiter=';')
    helpers.bulk(es, reader, index='jobs_stepstone')