#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:40:08 2020

@author: Justin
"""
import glob
import os
#import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


#### Inputs ####

from_dir = False
normalized = False # if true, data will be normalized
two_axis = True # if true, 1st and 2nd curve will have different axes
start = 60 # start/end define where the actual data is in the file. Default is 60.
end = -4 # default is -4
column1 = 3 # input which column contains the data, 1, 3, or 5
column2 = 3 # column 1 = 260 nm, 3 = 487 nm, 5 = pressure.
label1 = 'PCp2' # None if auto-label desired
label2 = 'pcp2 +SMA'
font_size = 14

# Use these settings if from_dir is true
path = "/Users/Justin/Documents/Projects/2020/TM-EphA2-PIP2/Data/SMALPs/Size Exclusion/FPLC/2020-06-03/" 
curve1_index = 0 # input a file number
curve2_index = 0

# use these settings if from_dir is false
path1 = '/Users/Justin/Documents/Projects/2020/TM-EphA2-PIP2/Data/SMALPs/Size Exclusion/FPLC/2020-06-03/JMW SUPERDEX200040.asc'
path2 = '/Users/Justin/Documents/Projects/2020/TM-EphA2-PIP2/Data/SMALPs/Size Exclusion/FPLC/2020-06-03/JMW SUPERDEX200048.asc'






#### Main Body ####


# Set labels based on data position.
# Matched columns for file 1 and file 2 get an automatic plot label.
# Relies on the fact that I always only run the same 2 wavelengths.
if column1 == 1 and column2 == 1:
    label = '260 nm'
    is_abs = True
elif column1 == 3 and column2 == 3:
    label = '487 nm'
    is_abs = True
elif column1 == 5 and column2 == 5:
    label = 'Pressure'
    is_abs = False    
else:
    label = ''
    is_abs = True



# Get the file names if pulling data from directory.
def get_filenames(ext='csv'): 
    '''returns list of all .ext file names in script directory.'''
    Fnames = sorted([i for i in glob.glob(os.path.join(path,'*.'+ext) )])
    print(("Found ")+str(len(Fnames))+(" files:"))     
    return Fnames

if from_dir:
    Fnames = get_filenames('asc') # Broken, should not try when from_dir is false
    for file in Fnames: print(file)   



# Read the data.
def get_data(file):
    file_handler = open(file, "r")
    dataframe = pd.read_csv(file_handler, sep = '\t')
    data = np.array(dataframe)
    file_handler.close()

    out_data = data[start:end,:].astype(np.float)
    return out_data

if from_dir:
    data_list = [get_data(fname) for fname in Fnames]
    s1 , s2 = [data_list[curve1_index], data_list[curve2_index]]
else:
    t1 , t2 = [get_data(path1), get_data(path2)]



# Subtract baseline or normalize the data.
def bs(one_curve):
    return one_curve-one_curve[0]

def norm(one_curve):
    return (one_curve-min(one_curve))/(max(one_curve)-min(one_curve))

if normalized:
    function = norm
else:
    function = bs


####  Style and plotting  ####
# If no labels specified, auto-label the data based on the file name.
if None in [label1, label2] and from_dir:
    label1 = Fnames[curve1_index][-23:-4]
    label2 = Fnames[curve2_index][-23:-4]
elif None in [label1, label2] and not from_dir:
    label1 = path1[-23:-4]
    label2 = path2[-23:-4]

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : font_size}

matplotlib.rc('font', **font)



def plot(s1, s2, label='', is_abs=True):
    '''
    Plotting function
    
    input:
        null
    output:
        a plot using global vars assigned in read_data function.
    '''
    plt.figure(figsize=(12,4))
    plt.plot(s1[:,0], function(s1[:,column1]),label=label1)
    plt.plot(s2[:,0], function(s2[:,column2]),label=label2)
    plt.legend()
    if is_abs:
        plt.ylabel('mAu')
    else:
        plt.ylabel('MPa')
    plt.xlabel('Time (minutes)')
    plt.xticks(np.arange(0, max(s1[:,0]), 5)) 
    plt.title(label)
    plt.show()

def subplot(s1, s2, label='', is_abs=True):
    '''
    Plotting function
    
    input:
        null
    output:
        a plot using global vars assigned in read_data function.
    '''
    
    if is_abs:
        ylabel = 'mAu'
    else:
        ylabel = 'MPa'
    xlabel = 'Time (minutes)'
    
    fig, ax1 = plt.subplots(figsize=(12,4))
    x1, y1 = s1[:,0], function(s1[:,column1])
    x2, y2 = s2[:,0], function(s2[:,column2])
    
    
    color = 'tab:blue'
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel, color=color)
    subplot1 = ax1.plot(x1, y1, color=color, label=label1)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
        
    color = 'tab:orange'
    ax2.set_ylabel(ylabel, color=color)  # we already handled the x-label with ax1
    subplot2 = ax2.plot(x2, y2, color=color, label=label2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    subplots = subplot1+subplot2
    labels = [l.get_label() for l in subplots]
    fig.legend(subplots, labels, loc='upper right', bbox_to_anchor=(0.9,0.9))
    
    
    fig.tight_layout()
    plt.title(label)
    plt.show()


if two_axis:
    if from_dir:
        subplot(s1, s2, label, is_abs)
    else:
        subplot(t1, t2, label, is_abs)
else:
    if from_dir:
        plot(s1, s2, label, is_abs)
    else:
        plot(t1, t2, label, is_abs)


