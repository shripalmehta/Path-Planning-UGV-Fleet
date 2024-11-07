import streamlit as st
import geopandas as gpd
import os
import pandas as pd
from utils import calculate_pothole_metrics
from job_planning import create_repair_jobs, plan_routes
from map_utils import create_and_display_map, get_coordinates

def main():
    st.title("Road Fixer")

    # Input for number of bots, payload capacity, area factor, and volume factor in the same row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        num_bots = st.number_input("Number of bots in the fleet:", min_value=1, value=1, step=1)
    with col2:
        payload_capacity = st.number_input("Payload capacity for all bots (kg):", min_value=100, value=100, step=100)
    with col3:
        area_factor = st.number_input("Enter area factor:", min_value=100, value=100, step=100)
    with col4:
        volume_factor = st.number_input("Enter volume factor:", min_value=100, value=100, step=100)

    # Partition line
    st.markdown("---")

    # Display the entered values
    st.write(f"Fleet size: {num_bots} bot{'s' if num_bots > 1 else ''}")
    st.write(f"Payload capacity per bot: {payload_capacity} kg")

    # Input for postcode
    postcode = st.text_input("Enter postcode for station location:")
    
    if postcode:
        # Get coordinates for the station
        # station_coords = get_coordinates(postcode)
        station_coords = (53.789386, -1.517644)
        
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

        # Calculate setup time based on road surface defect type
        gdf['setup_time'] = gdf['defect'].map({'crack': 200, 'pothole': 300, 'dent': 600})
        
        # Calculate service time based on area and volume
        gdf['service_time'] = gdf['area'] * area_factor + gdf['volume'] * volume_factor
        
        # Display full list of records
        st.write(gdf)
        
        # Create repair jobs
        repair_jobs = create_repair_jobs(gdf)
        st.write(f"Total number of repair jobs created: {len(repair_jobs)}")
        
        if postcode and station_coords:
            # Plan routes
            route_plans = plan_routes(repair_jobs, station_coords, num_bots, payload_capacity)
            st.write(f"Number of route plans: {len(route_plans)}")
            
            for plan in route_plans:
                st.write(f"Trip {plan['trip_number']}:")
                st.write(f"  Number of routes: {len(plan['routes'])}")
                st.write(f"  Number of unassigned jobs: {len(plan['unassigned'])}")
                
                # Create a DataFrame for the current plan
                plan_data = []
                for route in plan['routes']:
                    for step in route['steps']:
                        plan_data.append({
                            'Trip': plan['trip_number'],
                            'Bot ID': route['vehicle'],
                            'Step Type': 'job' if 'job' in step else step['type'],
                            'Job ID': step.get('job', 'N/A'),
                            'Arrival Time': step['arrival'],
                            'Start Time': step.get('service', 'N/A'),
                            'End Time': step.get('service_end', 'N/A'),
                            'Amount': step.get('load', 'N/A')
                        })
                
                plan_df = pd.DataFrame(plan_data)
                st.write(plan_df)

            # Create and display the map
            create_and_display_map(station_coords, gdf)
        elif postcode:
            st.error("Unable to display map. Please check the entered postcode.")
    else:
        st.error(f"File not found: {file_path}")

if __name__ == "__main__":
    main()