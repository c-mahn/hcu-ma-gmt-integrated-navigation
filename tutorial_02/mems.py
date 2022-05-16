# Micro Electro Mechanical Systems
# #############################################################################

# This python script...

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

# import string as st
# import random as r
# import re
# import matplotlib.pyplot as plt
# from scipy import interpolate
import numpy as np
# import math as m
# import sys
import os
# from scipy.fft import fft, fftfreq
# from scipy import signal


# -----------------------------------------------------------------------------
# Settings

verbose = True  # Shows more debugging information


# Functions
# -----------------------------------------------------------------------------


# Importing the data
def import_data(input_filename):
    if(verbose):
        print(f'[Info] Opening file "{input_filename}"', end="\r")
    with open(os.path.join("data", input_filename)) as file:
        if(verbose):
            print(f'[Info] Reading file "{input_filename}"', end="\r")
        data = file.readlines()
    if(verbose):
        print(f'[Info] Read file "{input_filename}" successfully')

    for i, e in enumerate(data):
        try:
            data[i] = e.split(';')
            for j, e in enumerate(data[i]):
                if(verbose):
                    print(f'[Info][{i+1}/{len(data)}][{j+1}/{len(data[i])}] Importing entries', end="\r")
                if(j==0):
                    data[i][j] = int(e.strip())
                else:
                    data[i][j] = float(e.strip())
        except(ValueError):
            if(verbose):
                print(f'[Info] Detected file header at line {i+1}{20*" "}')
    if(verbose):
        print("")
    return(data)      

# Determination of the biases
def bias_det(data):
    value = len(data)
    data = np.array(data)
    bias = np.array([np.mean(data[0:value,1]), np.mean(data[0:value,2]), np.mean(data[0:value,3]), np.mean(data[0:value,4]), np.mean(data[0:value,5]), np.mean(data[0:value,6])])
    return bias

def write_bias(bias, output_filename):
        if(verbose):
            print(f'[Info][{i+1}] Writing to file "biases.txt"')
        with open(os.path.join("data", f'{output_filename}.txt'), "a") as file:
            file.write(f'The biases for file {i+1:02d} are: {bias[0]:.6f} m/s², {bias[1]:.6f} m/s², {bias[2]:.6f} m/s², {bias[3]:.6f} °/s, {bias[4]:.6f} °/s, {bias[5]:.6f} °/s\n')
            if(verbose):
                print("")

  

# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    with open(os.path.join("data", "biases.txt"), "w") as file:
        file.write("")
    for i in range(12):
        data = import_data(f"data_rotation_{i+1:02d}.csv")
        bias = bias_det(data)
        write_bias(bias, "biases")