# -*- coding: utf-8 -*-
"""
WORKING SCRIPT
Created on Wed Oct 28 10:46:18 2020
@author: Vinicius 
"""

import serial
import RPi.GPIO as GPIO
import os
import pandas as pd
import statistics as stats
import time
from datetime import datetime

from Maze import Maze
from RFID import RFID
from OpenScale import OpenScale

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# set pin inputs from arduino
ard_pi_1 = 35
ard_pi_2 = 36
ard_pi_3 = 37
ard_pi_4 = 38
ard_pi_5 = 33
clk=12

GPIO.setup(ard_pi_1,GPIO.IN)
GPIO.setup(ard_pi_2,GPIO.IN)
GPIO.setup(ard_pi_3,GPIO.IN)
GPIO.setup(ard_pi_4,GPIO.IN)
GPIO.setup(ard_pi_5,GPIO.IN)

GPIO.setup(clk,GPIO.IN)
clkLastState=GPIO.input(clk)

# set pin outputs to arduino
Pi_RFID = 16
Pi_exit = 15
Pi_end = 13
Pi_capture_1=40
PiArd_reset=18

GPIO.setup(Pi_RFID,GPIO.OUT)
GPIO.setup(Pi_exit,GPIO.OUT)
GPIO.setup(Pi_end,GPIO.OUT)
GPIO.setup(Pi_capture_1,GPIO.OUT)
GPIO.setup(PiArd_reset,GPIO.OUT)

GPIO.output(Pi_RFID,False)
GPIO.output(Pi_exit,False)
GPIO.output(Pi_end,False)
GPIO.output(Pi_capture_1,False)

GPIO.output(PiArd_reset,False)
time.sleep(0.3)
GPIO.output(PiArd_reset,True)

#state variables
beam_break_flag = 0
task_complete = 0
choice_flag=False
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=0
food_flag=0
flag_two_animals=False
previous_animal = []
current_animal = []
prevent_entry_flag = False
flag_animals_left = False
allow_entry_flag = False
sequence_index = 0

# instatiating classes

rfid = RFID()
maze = Maze()
scale = OpenScale()

mode = 1

while True:
    while True:
        if mode == 1: 
            print("\nMODE 1\n")
            rfid.read_tag()
            global animaltag
            animaltag = rfid.datacheck()
            prevent_entry_flag = rfid.sequential_check()
            
            print(prevent_entry_flag)
            print(allow_entry_flag)

            if prevent_entry_flag:
                break
                
            if not prevent_entry_flag:
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True)
                
                print(animaltag)

                #Append data
                maze.append_event("+", "START")
                
                # switch mode and clean up RFID
                mode = 2
        if mode == 2 and GPIO.input(ard_pi_1): 
            print("\nMODE 2\n")
            maze.append_event("+", "Session start")
            scale.acquire_weight(100)

            if flag_two_animals == True:
                GPIO.output(Pi_RFID,False) # open door 1
                scale.wait_animals_left()
            
            if flag_animals_left:
                GPIO.output(Pi_end,True) # close door 1
                time.sleep(10)
                mode = 1
                flag_animals_left = False
                break

            if not flag_two_animals:
                scale.weight_stats()
                GPIO.output(Pi_RFID,True) # start signal = high
                mode = 3
                choice_flag = True
            
            print("\nMODE 3\n")
                        
        if mode == 3 and GPIO.input(ard_pi_2) and not choice_flag: #log a trial start
            #append run wheel here
            print("\ntrial start\n")
            
            # only append BB2 for the first time the animal enters the maze
            if maze.event_list["Type"] == ["Session start"]:
                maze.append_event("*", "BB2")
            
            if food_flag==1:
                print("appending food pod data")
                cycles_str = round(counter/cycle,4)
                maze.append_event(cycles_str, "Food_log")
            
            if run_flag==1:
                print("appending running wheel data")
                cycles_str = round(counter/cycle,4)
                maze.append_event(cycles_str, "Run_log")
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)

            choice_flag=True
            run_flag=False
            food_flag=False
            counter=0
            
        if mode == 3 and GPIO.input(ard_pi_3): #animal going back home
            flag_animals_left = scale.wait_animals_left()
            if flag_animals_left:
                GPIO.output(Pi_RFID,True)
                GPIO.output(Pi_exit,True)
                GPIO.output(Pi_capture_1,False)
                #appending data to database
                mode = 4
                flag_animals_left = False

        if mode == 4 and GPIO.input(ard_pi_1):
            maze.append_event("-", "END")
            mode = 1
            GPIO.output(Pi_RFID,False)
            GPIO.output(Pi_exit,False)
            GPIO.output(Pi_end,False)
            GPIO.output(Pi_capture_1,False)
            #sequence_index = (sequence_index + 1) % 2 # works for two animals
            sequence_index = (sequence_index + 1) % 3 # works for three animals
            break
                    
        if mode == 3 and GPIO.input(ard_pi_4) and choice_flag: #log food pod
            maze.append_event("*", "BB4")
            print("\nfood pod\n")
            
            choice_flag=False
            food_flag=True
            limit=cycle

        if mode == 3 and GPIO.input(ard_pi_3) and choice_flag: #log a maze event running wheel
            print("\nrunning wheel\n")
            maze.append_event("*", "BB3")
            
            choice_flag=False
            run_flag=True
            limit=cycle

        if run_flag or food_flag: #record running wheel
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle                 

    allow_entry_flag = False
    prevent_entry_flag = False
    print("finally")