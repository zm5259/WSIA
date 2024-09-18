#####################################################################
#                                                                   
# This script modifies parameters in a specified parameter file 
# (located in the DATA folder) according to a given dictionary of 
# parameter names and their new values. The script preserves the 
# formatting of the original file, ensuring that parameter values 
# are updated correctly while keeping the position of the equals 
# sign unchanged. 
#                                                                   
# Author: Zhangming at USTC
# Contact: zm5259@mail.ustc.edu.cn                     
# Date: September 2024
#
#####################################################################

import re
import sys

def format_value(value):
    """
    Format the value as a string. If it is a float with more than three decimal places,
    format it in scientific notation. Otherwise, convert it to a string directly.
    
    :param value: The value to format
    :return: The formatted value as a string
    """
    if isinstance(value, float):
        # If there are more than three decimal places, use scientific notation
        if len(f"{value:.10f}".rstrip('0').split('.')[-1]) > 3:
            return f"{value:.1e}"
        else:
            return f"{value:.10f}".rstrip('0').rstrip('.')  # Keep trailing zeroes and dot if necessary
    elif isinstance(value, bool):
        return '.true.' if value else '.false.'
    else:
        return str(value)

def modify_par_file(modifications):
    """
    Modify parameters in a parameter file by changing values after the equals sign,
    while keeping the position of the equals sign unchanged.
    
    :param modifications: Dictionary of parameter names and their new values
    """
    # Read file content
    with open('./DATA/Par_file', 'r') as file:
        lines = file.readlines()

    # Modify the needed parameters
    for i, line in enumerate(lines):
        # Use regex to find parameter name, equals sign, and value after equals sign
        match = re.match(r'(\s*\S+)(\s*=\s*)(.*)', line)
        if match:
            param_name, equal_sign, param_value = match.groups()
            # If parameter name is in the dictionary, update its value
            if param_name.strip() in modifications:
                new_value = format_value(modifications[param_name.strip()])
                # Convert boolean values to .true. or .false.
                if isinstance(new_value, bool):
                    new_value = '.true.' if new_value else '.false.'
                else:
                    # Convert other types to string
                    new_value = str(new_value)
                # Update value after equals sign, keeping format intact
                try:
                    lines[i] = f"{param_name}{equal_sign}{new_value.ljust(len(param_value))}\n"
                except Exception as e:
                    print(f"Error formatting line {i}: {e}")

    # Write updated content back to the file
    with open('./DATA/Par_file', 'w') as file:
        file.writelines(lines)
    
    print(f"Parameters in './DATA/Par_file' have been updated.")

def main():
    # Specify parameters to modify
    modifications = {
        'NPROC': 1,
        'NSTEP': 8000,
        'DT'   : 1.e-4,
        'GPU_MODE': True  # Use boolean value
        # Add more parameters and values here if needed
    }

    # Call function to modify the file
    modify_par_file(modifications)

if __name__ == "__main__":
    main()
