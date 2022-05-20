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



# ---------------------------------------------------------------------------------------------------------------------------------

    
    
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

        distance = calc_distance(positions, stationary_track["before"][measurement_id], stationary_track["after"][measurement_id])
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
        data_rotation = import_data(f'data_turntable_{measurement_id_rotation+1:02d}.csv')

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

        turn = calc_rotation(norm_acc_rotation, timestamps_rotation)
        if(verbose):
            print("\n")
        # Plotting the integrated values
        # plot_data([turn["x"], turn["y"], turn["z"]], None, ["turn_x", "turn_y", "turn_z"])

        # Plotting the results
        # plot_results([norm_acc_rotation["x"], norm_acc_rotation["y"], norm_acc_rotation["z"]], f'Rotation-rate for measurement {measurement_id_rotation+1} on the turntable', "time [s]", "rotation [°/s]", ["x", "y", "z"], timestamp_rotation)
        # plot_results([turn["x"], turn["y"], turn["z"]], f'Rotation for measurement {measurement_id_rotation+1} on the turntable', "time [s]", "rotation [°]", ["x", "y", "z"], timestamp_rotation)
