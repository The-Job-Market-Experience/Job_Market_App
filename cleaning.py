import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############### Stepstone Welcome to the jungle

df = pd.read_csv('WttJ_jobs_new.csv', sep =',')



# Split the 'salary' column
df[['salary_min', 'salary_max']] = df['salary_range'].str.split(' to ', expand=True)

# Remove 'k' and convert to integer
df['salary_min'] = df['salary_min'].str.rstrip('K').astype(float) * 1000
df['salary_max'] = df['salary_max'].str.rstrip('K').astype(float) * 1000


df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)


############### Stepstone


# df.to_csv('WttJ_jobs_new_cleaned.csv', index=False)

df2 = pd.read_csv('jobs_stepstone2.csv', sep =';')
# First I change it to datetime to be sure that all is same format and then I change to YYYY-MM-DD HH-MM
df2['date'] = pd.to_datetime(df2['date'])
df2['date'] = df2['date'].dt.strftime('%Y-%m-%d %H:%M')


# Split the 'salary' column
df2[['salary_min', 'salary_max']] = df2['salary_range'].str.split(' - ', expand=True)

# Remove 'k' and convert to integer
df2['salary_min'] = df2['salary_min'].astype(float) * 1000
df2['salary_max'] = df2['salary_max'].str.rstrip('€').astype(float) * 1000


df2['salary_avg'] = df2[['salary_min', 'salary_max']].mean(axis=1)

# Concatenate the DataFrames
df = pd.concat([df, df2])

df.head(10)


# # Save the result to a new CSV file
# df.to_csv('merged.csv', index=False)