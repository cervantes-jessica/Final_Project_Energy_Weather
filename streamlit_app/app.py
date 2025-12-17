import streamlit as st

st.title("Weather and Electricity Prices")

st.write("Electricity prices are reported at wholesale market price hubs rather than uniformly at the state level. Because weather data is location-based, we associate each price hub with a representative geographic location (typically the state capital or a major metropolitan area near the hub). All analyses and visualizations are therefore conducted at the price hub level, rather than strictly by state boundaries.")


state = st.selectbox("Select Price Hub", ["Indiana Hub RT Peak",
                                          "Palo Verde Peak"])

variable = st.selectbox("Weather Variable", ["temp_c", "wind_speed"])


