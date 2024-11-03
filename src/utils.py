import pandas as pd

def calculate_pothole_metrics(gdf):
    # Extract length, width, and depth from dim
    gdf[['length', 'width', 'depth']] = gdf['dim'].str.split('x', expand=True).astype(float)
    
    # Calculate area, volume, and material required
    gdf['area'] = gdf['length'] * gdf['width']
    gdf['volume'] = gdf['length'] * gdf['width'] * gdf['depth']
    gdf['material_required'] = gdf['volume'] * 2800  # kg
    
    return gdf