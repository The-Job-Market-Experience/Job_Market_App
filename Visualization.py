import pandas as pd
import matplotlib.pyplot as plt

####### distribution of avg_salary in Berlin

# Filter the DataFrame
df_berlin = df[df['location'] == 'Berlin']

# Create a bar plot of the 'salary_avg' column
df_berlin['salary_avg'].plot(kind='bar', legend=False)

# Show the plot
plt.show()



####### AVG salary in Berlin
# Filter the DataFrame
df_filtered = df[df['location'].isin(['Berlin'])]

# Group by 'location' and calculate the mean of 'salary_avg'
df_grouped = df_filtered.groupby('location')['salary_avg'].mean()

# Create a bar plot of the average salaries
df_grouped.plot(kind='bar', legend=False)

# Show the plot
plt.show()

####### distribution of avg_salary in Berlin, Hamburg and Munich

# Filter the DataFrame
df_filtered = df[df['location'].isin(['Berlin', 'Hamburg', 'Munich'])]

# Group by 'location' and calculate the mean of 'salary_avg'
df_grouped = df_filtered.groupby('location')['salary_avg'].mean()

# Create a bar plot of the average salaries
df_grouped.plot(kind='bar', legend=False)

# Show the plot
plt.show()
