import streamlit as st
import geopandas as gpd
import os
import pandas as pd
from utils import calculate_pothole_metrics
from job_planning import create_repair_jobs, plan_routes
from map_utils import create_and_display_map, get_coordinates

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
        
        # Calculate pothole metrics
        gdf = calculate_pothole_metrics(gdf)
        
        # Display full list of records
        st.write(gdf)

        # Create repair jobs
        repair_jobs = create_repair_jobs(gdf, payload_capacity)
        st.write(f"Total number of repair jobs created: {len(repair_jobs)}")
        
        # Plan routes
        route_plans = plan_routes(repair_jobs, station_coords, num_bots)
        st.write(f"Number of route plans: {len(route_plans)}")
        for i, plan in enumerate(route_plans):
            st.write(f"Plan {i+1}:")
            st.write(f"  Number of routes: {len(plan['routes'])}")
            st.write(f"  Number of unassigned jobs: {len(plan['unassigned'])}")

            
            # Create a DataFrame for the current plan
            plan_data = []
            for j, route in enumerate(plan['routes']):
                for step in route['steps']:
                    plan_data.append({
                        'Plan': i+1,
                        'Route': j+1,
                        'Step Type': step['type'],
                        'Job ID': step.get('id', 'N/A'),
                        'Arrival Time': step['arrival'],
                        'Amount': step.get('amount', 'N/A')
                    })
            
            plan_df = pd.DataFrame(plan_data)
            st.write(plan_df)
        
        if postcode and station_coords:
            # Create and display the map
            create_and_display_map(station_coords, gdf)
        elif postcode:
            st.error("Unable to display map. Please check the entered postcode.")
    else:
        st.error(f"File not found: {file_path}")

if __name__ == "__main__":
    main()