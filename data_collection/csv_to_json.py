import csv, json

jobs_csv= 'jobs.csv'
jobs_json = 'jobs_dict.json'

## read csv file and add to data

data = {}
with open(jobs_csv, encoding='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        key = rows[""]
        data[key] = rows

## create new json file and write data in it

with open(jobs_json, 'w', encoding='utf-8') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))