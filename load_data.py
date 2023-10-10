import pandas as pd
import geopandas as gpd

# Load air pollution data from global.csv
air_pollution_data = pd.read_csv('global.csv')

# Load Uganda district boundaries GeoJSON file
uganda_districts = gpd.read_file('uganda_districts.geojson')

print(air_pollution_data.head(5))
print(uganda_districts.head(5))