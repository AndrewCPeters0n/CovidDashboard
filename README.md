# CovidDashboard
This repository contains a dashboard to interactively view Covid death rates across different countries.

## Guide For Running ScrapeWebsite.py
The web scraping module used was BeautifulSoup, and the parser used was html5lib. To familiarize with this module, the following tutorial website was used: https://www.geeksforgeeks.org/python-web-scraping-tutorial/. To execute ScrapeWebsite.py, first install the appropriate modules by executing the following commands in command prompt:

  * pip install requests
  * pip install beautifulsoup4
  * pip install html5lib
  * pip install pandas

Once these installations are complete, open ScrapeWebsite.py in Visual Studio Code, or whichever IDE you prefer. Near the end of the file is an "outpath" string variable with a "fr" prefix. Change the path within the quotes to the file-path for the folder you want the JSON file to appear in once the code is executed. The naming convention for the output file is "covid_data_{yesterday's date}.json". Save and close ScrapeWebsite.py.

Next, open command prompt in the folder containing ScrapeWebsite.py. Run the following command: "python ScrapeWebsite.py". On average, it took roughly 3.5 minutes for the execution to complete and the JSON file to appear in the designated "outpath" folder.

## Guide For Running DataDisplay.py
The library used to create the interactive visuulaization tools in DataDisplay.py come from Bokeh, an open source tool that helps create common plots and handle custom use-cases. NumPy, another library used to work with arrays in Python was used to manipulate data in our graphs. To install these libararies, use the folllowing command line:
  * pip install bokeh
  * pip install numpy

A few items to check before running DataDisplay.py
1. Make sure at least three consecutive days of JSON data are present, this is required for the pandas dataframes. 
2. Run UpdatedCountries.py and ensure that a CSV file titled updated_countries.csv is created.
3. Update the file path at the top of DataDisplay.py with the location of the JSON files.

After this, you should be able to run DataDisplay.py after navigating to the correct folder.
