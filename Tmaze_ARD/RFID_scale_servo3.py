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
import time
import RPi.GPIO as GPIO
import os.path

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10000
#specify timeout when using readline()
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

# set pin inputs from arduino
ard_pi_1 = 35
ard_pi_2 = 36
ard_pi_3 = 37
ard_pi_4 = 38

GPIO.setup(ard_pi_1,GPIO.IN)
GPIO.setup(ard_pi_2,GPIO.IN)
GPIO.setup(ard_pi_3,GPIO.IN)
GPIO.setup(ard_pi_4,GPIO.IN)

# set pin outputs to arduino
Pi_RFID = 12
Pi_scale = 13

GPIO.setup(Pi_RFID,GPIO.OUT)
GPIO.setup(Pi_scale,GPIO.OUT)
GPIO.output(Pi_RFID,False)
GPIO.output(Pi_scale,False)
# GPIO.output(Pi_2_Arduino,False) # initialize output as false
# time.sleep(0.1)
beam_break_flag = 0
task_complete = 0
toggle_RFID = True
MODE = 1

try: 
    while True:
        if MODE == 1:
            ser_string = serRFID.readline()
            ser_string = str(ser_string)
                
            if len(ser_string) > 0 and toggle_RFID == True:
                # trigger arduino to open servo1
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high
                #time.sleep(0.5)
                #GPIO.output(Pi_2_Arduino,False)
                #time.sleep(0.5)
                
                # fixing animal tag 
                ind = ser_string.find("x")
                animaltag = ser_string[len(ser_string)-19:len(ser_string)-5]
                print(ser_string)
                
                # getting date and time of trial start
                timestr = time.strftime("%Y%m%d-%H%M%S")
                MODE = 2
            
        if MODE == 2 and GPIO.input(ard_pi_1): # TODO: CHECK SYNTAXif beam_break1, trigger OpenScale and matplotlib
            GPIO.output(Pi_RFID,False)
            print("ard_pi_1 is HIGH")
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
            plt.pause(10) # acquire data for 30 seconds
            
            # data thresholding
            treated_data = str(sum(ys)/len(ys))
            
            # save individual figures
            plt.savefig("/home/pi/Desktop/RFID_scale/" + animaltag + "-" + timestr + ".png")
            plt.close()
            
            # save data in txt file
            completeName = os.path.join("/home/pi/Desktop/RFID_scale/",  timestr[0:8] + "_weight_data.txt")
            
            file1 = open(completeName, "a")
            L = animaltag + "\t" + timestr + "\t" + treated_data + "\n"
            
            file1.writelines(L)
            file1.close() 
            
            # restart loop (wait for a new RFID signal)
            
            ser_string = 0
            beam_break_flag = 0
            
            GPIO.output(Pi_scale,True)
            time.sleep(0.5)
            GPIO.output(Pi_scale,False)
            
            GPIO.output(Pi_RFID,True) # start signal = high
            
            MODE = 3
            
        if MODE == 3 and GPIO.input(ard_pi_3):
            GPIO.output(Pi_RFID,False)
            MODE = 1
            GPIO.cleanup()
#             def restart():
#                 import sys
#                 print("argv was", sys.argv)
#                 print("sys.executable was", sys.executable)
#                 print("restart now")
#     
#                 import os
#                 os.execv(sys.executable, ['python'] + sys.argv)
finally:
    GPIO.cleanup()
        
#    if BB2 and task_complete == 0: # if beam_break2
        # close servo 2
#    if BB3 or BB4 and task_complete == 0: # if beam_break3 or beam_break4
        # append choice to data file
        # task_complete = 1
        
# Once task_complete == 1, then the animal is moving back in the maze 

#    if BB3 or BB4 and task_complete == 1: # if beam_break3 or beam_break4
        # pass
#    if BB2 and task_complete == 1: # if beam_break2
        # open servo 2
#    if BB1 and task_complete == 1:
        # close servo 2
        # start openscale(30s)
        # open servo 1
#    if RFID and task_complete ==1:
        # close servo 1
        # append total trial time to data file