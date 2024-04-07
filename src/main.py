import openrouteservice as ors
import pandas as pd
import folium

import utils
import fleet_manager as fm
import constants

if __name__ == "__main__":
    # input postcode # assume it is valid
    # TODO replace hard-coded values with user input
    # postcode = input()
    postcode = 'LS9 0BT'
    
    # input 'n'
    # bot_count = int(input())
    bot_count = 3

    # customise? input
    # customise = bool(input())
    customise = False
    
    # TODO 
    # take bot_customisations once; and if the system is heterogenous, take again for all.

    # create client
    client = ors.Client(constants.API_KEY)

    # find the postcode coordinates
    station = client.pelias_search(text=postcode)
    station_coords = station['features'][0]['geometry']['coordinates']

    m = folium.Map(location=list(reversed(station_coords)), tiles="cartodbpositron", zoom_start=15)
    # TODO create & add marker for station_location

    # each app instance shall have only 1 FM.
    # # create fleet managers (multiple to provide options)
    # for i in range(len(fleet_options)):
    #     fleets[i] = FleetManager(id=i, bot_count=bot_count)
    
    # create fleet and create 'n' bots
    fleet = fm.FleetManager(bot_count=bot_count, start=station_coords)

    # get potholes data
    potholes_data = pd.read_json(constants.SMALL_POTHOLES_DATA_FILEPATH)
    # TODO logic to select only those potholes lying in a vicinity

    # TODO logic to select only road-defects from a database of multiple notes/landmarks/items; and create markers for them (along with tooltips having estimates).

    # calculate estimates and # create jobs
    ut = utils.Utils()
    pothole_estimates = [] # vol, surface_area, qty_reqd, setup_time, service_time
    
    jobs = []
    for feature in potholes_data['features']:
        volume, surface_area, qty_reqd, setup_time, service_time = ut.calculate_eta(feature)
        pothole_estimates.append({
            'id': feature['id'], 
            'defect': feature['properties']['defect'], 
            'volume': volume, 
            'surface_area': surface_area, 
            'qty_reqd': qty_reqd, 
            'setup_time': setup_time, 
            'service_time': service_time})
        jobs.append(ors.optimization.Job(
            location=feature['geometry']['coordinates'], 
            id=feature['id'], 
            setup=setup_time, 
            service=service_time, 
            amount=[qty_reqd])
            )

    # plan route using ORS
    route_plan = ors.optimization.optimization(client,
                                  jobs=jobs,
                                  vehicles=fleet.bots,
                                  shipments=None,
                                  matrix=None,
                                  geometry=True,
                                  dry_run=None)
    
    # plot maps, charts, comparisons
    for pothole in potholes_data['features']:
        folium.Marker(
            location=pothole['geometry']['coordinates'],
            tooltip=pothole['properties']['id'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    for route in route_plan['routes']:
        folium.PolyLine(locations=route['geometry']['coordinates'], weight=5, color='blue').add_to(m)
        
    m.save('potholes_map.html')
    
    
    # conclude w/ report
