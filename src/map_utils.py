import folium
import os
import requests
from streamlit_folium import folium_static

def get_coordinates(postcode):
    api_key = os.environ['ORS_key']
    base_url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": api_key,
        "text": postcode,
        "size": 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return (coordinates[1], coordinates[0])  # Return as (lat, lon)
    return None  # Return None if coordinates not found

def create_and_display_map(station_coords, gdf):
    # Create a map centered on the station
    m = folium.Map(location=station_coords, zoom_start=12)

    # Add marker for the station
    folium.Marker(
        station_coords,
        popup="Station",
        icon=folium.Icon(color="red", icon="fa-home", prefix='fa'),
    ).add_to(m)

    # Add markers for potholes
    for idx, row in gdf.iterrows():
        folium.Marker(
            [row['geometry'].y, row['geometry'].x],
            popup=f"Pothole {idx}",
            icon=folium.Icon(color="blue", icon="fa-person-digging", prefix='fa'),
        ).add_to(m)

    # Display the map
    folium_static(m)