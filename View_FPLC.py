#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:40:08 2020

@author: Justin
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




### User Inputs ###

# Start is the number of data points at the beginnnig to skip (e.g. if too high)
# Default is 60 to avoid the zeroing bump
start = 10
end = -4

# Plot range. Change one of these to None for automatic.
# Unfortunately, it's all or nothing for now. full manual or full auto.
yrange = [ymin, ymax] = [None, None] # Set these to pick min and max on plot

# Update the file path to where the .asc file.
file = "/Users/Justin/Documents/Projects/2020/TM-EphA2-PIP2/Data/SMALPs/Size Exclusion/FPLC/2020-01-22/JMW SUPERDEX 200012 - SMA.asc"
#np_data = np.genfromtxt(file)
#print(np_data)




### Automated processes ###

# Determine whether manual range was selected above.
if None not in yrange:
    manual_range=True
else:
    manual_range=False

# Read in the data
file_handler = open(file, "r")
pd_data = pd.read_csv(file_handler, sep = '\t')
pd_data = np.array(pd_data)
file_handler.close()

def convert_float(data_to_convert):
    float_list = []
    for datum in data_to_convert:
        if not datum.isspace():
            float_list.append(float(datum))            
    return np.array(float_list)

def plot(x, y, label='', is_abs=True):
    '''
    Plotting function
    
    input:
        null
    output:
        a plot using global vars assigned in read_data function.
    '''
    plt.figure(figsize=(9,3))
    plt.plot(x[:len(y)], y)
    
    # axis range
    if manual_range:
        axes = plt.gca() # set up axis
        axes.set_ylim(ymin,ymax)

    #labeling
    if is_abs:
        plt.ylabel('mAu')
    else:
        plt.ylabel('MPa')
    plt.xlabel('Time (minutes)')
    plt.title(label)
    
    # ticks
    plt.xticks(np.arange(0, max(x), 5))
    if manual_range:
        step_size = (ymax-ymin)*0.1
        plt.yticks(np.arange(ymin, ymax, step_size))
    else:
        if max(y)>1000:
            step_size = round((max(y)-min(y))*0.1,0)
        else:
            step_size = round((max(y)-min(y))*0.1,2)
        plt.yticks(np.arange(min(y), max(y), step_size)) 

    plt.show()

# Data Assignments. Comment out curves that weren't saved.
x = convert_float(pd_data[start:end,0])
y260 = convert_float(pd_data[start:end,1])
y487 = convert_float(pd_data[start:end,3])
#pres = convert_float(pd_data[start:end,5])

# Output plots. Comment out plots not desired.
plot(x, y260, "260 nm")
plot(x, y487, "487 nm")
#plot(x, pres, "Pressure", False)
