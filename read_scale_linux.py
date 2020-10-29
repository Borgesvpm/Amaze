# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:46:18 2020

@author: Administrator2
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import datetime
import time

#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here

for x in range(8): # skip first few lines
    line=ser.readline()
    print(line)
    time.sleep(0.1)
    
# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    #Aquire and parse data from serial port

        
    line=ser.readline()      #ascii
    line_as_list = line.split(b',')
    i = int(line_as_list[0])
    i = i/1000

    relProb = line_as_list[1]
    relProb_as_list = relProb.split(b'\n')
    relProb_float = float(relProb_as_list[0])
    relProb_float = relProb_float
    
    # Add x and y to lists
    xs.append(i)
    ys.append(relProb_float)

    # Limit x and y lists to 20 items
    #xs = xs[-20:]
    #ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Real-time weight data')
    plt.ylabel('Incoming weight data')
    plt.xlabel('Time(s)')
    #plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()