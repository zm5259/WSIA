#####################################################################
#                                                                   
# The main flow of wave field simulation of irregular asteroids     
# based on cubit and spectral element method is shown here          
#                                                                   
# by Zhangming at USTC, zm5259@mail.ustc.edu.cn                     
#                                            
# Sept, 2024
#
# Workflow
#
#####################################################################

# import modules
import os
from lib import  zoom,tomography_model,write_source_station,\
                plot_observation ,write_par_file,forward,generate_mesh,plot_wave

# SPECFEM and CUBIT Software install path
CUBIT_PATH = '/home/zhangming/Software/cubit/bin/'
SPECFEM_PATH = '/home/zhangming/Software/specfem/specfem3d/bin'
SPECFEM_GEOCUBIT_PATH =SPECFEM_PATH.rsplit('/',1)[0] +'/CUBIT_GEOCUBIT/geocubitlib/'
print(CUBIT_PATH,SPECFEM_PATH,SPECFEM_GEOCUBIT_PATH)


### adjust the STL file (model)
stl_file = './model/Phobos.stl'  # the model stl file that needs to be simulated
scale_factor = 18.0              # adjust to the size you need 
(dimensions1, length1, width1, height1),\
      (dimensions2, length2, width2, height2),new_stl_file = zoom.zoom_stl(stl_file, scale_factor)
# Print size before and after scaling
print(f'原始模型尺寸: 长 {dimensions1[0]}, 宽 {dimensions1[1]}, 高 {dimensions1[2]}')
print(f'原始模型包裹体尺寸: 长 {length2}, 宽 {width2}, 高 {height2}')
print(f'缩放后模型尺寸: 长 {dimensions2[0]}, 宽 {dimensions2[1]}, 高 {dimensions2[2]}')
print(f'缩放后模型包裹体尺寸: 长 {length2}, 宽 {width2}, 高 {height2}')

### create cubit model and convert mesh 
mesh_size=40      # mesh size
generate_mesh.generate_mesh(mesh_size,CUBIT_PATH,SPECFEM_GEOCUBIT_PATH) # call cubit split model and transform

### prepare velocity
# prepare velocity data
vp_max=6600           # vp_max
vp_min=5400           # vp_min
vs_max=4200           # vs_max
vs_min=3300           # vs_min
rho=2400              # rho (default density consistency)
gradient=0.0          # velocity gradient

# use the speed of the stl file inclusion to interpolate  
tomography_model.create_tomography_model(length2, width2, height2, mesh_size, 
                             vp_min, vp_max, vs_min, vs_max, rho, gradient)

### prepare source and station
# source
source=(0.0,500.0,0.0) # source=(longitude/x,latitude/y,depth/z)
f0 = 0.02              # Dominant frequency in Hz
M=(1.0e+23,1.0e+23,1.0e+23,0.0,0.0,0.0) # M=(Mrr,Mtt,Mpp,Mrt,Mrp,Mtp)
write_source_station.write_source( source, f0, M)

# receiver
R = 800            # Station layout radius of a circle
write_source_station.write_station(R)

### write par_file
# Control parameter file that needs to be modified
modifications = {
        'NPROC': 1,
        'NSTEP': 8000,
        'DT'   : 1.e-4,
        'GPU_MODE': True
        # Add more parameters and values here if needed
    }
# Call function to modify the file
write_par_file.modify_par_file( modifications)

### Forward and prepare vtk file of wave field snapshot
# (PATH,NTSTEP_BETWEEN_OUTPUT_SEISMOS NSTEP NTSTEP_BETWEEN_OUTPUT_SEISMOS*N )
forward.main(SPECFEM_PATH,100,2000,100)     


# ### Visualization
# # Plot STL files and save plots
# zoom.plot_stl_3d(stl_file, title='Original STL', save_as=os.path.join('model', 'original_stl.png'))
# zoom.plot_stl_3d(new_stl_file, title='Scaled STL', save_as=os.path.join('model', 'scaled_stl.png'))
# #plot observation
# plot_observation.main()
# plot wave from 
plot_wave.plot_seismic_waveform(dt=1e-4, nt=8000)
