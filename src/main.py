import streamlit as st
import geopandas as gpd
import os

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
    else:
        st.error(f"File not found: {file_path}")

if __name__ == "__main__":
    main()