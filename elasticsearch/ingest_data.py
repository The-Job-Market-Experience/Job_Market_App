#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import csv
import os

mapping = {
    "mappings" : {
      "properties" : {
        "benefits" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "company" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "contract_type" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "description_title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "employment_status" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "job_title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "location" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "publish_date" : {
          "type" : "date"
        },
        "salary_avg" : {
          "type" : "float"
        },
        "salary_max" : {
          "type" : "float"
        },
        "salary_min" : {
          "type" : "float"
        },
        "website" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "work_mode" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }

# Connection to the cluster
es = Elasticsearch(hosts = "http://@localhost:9200")
print(es.ping())

# path to .csv file
file_path = os.path.join(os.path.dirname(__file__), 'merged.csv')
print(file_path)

# Delete the index if it already exists
if es.indices.exists(index='jobs'):
    es.indices.delete(index='jobs')
    
    
es.indices.create(index='jobs', body=mapping)

with open(file_path, newline="", encoding='utf-8') as f:
    reader = csv.DictReader(f,  delimiter=';')
    helpers.bulk(es, reader, index='jobs')