# CovidDashboard
This repository contains a dashboard to interactively view Covid death rates across different countries.

## Guide For Running ScrapeWebsite.py
The web scraping module used was BeautifulSoup, and the parser used was html5lib. To familiarize with this module, the following tutorial website was used: https://www.geeksforgeeks.org/python-web-scraping-tutorial/. To execute ScrapeWebsite.py, first install the appropriate modules by executing the following commands in command prompt:

  * pip install requests
  * pip install beautifulsoup4
  * pip install html5lib

Once these installations are complete, open ScrapeWebsite.py in Visual Studio Code, or whichever IDE you prefer. Near the end of the file is an "outpath" string variable with a "fr" prefix. Change the path within the quotes to the file-path for the folder you want the JSON file to appear in once the code is executed. The naming convention for the output file is "covid_data_{yesterday's date}.json". Save and close ScrapeWebsite.py.

Next, open command prompt in the folder containing ScrapeWebsite.py. Run the following command: python ScrapeWebsite.py. On average, it took roughly 3.5 minutes for the execution to complete and the JSON file to appear in the designated "outpath" folder.
