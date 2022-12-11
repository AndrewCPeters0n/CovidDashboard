from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource, TableColumn, DataTable,GeoJSONDataSource, HoverTool,ColorBar, NumeralTickFormatter
from bokeh.layouts import gridplot, layout
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import OrRd, RdYlGn, TolYlOrBr
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.io import show
from datetime import date, timedelta
import pandas as pd
import numpy as np
# Run ScrapeWebsite.py before running this code to get the latest COVID data


file_location = fr'C:path\to\JSON\file'
string_1 = (fr"{file_location}\covid_data_{str(date.today() - timedelta(days = 1))}.json")
string_2 = (fr"{file_location}\covid_data_{str(date.today() - timedelta(days = 2))}.json")
string_3 = (fr"{file_location}\covid_data_{str(date.today() - timedelta(days = 3))}.json")
# Load the last three json files of data using pandas
df1 = pd.read_json(string_1)
df2 = pd.read_json(string_2)
df3 = pd.read_json(string_3)

# TABLE 1: Table giving data from yesterday about all the columns collected
# Tell Bokeh to use df1 as our source for the table                                                                                                  
source = ColumnDataSource(df1)
# Enter the table data and titles
columns = [
    TableColumn(field= 'Country',title= 'Country'),
    TableColumn(field= 'Total Deaths',title= 'Total Country Deaths'),
    TableColumn(field= 'New Deaths',title= 'New Deaths'),
    TableColumn(field= 'Deaths/1M', title= 'Deaths / 1M'),
    TableColumn(field= 'New Deaths/1M', title= 'New Deaths / 1M')
]
t1 = DataTable(source=source,columns=columns)

# FIGURE 1: World map with interactive new deaths by hovering 
# Load the coordinate data from countries.csv
df4 = pd.read_csv(r'updated_countries.csv')
# Run the updated_countries script to get the coordinates of the top 100 covid countries



# Define function to switch from lat/long to mercator coordinates
#    x_coord function sourced from: https://github.com/nadinezab
def x_coord(x, y):

    lat = x
    lon = y
    
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x/lon
    y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + 
        lat * (np.pi/180.0)/2.0)) * scale
    return (x, y)
# Define the coords as tuple (lat,long)
df4['coordinates'] = list(zip(df4['latitude'], df4['longitude']))
# Obtain list of mercator coordinates
mercators = [x_coord(x, y) for x, y in df4['coordinates'] ]
# Create mercator column in our df
df4['mercator'] = mercators
# Split that column out into two separate columns - mercator_x and mercator_y
df4[['mercator_x', 'mercator_y']] = df4['mercator'].apply(pd.Series)
# Select tile set to use
chosentile = get_provider(Vendors.STAMEN_TONER)
# Choose palette
palette = TolYlOrBr[9]
# Tell Bokeh to use df4 as the source of the data
source = ColumnDataSource(data=df4)
# Define color mapper - which column will define the colour of the data points
color_mapper = linear_cmap(field_name = 'NewDeaths', palette = palette, low = df4['NewDeaths'].min(), high = df4['NewDeaths'].max())
# Set tooltips HoverTool
tooltips = [("Country","@name"),("New Deaths","@NewDeaths"), ("Cumulative Deaths","@TotalDeaths")]
p1 = figure(title = 'World Map',
           x_axis_type="mercator", y_axis_type="mercator",
           x_axis_label = 'Longitude', y_axis_label = 'Latitude', tooltips = tooltips)
# Add map tile
p1.add_tile(chosentile)
# Add points using mercator coordinates
p1.circle(x = 'mercator_x', y = 'mercator_y', color = color_mapper, source=source, size=15, fill_alpha = 0.7)
#Defines color bar
color_bar = ColorBar(color_mapper=color_mapper['transform'], 
                     formatter = NumeralTickFormatter(format='0.0[0000]'), 
                     label_standoff = 13, width=8, location=(0,0))
# Set color_bar location
p1.add_layout(color_bar, 'right')

# FIGURE 2: Interactive cumulative death plot of top 5 countries
p2 = figure(title='click on legend entries to hide country data', y_axis_label='Number of Deaths', height=400, x_axis_type='datetime')
# rearrange the data so new deaths is sorted from high to low
df1 = df1.sort_values(by='New Deaths', ascending=False)
df2 = df2.sort_values(by='New Deaths', ascending=False)
df3 = df3.sort_values(by='New Deaths', ascending=False)
# add data to the figure
top_countries = df1['Country'].head(5).to_list()
total_deaths1 = df1['New Deaths'].head(10).to_list()
total_deaths2 = df2['New Deaths'].head(10).to_list()
total_deaths3 = df3['New Deaths'].head(10).to_list()
df1['Date'] = pd.to_datetime(df1['Date'])
df2['Date'] = pd.to_datetime(df2['Date'])
df3['Date'] = pd.to_datetime(df3['Date'])

p2.circle([df1['Date'][0],df2['Date'][0],df3['Date'][0]],[total_deaths1[0], total_deaths2[0],total_deaths3[0]],
          fill_color='red',size=8,legend_label=top_countries[0])
p2.circle([df1['Date'][0],df2['Date'][0],df3['Date'][0]],[total_deaths1[1], total_deaths2[1],total_deaths3[1]],
          fill_color='orange',size=8,legend_label=top_countries[1])
p2.circle([df1['Date'][0],df2['Date'][0],df3['Date'][0]],[total_deaths1[2], total_deaths2[2],total_deaths3[2]],
          fill_color='yellow',size=8,legend_label=top_countries[2])
p2.circle([df1['Date'][0],df2['Date'][0],df3['Date'][0]],[total_deaths1[3], total_deaths2[3],total_deaths3[3]],
          fill_color='green',size=8,legend_label=top_countries[3])
p2.circle([df1['Date'][0],df2['Date'][0],df3['Date'][0]],[total_deaths1[4], total_deaths2[4],total_deaths3[4]],
          fill_color='blue',size=8,legend_label=top_countries[4])

p2.legend.location = 'top_left'
p2.legend.click_policy='hide'
# arrange these using the gridplot function
layout = gridplot([
    [p1,None],
    [t1,p2]
])

show(layout)