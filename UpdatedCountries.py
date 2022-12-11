import pandas as pd

df1 = pd.read_json('covid_data_2022-12-02.json')
df2 = pd.read_csv('countries.csv',encoding='latin-1')
# drop country from country.csv file
df2 = df2.drop('country',axis=1)
# rename country to name
df1 = df1.rename(columns={'Country': 'name'})
# lowercase them all
df1['name'] = df1['name'].str.lower()
df2['name'] = df2['name'].str.lower()
# merge the two df together with matching names
df3 = pd.merge(df1,df2,on='name')
# rename New Deaths to NewDeaths 
df3 = df3.rename(columns={'New Deaths': 'NewDeaths'})
# rename Total Deaths to TotalDeaths
df3 = df3.rename(columns={'Total Deaths': 'TotalDeaths'})
# capitalize each country name
df3['name'] = df3['name'].str.capitalize()
# save the file to a new updated countries.csv file
df3.to_csv('updated_countries.csv')
print("Newly updated csv file sucessfully created")