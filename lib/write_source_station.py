#####################################################################
#                                                                   
# This script generates two key files used in seismic simulations:
# 
# 1. CMTSOLUTION: This file contains information about the seismic
#    event's source location, magnitude, and other parameters. It is 
#    generated using the `write_source` function.
# 
# 2. STATIONS: This file defines the coordinates of receiver stations 
#    distributed around a spherical object (e.g., an asteroid). It is 
#    generated using the `write_station` function.
# 
# By Zhangming at USTC, zm5259@mail.ustc.edu.cn                     
#                                            
# Sept, 2024
#
#####################################################################

import os
import numpy as np

def write_source(source, f0, M):
    """
    Create the CMTSOLUTION file with event information.

    Parameters:
    source : tuple
        A tuple (longitude/x, latitude/y, depth/z) for the source location.
    f0 : float
        The frequency parameter for the source.
    M : tuple
        A tuple (Mrr, Mtt, Mpp, Mrt, Mrp, Mtp) representing the moment tensor.
    """
    
    # Create the directory to store event file
    event_dir = 'DATA'
    if not os.path.exists(event_dir):
        os.makedirs(event_dir)

    # Event file path
    event_file = os.path.join(event_dir, 'CMTSOLUTION')

    # Write the event data to the file
    with open(event_file, 'w') as f:
        f.write(f'PDE 2024 1 1 1 1 1 {source[1]:>10.6f} {source[0]:>10.6f} {source[2]:>10.6f} 0 0 Asteroid_forward \n')
        f.write('event name:       Asteroid_forward \n')
        f.write('time shift:       0.0000\n')
        f.write(f'f0:       {f0:>10.6f}\n')
        f.write(f'latorUTM:       {source[1]:>10.6f}\n')
        f.write(f'longorUTM:       {source[0]:>10.6f}\n')
        f.write(f'depth:       {source[2]:>10.6f}\n')
        f.write(f'Mrr:       {M[0]:>10.6f}\n')
        f.write(f'Mtt:       {M[1]:>10.6f}\n')
        f.write(f'Mpp:       {M[2]:>10.6f}\n')
        f.write(f'Mrt:       {M[3]:>10.6f}\n')
        f.write(f'Mrp:       {M[4]:>10.6f}\n')
        f.write(f'Mtp:       {M[5]:>10.6f}\n')

    print(f"Event file created: {event_file}")

def write_station(R, ntr=72, filepath='./DATA/STATIONS'):
    """
    Generate receiver coordinates based on a given radius R and write them to a file.

    Parameters:
    R : float
        The radius of the sphere.
    ntr : int, optional
        The number of receivers (default is 72).
    filepath : str, optional
        Output file path (default is './DATA/STATIONS').
    """
    
    # Define the angular range
    phiar = np.arange(0, 361, 5) * np.pi / 180
    thetar = 0.5 * np.pi
    xr, yr, zr = [], [], []
    
    # Generate the coordinates
    for i in range(ntr):
        rr = R
        phir = phiar[i]
        xr.append(rr * np.sin(thetar) * np.cos(phir))
        yr.append(rr * np.sin(thetar) * np.sin(phir))
        zr.append(0)
    
    vecr = np.column_stack([yr, xr, zr])
    
    # Create coordinate list
    coordinates = []
    
    for i in range(ntr):
        row = []
        # Generate receiver name
        char1 = chr(65 + (i // 26))  # First letter (ASCII)
        char2 = chr(65 + (i % 26))   # Second letter (ASCII)
        row.append(f'X{i+1}')
        row.append(f'{char1}{char2}')
        row.extend([yr[i], xr[i], 0.0, zr[i]])  # x, y, z coordinates
        
        coordinates.append(row)
    
    # Write the coordinates to the file
    with open(filepath, "w") as file:
        for row in coordinates:
            file.write(" ".join(map(str, row)) + "\n")
    
    print(f"Station file written to: {filepath}")

if __name__ == "__main__":
    # Default values for source and moment tensor, can be passed in externally
    source = (0.0, 500.0, 0.0)  # source = (longitude/x, latitude/y, depth/z)
    f0 = 0.02                   # Frequency
    M = (1.0e+23, 1.0e+23, 1.0e+23, 0.0, 0.0, 0.0)  # M = (Mrr, Mtt, Mpp, Mrt, Mrp, Mtp)

    # Call function to create the event file
    write_source(source, f0, M)

    R = 800  # Radius can be passed externally
    write_station(R)
