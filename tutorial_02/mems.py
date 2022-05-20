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
from turtle import position
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
# stationary = [{"start": 0, "end": 2500},
#               {"start": 0, "end": 1400},
#               {"start": 0, "end": 750},
#               {"start": 0, "end": 600},
#               {"start": 0, "end": 600},
#               {"start": 0, "end": 1950},
#               {"start": 0, "end": 130},
#               {"start": 0, "end": 215},
#               {"start": 0, "end": 800},
#               {"start": 0, "end": 390},
#               {"start": 0, "end": 350},
#               {"start": 0, "end": 200}]
stationary_track = {"before": [{"start": 15, "end": 710},
                               {"start": 7, "end": 597},
                               {"start": 11, "end": 485},
                               {"start": 7, "end": 522},
                               {"start": 7, "end": 250},
                               {"start": 16, "end": 300},
                               {"start": 16, "end": 509},
                               {"start": 34, "end": 548},
                               {"start": 14, "end": 556},
                               {"start": 23, "end": 432},
                               {"start": 0, "end": 0},
                               {"start": 17, "end": 576},
                               {"start": 23, "end": 392}],
                    "after": [{"start": 1125, "end": 1654},
                              {"start": 973, "end": 1320},
                              {"start": 923, "end": 1691},
                              {"start": 772, "end": 1467},
                              {"start": 821, "end": 1321},
                              {"start": 939, "end": 1391},
                              {"start": 1438, "end": 2041},
                              {"start": 1914, "end": 2338},
                              {"start": 1535, "end": 2229},
                              {"start": 1931, "end": 2294},
                              {"start": 0, "end": 0},
                              {"start": 1658, "end": 1999},
                              {"start": 1503, "end": 2348}]}
stationary_turntable = {"before": [{"start": 452, "end": 2574},
                                   {"start": 38, "end": 1427},
                                   {"start": 24, "end": 768},
                                   {"start": 17, "end": 589},
                                   {"start": 12, "end": 617},
                                   {"start": 21, "end": 1967},
                                   {"start": 7, "end": 140},
                                   {"start": 4, "end": 213},
                                   {"start": 10, "end": 818},
                                   {"start": 9, "end": 389},
                                   {"start": 6, "end": 354},
                                   {"start": 6, "end": 202}],
                        "after": [{"start": 5262, "end": 5583},
                                  {"start": 3621, "end": 3802},
                                  {"start": 2365, "end": 2840},
                                  {"start": 2250, "end": 2406},
                                  {"start": 1642, "end": 1879},
                                  {"start": 2901, "end": 3004},
                                  {"start": 1405, "end": 1645},
                                  {"start": 1249, "end": 1304},
                                  {"start": 1762, "end": 1834},
                                  {"start": 1760, "end": 1820},
                                  {"start": 1245, "end": 1346},
                                  {"start": 1158, "end": 1406}]}


# Functions
# -----------------------------------------------------------------------------

def printf(string, filename="output", end="\n"):
    """
    This function writes a string to a file instead of the command line. The
    output will always be appended to the file.

    Args:
        string (str): This string will be written
        filename (str, optional): This is the name of the file, the string will
                                  be written to. Defaults to "output.txt".
        end (str, optional): This is a appended return-character, that can also
                             be changed. Defaults to "\n".
    """
    if(verbose):
        print(f'[Info] Writing "{string}" to "{filename}.txt"')
    with open(os.path.join("data", f'{filename}.txt'), "a") as file:
        file.write(f'{string}{end}')


def clearf(filename="output"):
    """
    This function removes the contents of a file.

    Args:
        filename (str, optional): This specifies the file to be cleared.
                                  Defaults to "output".
    """
    if(verbose):
        print(f'[Info] Clearing "{filename}.txt"')
    with open(os.path.join("data", f'{filename}.txt'), "w") as file:
        file.write("")


def import_data(input_filename):
    """
    This function is used to import a singe measurement string of ins-data.

    Args:
        input_filename (str): This specifies the name of the file, that will be
        imported.
    """
    # Opening and reading file from disk
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if(verbose):
        print(f'[Info] Opening file "{input_filename}"', end="\r")
    with open(os.path.join("data", input_filename)) as file:
        if(verbose):
            print(f'[Info] Reading file "{input_filename}"', end="\r")
        data = file.readlines()
    if(verbose):
        print(f'[Info] Read file "{input_filename}" successfully')

    # Formating the data from disk into a two-dimentional list
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
                print(f'[Warn] Found weiredly formatted data at line {i+1}{20*" "}')
    if(verbose):
        print("")
    
    # Return the loaded data
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return(data)      


def calc_offset(data, start=0, end=None):
    """
    This function determines the offset/bias of a specific set of values from a
    list. Using the optional start and end indexes a specific set of values can
    be selected from the data.

    Args:
        data ([float]): A list with values serves as the provided data
        start (int, optional): By providing a starting value the data partially
                               selected
        end (int, optional): By providing an ending value the data partially
                             selected
    """
    if(verbose):
        print(f'[Info] Determing a bias')
    if(end==None):
        end = len(data)
    data = np.array(data)
    bias = np.mean(data[start:end])
    return(bias)


def remove_bias(data, bias):
    """
    This function substracts an offset of a list of sensor-values.

    Args:
        data ([float]): This is the sensor-data that will be removed of bias
        bias (float): This is the bias, that will be removed from the data
    """
    for i, e in enumerate(data):
        if(verbose):
            print(f'[Info][{i+1}/{len(data)}] Removing bias from data', end="\r")
        data[i] = e-bias
    if(verbose):
        print("")
    return(data)


def remove_bias_advanced(data, bias1, bias2, index1, index2):
    """
    This function removes bias from data. For anything before index1, bias1
    will be removed and after index2, bias2 will be removed. In between index1
    and index2 the removal of the bias will be interpolated in a linear way.

    Args:
        data ([float]): This data the bias-removal will be applied to
        bias1 (float): bias at the beginning of the measurement
        bias2 (_type_): bias at the end of the measurement
        index1 (int): index marking the beginning of the movement
        index2 (int): index marking the end of the movement
    """
    for i, e in enumerate(data):
        if(verbose):
            print(f'[Info][{i+1}/{len(data)}] Removing bias from data (advanced)', end="\r")
        if(i <= index1):
            data[i] = e-bias1
        elif(i >= index2):
            data[i] = e-bias2
        else:
            bias2_part = (i-index1)/(index2-index1)
            bias1_part = 1-bias2_part
            data[i] = e-(bias1*bias1_part)-(bias2*bias2_part)
    if(verbose):
        print("")
    return(data)


def calc_velocity(accelerometer_data, timestamp_data):
    """
    This function calculates the velocity from data of an accelerometer and
    their designated timestamps.

    Args:
        accelerometer_data ([{"x": float, "y": float, "z": float}]): This is the accelerometer-data
                                                                     and must be formatted as dictionaries
                                                                     inside of a list
        timestamp_data ([float]): This is timestamp-data from the measurements
                                  of the accelerometer
    """
    velocity = {"x": [], "y": [], "z": []}
    velocity_i = {"x": 0.0, "y": 0.0, "z": 0.0}
    for i, e in enumerate(timestamp_data):
        for j, xyz in enumerate(["x", "y", "z"]):
            if(verbose):
                print(f'[Info][{i+1}/{len(timestamp_data)}][{j+1}/3] Calculating velocities', end="\r")
            if(i==0):
                velocity_i[xyz] += accelerometer_data[xyz][i]*e
            else:
                velocity_i[xyz] += accelerometer_data[xyz][i]*(e-timestamp_data[i-1])
            velocity[xyz].append(velocity_i[xyz])
    if(verbose):
        print("")
    return(velocity)


def calc_position(accelerometer_data, timestamp_data, velocity_data):
    """
    This function calculates positions based on velocity-data and timestamps.

    Args:
        accelerometer_data ([{"x": float, "y": float, "z": float}]): This is the accelerometer-data
                                                                     and must be formatted as dictionaries
                                                                     inside of a list
        timestamp_data ([float]): This is timestamp-data for the velocity-data
    """
    position = {"x": [], "y": [], "z": []}
    position_i = {"x": 0.0, "y": 0.0, "z": 0.0}
    for i, e in enumerate(timestamp_data):
        for j, xyz in enumerate(["x", "y", "z"]):
            if(verbose):
                print(f'[Info][{i+1}/{len(timestamp_data)}][{j+1}/3] Calculating positions', end="\r")
            if(i==0):
                position_i[xyz] += 0.5*accelerometer_data[xyz][i]*(e**2)+velocity_data[xyz][i]*e
            else:
                position_i[xyz] += 0.5*accelerometer_data[xyz][i]*((e-timestamp_data[i-1])**2)+velocity_data[xyz][i]*(e-timestamp_data[i-1])
            position[xyz].append(position_i[xyz])
    # if(verbose):
    #     print("")
    return(position)


def calc_turnrates(gyroscope_data, timestamp_data):
    """
    This function calculates the rotation based on velocity-data and timestamps.

    Args:
        gyroscope_data ([{"x": float, "y": float, "z": float}]):     his is the gyroscope-data
                                                                     and must be formatted as dictionaries
                                                                     inside of a list
        timestamp_data ([float]): This is timestamp-data for the velocity-data
    """
    turnrates = {"x": [], "y": [], "z": []}
    turnrates_i = {"x": 0.0, "y": 0.0, "z": 0.0}
    for i, e in enumerate(timestamp_data):
        for j, xyz in enumerate(["x", "y", "z"]):
            if(verbose):
                print(f'[Info][{i+1}/{len(timestamp_data)}][{j+1}/3] Calculating turnrates', end="\r")
            if(i==0):
                turnrates_i[xyz] += gyroscope_data[xyz][i]*e
            else:
                turnrates_i[xyz] += gyroscope_data[xyz][i]*(e-timestamp_data[i-1])
            turnrates[xyz].append(turnrates_i[xyz])
    # if(verbose):
    #     print("")
    return(turnrates)


def calc_distances(positions, stationary_start, stationary_end):
    """
    This function calculates the rotation based on velocity-data and timestamps.

    Args:
        gyroscope_data ([{"x": float, "y": float, "z": float}]):     his is the gyroscope-data
                                                                     and must be formatted as dictionaries
                                                                     inside of a list
        timestamp_data ([float]): This is timestamp-data for the velocity-data
    """
    delta = []
    for xyz in ["x", "y", "z"]:
        delta.append((positions[xyz][stationary_end["start"]]-positions[xyz][stationary_start["end"]])**2)
    distance = np.sqrt(delta[0]+delta[1]+delta[2])
    # if(verbose):
    #     print("")
    return(distance)


def write_bias_acceleration(bias_data, filename, measurement):
    """
    This funtion writes the bias of the measurements to a file on disk.

    Args:
        bias_data ([float]): The bias of the data must be formatted in
                          [x, y, z] and the unit of measurement must be m/s²
        filename (str): This is the filename under wich the data will be
                        appended to.
        measurement (str): This specifies the description of the measurement
                           and will be printed only for user-friendlyness
                           purposes
    """
    if(verbose):
        print(f'[Info] Writing biases of measurement {measurement} to "{filename}.txt"')
    printf(f'The following biases were determined for measurement "{measurement}":', filename)
    printf(f'X: {bias_data[0]:.6f} m/s^2', filename)
    printf(f'Y: {bias_data[1]:.6f} m/s^2', filename)
    printf(f'Z: {bias_data[2]:.6f} m/s^2', filename)
    printf(f'{15*"- "}-', filename)
    printf("", filename)


def write_bias_rotation(bias_data, filename, measurement):
    """
    This funtion writes the bias of the measurements to a file on disk.

    Args:
        bias_data ([float]): The bias of the data must be formatted in
                          [x, y, z] and the unit of measurement must be m/s²
        filename (str): This is the filename under wich the data will be
                        appended to.
        measurement (str): This specifies the description of the measurement
                           and will be printed only for user-friendlyness
                           purposes
    """
    if(verbose):
        print(f'[Info] Writing biases of measurement {measurement} to "{filename}.txt"')
    printf(f'The following biases were determined for measurement "{measurement}":', filename)
    printf(f'X: {bias_data[0]:.6f} degree/s', filename)
    printf(f'Y: {bias_data[1]:.6f} degree/s', filename)
    printf(f'Z: {bias_data[2]:.6f} degree/s', filename)
    printf(f'{15*"- "}-', filename)
    printf("", filename)


def write_distance(distance, filename, measurement):
    """
    This funtion writes a distance of a measurement to a file on disk.

    """
    if(verbose):
        print(f'[Info] Writing distances of measurement {measurement} to "{filename}.txt"')
    printf(f'The following distance was determined for measurement "{measurement}":', filename)
    printf(f'{distance:.6f} m', filename)
    printf(f'{15*"- "}-', filename)
    printf("", filename)


def plot_data(datenreihen, timestamps=None, name=["Messwerte"]):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        if(timestamps==None):
            timestamps = range(len(datenreihe))
        plt.plot(timestamps, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    plt.title(name[0])
    plt.show()

def plot_data2(datenreihe1, datenreihe2, name=["Messwerte"]):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    plt.plot(datenreihe1, datenreihe2)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    plt.title(name[0])
    plt.show()

def plot_results(datenreihen, title_label, x_label, y_label, data_label, timestamps=None):
    """
    Temp text

    Args:
        datenreihen (_type_): _description_
        title_label (_type_): _description_
        x_label (_type_): _description_
        y_label (_type_): _description_
        data_label (_type_): _description_
        timestamps (_type_, optional): _description_. Defaults to None.
    """
    for i, datenreihe in enumerate(datenreihen):
        if(timestamps==None):
            timestamps = range(len(datenreihe))
        plt.plot(timestamps, datenreihe)
    plt.legend(data_label)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title_label)
    plt.show()


def process_data(measurement, number_of_measurements, stationary_indices):
    """
    Temp text.

    Args:
        measurement_data (_type_): _description_
        stationary_indices (_type_): _description_
    """
    # Clearing output-files
    clearf(f"{measurement}_biases")
    clearf(f"{measurement}_distances")
    
    # Running data-processing for each measurement
    for measurement_id in range(number_of_measurements):
        data = import_data(f"{measurement}_{measurement_id+1:02d}.csv")

        # Putting the data into sensor-streams as lists
        accelerometer = {"x": [], "y": [], "z": []}
        gyroscope = {"x": [], "y": [], "z": []}
        timestamps = []
        for sensor_info in data:
            timestamps.append(sensor_info[0]/1000)
            for i, e in enumerate(["x", "y", "z"]):
                accelerometer[e].append(sensor_info[i+1])
                gyroscope[e].append(sensor_info[i+4])

        # Determine the biases before and after the movement for the accelerometer
        accelerometer_bias = {"before": {"x": 0.0, "y": 0.0, "z": 0.0},
                              "after": {"x": 0.0, "y": 0.0, "z": 0.0}}
        for i in ["before", "after"]:
            for xyz in ["x", "y", "z"]:
                accelerometer_bias[i][xyz] = calc_offset(accelerometer[xyz],
                                                       stationary_indices[i][measurement_id]["start"],
                                                       stationary_indices[i][measurement_id]["end"])
            write_bias_acceleration([accelerometer_bias[i]["x"],
                                     accelerometer_bias[i]["y"],
                                     accelerometer_bias[i]["z"]],
                                     f'{measurement}_biases',
                                     f'{measurement_id+1:02d} ({i} movement)')

        # Determine the biases before and after the movement for the gyroscope
        gyroscope_bias = {"before": {"x": 0.0, "y": 0.0, "z": 0.0},
                          "after": {"x": 0.0, "y": 0.0, "z": 0.0}}
        for i in ["before", "after"]:
            for xyz in ["x", "y", "z"]:
                gyroscope_bias[i][xyz] = calc_offset(gyroscope[xyz],
                                                   stationary_indices[i][measurement_id]["start"],
                                                   stationary_indices[i][measurement_id]["end"])
            write_bias_rotation([gyroscope_bias[i]["x"],
                                 gyroscope_bias[i]["y"],
                                 gyroscope_bias[i]["z"]],
                                 f'{measurement}_biases',
                                 f'{measurement_id+1:02d} ({i} movement)')

        # Removing biases
        for xyz in ["x", "y", "z"]:
            accelerometer_without_bias = remove_bias_advanced(accelerometer[xyz],
                                                              accelerometer_bias["before"][xyz],
                                                              accelerometer_bias["after"][xyz],
                                                              stationary_indices["before"][measurement_id]["end"],
                                                              stationary_indices["after"][measurement_id]["start"])
            gyroscope_without_bias = remove_bias_advanced(gyroscope[xyz],
                                                          gyroscope_bias["before"][xyz],
                                                          gyroscope_bias["after"][xyz],
                                                          stationary_indices["before"][measurement_id]["end"],
                                                          stationary_indices["after"][measurement_id]["start"])


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    process_data("data_track", 13, stationary_track)
    process_data("data_rotation", 12, stationary_turntable)
    
    
    list_of_distances = []
    
    # Clear files of any content
    with open(os.path.join("data", "biases.txt"), "w") as file:
        file.write("")
    with open(os.path.join("data", "distances.txt"), "w") as file:
        file.write("")
    with open(os.path.join("data", "biases_rotation.txt"), "w") as file:
        file.write("")
    
    # Processing the Track-Data
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Iterating over several measurements the data get's processed
    for measurement_id in range(13):
        data = import_data(f'data_track_{measurement_id+1:02d}.csv')

        # Putting the data into sensor-streams as lists
        accelerometer = {"x": [], "y": [], "z": []}
        gyroscope = {"x": [], "y": [], "z": []}
        timestamps = []
        for sensor_info in data:
            timestamps.append(sensor_info[0]/1000)
            for i, e in enumerate(["x", "y", "z"]):
                accelerometer[e].append(sensor_info[i+1])
                gyroscope[e].append(sensor_info[i+4])

        # Plotting the sensor-information for determinating the stationary
        # parts during measurement
        # plot_data([accelerometer["x"], accelerometer["y"], accelerometer["z"],
        #            gyroscope["x"], gyroscope["y"], gyroscope["z"]], None,
        #           ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"])
        
        # Calculating the biases for the accelerometer
        bias = {"x": 0.0, "y": 0.0, "z": 0.0}
        for i in ["x", "y", "z"]:
            bias[i] = calc_offset(accelerometer[i],
                                  stationary_track["before"][measurement_id]["start"],
                                  stationary_track["before"][measurement_id]["end"])
        write_bias_acceleration([bias["x"], bias["y"], bias["z"]], "biases", f'{measurement_id+1:02d}')
        
        norm_acc = {"x": [], "y": [], "z": []}
        for i in ["x", "y", "z"]:
            norm_acc[i] = remove_bias(accelerometer[i], bias[i])

        # Plotting the normalised values
        # plot_data([norm_acc["x"], norm_acc["y"], norm_acc["z"]], None, ["acc_x", "acc_y", "acc_z"])

        velocities = calc_velocity(norm_acc, timestamps)
        positions = calc_position(norm_acc, timestamps, velocities)

        # Plotting the integrated values
        # plot_data([velocities["x"], velocities["y"], velocities["z"]], None, ["velocity_x", "velocity_y", "velocity_z"])
        # plot_data([positions["x"], positions["y"], positions["z"]], timestamp, ["position_x", "position_y", "position_z"])
        # plot_data2(positions["x"], positions["y"])

        distance = calc_distances(positions, stationary_track["before"][measurement_id], stationary_track["after"][measurement_id])
        if(measurement_id != 10):
            list_of_distances.append(distance)
        write_distance(distance, "distances", f'{measurement_id+1:02d}')
        if(verbose):
            print("")

        # Plotting the results
        # plot_results([norm_acc["x"], norm_acc["y"], norm_acc["z"]], f'Acceleration for measurement {measurement_id+1} on the track', "time [s]", "acceleration [m/s²]", ["x", "y", "z"], timestamp)
        # plot_results([velocities["x"], velocities["y"], velocities["z"]], f'Velocities for measurement {measurement_id+1} on the track', "time [s]", "velocity [m/s]", ["x", "y", "z"], timestamp)
        # plot_results([positions["x"], positions["y"], positions["z"]], f'Positions for measurement {measurement_id+1} on the track', "time [s]", "position [m]", ["x", "y", "z"], timestamp)

    distance_min = np.min(np.array(list_of_distances))
    printf(f'Min: {distance_min:6.3f} m', "distances")
    distance_max = np.max(np.array(list_of_distances))
    printf(f'Max: {distance_max:6.3f} m', "distances")
    distance_avg = np.average(np.array(list_of_distances))
    printf(f'Avg: {distance_avg:6.3f} m', "distances")
    distance_std = np.std(np.array(list_of_distances))
    printf(f'Std: {distance_std:6.3f} m', "distances")

    # Processing the Rotation-Data
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Iterating over several measurements the data get's processed
    for measurement_id_rotation in range(12):
        data_rotation = import_data(f'data_rotation_{measurement_id_rotation+1:02d}.csv')

        # Putting the data into sensor-streams as lists
        accelerometer_rotation = {"x": [], "y": [], "z": []}
        gyroscope_rotation = {"x": [], "y": [], "z": []}
        timestamps_rotation = []
        for sensor_info_rotation in data_rotation:
            timestamps_rotation.append(sensor_info_rotation[0]/1000)
            for i, e in enumerate(["x", "y", "z"]):
                accelerometer_rotation[e].append(sensor_info_rotation[i+1])
                gyroscope_rotation[e].append(sensor_info_rotation[i+4])

        # Plotting the sensor-information for determinating the stationary
        # parts during measurement
        # plot_data([accelerometer_rotation["x"], accelerometer_rotation["y"], accelerometer_rotation["z"],
        #            gyroscope_rotation["x"], gyroscope_rotation["y"], gyroscope_rotation["z"]], None,
        #           ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"])
        
        # Calculating the biases for the accelerometer
        bias_rotation = {"x": 0.0, "y": 0.0, "z": 0.0}
        for i in ["x", "y", "z"]:
            bias_rotation[i] = calc_offset(gyroscope_rotation[i],
                                           stationary_turntable["before"][measurement_id_rotation]["start"],
                                           stationary_turntable["before"][measurement_id_rotation]["end"])
        write_bias_rotation([bias_rotation["x"], bias_rotation["y"], bias_rotation["z"]], "biases_rotation", f'{measurement_id_rotation+1:02d}')
        
        norm_acc_rotation = {"x": [], "y": [], "z": []}
        for i in ["x", "y", "z"]:
            norm_acc_rotation[i] = remove_bias(gyroscope_rotation[i], bias_rotation[i])
    
        # Plotting the normalised values
        # plot_data([norm_acc_rotation["x"], norm_acc_rotation["y"], norm_acc_rotation["z"]], None, ["gyro_x", "gyro_y", "gyro_z"])

        velocities_rotation = calc_velocity(norm_acc_rotation, timestamps_rotation)
        positions_rotation = calc_position(norm_acc_rotation, timestamps_rotation, velocities_rotation)
        # plot_data2(positions_rotation["x"], positions_rotation["y"])

        turn = calc_turnrates(norm_acc_rotation, timestamps_rotation)
        if(verbose):
            print("\n")
        # Plotting the integrated values
        # plot_data([turn["x"], turn["y"], turn["z"]], None, ["turn_x", "turn_y", "turn_z"])

        # Plotting the results
        # plot_results([norm_acc_rotation["x"], norm_acc_rotation["y"], norm_acc_rotation["z"]], f'Rotation-rate for measurement {measurement_id_rotation+1} on the turntable', "time [s]", "rotation [°/s]", ["x", "y", "z"], timestamp_rotation)
        # plot_results([turn["x"], turn["y"], turn["z"]], f'Rotation for measurement {measurement_id_rotation+1} on the turntable', "time [s]", "rotation [°]", ["x", "y", "z"], timestamp_rotation)
