# -*- coding: utf-8 -*-
"""
WORKING SCRIPT
Created on Wed Oct 28 10:46:18 2020
@author: Vinicius 
"""

import serial
import time
import RPi.GPIO as GPIO
import os
import pandas as pd
from datetime import datetime

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")


# function used to append weight data. 
"""
It uses the weight_list variable dictionary list to create a structured .csv file.
Whenever the function is called, datetime.now() is ran to update the current date and time.
If the RFID tag has been seen before, the data is appended to the existing file.
If the RFID tag has never been seen before, a new file is created.

CSV output looks like:
Weight Date_Time
3.4    2021-02-20 14:03:00.228348
4.3    2021-02-20 15:02:51.248299
2.5    2021-02-21 12:25:40.663348
"""
def append_weight(weight=[]):
    weight_list.update({'Weight': [weight_data]})
    weight_list.update({'Date_Time': [datetime.now()]})
    
    df_w = pd.DataFrame(weight_list)
    print(df_w)

    if not os.path.isfile(animaltag + "_weight.csv"):
        df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
    else:
        df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    
# Exact same structure as append_weight, but it has three variables instead
"""
CSV output looks like:
Rotation  Type  Date_Time
+         START 2021-02-20 14:03:00.228348
5.225     Food  2021-02-20 14:04:02.724573
2.652     Run   2021-02-20 14:05:52.846536
-         END   2021-02-21 14:07:23.543257
"""
def append_event(cycles_str=[],event_type=[]):
    event_list.update({'Rotation': [cycles_str]})
    event_list.update({'Type': [event_type]})
    event_list.update({'Date_Time': [datetime.now()]})
    
    df_e = pd.DataFrame(event_list)
    print(df_e)

    if not os.path.isfile(animaltag + "_events.csv"):
        df_e.to_csv(animaltag + "_events.csv", encoding="utf-8-sig", index=False)
    else:
        df_e.to_csv(animaltag + "_events.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)

# creates empty dictionaries for the weight_list and event_list (it is a dictionary because of Pandas compatibility)
weight_list = {
    "Weight": [],
    "Date_Time": []
}

event_list = {
    "Rotation": [],
    "Type" : [],
    "Date_Time": []
}

# should we consolidate the following code? It does the same thing for two USB devices.

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 100000 # we do not want the device to timeout
# test device connection
ser.open()
ser.flush()
if ser.is_open==True:
    print("\nScale ok. Configuration:\n")
    print(ser, "\n") #print serial parameters
ser.close()

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = '/dev/ttyUSB1' #Arduino serial port
serRFID.baudrate = 9600
serRFID.timeout = 100000 # we do not want the device to timeout
# test device connection
serRFID.open()
if serRFID.is_open==True:
    print("\nRFID antenna ok. Configuration:\n")
    print(serRFID, "\n") #print serial parameters
serRFID.close()

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD) 

# set pin inputs from arduino
beam_break_1 = 35 # beam break 1
beam_break_2 = 36
beam_break_3 = 33
beam_break_4 = 38
beam_break_5 = 37
clk=12 # clock for running wheel

GPIO.setup(beam_break_1,GPIO.IN)
GPIO.setup(beam_break_2,GPIO.IN)
GPIO.setup(beam_break_3,GPIO.IN)
GPIO.setup(beam_break_4,GPIO.IN)
GPIO.setup(beam_break_5,GPIO.IN)
GPIO.setup(clk,GPIO.IN)
clkLastState=GPIO.input(clk)

# set pin outputs to arduino
Pi_RFID = 16 
Pi_scale = 15
Pi_capture_1 = 40
PiArd_reset = 18 # reset arduino whenever script is run

GPIO.setup(Pi_RFID,GPIO.OUT)
GPIO.setup(Pi_scale,GPIO.OUT)
GPIO.setup(Pi_capture_1,GPIO.OUT)
GPIO.setup(PiArd_reset,GPIO.OUT)

GPIO.output(Pi_RFID,False)
GPIO.output(Pi_scale,False)
GPIO.output(Pi_capture_1,False)
GPIO.output(PiArd_reset,False)
time.sleep(0.3)
GPIO.output(PiArd_reset,True)

#state variables
MODE = 1
"""
MODE 1 = Listening for RFID input
MODE 2 = Listening for Beam Break 1 (after it is triggered, the animal will be weighed)
MODE 3 = Listening for Beam Break 2 (after it is triggered, the Pi camera is activated) and Beam Break 5 (after it is triggered, the animal has finished the session)
    - flag 1 = The animal is inside the maze and it will be able to choose between left and right
    - flag 0 = The animal has made a choice, either left or right
"""
flag = 1 # see illustration for flag system
cycle=1200 # cycle on running wheel gives approx this many counts
run_flag = 0
food_flag = 0
counter = 0

while True: # this infinite loop means that the system is always waiting for the RFID signal to start a new session
    while True: # this infinite loop is broken after one session is complete
        if MODE == 1: # 
            print("\nMODE 1\n")

            serRFID.open()
            serRFID.flush() # waits for transmission of outgoing serial data to be completed

            ser2 = serRFID.readline() # RFID string
            ser_string = str(ser2)
            print(ser_string)
                
            if len(ser_string) > 5:
                # trigger arduino to open servo1
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high
                # fixing animal tag (removes unnecessary characters)
                animaltag = ser_string[len(ser_string)-19:len(ser_string)-5]
                print(ser_string)

                #Append data
                append_event("+", "START")
                
                # switch mode and clean up RFID
                MODE = 2
                serRFID.close()
            print("\nMODE 2\n")

        if MODE == 2 and GPIO.input(beam_break_1): 
            print("\nMODE 2\n")
            GPIO.output(Pi_RFID,False) # closes door behind animal
            openscale = [] #store weight list

            ser.open()
            ser.flush()
            for x in range(8): # chuck eight lines of garbage 
                line=ser.readline()
                print(line)
            for x in range(20): # read 20lines*400ms=8s of data points
                line=ser.readline()
                print(line)
                # fixing string and converts to float
                line_as_list = line.split(b',')
                relProb = line_as_list[1]
                relProb_as_list = relProb.split(b'\n')
                relProb_float = float(relProb_as_list[0])
                relProb_float = relProb_float*1000 # kg to g
                openscale.append(relProb_float) # appends to list

            ser.close()
            weight_data = sum(openscale)/len(openscale) # average of data points
            # TO DO: CHECK IF STRING CONVERSION IS NECESSARY
            weight_data = str(round(weight_data,2)) # two digits of precision and converts to str

            # needs to be deleted for the next session
            del ser_string
            del ser2
            del openscale
            GPIO.output(Pi_RFID,True) # start signal = high

            #appending data to database
            append_weight(weight_data)

            # change mode and clean up
            MODE = 3
            flag=1
            print("\nMODE 3\n")
                        
        if MODE == 3 and GPIO.input(beam_break_2) and flag==1: #log a trial start
            print("\ntrial start\n")
            
            if food_flag==1:
                print("appending food pod data")
                cycles_str = str(round(counter/cycle, 2))
                append_event(cycles_str, "Food")
            
            if run_flag==1:
                print("appending running wheel data")
                cycles_str = str(round(counter/cycle, 2))
                append_event(cycles_str, "Run")
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            flag=0
            run_flag=0
            food_flag=0
            counter=0
            
        if MODE == 3 and GPIO.input(beam_break_5): #animal going back home
            print("\nAnimal is returning to home cage\n")
            GPIO.output(Pi_RFID,False) #stop camera capture/opto
            GPIO.output(Pi_capture_1,False)
            # Search for better alternatives
            time.sleep(10) #so the RFID doesn't read while animal is going back to cage
            MODE = 1

            #appending data to database
            append_event("-", "END")
            
            #BREAK OUT OF THE SESSION INFINITE LOOP
            break
                    
        if MODE == 3 and GPIO.input(beam_break_4) and flag==0: #log a maze event food
            print("\nfood pod\n")
            # more features to be added later: Pellet dispenser integration
            
            flag=1
            food_flag=1
            limit=cycle
            
        if food_flag==1: #record running wheel
            # to do: consolidate into function
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle

        if MODE == 3 and GPIO.input(beam_break_5) and flag==0: #log a maze event running wheel
            print("\nrunning wheel\n")
            
            flag=1
            run_flag=1
            limit=cycle

        if run_flag==1: #record running wheel
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle

    print("finally")