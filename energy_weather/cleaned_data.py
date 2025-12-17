#importing libraries needed
import pandas as pd
import numpy as np

#load data
electricity_raw = pd.read_csv("data/raw/ice_electric-2025.csv")
indianapolis_weather_raw = pd.read_csv("data/raw/Indianapolis_Weather.csv")
phoenix_weather_raw = pd.read_csv("data/raw/Phoenix_Weather.csv")

#checking if data was read correctly
electricity_raw.head(10)
indianapolis_weather_raw.head(10)
phoenix_weather_raw.head(10)

#cleaning the individual data sets to prep for the joining

#WEATHER DATA
#remove columns not relevant to the scope of the analysis
indianapolis_weather_col_filtered = indianapolis_weather_raw.iloc[:,[0,2,3,4,5]]
phoenix_weather_col_filtered = phoenix_weather_raw.iloc[:,[0,2,3,4,5]]

#change "Date" columns to be datetime 
indianapolis_weather_col_filtered['Date'] = pd.to_datetime(indianapolis_weather_col_filtered['Date'])
phoenix_weather_col_filtered['Date'] = pd.to_datetime(phoenix_weather_col_filtered['Date'])

#filter to only 2025 data
indianapolis_weather_row_filtered = indianapolis_weather_col_filtered[indianapolis_weather_col_filtered['Date'].dt.year == 2025]
phoenix_weather_row_filtered = phoenix_weather_col_filtered[phoenix_weather_col_filtered['Date'].dt.year == 2025]

#add in 'hub' identifier to mark each weather data with its corresponding trade hub for easy data merging
indianapolis_weather_row_filtered['hub'] = "Indiana Hub RT Peak"
phoenix_weather_row_filtered['hub'] = "Palo Verde Peak"

#concatenate the weather data together
weather_filtered = pd.concat([indianapolis_weather_row_filtered,phoenix_weather_row_filtered])

#ELECTRICITY DATA
#remove columns we don't care about for the analysis
electricity_col_filtered = electricity_raw.iloc[:,[0,1,4,5]]

#change the datatype of the trade date column to actually be a date
electricity_col_filtered['Trade date'] = pd.to_datetime(electricity_col_filtered['Trade date'])

#filter the electricity data to only include the two hubs of interest
valid_hubs = ['Indiana Hub RT Peak','Palo Verde Peak']
electricity_row_filtered = electricity_col_filtered[electricity_col_filtered['Price hub'].isin(valid_hubs)]

#DATA JOIN
full_data = pd.merge(electricity_row_filtered,weather_filtered, how = 'inner', 
    left_on = ['Trade date','Price hub'],
    right_on = ['Date','hub'])
#drop duplicate columns
full_data = full_data.drop(['Trade date','hub'])