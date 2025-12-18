#libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


#read in cleaned data
data = pd.read_csv("data/processed/energy_weather_2025.csv")

#checking data is read correctly
data.head(10)
print(data.info())
print(data.isna().sum())

# Correlation matrix
corr = data[['High price', 'Low price','PRCP']].corr()
print(corr)

# Heatmap
sns.heatmap(corr, annot=True, cmap='cool')
plt.title("Correlation between Electricity Prices and Weather")
plt.show()


# Features and target
x = data[['PRCP']]
y = data['High price']

# Fit model
model = LinearRegression()
model.fit(x, y)

# Coefficients
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_[0])

data['High_price_pred'] = model.predict(x)
print("R² score:", r2_score(y, data['High_price_pred']))

# Plot actual vs predicted
sns.scatterplot(x=data['High price'], y=data['High_price_pred'])
plt.xlabel("Actual High Price")
plt.ylabel("Predicted High Price")
plt.title("Actual vs Predicted High Price")
plt.show()

# Create graph and layout
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)

# High price vs PRCP
sns.scatterplot(
    data=data,
    x='PRCP',
    y='High price',
    hue='Price hub',
    ax=axes[0]
)
axes[0].set_title("High Price vs Precipitation")

# Low price vs PRCP
sns.scatterplot(
    data=data,
    x='PRCP',
    y='Low price',
    hue='Price hub',
    ax=axes[1]
)
axes[1].set_title("Low Price vs Precipitation")

# Layout the graphs to be shown side by side
plt.tight_layout()
plt.show()

# Create graph
fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=False)

# Subsets
indiana = data[data['Price hub'] == 'Indiana Hub RT Peak']
arizona = data[data['Price hub'] == 'Palo Verde Peak']

# High Price
sns.scatterplot(
    data=indiana,
    x='PRCP',
    y='High price',
    color='blue',
    ax=axes[0, 0])

axes[0, 0].set_title("Indiana: High Price vs Precipitation")
axes[0, 0].set_ylabel("High Electricity Price (USD per MWh)")

sns.scatterplot(
    data=arizona,
    x='PRCP',
    y='High price',
    color='orange',
    ax=axes[0, 1])

axes[0, 1].set_title("Arizona: High Price vs Precipitation")

# Low Price 
sns.scatterplot(
    data=indiana,
    x='PRCP',
    y='Low price',
    color='blue',
    ax=axes[1, 0])

axes[1, 0].set_title("Indiana: Low Price vs Precipitation")
axes[1, 0].set_xlabel("Daily Precipitation (inches)")
axes[1, 0].set_ylabel("Low Electricity Price (USD per MWh)")

sns.scatterplot(
    data=arizona,
    x='PRCP',
    y='Low price',
    color='orange',
    ax=axes[1, 1]
)
axes[1, 1].set_title("Arizona: Low Price vs Precipitation")
axes[1, 1].set_xlabel("Daily Precipitation (inches)")

#create grid to compare all 4 together
plt.tight_layout()
plt.show()


# Date focused 

#Indiana
hub = "Indiana Hub RT Peak"
subset = data[data["Price hub"] == hub]

# Line plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=subset, x="Trade date", y="High price")
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("High Price ($/MWh)")
plt.title(f"High Price Trend Over 2025 - {hub}")
plt.tight_layout()
plt.show()

# Filter for Phoenix hub

data['Trade date'] = pd.to_datetime(data['Trade date'])
hub = "Palo Verde Peak"
subset = data[data["Price hub"] == hub]
subset['Month'] = subset['Trade date'].dt.month

# Line plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=subset, x="Trade date", y="High price", color="orange")  # optional: set color
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("High Price ($/MWh)")
plt.title(f"High Price Trend Over 2025 - {hub}")
plt.tight_layout()
plt.show()



