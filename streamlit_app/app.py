#libraries needed
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#title
st.title("Weather and Electricity Prices")

#intro paragraph
st.write("Electricity prices are reported at wholesale market price hubs rather than uniformly at the state level. Because weather data is location-based, we associate each price hub with a representative geographic location (typically the state capital or a major metropolitan area near the hub). All analyses and visualizations are therefore conducted at the price hub level, rather than strictly by state boundaries.")

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
