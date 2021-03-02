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

from Maze import Maze
from RFID import RFID
from OpenScale import OpenScale

M = Maze()
R = RFID()
S = OpenScale()

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# set pin inputs from arduino
ard_pi_1 = 35
ard_pi_2 = 36
ard_pi_3 = 33
ard_pi_4 = 38
ard_pi_5 = 37

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

choice_flag= False
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=False
food_flag=False
animaltag = input("Which animal is in? ")

M_RFID = True

while True:
    while True:
        if M_RFID: 
            M.log("\nMODE 1\n")

            ser_string = R.read_tag()
            M.log(ser_string)
                
            if len(ser_string) > 5:
                M.log('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high

                #Append data
                M.append_event("+", "START")
                
                # switch mode and clean up RFID
                M_RFID = False
                M_scale = True
            M.log("\nMODE 2\n")

        if M_scale and GPIO.input(ard_pi_1): 
            M.log("\nMODE 2\n")
            M.append_event("+", "Session start")
            S.acquire_weight()
            
            GPIO.output(Pi_RFID,True) # start signal = high
            
            M_scale = False
            M_choice = True
            M.log("\nMODE 3\n")
                        
        if M_choice and GPIO.input(ard_pi_2) and not choice_flag: #log a trial start
            #append run wheel here
            M.log("\ntrial start\n")
            M.append_event("*", "BB2")
            
            if food_flag:
                M.log("appending food pod data")
                cycles_str = str(counter/cycle)
                append_event(cycles_str, "Food")
            
            if run_flag:
                M.log("appending running wheel data")
                cycles_str = str(counter/cycle)
                append_event(cycles_str, "Run")
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)

            M_choice = False
            choice_flag=True
            run_flag=False
            food_flag=False
            counter=0
            
        if M_choice and GPIO.input(ard_pi_5): #animal going back home
            M.log("\nMODE 4\n")
            M.append_event("*", "BB5")
            GPIO.output(Pi_RFID,False)
            #stop camera capture/opto
            GPIO.output(Pi_capture_1,False)
            time.sleep(15)#so the RFID doesn't read while animal is going back to cage
            MODE = 1

            #appending data to database
            M.append_event("-", "END")
            
            #BREAK OUT OF THE INFINITE LOOP 
            break
                    
        if M_choice and GPIO.input(ard_pi_4) and choice_flag: #log food pod
            M.append_event("*", "BB4")
            M.log("\nfood pod\n")
            
            choice_flag=False
            food_flag=True
            limit=cycle

        if M_choice and GPIO.input(ard_pi_3) and choice_flag: #log a maze event running wheel
            M.log("\nrunning wheel\n")
            M.append_event("*", "BB3")
            
            choice_flag=False
            run_flag=True
            limit=cycle

        if run_flag or food_flag: #record running wheel
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                M.log(counter)    
                limit=counter+cycle                 

    M.log("finally")