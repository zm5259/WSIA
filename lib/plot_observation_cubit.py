#####################################################################
#                                                                   
# This script maps the current observation system using CUBIT software.
# It plots the STL model, stations, and source location in CUBIT.
# Note: This script must be run within the CUBIT software environment.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import os
import sys

def read_parameters(param_file, *param_names):
    """ Read specified parameters from a parameter file and return their values.
    
    :param param_file: Path to the parameter file
    :param param_names: Names of the parameters to read
    :return: List of parameter values
    """
    params = []

    if not os.path.isfile(param_file):
        print(f"Error: {param_file} does not exist.")
        return params

    with open(param_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#') and ':' in line:
                name, value = line.split(':', 1)
                name = name.strip()
                value = value.strip()
                if name in param_names:
                    try:
                        params.append(float(value))
                    except ValueError:
                        try:
                            params.append(int(value))
                        except ValueError:
                            params.append(value)
    return params

def read_stations(stations_file):
    """ Read the station file and return the station coordinates.
    
    :param stations_file: Path to the station file
    :return: List of station coordinates
    """
    coordinates = []
    
    if not os.path.isfile(stations_file):
        print(f"Error: {stations_file} does not exist.")
        return coordinates
    
    with open(stations_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 6:
                try:
                    x = float(parts[2])
                    y = float(parts[3])
                    z = float(parts[5])
                    coordinates.append((x, y, z))
                except ValueError:
                    print(f"Error: Invalid coordinate values in line: {line.strip()}")
    return coordinates

# Set CUBIT path and import cubit module
sys.path.append("/home/zhangming/Software/cubit/bin/")
try:
    import cubit
except ImportError:
    print("Error: Unable to import Cubit. Make sure the CUBIT_PATH is correct.")
    sys.exit(1)

# File paths
param_file = './DATA/CMTSOLUTION'
station_file = './DATA/STATIONS'
model_folder = './model'

# Read source parameters
source = read_parameters(param_file, 'longorUTM', 'latorUTM', 'depth')
if not source:
    print("Error: Could not read source parameters.")
    sys.exit(1)

# Create source vertex in CUBIT
cubit.cmd(f'create vertex location {source[0]} {source[1]} {source[2]} color red')

# Read and plot stations
stations = read_stations(station_file)
for station in stations:
    cubit.cmd(f'create vertex location {station[0]} {station[1]} {station[2]} color black')

# Import STL model and adjust visualization
cubit.cmd('import cubit "./MESH/meshing.cub"')
cubit.cmd('block all visibility off')
cubit.cmd('Mesh visibility off')
cubit.cmd('graphics mode wireframe geometry')
cubit.cmd('hardcopy "./model/receiver_source_1.png" png')
cubit.cmd('graphics mode transparent geometry')
cubit.cmd('hardcopy "./model/receiver_source_2.png" png')

print("Mesh and stations plotted in Cubit.")
