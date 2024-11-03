import streamlit as st
import geopandas as gpd
import os
import requests
import folium
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

def main():
    st.title("Road Fixer")

    # Input for number of bots and payload capacity in the same row
    col1, col2 = st.columns(2)
    with col1:
        num_bots = st.number_input("Number of bots in the fleet:", min_value=1, value=1, step=1)
    with col2:
        payload_capacity = st.number_input("Payload capacity for all bots (kg):", min_value=0.1, value=100.0, step=0.1)

    # Partition line
    st.markdown("---")

    # Display the entered values
    st.write(f"Fleet size: {num_bots} bot{'s' if num_bots > 1 else ''}")
    st.write(f"Payload capacity per bot: {payload_capacity} kg")

    # Input for postcode
    postcode = st.text_input("Enter postcode for station location:")
    
    if postcode:
        # Get coordinates for the station
        station_coords = get_coordinates(postcode)
        
        if station_coords:
            st.success(f"Station coordinates: {station_coords}")
        else:
            st.error("Unable to find coordinates for the given postcode.")

    # Read GeoJSON file
    data_dir = "data"
    geojson_file = "LS90BT.geojson"
    file_path = os.path.join(data_dir, geojson_file)

    if os.path.exists(file_path):
        gdf = gpd.read_file(file_path)
        st.write(f"Successfully loaded {len(gdf)} records from {geojson_file}")
        
        # Extract length, width, and depth from dim
        gdf[['length', 'width', 'depth']] = gdf['dim'].str.split('x', expand=True).astype(float)
        
        # Calculate area and volume
        gdf['area'] = gdf['length'] * gdf['width']
        gdf['volume'] = gdf['length'] * gdf['width'] * gdf['depth']
        
        # Display full list of records
        st.write(gdf)

        if postcode and station_coords:
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
        elif postcode:
            st.error("Unable to display map. Please check the entered postcode.")
    else:
        st.error(f"File not found: {file_path}")

if __name__ == "__main__":
    main()