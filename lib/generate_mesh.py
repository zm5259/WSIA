#####################################################################
#                                                                   
# This part of the program is mainly based on CUBIT for model 
# mesh generation and file conversion required by SPECFEM.
# It finds an STL file with 'zoom' in the filename, generates 
# a mesh using CUBIT, and prepares files for SPECFEM.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import os
import sys
import glob

def find_zoom_stl_file(model_directory):
    """ Find STL file with 'zoom' in the filename
    
    :param model_directory: Directory to search for STL files
    :return: Path to the first STL file containing 'zoom' in the name
    :raises FileNotFoundError: If no such STL file is found
    """
    stl_files = glob.glob(os.path.join(model_directory, '*zoom*.stl'))
    if stl_files:
        return stl_files[0]  # Return the first match
    else:
        raise FileNotFoundError("No STL file with 'zoom' in the name was found.")

def generate_mesh(mesh_size, CUBIT_PATH, SPECFEM_PATH):
    """ Generate mesh using CUBIT and convert files for SPECFEM
    
    :param mesh_size: Desired size of the mesh
    :param CUBIT_PATH: Path to the CUBIT software
    :param SPECFEM_PATH: Path to the SPECFEM conversion library
    """
    # Find the STL file with 'zoom' in the name
    stl_file = find_zoom_stl_file('model')
    print(f"Using STL file: {stl_file}")

    # Setup the paths for cubit and specfem
    sys.path.append(CUBIT_PATH)
    sys.path.append(SPECFEM_PATH)

    try:
        import cubit
        import boundary_definition
        import cubit2specfem3d
    except ImportError as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)

    # Create a unique directory for mesh files
    os.makedirs('MESH', exist_ok=True)
    
    # Initialize cubit commands
    cubit.cmd('set duplicate block elements on')
    
    # Import STL file and adjust geometry
    cubit.cmd(f'import stl "{stl_file}" feature_angle 135.00 Spline merge ')
    cubit.cmd('vol 1 move x 0 y 0 z -980')
    cubit.cmd('merge all')
    
    # Generate mesh with specified size
    cubit.cmd(f'sculpt parallel volume all size {mesh_size}')
    
    # Define blocks and attributes
    cubit.cmd('block 1 add hex in volume 1 ')
    cubit.cmd('block 1 name "elastic tomography_model.xyz 1" ')
    cubit.cmd('block 1 attribute count 2')
    cubit.cmd('block 1 attribute index 1 -1')
    cubit.cmd('block 1 attribute index 2 2')
    
    # Define custom free surface
    cubit.cmd('skin block 1 make block 1000')
    cubit.cmd('block 1000 name "free_or_absorbing_surface_file_zmax" ')
    
    # Export to SPECFEM3D
    cubit2specfem3d.export2SPECFEM3D('MESH/')
    
    # Save the cubit file
    cubit.cmd(f'save as "MESH/meshing.cub" overwrite')

if __name__ == "__main__":
    # Define paths and parameters
    CUBIT_PATH = '../../../cubit/bin/'
    SPECFEM_PATH = '../../../specfem/CUBIT_GEOCUBIT/geocubitlib/'
    mesh_size = 20  # Example mesh size

    try:
        generate_mesh(mesh_size, CUBIT_PATH, SPECFEM_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
