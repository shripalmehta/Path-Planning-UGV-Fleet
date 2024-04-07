import random
import pandas as pd
from controller import Supervisor

# Initialize the Webots supervisor
supervisor = Supervisor()

# Define the area where you want to place the potholes
# Update these values according to your OSM map dimensions
X_MIN, X_MAX = -100, 100
Z_MIN, Z_MAX = -100, 100

# Function to create a pothole at a given position
def create_pothole(x, z):
    pothole_proto = 'Pothole {} {{ translation {} 0 {} }}'.format(random.randint(0, 10000), x, z)
    root_children_field = supervisor.getRoot().getField('children')
    root_children_field.importMFNodeFromString(-1, pothole_proto)

# DataFrame to store pothole locations
df = pd.DataFrame(columns=['Pothole_ID', 'X_Coordinate', 'Z_Coordinate'])

# Randomly place 5 potholes and record their positions
for i in range(5):
    x = random.uniform(X_MIN, X_MAX)
    z = random.uniform(Z_MIN, Z_MAX)
    create_pothole(x, z)
    df.loc[i] = [i, x, z]

# Save the DataFrame to a CSV file
df.to_csv('pothole_locations.csv', index=False)

# Main loop
while supervisor.step(32) != -1:
    pass
