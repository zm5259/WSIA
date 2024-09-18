#####################################################################
#                                                                   
# This script provides a Python-based method to visualize an 
# observation system. It plots the STL model, stations, and 
# source location using matplotlib. The script includes functions 
# to read parameters and station coordinates, locate the STL file, 
# and generate the plot.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import os
import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import glob

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

def plot_stl_and_stations(stl_file, stations, source):
    """ Plot STL model, stations, and source using matplotlib.
    
    :param stl_file: Path to the STL file
    :param stations: List of station coordinates
    :param source: Coordinates of the source
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    model_mesh = mesh.Mesh.from_file(stl_file)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for f in model_mesh.vectors:
        tri = Poly3DCollection([f], alpha=0.5, linewidths=0.5)
        ax.add_collection3d(tri)

    scale = model_mesh.vectors.flatten()
    ax.auto_scale_xyz(scale, scale, scale)

    ax.scatter(source[0], source[1], source[2], color='r', marker='*', s=100, label='Source')

    stations = np.array(stations)
    ax.scatter(stations[:, 0], stations[:, 1], stations[:, 2], color='k', marker='^', label='Stations')

    ax.set_title('STL Model with Source and Stations')

    output_dir = './model'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, 'observation.png'))

def find_zoom_stl_file(model_folder):
    """ Find the STL file containing 'zoom' in the specified folder.
    
    :param model_folder: Path to the folder containing STL files
    :return: Path to the found STL file or None if not found
    """
    stl_files = glob.glob(os.path.join(model_folder, '*zoom*.stl'))
    if not stl_files:
        print("Error: No STL file containing 'zoom' found.")
        return None
    return stl_files[0]

def main():
    """ Main function for Python plotting.
    """
    param_file = './DATA/CMTSOLUTION'
    station_file = './DATA/STATIONS'
    model_folder = './model'

    stl_file = find_zoom_stl_file(model_folder)
    if not stl_file:
        return

    source = read_parameters(param_file, 'longorUTM', 'latorUTM', 'depth')
    if not source:
        print("Error: Could not read source parameters.")
        return

    stations = read_stations(station_file)
    if not stations:
        print("Error: No stations found.")
        return

    plot_stl_and_stations(stl_file, stations, source)

if __name__ == "__main__":
    main()
