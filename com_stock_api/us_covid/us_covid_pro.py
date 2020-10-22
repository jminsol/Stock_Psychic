import pandas as pd
import os


path = os.path.abspath(__file__+"/.."+"/data")

# 1. Preprocessing California covid cases which is organized by county to the total numebers
'''
df = pd.read_csv(path + "/statewide_cases.csv")

df.drop('county', axis = 1, inplace=True)
df.drop('newcases', axis = 1, inplace=True)
df.drop('newdeaths', axis = 1, inplace=True)
# print(df.head())
  
dfout = df.groupby(['date']).sum()
dfout.reset_index(level=0, inplace=True)
finaldf = dfout[['date', 'cases', 'deaths']]
finaldf.columns = ['date', 'ca_cases', 'ca_deaths']
finaldf.to_csv(path+"/ca.csv", index=False)


# print(finaldf.head())
'''

#2. Change their date type, float to integer

df = pd.read_csv(path+"/ca.csv")
df_us = pd.read_csv(path+"/us.csv")

df_all = pd.merge(df_us, df, on=['date','date'], how='left')

df_all['total_cases'] = pd.to_numeric(df_all['total_cases'], errors='coerce').fillna(0).astype(int)
df_all['total_deaths'] = pd.to_numeric(df_all['total_deaths'], errors='coerce').fillna(0).astype(int)
df_all['ca_cases'] = pd.to_numeric(df_all['ca_cases'], errors='coerce').fillna(0).astype(int)
df_all['ca_deaths'] = pd.to_numeric(df_all['ca_deaths'], errors='coerce').fillna(0).astype(int)

df_all.to_csv(path+"/covid.csv")
print(df_all.head())