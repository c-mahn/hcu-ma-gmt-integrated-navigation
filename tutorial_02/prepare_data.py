# Micro Electro Mechanical Systems
# #############################################################################

# This python script prepares the data for further processing.

# Authors:
# Christopher Mahn
# Parastoo Oghlansheikhha
# Lukas-René Schulz
# Silas Teske
# Joshua Wolf
# Hajar Zare

# #############################################################################

# Import of Libraries
# -----------------------------------------------------------------------------

# import math as m
# import string as st
# import random as r
# import re
import os


# -----------------------------------------------------------------------------
# Debugging-Settings

verbose = True  # Shows more debugging information


# Functions
# -----------------------------------------------------------------------------

def convert_data(input_filename, output_filename):
    """
    This function takes the data from the file and converts it in a standard
    format for later processing.

    Args:
        input_filename (str): name of the file that will be converted
        output_filenames (str): the name of the output files the data will be
                                split and converted into. The different files
                                will be appended with "_01", "_02" and so on.
    """
    
    # Import of measurements
'''     file = open(os.path.join("data", input_filename))
    data = file.readlines()
    file.close()
    data.pop(0)
    for i, e in enumerate(data):
        if(verbose):
            print(f"[{i+1}/{len(data)}] Import", end="\r")
        if(e[0] != "/"):
            data[i] = e.strip().split(",")
            temp = []
            for j, f in enumerate(data[i]):
                if(j == 0):
                    temp.append(int(f)/int(Hz))  # Berechnung der Timestamps
                else:
                    temp.append(float(f))
            data[i] = temp '''

    # Export of converted measurements
'''     file = open(os.path.join("data", output_filename),f"w")
    for i, e in enumerate(data):
        if(verbose):
            print(f"[{i+1}/{len(data)}] Export", end="\r")
        for j, f in enumerate(e):
            if(j == 0):
                file.writelines(f"{f}")
            else:
                file.writelines(f"; {f}")
        file.writelines(f"\n")
    file.close()
    if(verbose):
        print(f"[{i+1}/{len(data)}] Done  ") '''


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    pass
