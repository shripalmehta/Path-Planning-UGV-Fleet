import streamlit as st
import geopandas as gpd
import os
import requests
import folium
from streamlit_folium import folium_static

def get_coordinates(postcode):
    # TODO: Implement Pelias search to get coordinates
    # For now, return a dummy coordinate
    return (51.5074, -0.1278)  # London coordinates

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

        if postcode:
            # Get coordinates for the station
            station_coords = get_coordinates(postcode)

            # Create a map centered on the station
            m = folium.Map(location=station_coords, zoom_start=12)

            # Add marker for the station
            folium.Marker(
                station_coords,
                popup="Station",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(m)

            # Add markers for potholes
            for idx, row in gdf.iterrows():
                folium.Marker(
                    [row['geometry'].y, row['geometry'].x],
                    popup=f"Pothole {idx}",
                    icon=folium.Icon(color="blue", icon="road"),
                ).add_to(m)

            # Display the map
            folium_static(m)
    else:
        st.error(f"File not found: {file_path}")

if __name__ == "__main__":
    main()