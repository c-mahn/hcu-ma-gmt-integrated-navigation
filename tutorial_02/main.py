# Main-Script
# #############################################################################

# This python script automatically launches all other python scripts in the
# right order and computes the entire task.

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

def run_script(script_name):
    """
    This function executes python scripts via the command line.

    Args:
        script_name (str): name of the python script (eg: "demo.py")
    """
    if(verbose):
        print(f'[Info] Executing "{script_name}"')
    os.system(f'python3 {script_name}')
    os.system(f'C:/Users/wolfj/anaconda3/python.exe {script_name}')
    os.system(f'C:/Users/lukas/anaconda3/python.exe {script_name}')
    


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    run_script("prepare_data.py")
    run_script("mems.py")
