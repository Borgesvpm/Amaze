# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:46:18 2020

@author: Vinicius
"""

import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = 'COM3' 
ser.baudrate = 9600
ser.timeout = 100 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n") #print serial parameters

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = 'COM5' 
serRFID.baudrate = 9600
serRFID.timeout = 10000 #specify timeout when using readline()
serRFID.open()

while True:
    ser_string = serRFID.readline()
    ser_string = str(ser_string)

    if len(ser_string) > 5: 
        # fixing animal tag 
        ind = ser_string.find("x")
        animaltag = ser_string[len(ser_string)-19:len(ser_string)-5]
        print(ser_string)
        # getting date and time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        # triggering Openscale acquisition and plotting
        toggle = True
    #start plotting
    if toggle == True:
        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = [] #store trials here (n)
        ys = [] #store relative frequency here

        for x in range(8): # skip first few lines of data acquisition
            line=ser.readline()
            print(line)

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
            relProb_float = relProb_float*1000
            
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
            plt.ylabel('Incoming weight data (g)')
            plt.xlabel('Time(s)')
            plt.title(animaltag)
            
        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
        plt.show(block=False)
        plt.pause(30) # acquire data for 30 seconds
        
        # data thresholding
        treated_data = str(sum(ys)/len(ys))
        
        # save individual figures
        plt.savefig('C:/Users/Administrator2/Dropbox/My PC (DESKTOP-T85O4L4)/Desktop/' + animaltag + "-" + timestr + '.png')
        plt.close()
        
        # save data in txt file
        file1 = open(timestr[0:8] + "_weight_data.txt","a") 
        L = animaltag + "\t" + timestr + "\t" + treated_data + "\n"
        file1.writelines(L)
        file1.close() 
        
        # restart loop (wait for a new RFID signal)
        toggle=False
