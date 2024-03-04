# Data Source: https://www.kaggle.com/code/ravivarmaodugu/earthquakes-data-analytics/input?select=earthquake_1995-2023.csv

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import plugins 
from geopy.geocoders import Nominatim
import time

APP_TITLE = 'Earthquake Analysis'
APP_SUB_TITLE = 'Source: Kaggle Earthquake Dataset'
def get_lat_lon(location):
    geolocator = Nominatim(user_agent="geoapi")
    loc = geolocator.geocode(location)
    if loc:
        return loc.latitude, loc.longitude
    else:
        return None, None

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    
    df=pd.read_csv('data/earthquake.csv')

    # Sidebar filter for country selection
    selected_country = st.sidebar.selectbox("Select Country", df["country"].unique())

    ## We will conclude the notebook by visualizing the worldwide earthquake events by latitude and longitude 
    st.write(f"Earthquakes in {selected_country}")

    # Filter data based on selected country
    filtered_df = df[df["country"] == selected_country]

    # Get latitude and longitude of the selected country
    country_lat, country_lon = get_lat_lon(selected_country)

    if country_lat is not None and country_lon is not None:
        # Create map centered around selected country
        country_map = folium.Map(location=[country_lat, country_lon], zoom_start=5)

        # Generate heatmap data
        heat_map_data = filtered_df[["latitude", "longitude"]].values.tolist()

        # Add heatmap layer to map
        c_map=country_map.add_child(plugins.HeatMap(heat_map_data, min_opacity=0.3, radius=13))

        # Display the map
        st_c_map = st_folium(c_map, width=700, height=450)
    else:
        st.write("Location data not found for the selected country.")

    ####################################################################

    # Display the title
    st.write("Earthquakes Across the World - Heat Map")

    # Create the base map centered around the mean latitude and longitude of the dataset
    world_map = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=1)

    # Add different tile layers
    # folium.TileLayer('Stamen Terrain').add_to(world_map)
    # folium.TileLayer('cartodbpositron').add_to(world_map)
    folium.TileLayer('cartodbdark_matter').add_to(world_map)

    # # Add Layer Control to enable switching between different tile layers
    # folium.LayerControl().add_to(world_map)

    # Generate heatmap data
    heat_map_data = df[["latitude", "longitude"]].values.tolist()

    # Add HeatMap layer to the map
    plugins.HeatMap(heat_map_data, min_opacity=0.3, radius=13).add_to(world_map)

    # Display the map
    st_folium(world_map, width=700, height=450)


    ####################################################################

    # Sidebar filter for country selection
    selected_year = st.sidebar.selectbox("Select Year", df["Year"].unique())
    ## We will conclude the notebook by visualizing the worldwide earthquake events by latitude and longitude 
    st.write(f"Earthquakes in {selected_year}")
    # Filter data based on selected country
    filtered_df = df[df["Year"] == selected_year]
    # Get latitude and longitude of the selected country
    year_lat, year_lon = get_lat_lon(selected_year)
    if year_lat is not None and year_lon is not None:
        # Create map centered around selected country
        year_map = folium.Map(location=[year_lat, year_lon], zoom_start=1)
        # Generate heatmap data
        heat_map_data = filtered_df[["latitude", "longitude"]].values.tolist()
        # Add heatmap layer to map
        y_map=year_map.add_child(plugins.HeatMap(heat_map_data, min_opacity=0.3, radius=13))
        # Display the map
        st_y_map = st_folium(y_map, width=700, height=450)
    else:
        st.write("Location data not found for the selected country.")
    
####################################################################
    
if __name__ == "__main__":
    main()