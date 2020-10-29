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
import serial
import datetime
import time
import RPi.GPIO as GPIO

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 100 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n") #print serial parameters

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = '/dev/ttyUSB1' #Arduino serial port
serRFID.baudrate = 9600
serRFID.timeout = 10000 #specify timeout when using readline()
serRFID.open()

#initialize servo motor parameters
# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# set pin 11 as an output and set servo1 as pin as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11, 50 hz
servo1.start(0)
"""
The following code is an infinite loop.
1) The pi waits for an RFID signal
2) Once the RFID signal is receive, it moves the servo motor for 5 seconds and start plotting 30 seconds of weight data
3) The weight data is automatically saved in a txt file for the day and the individual plot figures are saved
in the same folder for later double checking 
4) After the weight data is saved, the pi returns to its original state, waiting for an RFID signal

TO DO:
3)
"""
while True:
    ser_string = serRFID.readline()
    if len(str(ser_string)) > 5: 
        print(str(ser_string))
        servo1.ChangeDutyCycle(7)
        time.sleep(5)
        servo1.ChangeDutyCycle(2)
        toggle = True
    #start plotting
    if toggle == True:
        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = [] #store trials here (n)
        ys = [] #store relative frequency here

        for x in range(10): # skip first few lines
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
            plt.title(str(ser_string))
            plt.ylabel('Incoming weight data (g)')
            plt.xlabel('Time(s)')
            
            # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
        plt.show(block=False)
        plt.pause(30)
        plt.savefig('/home/pi/Desktop/001.png')
        plt.close()
        toggle=False
