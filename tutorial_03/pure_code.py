import numpy as np
import matplotlib.pyplot as plt
import math
import os

# !pip install utm
import utm

location_gps = os.path.join("data", "trajectory_GPS.txt")
data_gps = np.loadtxt(location_gps, delimiter=";", skiprows=1)
# data_gps[:,0] = TIME | data_gps[:,1] = LAT | data_gps[:,2] = LON | data_gps[:,3] = ALT | data_gps[:,4] = sigma

measurement = np.zeros((len(data_gps),3))

for i in range(len(data_gps[:,0])):
  x, y, zone, ut = utm.from_latlon(data_gps[i,1], data_gps[i,2])
  measurement[i,0] = x
  measurement[i,1] = y
  measurement[i,2] = data_gps[i,3]

def printmeasurement(measurement, data_gps, end="\n"):
    with open(os.path.join("data", f'measurements.txt'), "a") as file:
      for i in range(len(measurement)):
        file.write(f'{data_gps[i,0]};{measurement[i,0]};{measurement[i,1]};{measurement[i,2]}{end}')

printmeasurement(measurement, data_gps)

"""
plt.plot(measurement[:,0], measurement[:,1], label='2D position')
plt.title('Plot of original data - position in x and y')
plt.xlabel('R [m]')
plt.ylabel('H [m]')
plt.legend()
plt.grid()
plt.show()

plt.plot(data_gps[:,0], measurement[:,2], label='hight')
plt.title('Plot of original data - position in z')
plt.xlabel('Time [s]')
plt.ylabel('Hight [m]')
plt.legend()
plt.grid()
plt.show()
"""

# x_dach_vektor = np.array([[547859.401, 5924922.99, 6.92086029]]).T # first measured point
x_dach_vektor = np.array([[547859.940, 5924919.95, 5.0]]).T

kov_x_dach_matrix = np.diag([1, 1, 1])

t_matrix = np.diag([1, 1, 1])

c_matrix = np.diag([1, 1, 1])

a_matrix = np.diag([1, 1, 1])

x_save_update = np.zeros((len(measurement),3))
P_save_update = np.zeros((len(measurement),3))

for j in range(len(measurement)):
  w_vektor = np.array([((np.random.randn(1,1)**2) * 5), ((np.random.randn(1,1)**2) * 5), ((np.random.randn(1,1)**2) * 5)])
  # w_vektor = np.array([np.random.normal(2, 1)**2, np.random.normal(2, 1)**2, np.random.normal(6, 3)**2])
  kov_w_matrix = np.identity(len(w_vektor))

  # step 0 - observation model
  l_vektor = np.array([[measurement[j,0], measurement[j,1], measurement[j,2]]]).T
  # observation uncertainty
  kov_l_matrix = np.diag([data_gps[j,4], data_gps[j,4], data_gps[j,4]*1.5])

  # step 1 - Prediction
  x_strich_vektor = np.array([x_dach_vektor[0], x_dach_vektor[1], x_dach_vektor[2]])  # state matrix
  kov_x_strich_matrix = t_matrix@kov_x_dach_matrix@np.transpose(t_matrix)+c_matrix@kov_w_matrix@np.transpose(c_matrix)  # stochastical model
  
  # step 2 - Innovation
  d_vektor = l_vektor-a_matrix@x_strich_vektor  # residuals between observation and prediction
  kov_d_matrix = kov_l_matrix+a_matrix@kov_x_strich_matrix@np.transpose(a_matrix)  # system uncertainty
  
  # step 3 - Kalman gain
  k_matrix = kov_x_strich_matrix@np.transpose(a_matrix)@np.linalg.inv(kov_d_matrix)  # Kalman gain  
  
  # step 4 - Update
  x_dach_vektor = x_strich_vektor+k_matrix@d_vektor  # update of state matrix
  kov_x_dach_matrix = (np.identity(len(k_matrix@a_matrix))-kov_x_dach_matrix)@kov_x_strich_matrix  # update of stochastical model
  
  # Value storage for visualisation
  x_save_update[j,0] = x_dach_vektor[0]
  x_save_update[j,1] = x_dach_vektor[1]
  x_save_update[j,2] = x_dach_vektor[2]

  P_save_update[j,0] = kov_x_dach_matrix[0,0]
  P_save_update[j,1] = kov_x_dach_matrix[1,1]
  P_save_update[j,2] = kov_x_dach_matrix[2,2]

def printx_save_update(x_save_update, data_gps, end="\n"):
    with open(os.path.join("data", f'x_save_update.txt'), "a") as file:
      for i in range(len(x_save_update)):
        file.write(f'{data_gps[i,0]};{x_save_update[i,0]};{x_save_update[i,1]};{x_save_update[i,2]}{end}')

printx_save_update(x_save_update, data_gps)

plt.plot(measurement[:,0], measurement[:,1], 'r-', label='original')
plt.plot(x_save_update[:,0], x_save_update[:,1], 'g-', label='filtered')
plt.title('Comparison - position in x and y')
plt.xlabel('R [m]')
plt.ylabel('H [m]')
plt.legend()
plt.grid()
plt.show()

plt.plot(data_gps[:,0], measurement[:,2], 'r-', label='original')
plt.plot(data_gps[:,0], x_save_update[:,2], 'g-', label='filtered')
plt.title('Comparison - position in z')
plt.xlabel('Time [s]')
plt.ylabel('Height [m]')
plt.legend()
plt.grid()
plt.show()