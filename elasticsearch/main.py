# -*- coding: utf-8 -*-

from fastapi import FastAPI
from elasticsearch import Elasticsearch
import warnings

warnings.filterwarnings("ignore")

# Connection to the cluster
client = Elasticsearch(hosts = "http://@localhost:9200")

query2 = {
  "size": 0,
  "query": {
    "match": {
      "contract_type": {
        "query": "Internship Trainee"
      }
    }
  },
  "aggs": {
    "results": {
      "terms": {
        "field": "company.keyword",
        "size": 20
      }
    }
  }
}

query3 = {
  "size": 0,
  "query": {
    "match": {
      "job_title": {
        "query": "Data"
      }
    }
  },
  "aggs": {
    "results": {
      "terms": {
        "field": "location.keyword",
        "size": 100,
        "min_doc_count": 5
      }
    }
  }
}

app = FastAPI()

@app.get("/internships_by_company")
def get_internships_by_company():
    response = client.search(index="jobs", body=query2)
    result = dict(response)['aggregations']['results']['buckets']
    print(result)
    return result

@app.get("/jobs_by_location")
def get_jobs_by_location():
    print('hola')
    response = client.search(index="jobs", body=query3)
    print(response)
    result = dict(response)['aggregations']['results']['buckets']
    print(result)
    return result