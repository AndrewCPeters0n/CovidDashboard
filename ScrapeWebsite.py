import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import date
from datetime import timedelta

def scrape_country(country, url):
    # Regular Expression pattern to remove unnecessary whitespace from html data
    wspace = re.compile(r'\s+')
    
    # String to initially hold country data
    outstr = ''
    
    # List to temporarily hold country data
    tempdata = []
    
    # Output list used to hold data with properly converted data types
    outdata = []
    
    # Obtaining html data from provided URL
    request = requests.get(url)
    
    # Parse through html data
    soup = BeautifulSoup(request.content, 'html5lib')
    
    # Navigate through html data to find the appropriate data table, then find all tags containing table data
    cd_data = soup.find('table', attrs = {'id':'main_table_countries_yesterday'}).find('tbody').find_all('td')

    # Iterate through all tags found above to check for the provided country name, then extract the data about that country
    # The string "outstr" is delimited with _ because commas were used in the format of numerical data in the table
    for i in range(len(cd_data)):
        if cd_data[i].text.lower() == country.lower():
            outstr = f"{country}_{cd_data[i+3].text.strip().replace(',', '')}_{cd_data[i+4].text.strip().replace(',', '').replace('+', '')}_{cd_data[i+10].text.strip().replace(',', '')}_{cd_data[i+19].text.strip()}"

    # Split the string to obtain a list of the scraped data values
    tempdata = outstr.split('_')

    # Since int('') results in an error, all blank strings from the html data are replaced with '0'
    for i in range(len(tempdata)):
        if tempdata[i] == '':
            tempdata[i] = '0'

    # Append each data value to the outdata list while converting to the appropriate data type
    outdata.append(tempdata[0].upper())
    outdata.append(int(tempdata[1]))
    outdata.append(int(tempdata[2]))
    outdata.append(float(tempdata[3]))
    outdata.append(float(tempdata[4]))
    outdata.append(date.today() - timedelta(days = 1)) # Include the associated date value to avoid duplicates

    # Return list of country data
    return outdata

# URL for population data
pops = "https://www.worldometers.info/world-population/population-by-country/"

# HTML request for URL
pops_html = requests.get(pops)

# Parse HTML request
pops_html_parsed = BeautifulSoup(pops_html.content, 'html5lib')

# Find all 'a' tags in parsed HTML, each containing a country name
pop_data = pops_html_parsed.find('tbody').find_all('a')

# Declare empty list for country names
countries = []

# Declare iterator
j = 0

# Used to return top 'X' countries according to population size
numcountries = 100

for i in pop_data:
    if j <= numcountries:   # This line technically makes it the top 101, however North Korea is not found in the covid data table. It's removed from the list in the next step
        countries.append(i.text)
    else:
        break
    j += 1
    
# Although the country names from the two sources are from the same website, there are discrepancies for the name of a couple country across the two pages
# This conditional tree loop handles those discrepancies
for i in range(numcountries):
    if countries[i].lower() == 'united states':
        countries[i] = 'USA'
    elif countries[i].lower() == 'dr congo':
        countries[i] = 'Congo'
    elif countries[i].lower() == 'united kingdom': 
        countries[i] = 'UK'
    elif countries[i].lower() == 'south korea':
        countries[i] = 'S. Korea'
    elif countries[i].lower() == "côte d'ivoire":
        countries[i] = 'Ivory Coast'
    elif countries[i].lower() == 'north korea':
        countries.pop(i)
    elif countries[i].lower() == 'czech republic (czechia)': 
        countries[i] = 'Czechia'
    elif countries[i].lower() == 'united arab emirates':
        countries[i] = 'UAE'

# Create list to contain covid data
covid = []

# Iterate through list of country names & apply ScrapeCountry to each one, appending to covid data list
for i in countries:
    covid.append(scrape_country(i,"https://www.worldometers.info/coronavirus/#main_table"))
    
# Create pandas dataframe object using covid data list
pd_covid = pd.DataFrame(data = covid, columns = ['Country', 'Total Deaths', 'New Deaths', 'Deaths/1M', 'New Deaths/1M', 'Date'])

# Change this path variable to designate where the JSON output file will be located after executing in command prompt
outpath = fr"C:\Users\Kknam\Documents"

# Write pandas dataframe to JSON file with date naming convention within formatted raw string for path\filename
pd_covid.to_json(fr"{outpath}\covid_data_{str(date.today() - timedelta(days = 1))}.json")