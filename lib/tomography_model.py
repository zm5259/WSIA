#####################################################################
#                                                                   
# This script generates a tomography model for an irregular asteroid
# based on input parameters. The model assigns velocities to a grid 
# that corresponds to the STL inclusion in the asteroid. The script 
# calculates grid points, assigns velocity values based on a gradient, 
# and writes the model to a file.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import os
import math
import argparse

def create_tomography_model(length, width, height, mesh_size, 
                            vp_min, vp_max, vs_min, vs_max, rho, gradient):
    """
    Create a tomography model for an irregular asteroid and save it to a file.
    
    :param length: Length of the model in x-direction
    :param width: Width of the model in y-direction
    :param height: Height of the model in z-direction
    :param mesh_size: Size of each grid cell
    :param vp_min: Minimum P-wave velocity
    :param vp_max: Maximum P-wave velocity
    :param vs_min: Minimum S-wave velocity
    :param vs_max: Maximum S-wave velocity
    :param rho: Density of the model
    :param gradient: Gradient of velocity change with depth
    """
    # Calculate origin and endpoint coordinates
    orig_x = -length / 2.0
    orig_y = -width / 2.0
    orig_z = -height / 2.0
    end_x = length / 2.0
    end_y = width / 2.0
    end_z = height / 2.0  # depth in negative z-direction

    # Calculate number of grid points
    nx = math.ceil(length / mesh_size)
    ny = math.ceil(width / mesh_size)
    nz = math.ceil(height / mesh_size)

    # Create header info
    header = f"{orig_x} {orig_y} {orig_z} {end_x} {end_y} {end_z}\n"
    header += f"{mesh_size} {mesh_size} {mesh_size}\n"
    header += f"{nx} {ny} {nz}\n"
    header += f"{vp_min} {vp_max} {vs_min} {vs_max} {rho} {rho}\n"

    # Create model values
    model_values = []
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                x = orig_x + i * mesh_size
                y = orig_y + j * mesh_size
                z = orig_z + k * mesh_size
                vp = vp_min + gradient * z
                vs = vs_min + gradient * z 
                model_values.append(f"{x} {y} {z} {vp} {vs} {rho}")

    # Write to file in DATA/tomo_files/
    tomo_dir = os.path.join('DATA/tomo_files')
    os.makedirs(tomo_dir, exist_ok=True)
    output_file = os.path.join(tomo_dir, 'tomography_model.xyz')
    
    with open(output_file, 'w') as f:
        f.write(header)
        f.write("\n".join(model_values))

    print(f"Created file: {output_file}")

# Allows the script to be called both as a function and run directly
if __name__ == "__main__":
    # Use argparse to receive command line parameters
    parser = argparse.ArgumentParser(description="Generate tomography model for STL inclusion")
    parser.add_argument('--length', type=float, default=100.0, help="Length of the model")
    parser.add_argument('--width', type=float, default=100.0, help="Width of the model")
    parser.add_argument('--height', type=float, default=50.0, help="Height of the model")
    parser.add_argument('--mesh_size', type=float, default=10.0, help="Mesh size for grid")
    parser.add_argument('--vp_min', type=float, default=3000.0, help="Minimum P-wave velocity")
    parser.add_argument('--vp_max', type=float, default=5000.0, help="Maximum P-wave velocity")
    parser.add_argument('--vs_min', type=float, default=1500.0, help="Minimum S-wave velocity")
    parser.add_argument('--vs_max', type=float, default=3000.0, help="Maximum S-wave velocity")
    parser.add_argument('--rho', type=float, default=2500.0, help="Density")
    parser.add_argument('--gradient', type=float, default=0.5, help="Gradient of velocity change with depth")
    
    args = parser.parse_args()

    # Call the function to generate the model
    create_tomography_model(args.length, args.width, args.height, args.mesh_size, 
                            args.vp_min, args.vp_max, args.vs_min, args.vs_max, 
                            args.rho, args.gradient)

# Example command to run the script:
# python script.py --length 200 --width 200 --height 100 --mesh_size 5
