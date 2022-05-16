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
import matplotlib.pyplot as plt
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
stationary = [2500, 1400, 750, 600, 600, 1950, 130, 215, 800, 390, 350, 200]

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
def bias_det(data, end, start=0):
    data = np.array(data)
    bias = [np.mean(data[start:end, 1]), np.mean(data[start:end, 2]), np.mean(data[start:end, 3])]
    return(bias)

# Writing the biases to a txt-file
def write_bias(bias, output_filename, index):
    for i, e in enumerate(bias):
        if(verbose):
            print(f'[Info][{index}] Writing to file "{output_filename}.txt"')
        with open(os.path.join("data", f'{output_filename}.txt'), "a") as file:
            file.write(f'The biases for file {index} are: {e[0]:.6f} m/s², {e[1]:.6f} m/s², {e[2]:.6f} m/s²\n')
            if(verbose):
                print("")

def plot_data(datenreihen, name=["Messwerte"]):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        zeit = range(len(datenreihe))
        if(i == 0):
            plt.plot(zeit, datenreihe, "o")
        else:
            plt.plot(zeit, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    plt.title(name[0])
    plt.show()

def int_acc(data, bias):
        # Normalization of the acceleration
        print(data)
        
        norm_acc = []
        for i in data[0]:
            norm_acc.append([i[1] + bias[0], i[2] + bias[1], i[3] + bias[2]])
        return(norm_acc)   
        
        


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    with open(os.path.join("data", "biases.txt"), "w") as file:
        file.write("")
    for i in range(12):
        data = import_data(f"data_rotation_{i+1:02d}.csv")
        #plot_data(np.transpose(data))    
        bias = []
        bias.append(bias_det(data, stationary[i]))
        write_bias(bias, "biases", f'{i+1:02d}')
        #norm_acc = int_acc(data, bias)       
        #plot_data(np.transpose(norm_acc))