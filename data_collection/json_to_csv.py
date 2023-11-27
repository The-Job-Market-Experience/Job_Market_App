import pandas as pd
import json

with open('jobs_dict.json', 'r', encoding='utf-8') as inputfile:
    data = json.load(inputfile)

df = pd.DataFrame.from_dict(data, orient='index')
df.to_csv('jobs.csv', encoding='utf-8', index=False)