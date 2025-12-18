#libraries needed
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#title
st.title("Weather and Electricity Prices")

#intro paragraph
st.write("For this project, we’re focusing on two electricity market hubs: Indiana Hub RT Peak and Palo Verde Peak. We chose these two because they are in very different regions of the country with distinct weather patterns: Indiana experiences temperate, seasonal weather, while Phoenix, Arizona is hot and dry with lots of solar energy production. This contrast allows us to explore how weather influences electricity prices in very different environments."
"Use the options below to see how each hub’s electricity prices and precipitation vary throughout 2025 and to compare the differences between the two locations.")

#load data in
@st.cache_data
def we_data():
    df = pd.read_csv("../data/processed/energy_weather_2025.csv")
    df['Trade date'] = pd.to_datetime(df['Trade date'])  # ensure datetime
    return df

data = we_data() 


# Select hub
hub = st.selectbox("Select Price Hub", data["Price hub"].unique())

subset = data[data["Price hub"] == hub]

# Plot High Price
st.subheader(f"High Price Over 2025 - {hub}")
fig, ax = plt.subplots(figsize=(12, 4))
sns.lineplot(data=subset, x="Trade date", y="High price", ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("High Price ($/MWh)")
ax.set_title(f"High Price Trend for {hub}")
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot Precipitation
st.subheader(f"Precipitation Over 2025 - {hub}")
fig2, ax2 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=subset, x="Trade date", y="PRCP", ax=ax2, color="orange")
ax2.set_xlabel("Date")
ax2.set_ylabel("Precipitation (inches)")
ax2.set_title(f"Precipitation Trend for {hub}")
plt.xticks(rotation=45)
st.pyplot(fig2)
