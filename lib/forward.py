#####################################################################
#                                                                   
# This script performs data forward modeling of wave fields on 
# irregular asteroids using SPECfem, including mesh generation 
# with CUBIT and file conversion required by SPECfem. 
# It sets up the environment, decomposes the mesh, generates 
# necessary databases, runs the SPECfem solver, and prepares 
# visualization of the wave field snapshots.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
# Usage:
# python script.py <start> <stop> <step>
# - <start>: The starting iteration for combining VTK files.
# - <stop>: The ending iteration for combining VTK files.
# - <step>: The step size between iterations for combining VTK files.
#
# Dependencies:
# - SPECfem software with binaries located at <SPECFEM_PATH>.
# - Python libraries: os, shutil, subprocess, datetime, sys.
#
# The script performs the following steps:
# 1. Set up the working environment by creating necessary directories,
#    linking executable files, and copying configuration files.
# 2. Decompose the mesh for parallel processing.
# 3. Generate databases required for the SPECfem solver.
# 4. Run the SPECfem solver for wave field simulation.
# 5. Combine VTK files to prepare snapshots of the wave field.
#
#####################################################################


import os
import shutil
import subprocess
from datetime import datetime
import sys

def run_command(command):
    """ Run a shell command and check for errors. 
    """
    result = subprocess.run(command, shell=True, check=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        exit(1)

def setup_example(currentdir, software_bin_path, data_dir):
    """ Set up the example environment. 
    """
    output_dir = os.path.join(currentdir, 'OUTPUT_FILES')
    bin_dir = os.path.join(currentdir, 'bin')
    
    # Setup directory structure
    os.makedirs(output_dir, exist_ok=True)
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)

    # Link executable files
    os.makedirs(bin_dir, exist_ok=True)
    for f in os.listdir(software_bin_path):
        if f.startswith('x'):
            src = os.path.join(software_bin_path, f)
            dst = os.path.join(bin_dir, f)
            if os.path.exists(dst):
                os.remove(dst)
            os.symlink(src, dst)

    # Copy configuration files
    shutil.copy(os.path.join(data_dir, 'Par_file'), output_dir)
    shutil.copy(os.path.join(data_dir, 'CMTSOLUTION'), output_dir)
    shutil.copy(os.path.join(data_dir, 'STATIONS'), output_dir)

def decompose_mesh(NPROC, mesh_dir, base_mpi_dir):
    """ Decompose the mesh. 
    """
    print("\n  Decomposing mesh...\n")
    run_command(f'./bin/xdecompose_mesh {NPROC} {mesh_dir} {base_mpi_dir}')

def generate_databases(NPROC):
    """ Generate databases. 
    """
    if NPROC == 1:
        print("\n  Running database generation...\n")
        run_command('./bin/xgenerate_databases')
    else:
        print(f"\n  Running database generation on {NPROC} processors...\n")
        run_command(f'mpirun -np {NPROC} ./bin/xgenerate_databases')

def run_solver(NPROC):
    """ Run the SPECfem solver. 
    """
    if NPROC == 1:
        print("\n  Running solver...\n")
        run_command('./bin/xspecfem3D')
    else:
        print(f"\n  Running solver on {NPROC} processors...\n")
        run_command(f'mpirun -np {NPROC} ./bin/xspecfem3D')

def combine_vtk(output_dir, start, stop, step):
    """ Prepare VTK file of wave field snapshot. 
    """
    output_combine_dir = os.path.join('Visualization', 'wave_field')
    os.makedirs(output_combine_dir, exist_ok=True)
    for line in range(start, stop + 1, step):
        run_command(f'./bin/xcombine_vol_data_vtk 0 0 velocity_Z_it{line:06}\
             {os.path.join(output_dir, "DATABASES_MPI")} {output_combine_dir} 0')

def main(specfem_path, start, stop, step):
    """ Main workflow for forward modeling. 
    """
    print(f"Running example: {datetime.now()}")
    currentdir = os.getcwd()
    software_bin_path = specfem_path
    data_dir = os.path.join(currentdir, 'DATA')
    setup_example(currentdir, software_bin_path, data_dir)

    # Get processor count and MPI path
    base_mpi_dir = None
    with open(os.path.join(data_dir, 'Par_file')) as f:
        for line in f:
            if line.startswith('NPROC') and '#' not in line:
                NPROC = int(line.split('=')[1].strip())
            if line.startswith('LOCAL_PATH'):
                base_mpi_dir = line.split('=')[1].strip()

    if base_mpi_dir:
        os.makedirs(base_mpi_dir, exist_ok=True)
    else:
        print("Error: LOCAL_PATH not found in Par_file.")
        exit(1)

    decompose_mesh(NPROC, os.path.join(currentdir, 'MESH'), base_mpi_dir)
    generate_databases(NPROC)
    run_solver(NPROC)
    print(f"\nSee results in directory: {os.path.join(currentdir, 'OUTPUT_FILES')}/")
    print("\nDone")
    print(datetime.now())

    # Prepare VTK file of wave field snapshot
    combine_vtk(os.path.join(currentdir, 'OUTPUT_FILES'), start, stop, step)

if __name__ == "__main__":
    # Read parameters from command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python script.py <start> <stop> <step>")
        exit(1)

    try:
        start = int(sys.argv[1])
        stop = int(sys.argv[2])
        step = int(sys.argv[3])
    except ValueError:
        print("Error: All arguments must be integers.")
        exit(1)

    SPECFEM_PATH = '../../../specfem/bin'
    main(SPECFEM_PATH, start, stop, step)
