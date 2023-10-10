
import pandas as pd
import geopandas as gpd


# Load air pollution data from global.csv
air_pollution_data = pd.read_csv('global.csv')

# Load Uganda district boundaries GeoJSON file
uganda_districts = gpd.read_file('uganda_districts.geojson')

air_pollution_data.head(5)


# In[7]:


import pandas as pd
import geopandas as gpd
import folium
import random
import streamlit as st
from geopy.geocoders import Nominatim
from pushbullet import Pushbullet

# Load air pollution data from global.csv
air_pollution_data = pd.read_csv('global.csv')

# Load Uganda district boundaries GeoJSON file
uganda_districts = gpd.read_file('uganda_districts.geojson')

air_pollution_data.head(5)

# Function to get the district name from coordinates
def get_district_name(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    address = location.raw['address']
    district_name = address.get('county', '')  # Use 'county' instead of 'country' to get district name

    return district_name

# Function to send notifications based on air pollution levels
def send_notifications(district_name, pollution_value):
    pb = Pushbullet('o.61fA5UUNB8HmBRCHUSoys6O6OFw4G7wJ')  # Replace with your Pushbullet API key

    if pollution_value > 80:
        alert_message = f"High Pollution rates in {district_name}! Please move to a new area or put on a mask."
        pb.push_note(f"Air Quality Alert in {district_name}", alert_message)
    elif pollution_value < 20:
        alert_message = f"The air in {district_name} is now safe to breathe. Feel at home!"
        pb.push_note(f"Air Quality Improvement in {district_name}", alert_message)

# Function to generate random air pollution data for districts
def generate_random_data():
    districts = ['Abim', 'Amolatar', 'Alebtong']  # Replace with your district names
    air_pollution_values = [random.uniform(0, 100) for _ in districts]
    data = {'name': districts, 'air_pollution_value': air_pollution_values}
    return pd.DataFrame(data)

# Main Streamlit app
def main():
    st.title("Uganda Air Pollution Monitoring")

    # Get user's location coordinates
    latitude = st.number_input("Enter Latitude:")
    longitude = st.number_input("Enter Longitude:")

    # Convert coordinates to district name
    district_name = get_district_name(latitude, longitude)
    st.write(f"You are in {district_name}.")

    # Generate and display air pollution data for the district
    district_pollution = air_pollution_data[air_pollution_data['Country'] == district_name]

    st.subheader("Air Pollution Data for Your District")
    st.write(district_pollution)

    # Send notifications if pollution thresholds are met
    if not district_pollution.empty:
        pollution_value = district_pollution.iloc[0]['air_pollution_value']
        send_notifications(district_name, pollution_value)

    # Display a map with the user's location
    st.subheader("Map Showing Your Location")
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], tooltip="Your Location").add_to(m)
    st.write(m)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




