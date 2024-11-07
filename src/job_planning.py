import math
import requests
import os
from typing import List, Dict, Tuple
import openrouteservice as ors

def create_repair_jobs(gdf):
    jobs = []
    for idx, row in gdf.iterrows():
        jobs.append({
            'id': f"{idx}",
            'location': [row['geometry'].y, row['geometry'].x],
            'amount': row['material_required'],
            'service': int(row['service_time']),
            'setup': int(row['setup_time'])
        })
    return jobs

def plan_routes(jobs: List[Dict], station_coords: Tuple[float, float], num_bots: int, bot_capacity: float) -> List[Dict]:
    api_key = os.environ['ORS_key']
    client = ors.Client(key=api_key)
    
    route_plans = []
    pending_jobs = jobs.copy()
    trip_number = 1
    
    while pending_jobs:
        vehicles = [{
            'id': f'bot_{i+1}',
            'start': list(station_coords),
            'end': list(station_coords),
            'capacity': [bot_capacity]
        } for i in range(num_bots)]
        
        try:
            result = ors.optimization.optimization(
                client,
                jobs=pending_jobs,
                vehicles=vehicles,
                geometry=True
            )
            
            current_plan = {
                'trip_number': trip_number,
                'routes': result['routes'],
                'unassigned': result['unassigned']
            }
            
            route_plans.append(current_plan)
            
            # Remove assigned jobs from pending_jobs
            assigned_job_ids = set()
            for route in result['routes']:
                for step in route['steps']:
                    if 'job' in step:
                        assigned_job_ids.add(step['job'])
            
            pending_jobs = [job for job in pending_jobs if job['id'] not in assigned_job_ids]
            
            trip_number += 1
        
        except Exception as e:
            print(f"Error in optimization: {e}")
            break
    
    return route_plans