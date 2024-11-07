import math
import requests
import os
from typing import List, Dict, Tuple

def create_repair_jobs(gdf, bot_capacity):
    jobs = []
    for idx, row in gdf.iterrows():
        material_required = row['material_required']
        job_count = 1
        while material_required > 0:
            amount = min(material_required, bot_capacity)
            jobs.append({
                'id': f"{idx}_{job_count}",
                'location': (row['geometry'].y, row['geometry'].x),
                'amount': amount
            })
            material_required -= amount
            job_count += 1
    return jobs


def get_travel_time(start, end):
    api_key = os.environ['ORS_key']
    url = f"https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {'Authorization': api_key}
    params = {
        'start': f"{start[1]},{start[0]}",
        'end': f"{end[1]},{end[0]}"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['features'][0]['properties']['segments'][0]['duration']
    else:
        # Return a default value if API call fails
        return 1800  # 30 minutes in seconds

def plan_routes(jobs: List[Dict], station_coords: Tuple[float, float], num_bots: int) -> List[Dict]:
    route_plans = []
    pending_jobs = jobs.copy()
    offset_time = 0
    
    while pending_jobs:
        current_plan = {
            'routes': [],
            'unassigned': []
        }
        
        for _ in range(num_bots):
            if not pending_jobs:
                break
            
            route = {
                'steps': [
                    {'type': 'start', 'location': station_coords, 'arrival': offset_time}
                ],
                'total_time': offset_time
            }
            
            while pending_jobs:
                job = pending_jobs.pop(0)
                if isinstance(job, dict) and 'location' in job:
                    travel_time = get_travel_time(route['steps'][-1]['location'], job['location'])
                    service_time = 3600  # 1 hour service time
                    
                    route['total_time'] += travel_time + service_time
                    if isinstance(route['steps'], list):
                        route['steps'].append({
                            'type': 'job',
                            'location': job['location'],
                            'id': job['id'],
                            'amount': job['amount'],
                            'arrival': route['total_time'] - service_time
                        })
            
            # Return to station
            return_time = get_travel_time(route['steps'][-1]['location'], station_coords)
            route['total_time'] += return_time
            if isinstance(route['steps'], list):
                route['steps'].append({
                    'type': 'end',
                    'location': station_coords,
                    'arrival': route['total_time']
                })
            current_plan['routes'].append(route)
        
        route_plans.append(current_plan)
        
        if pending_jobs:
            # Offset time for the next plan
            offset_time = max(route['total_time'] for route in current_plan['routes'])
            
            for job in pending_jobs:
                job['offset_time'] = offset_time
    
    return route_plans