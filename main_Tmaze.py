# -*- coding: utf-8 -*-
"""
WORKING SCRIPT
Created on Wed Oct 28 10:46:18 2020
@author: Vinicius 
"""

import argparse
import numpy as np
import serial
import time
import RPi.GPIO as GPIO
import os
import pandas as pd
from time import sleep
from datetime import datetime

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

def append_weight(weight=[]):
    weight_list.update({'Weight': [weight_data]})
    weight_list.update({'Date_Time': [datetime.now()]})
    
    df_w = pd.DataFrame(weight_list)
    print(df_w)

    if not os.path.isfile(animaltag + "_weight.csv"):
        df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
    else:
        df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    
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



weight_list = {
    "Weight": [],
    "Date_Time": []
}

event_list = {
    "Rotation": [],
    "Type" : [],
    "Date_Time": []
}

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 100000
#specify timeout when using readline()
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
serRFID.timeout = 100000 #specify timeout when using readline()
serRFID.open()
if serRFID.is_open==True:
    print("\nRFID antenna ok. Configuration:\n")
    print(serRFID, "\n") #print serial parameters
serRFID.close()

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# set pin inputs from arduino
ard_pi_1 = 35
ard_pi_2 = 36
ard_pi_3 = 37
ard_pi_4 = 38
ard_pi_5 = 33
GPIO.setup(ard_pi_1,GPIO.IN)
GPIO.setup(ard_pi_2,GPIO.IN)
GPIO.setup(ard_pi_3,GPIO.IN)
GPIO.setup(ard_pi_4,GPIO.IN)
GPIO.setup(ard_pi_5,GPIO.IN)

#set pin inputs from running wheel rotary encoder
clk=12
# dt=11
GPIO.setup(clk,GPIO.IN)
# GPIO.setup(dt,GPIO.IN)
clkLastState=GPIO.input(clk)

# set pin outputs to arduino
Pi_RFID = 16
Pi_scale = 15
Pi_capture_1=40
PiArd_reset=18
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
beam_break_flag = 0
task_complete = 0
MODE = 1
flag=1
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=0
food_flag=0

while True:
    while True:
        if MODE == 1:
            print("\nMODE 1\n")
            serRFID.open()
            serRFID.flush()
            ser2 = serRFID.readline()
            ser_string = str(ser2)
            print(ser_string)
                
            if len(ser_string) > 5:
                # trigger arduino to open servo1
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high
                # fixing animal tag 
                ind = ser_string.find("x")
                animaltag = ser_string[len(ser_string)-19:len(ser_string)-5]
                print(ser_string)
                # getting date and time of trial start
                date_and_time = time.strftime("%Y%m%d-%H%M%S")
                date_var = time.strftime("%Y%m%d")
                time_var = time.strftime("%H%M%S")

                #Append data
                append_event("+", "START")
                
                # switch mode and clean up RFID
                MODE = 2
                serRFID.close()
            print("\nMODE 2\n")

        if MODE == 2 and GPIO.input(ard_pi_1): 
            print("\nMODE 2\n")
            GPIO.output(Pi_RFID,False)
            ys = [] #store weights here
            ser.open()
            ser.flush()
            for x in range(8): # chuck two lines 
                line=ser.readline()
                print(line)
            for x in range(20): # bag 20lines*400ms=8s of data 
                line=ser.readline()
                print(line)
                line_as_list = line.split(b',')
                relProb = line_as_list[1]
                relProb_as_list = relProb.split(b'\n')
                relProb_float = float(relProb_as_list[0])
                relProb_float = relProb_float*1000
                ys.append(relProb_float)
            ser.close()
            weight_data = sum(ys)/len(ys) # average
            weight_data = str(round(weight_data,2)) # two digits of precision
            del ser_string
            del ser2
            del ys 
            GPIO.output(Pi_RFID,True) # start signal = high

            #appending data to database
            append_weight(weight_data)

            # change mode and clean up
            MODE = 3
            flag=1
            print("\nMODE 3\n")
                        
        if MODE == 3 and GPIO.input(ard_pi_2) and flag==1: #log a trial start
            print("\ntrial start\n")
            
            if food_flag==1:
                print("appending food pod data")
                cycles_str = str(counter/cycle)
                append_event(cycles_str, "Food")
            
            if run_flag==1:
                print("appending running wheel data")
                cycles_str = str(counter/cycle)
                append_event(cycles_str, "Run")
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            flag=0
            run_flag=0
            food_flag=0
            counter=0
            
        if MODE == 3 and GPIO.input(ard_pi_3): #animal going back home
            print("\nMODE 4\n")
            GPIO.output(Pi_RFID,False)
            #stop camera capture/opto
            GPIO.output(Pi_capture_1,False)
            time.sleep(10)#so the RFID doesn't read while animal is going back to cage
            MODE = 1

            #appending data to database
            append_event("-", "END")
            
            #BREAK OUT OF THE INFINITE LOOP SO THAT THE DATA CAN BE EXPORTED
            break
                    
        if MODE == 3 and GPIO.input(ard_pi_4) and flag==0: #log a maze event food
            print("\nfood pod\n")
            
            flag=1
            food_flag=1
            limit=cycle
            
        if food_flag==1: #record running wheel
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle

        if MODE == 3 and GPIO.input(ard_pi_5) and flag==0: #log a maze event running wheel
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