import pandas as pd
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt

# USING ALL IMPERIAL UNITS... sorry... parachute stuff... also didn't include parachute stuff
air_data = pd.read_csv('airData.csv')

##  Inputs  ##

diameter = (4) / 12   # in-->ft
cd = .45

wet_weight = 14  # lbs
prop_weight = 4  # lbs  (can easily switch up inputs to have a prop fraction instead)
burn_time = 5
avg_thrust = 110  # lbs

delta_t = 0.1
launch_alt = 0  # ASL

##  Preliminary Calculations  ##

area = ((diameter / 2)**2) * 3.1415926  # ft^2
wet_mass = wet_weight / 32.172    # slugs
prop_mass = prop_weight / 32.172
mass_flow = prop_mass / (burn_time / delta_t)

## Flight Model ##

# setup
data_columns = ["time", "altitude", "velocity", "acceleration", "drag", "thrust", "mass"]
data_values = [0, launch_alt, 0, wet_weight, 0, 0, wet_mass]
data = dict(zip(data_columns, data_values))  # now you can reference these in the code by their names

print_interval = .25  # time interval for how often a row of data actually prints to the terminal

apogee = launch_alt # initializing variable for apogee
max_vel = 0 # same thing for max velocity

# actual thing
while data['altitude'] >= launch_alt:
    

    data['time'] += delta_t
    air_density = float(air_data[air_data["Altitude"] > launch_alt].iloc[0]["Density"])

    # i calculate all of the forces first because that's what newton likes

    # Propulsion Related Things
    if data['time'] <= burn_time:
        data['thrust'] = avg_thrust
        data['mass'] -= mass_flow
    else:
        data['thrust'] = 0
        data['mass'] = wet_mass - prop_mass
    
    # Drag: no parachutes :(
    if data['velocity'] > 0:
        data['drag'] = 0.5 * air_density * (data['velocity']**2) * cd * area * -1
    else:
        data['drag'] = 0.5 * air_density * (data['velocity']**2) * cd * area
    
    # Flight Profile Things
    weight = data['mass'] * -32.172
    data['acceleration'] = (data['thrust'] + data['drag'] + weight) / data['mass']
    data['velocity'] += data['acceleration'] * delta_t
    data['altitude'] += (data['velocity'] * delta_t) + 0.5 * data['acceleration'] * delta_t**2   # ASL

    # Apogee/ Max Vel.
    if data['altitude'] > apogee:
        apogee = data['altitude']
    if data['velocity'] > max_vel:
        max_vel = data['velocity']

    print("Time: %.2f  Altitude: %.2f  Velocity: %.2f" % (data['time'], data['altitude'], data['velocity']))


apogee -= launch_alt  # ASL --> AGL

print("Apogee: %i [ft]" % apogee)
print("Max Velocity: %i [ft/s]" % max_vel)