import pandas as pd

def get_employment_status(x):
    full_time = 'Vollzeit' in str(x)
    part_time = 'Teilzeit' in str(x)
    
    if full_time and part_time: return 'Full time or Part time'
    if full_time: return 'Full time'
    if part_time: return 'Part time'
    
    return ''

def get_work_mode(x):
    if 'Home Office' in str(x): return 'Hybrid remote'
    return ''

contract_mapping = {
    'Feste Anstellung': 'Permanent contract',
    'Studentenjobs, Werkstudent': 'Internship',
    'Praktikum, Studentenjobs, Werkstudent': 'Internship',
    'Praktikum': 'Internship',
    'Befristeter Vertrag': 'Temporary contract',
    'Berufseinstieg/Trainee': 'Trainee',
    'Ausbildung, Studium': 'Internship',
    'Feste Anstellung, Berufseinstieg/Trainee': 'Permanent contract, Trainee',
    'Bachelor-/Master-/Diplom-Arbeiten': 'Bachelor Theses',
    'Promotion/Habilitation': 'Promotion',
    'Ausbildung, Studium, Praktikum': 'Internship',
    'Arbeitnehmerüberlassung, Befristeter Vertrag': 'Temporary Contract',
    'Befristeter Vertrag, Praktikum': 'Temporary Contract, Internship',
    'Freie Mitarbeit/Projektmitarbeit, Handelsvertreter': 'Freelance',
    'Arbeitnehmerüberlassung': 'Temporary contract',
    'Feste Anstellung, Berufseinstieg/Trainee': 'Permanent contract, Trainee',
    'Bachelor-/Master-/Diplom-Arbeiten, Praktikum': 'Bachelor Theses, Internship',
    'Feste Anstellung, Befristeter Vertrag': 'Permanent contract, Temporary contract',
    'Ausbildung, Studium, Praktikum': 'Internship'
}

############### Welcome to the jungle

df = pd.read_csv('./WttJ_jobs.csv.csv', sep =',')

# Split the 'salary' column
df[['salary_min', 'salary_max']] = df['salary_range'].str.split(' to ', expand=True)

# Remove 'k' and convert to integer
df['salary_min'] = df['salary_min'].str.rstrip('K').astype(float) * 1000
df['salary_max'] = df['salary_max'].str.rstrip('K').astype(float) * 1000
df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)

df['website'] = 'Welcome to the jungle'

############### Stepstone

df2 = pd.read_csv('./elasticsearch/jobs_stepstone.csv', sep =';')

# Split the 'salary' column
df2[['salary_min', 'salary_max']] = df2['salary_range'].str.split(' - ', expand=True)

# Remove 'k' and convert to integer
df2['salary_min'] = df2['salary_min'].astype(float) * 1000
df2['salary_max'] = df2['salary_max'].str.rstrip('€').astype(float) * 1000
df2['salary_avg'] = df2[['salary_min', 'salary_max']].mean(axis=1)

df2['website'] = 'stepstone'
df2['publish_date'] = df2['date']

# mapping columns for translation
df2['contract_type'] = df2['contract_type'].map(contract_mapping)
df2['employment_status'] = df2['work_type'].apply(get_employment_status)
df2['work_mode'] = df2['work_type'].apply(get_work_mode)

df2 = df2.drop(['date', 'work_type'], axis=1)

# Concatenate the DataFrames
df_final = pd.concat([df, df2], ignore_index=True)
df_final = df_final.drop(['salary_range'], axis=1)

# Cut time from the date
df_final['publish_date'] = df_final['publish_date'].apply(lambda x: x[:10])

# # Save the result to a new CSV file
df_final.to_csv('./elasticsearch/merged_jobs.csv', sep=';', index=False)