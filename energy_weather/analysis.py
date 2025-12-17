#libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression

#read in cleaned data
data = pd.read_csv("data/processed/energy_weather_2025.csv")

#checking data is read correctly
data.head(10)
print(data.info())
print(data.isna().sum())

#basic scatterplot
sns.scatterplot(data=data, x='PRCP', y='High price', hue='Price hub')
plt.title("High Price vs Precipitation")
plt.show()

# Correlation matrix
corr = data[['High price', 'Low price','PRCP']].corr()
print(corr)

# Heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation between Electricity Prices and Weather")
plt.show()


# Features and target
X = data[['PRCP']]
y = data['High price']

# Fit model
model = LinearRegression()
model.fit(X, y)

# Coefficients
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

# Predicted values
data['High_price_pred'] = model.predict(X)

# Plot actual vs predicted
sns.scatterplot(x=data['High price'], y=data['High_price_pred'])
plt.xlabel("Actual High Price")
plt.ylabel("Predicted High Price")
plt.title("Actual vs Predicted High Price")
plt.show()
