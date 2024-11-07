import math
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
                # TODO: Calculate actual travel time using OpenRouteService API
                travel_time = 30  # Placeholder: 30 minutes travel time
                service_time = 60  # Placeholder: 60 minutes service time
                
                route['total_time'] = route['total_time'] + travel_time + service_time
                route['steps'].append({
                    'type': 'job',
                    'location': job['location'],
                    'id': job['id'],
                    'amount': job['amount'],
                    'arrival': route['total_time'] - service_time
                })
                
                # TODO: Add logic to check if bot capacity is exceeded
                # If so, return to station and start a new route
            
            # Return to station
            # TODO: Calculate actual travel time using OpenRouteService API
            return_time = 30  # Placeholder: 30 minutes travel time
            route['total_time'] = route['total_time'] + return_time
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