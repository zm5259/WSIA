#####################################################################
#                                                                   
# This script generates seismic waveform plots for an observation 
# system. It creates two types of plots: 
# 1. A plot showing the overall waveform for multiple stations, 
#    with data normalized and standardized.
# 2. A subplot figure showing the waveforms for four specific 
#    stations, allowing comparison of individual traces.
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_seismic_waveform(dt, nt, output_dir="./Visualization/wave_from/"):
    """
    Plot seismic waveforms and save the plots to files.
    
    :param dt: Time step in seconds
    :param nt: Number of time steps
    :param output_dir: Directory to save the output plots
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate time sequence
    time = np.linspace(0, nt * dt, nt)

    # Set the file path
    path1 = "./OUTPUT_FILES/"
    filehead = [chr(i) + chr(j) for i in range(65, 91) for j in range(65, 91)]  # Generate letter combinations
    
    # Plot the first figure showing waveforms for multiple stations
    plt.figure()
    for i in range(72):
        data_1 = np.loadtxt(path1 + filehead[i] + f'.X{i + 1}.FXZ.semd')
        # Standardize the data
        mean_data_1 = np.mean(data_1[:, 1])
        std_data_1 = np.std(data_1[:, 1])
        data_1[:, 1] = (data_1[:, 1] - mean_data_1) / std_data_1
        # Normalize the data
        max_data_1 = np.max(data_1[:, 1])
        min_data_1 = np.min(data_1[:, 1])
        data_1[:, 1] = (data_1[:, 1] - min_data_1) / (max_data_1 - min_data_1)
        plt.plot(time, data_1[:, 1] + 72 - i, 'k')

    plt.ylim(0, 72)
    plt.xlim(np.min(time), np.max(time))
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)
    plt.title('Seismic Waveform Plot', fontsize=15)
    plt.tight_layout()

    # Save the first figure
    plot1_path = os.path.join(output_dir, 'waveform_plot.png')
    plt.savefig(plot1_path, dpi=200)
    plt.close()

    # Data file paths for individual traces
    datapath1 = path1 + 'AA.X1.FXZ.semd'
    datapath2 = path1 + 'AS.X19.FXZ.semd'
    datapath3 = path1 + 'BK.X37.FXZ.semd'
    datapath4 = path1 + 'CC.X55.FXZ.semd'

    # Load the data for individual traces
    data1 = np.loadtxt(datapath1)[:, 1]
    data2 = np.loadtxt(datapath2)[:, 1]
    data3 = np.loadtxt(datapath3)[:, 1]
    data4 = np.loadtxt(datapath4)[:, 1]

    # Create a figure with 4 subplots for individual traces
    fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(8, 6))

    axs[0].plot(time, data1, color='k', linewidth=0.5)
    axs[0].set_title('Trace 1', fontsize=16)
    axs[0].set_ylabel('Value', fontsize=16)

    axs[1].plot(time, data2, color='k', linewidth=0.5)
    axs[1].set_title('Trace 19', fontsize=16)
    axs[1].set_ylabel('Value', fontsize=16)

    axs[2].plot(time, data3, color='k', linewidth=0.5)
    axs[2].set_title('Trace 37', fontsize=16)
    axs[2].set_ylabel('Value', fontsize=16)

    axs[3].plot(time, data4, color='k', linewidth=0.5)
    axs[3].set_title('Trace 55', fontsize=16)
    axs[3].set_xlabel('Time (s)', fontsize=16)
    axs[3].set_ylabel('Value', fontsize=16)

    # Remove top and right spines from each subplot for cleaner visualization
    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save the second figure
    plot2_path = os.path.join(output_dir, 'single_trace_plot.png')
    plt.savefig(plot2_path, dpi=200)
    plt.close()

    print(f"Plots saved at: {output_dir}")

# If running the script directly, call the function
if __name__ == "__main__":
    # External parameters dt and nt can be passed in
    plot_seismic_waveform(dt=1e-4, nt=8000)
