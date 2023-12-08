# -*- coding: utf-8 -*-

from fastapi import FastAPI
from elasticsearch import Elasticsearch
import warnings

warnings.filterwarnings("ignore")

# Connection to the cluster
client = Elasticsearch(hosts = "http://@localhost:9200")

app = FastAPI()

@app.get("/contract_types")
def get_contract_types():
    #Elasticsearch request
    response = client.search(index="jobs", body=query1)
    #get the query result
    result = dict(response)['aggregations']['results']['buckets']
    return parse_agg(result)

@app.get("/jobs_by_location")
def get_jobs_by_location():
    #Elasticsearch request
    response = client.search(index="jobs", body=query3)
    #get the query result
    result = dict(response)['aggregations']['results']['buckets']
    return parse_agg(result)

@app.get("/jobs_by_branch")
def get_jobs_by_branch():
    #Elasticsearch request
    response = client.search(index="jobs", body=query4)
    #get the query result
    result = dict(response)['aggregations']['results']['buckets']
    return result

@app.get("/internships_by_company")
def get_internships_by_company():
    #Elasticsearch request
    response = client.search(index="jobs", body=query2)
    #get the query result
    result = dict(response)['aggregations']['results']['buckets']
    return parse_agg(result)

# parse data from elasticsearch format
def parse_agg(data):
    result = {}
    for el in data:
        result[el["key"]] = el["doc_count"]
    return result
    

query1 = {
  "size": 0, 
  "aggs": {
    "results": {
      "terms": {
        "field": "contract_type.keyword",
        "size": 20
      }
    }
  }
}

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

query4 = {
  "size": 0,
  "aggs": {
    "results": {
      "filters": {
        "filters": {
          "engineer": { "match": { "job_title": "engineer" } },
          "scientist": { "match": { "job_title": "scientist" } },
          "analyst": { "match": { "job_title": "analyst" } },
          "devops": { "match": { "job_title": "devops" } }
        }
      }
    }
  }
}

