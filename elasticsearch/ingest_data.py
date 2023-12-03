#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv
import os

# Connection to the cluster
es = Elasticsearch(hosts = "http://@localhost:9200")
print(es.ping())

# path to .csv file
file_path = os.path.join(os.path.dirname(__file__), 'jobs_stepstone.csv')
print(file_path)

# Specify the delimiter as ;
delimiter = ';'

with open(file_path, encoding='utf-8') as f:
    reader = csv.DictReader(f,  delimiter=delimiter)
    helpers.bulk(es, reader, index='jobs_stepstone')