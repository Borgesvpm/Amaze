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
import statistics as stats
import time
from datetime import datetime

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

def RFID_readtag(RFIDnum):
    if RFIDnum == 1:
        try:
            serRFID.open()
            serRFID.flush()

            junk     = serRFID.read(1)
            tag      = serRFID.read(10)
            checksum = serRFID.read(2)
            junk2    = serRFID.read(3)
            
            clean_tag = str(int(tag, 16)) # transform from hexadecimal to a number
            serRFID.close()
            return clean_tag
        except:
            print("Something went wrong")
            clean_tag = 0
            return clean_tag
    elif RFIDnum == 2:
        try:
            serRFID2.open()
            serRFID2.flush()

            junk     = serRFID2.read(1)
            tag      = serRFID2.read(10)
            checksum = serRFID2.read(2)
            junk2    = serRFID2.read(3)
            
            clean_tag = str(int(tag, 16)) # transform from hexadecimal to a number
            serRFID2.close()
            return clean_tag
        except:
            print("Something went wrong")
            clean_tag = 0
            return clean_tag

def RFID_datacheck(clean_tag):
    if clean_tag == "137575399499":
        animaltag = "189005"
        print("Animal in: LONG_WHITE. ID: 189005")
        return animaltag
 
    elif clean_tag == "137575399602":
        animaltag = "189004"
        print("Animal in: SHORT_WHITE. ID: 189004")
        return animaltag
 
    elif clean_tag == "137575399650":
        animaltag = "189003"
        print("Animal in: NO_WHITE. ID: 189003")
        return animaltag
    
    elif clean_tag == "137575399500":
        animaltag = "Test"
        print("This is a test RFID.")
        return animaltag
    
    elif clean_tag == "137575399614":
        animaltag = "Test2"
        print("This is a test RFID.")
        return animaltag
    
    elif clean_tag == "137575399426":
        animaltag = "Test3"
        print("This is a test RFID.")
        return animaltag
    elif clean_tag == "137575399426":
        animaltag = "Stick_Y"
        print("This is a test RFID.")
        return animaltag
    
    elif clean_tag == "202100030":
        animaltag = "Stick_X"
        print("This is a test RFID.")
        return animaltag
    
    elif clean_tag == "2006010085":
        animaltag = "Stick_Z"
        print("This is a test RFID.")
        return animaltag
    else:
        pass

def RFID_sequential_check():
    global sequence_index
    global sequence_list
    
    #sequence_list = ["2006010085", "137575399426", "202100030"]
    #sequence_list_three = [137575399499, 137575399602, 137575399650]
    #sequence_list = ["137575399426", "137575399426", "137575399426"] #test tag3
    #sequence_list = ["137575399602", "137575399602", "137575399602"] #short_white only
    #sequence_list = ["137575399499", "137575399602", "137575399650"] #all3
    sequence_list = ["137575399499", "137575399602"] #no_white excluded
    #sequence_list = ["137575399499", "137575399650"] #short_white excluded
    
    if sequence_list[sequence_index] == clean_tag:
        print("Animal matches sequence")
        print("Entry allowed")
        entry_flag = True
        return entry_flag
    
    if sequence_list[sequence_index] != clean_tag:
        print("Animal does not match sequence")
        print("Next animal in line is " + sequence_list[sequence_index])
        print("Entry prevented")
        entry_flag = False
        return entry_flag
    
def check_bridge():
    ser.close()
    ser.open()
    ser.flush()
    data_zeros=[]
    for x in range(20):
        line=ser.readline()
        print(line)
        
    for x in range(10):
        line=ser.readline()
        print(line)    
        line_as_list = line.split(b',')
        relProb = line_as_list[0]
        relProb_as_list = relProb.split(b'\n')
        relProb_float = float(relProb_as_list[0])
        relProb_float = relProb_float*1000
        
        if relProb_float < 3:
            MODE = 1
            return MODE
        else:
            MODE = 0
            return MODE
        
def acquire_weight():
    flag_two_animals = False
    ys = [] #store weights here
    data_zeros = [] #store weights here
    ser.close()
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
        
        # If there are two animals on bridge:
        if relProb_float > 34:
            print("TWO ANIMALS ON BRIDGE")
            flag_two_animals = True
            return flag_two_animals

        else:
            ys.append(relProb_float)
    
    if not flag_two_animals:
        for i in range(len(ys)):
            ys[i] = round(ys[i],3)
        
        #weight_data_mean = round(weight_data_mean,2) # two digits of precision
        #weight_data_median = round(weight_data_median,2) # two digits of precision
        #weight_data_mode = round(weight_data_mode,2) # two digits of precision
        
        # mean 
        weight_data_mean = stats.mean(ys)
        # median
        weight_data_median = stats.median(ys)
        # mode
        try:
            weight_data_mode = stats.mode(ys)
        except:
            weight_data_mode = "NO MODE"
            
        # mode max TO DO
        try:
            weight_data_max_mode = stats.multimode(ys)
            weight_data_max_mode = weight_data_max_mode[-1] # largest of modes
        except:
            weight_data_max_mode = "NO MAX_MODE"
            
        return flag_two_animals

    
    #appending data to database
    append_weight(weight_data_mean, weight_data_median,
                  weight_data_mode, weight_data_max_mode,
                  animaltag)
    print("\nMODE 3\n")
    
    # change mode and clean up
    del ys
        
def append_weight(weight_data_mean, weight_data_median,
                  weight_data_mode, weight_data_max_mode,
                  animaltag):
    weight_list.update({'Weight_Mean': [weight_data_mean]})
    weight_list.update({'Weight_Median': [weight_data_median]})
    weight_list.update({'Weight_Mode': [weight_data_mode]})
    weight_list.update({'Weight_Max_Mode': [weight_data_max_mode]})
    weight_list.update({'Date_Time': [datetime.now()]})
    
    df_w = pd.DataFrame(weight_list)
    print(df_w)

    if not os.path.isfile(animaltag + "_weight.csv"):
        df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
    else:
        df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
    
def append_event(cycles_str,event_type,animaltag):
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
    "Weight_Max_Mode": [],
    "Date_Time": []
}

event_list = {
    "Rotation": [],
    "Type" : [],    
    "Date_Time": []
}

#initialize serial port for RFID2
serRFID2 = serial.Serial()
serRFID2.port = '/dev/ttyUSB2' #Arduino serial port
serRFID2.baudrate = 9600
serRFID2.timeout = 100000 #specify timeout when using readline()
serRFID2.open()
if serRFID2.is_open==True:
    print("\nRFID2 antenna ok. Configuration:\n")
    print(serRFID2, "\n") #print serial parameters
serRFID2.close()

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = '/dev/ttyUSB0' #Arduino serial port
serRFID.baudrate = 9600
serRFID.timeout = 100000 #specify timeout when using readline()
serRFID.open()
if serRFID.is_open==True:
    print("\nRFID antenna ok. Configuration:\n")
    print(serRFID, "\n") #print serial parameters
serRFID.close()

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB1' #Arduino serial port
ser.baudrate = 19200
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

Food_pod_retrieval = 11 # BNC output on the Feather
GPIO.setup(Food_pod_retrieval, GPIO.IN)

# Note: Pin 9 on the Feather is connected to X on the Arduino

#set pin inputs from running wheel rotary encoder
clk=12
# dt=11
GPIO.setup(clk,GPIO.IN)
# GPIO.setup(dt,GPIO.IN)
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
MODE=1
flag=1
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=0
food_flag=0
flag_two_animals=False
previous_animal = []
current_animal = []
flag_animals_left = False
task_complete_flag = False
entry_flag = False
sequence_index = 0
food_clk_end = 0
food_clk_start = 0

while True:
    MODE = check_bridge() # after every RFID trigger, check if the bridge is empty
    while True:
        if MODE == 1:
            print("\nMODE 1\n")
            clean_tag = RFID_readtag(1)
            animaltag = RFID_datacheck(clean_tag)
            entry_flag = RFID_sequential_check()

            if not entry_flag:
                break

            if entry_flag:
                # trigger arduino to open servo1
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high

                # switch mode
                MODE = 2

            
        if MODE == 2 and GPIO.input(ard_pi_1): 
            print("\nMODE 2\n")
            
            GPIO.output(Pi_RFID,False)
            
            #check if animal matches before appending the data
            while True:
                clean_tag = RFID_readtag(2)
                RFID_datacheck(clean_tag)
                entry_flag = RFID_sequential_check()

                if not entry_flag:
                    MODE = 0
                    break
                        
                elif entry_flag:
                    #Append data
                    append_event("+", "START", animaltag)
                    
                    flag=1
                    break
    
            # Starting weighing the animal once its identity is confirmed
            flag_two_animals = acquire_weight()
            if flag_two_animals:
                GPIO.output(Pi_exit,True)
                MODE = 0
            
            if not flag_two_animals:
                GPIO.output(Pi_RFID,True) # open door 2
                MODE = 3
                
                
        if MODE == 3 and GPIO.input(ard_pi_2) and flag==1: 
            #append run wheel here
            print("\ntrial start\n")

            # only append BB2 for the first time the animal enters the maze
            if event_list["Type"] == ["START"]:
                append_event("*", "BB2", animaltag)
            
            if food_flag==1:
                print("appending food pod data")
                cycles_str = round(counter/cycle,4)
                append_event(cycles_str, "Food_log", animaltag)
            
            if run_flag==1:
                print("appending running wheel data")
                cycles_str = round(counter/cycle,4)
                append_event(cycles_str, "Run_log", animaltag)
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            flag=0
            run_flag=0
            food_flag=0
            counter=0
            food_clk_end=0
            
            
        if MODE == 3 and GPIO.input(ard_pi_3): #animal going back home
            append_event("-", "END", animaltag)
            task_complete_flag = True
            MODE = 0
            
        if MODE ==0:
            GPIO.output(Pi_RFID,True)
            GPIO.output(Pi_exit,True)
            GPIO.output(Pi_capture_1,False)
            ser.close()
            ser.open()
            ser.flush()
            data_zeros=[]
            for x in range(8): # chuck two lines 
                line=ser.readline()
                print(line)
            for x in range(100000):
                
                line=ser.readline()
                print(line)
                
                line_as_list = line.split(b',')
                relProb = line_as_list[0]
                relProb_as_list = relProb.split(b'\n')
                relProb_float = float(relProb_as_list[0])
                relProb_float = relProb_float*1000
                
                if relProb_float < 3:
                    GPIO.output(Pi_end,True)
                    print("load cell clear sent to ARD")
                else:
                    GPIO.output(Pi_end,False)
                        
                if not GPIO.input(ard_pi_3):    
                    print("ARD said to stop. Load cell and BB5 clear")
                    
                    MODE = 4
                    break # from this for loop
                
        if MODE == 4:
            GPIO.output(Pi_RFID,False)
            GPIO.output(Pi_exit,False)
            GPIO.output(Pi_end,False)
            GPIO.output(Pi_capture_1,False)
            
            if task_complete_flag:
                sequence_index = (sequence_index + 1) % len(sequence_list) # works for two animals
            
            break
                        
        if MODE == 3 and GPIO.input(ard_pi_4) and flag==0: #log food pod
            append_event("*", "BB4", animaltag)
            food_clk_start = time.process_time()
            # arduino sends pulse to FED
            print("\nfood pod\n")
            
            flag=1
            food_flag=1
            limit=cycle

        if MODE == 3 and GPIO.input(ard_pi_5) and flag==0: #log a maze event running wheel
            print("\nrunning wheel\n")
            append_event("*", "BB3", animaltag)
            
            flag=1
            run_flag=1
            limit=cycle
            
        if food_flag or run_flag: #record running wheel
            clkState=GPIO.input(clk)
            if clkState != clkLastState:
                counter += 1  
                clkLastState = clkState
            if counter >= limit:
                print(counter)    
                limit=counter+cycle

        if GPIO.input(Food_pod_retrieval):
            food_clk_end = round(time.process_time() - food_clk_start, 4)
            append_event(food_clk_end, "Food_retrieval", animaltag)
            time.sleep(1) #Necessary because otherwise appends 10 data points ms apart

    # reset variables
    entry_flag = False
    flag_animals_left = False
    flag_two_animals=False
    
    print("finally")





