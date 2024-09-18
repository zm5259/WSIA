"""
This script processes STL files, allowing for scaling and visualization of 3D models. It includes the following functions:
1. `calc_dims`: Calculates the bounding box and dimensions of the STL model.
2. `scale_model`: Scales the STL model, centers it at the origin, and saves it as a new STL file.
3. `plot_stl_3d`: Plots the STL file in 3D using matplotlib, with options to display or save the plot.
4. `zoom_stl`: Combines reading, scaling, and saving the STL file, and records the original and scaled model details to a text file.
5. `main`: The main program function, which processes a sample STL file (`Phobos.stl`), applies scaling, and visualizes both the original and scaled models.

Parameters:
- `stl_file`: The input STL file path.
- `scale_factor`: Factor by which to scale the model.

The script saves the following outputs:
- Scaled STL file in the same directory as the input.
- Detailed information about the original and scaled STL models in `model/stl_details.txt`.
- 3D plots of both the original and scaled models, saved as PNG files.

Usage:
Run the script as a standalone program, or call its functions within another codebase for STL processing tasks.

"""

import os
import math
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def calc_dims(model_mesh):
    """ Calculate dimensions of the STL file 
    """
    vertices = model_mesh.vectors.reshape(-1, 3)  # extract all vertex coordinates
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)
    dimensions = max_coords - min_coords

    # Calculate bounding box dimensions
    length_width = math.ceil(max(dimensions[0], dimensions[1]) * 1.2 / 10) * 10  # Ensure length and width are the same and rounded to nearest 10
    height = math.ceil(dimensions[2] * 1.2 / 10) * 10  # Ensure height is rounded to nearest 10

    return min_coords, max_coords, dimensions, length_width, length_width, height


def scale_model(model_mesh, scale_factor, output_filename):
    """ Scale the STL model, center it at the origin, and save the new file. 
    """

    # Apply scaling factor
    model_mesh.vectors *= scale_factor

    # Calculate the center of the model
    vertices = model_mesh.vectors.reshape(-1, 3)  # Extract all vertex coordinates
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)
    center = (min_coords + max_coords) / 2

    # Move the model to center at the origin
    translation = -center
    model_mesh.vectors += translation

    # Save the scaled and centered model
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)  # Ensure directory exists
    model_mesh.save(output_filename)

def plot_stl_3d(stl_file, title='3D Plot', save_as=''):
    """ Plot STL file in 3D 
    """
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    model_mesh = mesh.Mesh.from_file(stl_file)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each triangle
    for f in model_mesh.vectors:
        tri = Poly3DCollection([f], alpha=0.5, linewidths=0.5)
        ax.add_collection3d(tri)
    
    # Auto scale to the mesh size
    scale = model_mesh.vectors.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    
    ax.set_title(title)
    if save_as:
        plt.savefig(save_as)  # Save the plot to a file
    else:
        plt.show()  # Show the plot

def zoom_stl(stl_file, scale_factor):
    """ Work with STL files: calculate dimensions, scale models, draw models 
    """
    
    # Read STL file
    model_mesh = mesh.Mesh.from_file(stl_file)

    # Original dimensions
    min_coords1, max_coords1, dimensions1, length1, width1, height1 = calc_dims(model_mesh)
    original_details = (
        f'*******************************************************************\n'
        f'Original STL: {stl_file}\n'
        f'Min coords: {min_coords1}, Max coords: {max_coords1}\n'
        f'Dimensions (LxWxH): {dimensions1[0]} x {dimensions1[1]} x {dimensions1[2]} \n'
        f'Bounding box (LxWxH): {length1} x {width1} x {height1}\n'
    )

    # Scale model
    new_stl_file = stl_file[:-4] + f'_zoom{scale_factor}.stl'
    scale_model(model_mesh, scale_factor, new_stl_file)

    # Dimensions after scaling
    new_model_mesh = mesh.Mesh.from_file(new_stl_file)
    min_coords2, max_coords2, dimensions2, length2, width2, height2 = calc_dims(new_model_mesh)
    scaled_details = (
        f'*******************************************************************\n'
        f'Scale_factor: {scale_factor}\n'
        f'*******************************************************************\n'
        f'Scaled STL: {new_stl_file}\n'
        f'Min coords: {min_coords2}, Max coords: {max_coords2}\n'
        f'Dimensions (LxWxH): {dimensions2[0]} x {dimensions2[1]} x {dimensions2[2]} \n'
        f'Bounding box (LxWxH): {length2} x {width2} x {height2}\n'
    )

    # Save details to stl_details.txt
    details_filename = os.path.join('model', 'stl_details.txt')
    with open(details_filename, 'w') as f:
        f.write(original_details)
        f.write(scaled_details)


    return (dimensions1, length1, width1, height1), (dimensions2, length2, width2, height2), new_stl_file


def main():
    
    stl_file = './model/Phobos.stl'  
    scale_factor = 1.5  

    original_dims, scaled_dims, new_stl_file = zoom_stl(stl_file, scale_factor)

    print("Original Dimensions (LxWxH):", original_dims)
    print("Scaled Dimensions (LxWxH):", scaled_dims)

    plot_stl_3d(stl_file, title='Original STL', save_as=os.path.join('model', 'original_stl.png'))
    plot_stl_3d(new_stl_file, title='Scaled STL', save_as=os.path.join('model', 'scaled_stl.png'))

if __name__ == "__main__":
    main()
