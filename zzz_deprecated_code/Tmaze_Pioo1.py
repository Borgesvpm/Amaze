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
import pandas as pd
from time import sleep

db_list = {
    "Animal": [],
    "Triggered by": [],
    "Occurance" : [],
    "Time": [],
    "Date": []
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
GPIO.setup(Pi_RFID,GPIO.OUT)
GPIO.setup(Pi_scale,GPIO.OUT)
GPIO.setup(Pi_capture_1,GPIO.OUT)
GPIO.output(Pi_RFID,False)
GPIO.output(Pi_scale,False)
GPIO.output(Pi_capture_1,False)

#state variables
beam_break_flag = 0
task_complete = 0
MODE = 1
flag=1
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=0

try: 
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

                #appending data to database
                db_list["Animal"].append(animaltag)
                db_list["Triggered by"].append("RFID")
                db_list["Task occurance"].append("Session started")
                db_list["Time"].append(time.strftime("%H%M%S"))
                db_list["Date"].append(time.strftime("%Y%m%d"))

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
            weight_data = str(sum(ys)/len(ys)) # average 
            completeName = os.path.join("/home/pi/Desktop/RFID_scale/",  date_and_time[0:8] + animaltag + "_data.txt")
            file1 = open(completeName, "a")# append data
            L = animaltag + "\t" + date_and_time + "\t" + weight_data + "\n"   
            file1.writelines(L)
            file1.close() 
            del ser_string
            del ser2
            del ys 
            GPIO.output(Pi_RFID,True) # start signal = high

            #appending data to database
            db_list["Animal"].append(animaltag)
            db_list["Triggered by"].append("Beam Break 1")
            db_list["Task occurance"].append("Weight = " + weight_data)
            db_list["Time"].append(time.strftime("%H%M%S"))
            db_list["Date"].append(time.strftime("%Y%m%d"))

            # change mode and clean up
            MODE = 3
            flag=1
            print("\nMODE 3\n")
                        
        if MODE == 3 and GPIO.input(ard_pi_2) and flag==1: #log a trial start
            print("\ntrial start\n")
            #make a note
            t2 = time.strftime("%Y%m%d-%H%M%S")      
            file1 = open(completeName, "a")# append data
            L = "\ntrial start\t" + t2 + "\n"
            file1.writelines(L)
            file1.close()
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            flag=0
            run_flag=0
            file1 = open(completeName, "a")# append running data
            cycles_str = str(counter/cycle)
            L = "\nrun cycles\t" + cycles_str + "\n"
            file1.writelines(L)
            file1.close()
            counter=0
            print(L)

            #appending data to database
            db_list["Animal"].append(animaltag)
            db_list["Triggered by"].append("Beam Break 2")
            db_list["Task occurance"].append("Run cycles = " + cycles_str)
            db_list["Time"].append(time.strftime("%H%M%S"))
            db_list["Date"].append(time.strftime("%Y%m%d"))
            
        if MODE == 3 and GPIO.input(ard_pi_3): #animal going back home
            print("\nMODE 4\n")
            GPIO.output(Pi_RFID,False)
            #make a note
            t3 = time.strftime("%Y%m%d-%H%M%S")      
            file1 = open(completeName, "a")# append data
            L = "\nreturn to cage\t" + t3 + "\n"
            file1.writelines(L)
            file1.close()
            #stop camera capture/opto
            GPIO.output(Pi_capture_1,False)
            time.sleep(10)#so the RFID doesn't read while animal is going back to cage
            MODE = 1

            #appending data to database
            db_list["Animal"].append(animaltag)
            db_list["Triggered by"].append("Beam Break 3")
            db_list["Task occurance"].append("Return to homecage")
            db_list["Time"].append(time.strftime("%H%M%S"))
            db_list["Date"].append(time.strftime("%Y%m%d"))
            
        

        #appending data to database
        db_list["Animal"].append(animaltag)
        db_list["Triggered by"].append("Beam Break 5")
        db_list["Task occurance"].append("Running wheel")
        db_list["Time"].append(time.strftime("%H%M%S"))
        db_list["Date"].append(time.strftime("%Y%m%d"))
                    
        if MODE == 3 and GPIO.input(ard_pi_4) and flag==0: #log a maze event food
            print("\nfood pod\n")
            #make a note
            t4 = time.strftime("%Y%m%d-%H%M%S")      
            file1 = open(completeName, "a")# append data
            L = "\nfood pod\t" + t4 + "\n"
            file1.writelines(L)
            file1.close()
            flag=1

            #appending data to database
            db_list["Animal"].append(animaltag)
            db_list["Triggered by"].append("Beam Break 4")
            db_list["Task occurance"].append("Food pod")
            db_list["Time"].append(time.strftime("%H%M%S"))
            db_list["Date"].append(time.strftime("%Y%m%d"))

        if MODE == 3 and GPIO.input(ard_pi_5) and flag==0: #log a maze event running wheel
            print("\nrunning wheel\n")
            #make a note
            t5 = time.strftime("%Y%m%d-%H%M%S")      
            file1 = open(completeName, "a")# append data
            L = "\nrunning wheel\t" + t5 + "\n"
            file1.writelines(L)
            file1.close()
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

        #appending data to database
        db_list["Animal"].append(animaltag)
        db_list["Triggered by"].append("Beam Break 5")
        db_list["Task occurance"].append("Running wheel")
        db_list["Time"].append(time.strftime("%H%M%S"))
        db_list["Date"].append(time.strftime("%Y%m%d"))
except:
    print("done except")

finally:
    print("done finally")
    GPIO.cleanup()
    df = pd.DataFrame(db_list)
    print(df)
    df.to_csv("Amaze_db.csv", encoding='utf-8-sig', index=False)