#importing libraries needed
import pandas as pd

#load data
electricity_raw = pd.read_csv("data/raw/ice_electric-2025.csv")
indianapolis_weather_raw = pd.read_csv("data/raw/Indianapolis_Weather.csv",skiprows=1)
phoenix_weather_raw = pd.read_csv("data/raw/Phoenix_Weather.csv", skiprows=1)

#checking if data was read correctly
electricity_raw.head(10)
indianapolis_weather_raw.head(10)
phoenix_weather_raw.head(10)


#cleaning the individual data sets to prep for the joining

#WEATHER DATA
#remove columns not relevant to the scope of the analysis
def clean_weather(df, hub_name):
    df = df.copy()

    # clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(r"\s*\(.*\)", "", regex=True)
    )

    # select the columns that are needed
    df = df[['DATE', 'PRCP']]

    # convert date
    df['DATE'] = pd.to_datetime(df['DATE'])

    # filter year
    df = df[df['DATE'].dt.year == 2025].reset_index(drop=True)

    # add price hub name for merging
    df['HUB'] = hub_name

    return df

#indiana weather cleaning
indianapolis_weather = clean_weather(
    indianapolis_weather_raw,
    "Indiana Hub RT Peak")

#arizona weather cleaning
phoenix_weather = clean_weather(
    phoenix_weather_raw,
    "Palo Verde Peak")

#combine both weather datas together
weather_filtered = pd.concat([indianapolis_weather, phoenix_weather])

#electricity data cleanining

electricity_raw.rename(columns={
    'High price $/MWh': 'High price',
    'Low price $/MWh': 'Low price'
}, inplace=True)
#selecting relevant col
electricity_col_filtered = electricity_raw[
    ['Trade date', 'Price hub', 'High price', 'Low price']
].copy()

#convert date to match col for merging
electricity_col_filtered['Trade date'] = pd.to_datetime(
    electricity_col_filtered['Trade date']
)

#filter hubs that go with IN and AZ
valid_hubs = ['Indiana Hub RT Peak', 'Palo Verde Peak']
electricity_row_filtered = electricity_col_filtered[
    electricity_col_filtered['Price hub'].isin(valid_hubs)
]


#inner join
full_data = pd.merge(
    electricity_row_filtered,
    weather_filtered,
    how='inner',
    left_on=['Trade date', 'Price hub'],
    right_on=['DATE', 'HUB']
)

#remove repetitive col 
full_data = full_data.drop(columns=['DATE', 'HUB'])

#testing data
full_data.head(20)

#moved full data into processed folder
full_data.to_csv(
    "data/processed/energy_weather_2025.csv",
    index=False)