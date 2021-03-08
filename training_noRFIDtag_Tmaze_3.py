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
import statistics as stats
import time
from datetime import datetime

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

def append_weight(weight_data_mean=[], weight_data_median=[], weight_data_mode=[]):
    weight_list.update({'Weight_Mean': [weight_data_mean]})
    weight_list.update({'Weight_Median': [weight_data_median]})
    weight_list.update({'Weight_Mode': [weight_data_mode]})
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
    "Weight_Mean": [],
    "Weight_Median": [],
    "Weight_Mode": [],
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
animaltag = input("Which animal is in? ")

while True:
    GPIO.output(Pi_RFID,True) # start signal = high
    MODE = 2   
    while True:
        if MODE == 2 and GPIO.input(ard_pi_1): 
            print("\nMODE 2\n")
            append_event("+", "Session start")
            GPIO.output(Pi_RFID,False)
            ys = [] #store weights here
            ser.open()
            ser.flush()
            for x in range(8): # chuck two lines 
                line=ser.readline()
                print(line)
            for x in range(100): # 100 lines*120ms per line=12s of data 
                line=ser.readline()
                print(line)
                line_as_list = line.split(b',')
                relProb = line_as_list[0]
                relProb_as_list = relProb.split(b'\n')
                relProb_float = float(relProb_as_list[0])
                relProb_float = relProb_float*1000
                
                # if relProb_float > 30:
                # GPIO.output(Pi_RFID,False)
                # MODE = 3
#                 if MODE == 3 and GPIO.input(ard_pi_3): #animal going back home
#                     print("\nMODE 4\n")
#                     append_event("*", "BB5")
#                     GPIO.output(Pi_RFID,False)
#                     #stop camera capture/opto
#                     GPIO.output(Pi_capture_1,False)
#                     time.sleep(15)#so the RFID doesn't read while animal is going back to cage
#                     print("second sleep")
#                     MODE = 1
# 
#                     #appending data to database
#                     append_event("x", "TWO ANIMALS")
#                     
#                     #BREAK OUT OF THE INFINITE LOOP 
#                     break
                ys.append(relProb_float)
            ser.close()
            
            for i in range(len(ys)):
                ys[i] = round(ys[i],3)
            
            #weight_data_mean = round(weight_data_mean,2) # two digits of precision
            #weight_data_median = round(weight_data_median,2) # two digits of precision
            #weight_data_mode = round(weight_data_mode,2) # two digits of precision
            
            GPIO.output(Pi_RFID,True) # start signal = high
            
            # mean 
            weight_data_mean = stats.mean(ys)
            # median
            weight_data_median = stats.median(ys)
            # mode
            try:
                weight_data_mode = stats.mode(ys)
            except:
                weight_data_mode = "NO MODE"

            #appending data to database
            append_weight(weight_data_mean, weight_data_median, weight_data_mode)

            # change mode and clean up
            del ys 
            MODE = 3
            flag=1
            print("\nMODE 3\n")
                        
        if MODE == 3 and GPIO.input(ard_pi_2) and flag==1: #log a trial start
            #append run wheel here
            print("\ntrial start\n")
            
            # only append BB2 for the first time the animal enters the maze
            if event_list["Type"] == ["Session start"]:
                append_event("*", "BB2")
            
            if food_flag==1:
                print("appending food pod data")
                cycles_str = round(counter/cycle,4)
                append_event(cycles_str, "Food_log")
            
            if run_flag==1:
                print("appending running wheel data")
                cycles_str = round(counter/cycle,4)
                append_event(cycles_str, "Run_log")
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            flag=0
            run_flag=0
            food_flag=0
            counter=0
            
        if MODE == 3 and GPIO.input(ard_pi_3): #animal going back home
            print("\nMODE 4\n")
            append_event("*", "BB5")
            GPIO.output(Pi_RFID,False)
            #stop camera capture/opto
            GPIO.output(Pi_capture_1,False)
            time.sleep(15)#so the RFID doesn't read while animal is going back to cage
            print("second sleep")
            MODE = 1

            #appending data to database
            append_event("-", "END")
            
            #BREAK OUT OF THE INFINITE LOOP 
            break
                    
        if MODE == 3 and GPIO.input(ard_pi_4) and flag==0: #log food pod
            append_event("*", "BB4")
            print("\nfood pod\n")
            
            flag=1
            food_flag=1
            limit=cycle
        if food_flag ==1:
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle

        if MODE == 3 and GPIO.input(ard_pi_5) and flag==0: #log a maze event running wheel
            print("\nrunning wheel\n")
            append_event("*", "BB3")
            
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

