# ScrapeWebsite.py Summary
This document details the sources from which the data was pulled, the methods(not detailed), and the JSON file data format.

## Sources & Methods
The first data source, https://www.worldometers.info/coronavirus/#main_table, contains covid data for many countries.
The second data source, https://www.worldometers.info/world-population/population-by-country/, contains population data for many countries.

The first source was used to get all the required data for this project.
The second source was used to obtain a list of countries from which we would pull the data for.

In the covid data source, the United States of America shows up as "USA", while in the population source it shows up as "United States".
There were several instances of this, all of which were accounted for in the ScrapeWebsite.py module.

The module iterates through country names using the first source as a URL to pass to scrape_country and each list element for the country.
Data was returned as a list, additionally including the data's date.

## Format & Reading Data
Data in the JSON file was stored as follows:

{

"Column":{"Index":Value, "Index":Value ...}

"Column":{ ... }

...

}

To read the data, use the Pandas DataFrame function: data = Pandas.read_JSON("filepath\filename.json")
