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
import sys
from datetime import datetime

# change directory to document data folder
os.chdir("/home/pi/Documents/data/")

def wheel_side(wheel):
    if wheel == "Left":
        FED = "Right"
    elif wheel == "Right":
        FED = "Left"
    return [wheel, FED]

wheel_position, FED_position = wheel_side("Right")

#Choose "Animal" or "Test" below
#trial_type = "Animal"
trial_type = "Test"

def RFID_readtag(RFIDnum):
    """
    This function reads the RFID tag, removes the junk incoming and returns the
    converted ID from hexadecimal to decimal.
    """
    if RFIDnum == "RFID1":
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
            serRFID.close()
            print("Something went wrong")
            clean_tag = 0
            return clean_tag
    elif RFIDnum == "RFID2":
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
            serRFID2.close()
            print("Something went wrong")
            clean_tag = 0
            return clean_tag

def RFID_datacheck(clean_tag):
    """
    This function converts the RFID tag to the actual animal's name in the AARC system.
    Some metadata (how the experimenters call the the animal) is printed.
    """
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
    
def RFID_sequential_check(animaltag, tt = trial_type):
    """
    For multiple animals with RFID tags, this function ensures that the animals do the
    task in the appropriate order, defined by the experimenter.
    
    This prevents the same animal from doing the task multiple times in a row.

    The sequence index is only updated at the end of a valid task (i.e. when the
    correct animal went in and out of the maze.
    """
    
    global sequence_index
    global sequence_list

    print(trial_type)

    if tt == "Test":
        sequence_list = ["Stick_X", "Stick_Y", "Stick_Z"]
    if tt == "Animal":  
        sequence_list = ["189005", "189004"] #out of study , "189003"
    
    if sequence_list[sequence_index] == animaltag:
        print(animaltag)
        print("Animal matches sequence")
        print("Entry allowed")
        entry_flag = True
        return entry_flag
    
    if sequence_list[sequence_index] != animaltag:
        print(animaltag)
        print("Animal does not match sequence")
        print("Next animal in line is " + sequence_list[sequence_index])
        print("Entry prevented")
        entry_flag = False
        return entry_flag
        
    
def check_bridge():
    """
    After every RFID trigger, check if the bridge is empty
    """
    print("Checking if bridge is empty")
    ser.close()
    ser.open()
    ser.flush()
    data_zeros=[]
    for x in range(20):
        line=ser.readline()
        
    for x in range(10):
        line=ser.readline()   
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
        
def exit_mode():
    """
    This is a function that opens door 1 and waits for the animal to leave before
    closing it behind it. It is used in four instances:
    1) When two animals come in to the bridge at the same time
    2) When the incorrect animal is on the bridge (one animal opened the door and
    another one jumped in)
    3) If an animal is detected during the bridge_check (sometimes the animals climb
    on the maze walls during the exit mode, which means they could be stuck in the bridge
    if the weight was not checked periodically)
    4) After the completion of a sucessful task
    """
    global Pi_RFID, Pi_exit, Pi_capture_1, Pi_end
    
    GPIO.output(Pi_RFID,True)
    GPIO.output(Pi_exit,True)
    GPIO.output(Pi_capture_1,False)
    ser.close()
    ser.open()
    ser.flush()
    data_zeros=[]
    for x in range(8): # chuck two lines 
        line=ser.readline()
    for x in range(100000):
        
        line=ser.readline()
        if x % 10 == 0:
            print(line)
        
        line_as_list = line.split(b',')
        relProb = line_as_list[0]
        relProb_as_list = relProb.split(b'\n')
        relProb_float = float(relProb_as_list[0])
        relProb_float = relProb_float*1000
        
        if relProb_float < 3:
            GPIO.output(Pi_end,True)
        else:
            GPIO.output(Pi_end,False)
                
        if not GPIO.input(ard_pi_3):
            return True
        
def acquire_weight(animaltag):
    """
    This function is used to acquire 100 datapoints of the animals weight and returns
    a few different parameters - mean, median, mode, max_mode(the latter does not
    work in python 3.7). In general, mode is always the most accurate metric.
    """
    print("Acquiring weight")
    flag_two_animals = False
    ys = [] #store weights here
    data_zeros = [] #store weights here
    ser.close()
    ser.open()
    ser.flush()
    for x in range(8): # chuck two lines 
        line=ser.readline()
        
    for x in range(100): # 100 lines*120ms per line=12s of data 
        line=ser.readline()
        if x % 10 == 0:
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
            
        #appending data to database
        save = SaveData()
        save.append_weight(weight_data_mean, weight_data_median,
        weight_data_mode, weight_data_max_mode,animaltag)
        return flag_two_animals


class SaveData:
    def append_weight(self,weight_data_mean, weight_data_median,
                      weight_data_mode, weight_data_max_mode,
                      animaltag):
        """
        Function used to save weight parameters to a .csv file
        """
        weight_list = {
        "Weight_Mean": [],
        "Weight_Median": [],
        "Weight_Mode": [],
        "Weight_Max_Mode": [],
        "Date_Time": []
        }
        weight_list.update({'Weight_Mean': [weight_data_mean]})
        weight_list.update({'Weight_Median': [weight_data_median]})
        weight_list.update({'Weight_Mode': [weight_data_mode]})
        weight_list.update({'Weight_Max_Mode': [weight_data_max_mode]})
        weight_list.update({'Date_Time': [datetime.now()]})
        
        df_w = pd.DataFrame(weight_list)
        print(df_w)

        if not os.path.isfile(animaltag + "_weight.csv"):
            df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
            print("File created sucessfully")
        else:
            df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
            print("File appended sucessfully")
        

    def append_event(self,rotation,food_time,event_type,animaltag,
                     wheel_position,FED_position):
        """
        Function used to save event parameters to a .csv file
        """
        global event_list

        event_list = {
            "Date_Time": [],
            "Rotation": [],
            "Pellet_Retrieval": [],
            "Type" : [],
            "Wheel_Position": [],
            "FED_Position": []    
        }
        
        event_list.update({'Rotation': [rotation]})
        event_list.update({'Pellet_Retrieval': [food_time]})
        event_list.update({'Type': [event_type]})
        event_list.update({'Date_Time': [datetime.now()]})
        event_list.update({'Wheel_Position': [wheel_position]})
        event_list.update({'FED_Position': [FED_position]})

        df_e = pd.DataFrame(event_list)
        print(df_e)

        if not os.path.isfile(animaltag + "_events.csv"):
            df_e.to_csv(animaltag + "_events.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(animaltag + "_events.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)

# set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) # Ignore warning for now

def emergency_button(channel):
    """
    To be used when there are one or multiple animals stuck inside the bridge. It opens
    door 1 and stops the program.
    """
    print("Emergency button was pushed!")
    GPIO.output(Pi_RFID,True)
    GPIO.output(Pi_exit,True)
    GPIO.cleanup() # Clean up
    sys.exit()
    
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(19,GPIO.RISING,callback=emergency_button) # Setup event on pin 10 rising edge

class Buzzer:
    def buzz(self, on):
        buzzer=22
        GPIO.setup(buzzer,GPIO.OUT)
        GPIO.output(buzzer, on)

#initialize serial port for RFID2
serRFID2 = serial.Serial()
serRFID2.port = '/dev/ttyUSB2' 
serRFID2.baudrate = 9600
serRFID2.timeout = 100000 #specify timeout when using readline()
serRFID2.open()
if serRFID2.is_open==True:
    print("\nRFID2 antenna ok. Configuration:\n")
    print(serRFID2, "\n") #print serial parameters
serRFID2.close()

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = '/dev/ttyUSB0' 
serRFID.baudrate = 9600
serRFID.timeout = 100000 #specify timeout when using readline()
serRFID.open()
if serRFID.is_open==True:
    print("\nRFID antenna ok. Configuration:\n")
    print(serRFID, "\n") #print serial parameters
serRFID.close()

#initialize serial port for OpenScale
ser = serial.Serial()
ser.port = '/dev/ttyUSB1' 
ser.baudrate = 19200
ser.timeout = 100000
#specify timeout when using readline()
ser.open()
ser.flush()
if ser.is_open==True:
    print("\nScale ok. Configuration:\n")
    print(ser, "\n") #print serial parameters
ser.close()



# set pin inputs from arduino
ard_pi_1 = 33 # 35
ard_pi_2 = 35 # 36
ard_pi_3 = 36 # 37

if wheel_position == "Left":
    ard_pi_4 = 37 # 38
    ard_pi_5 = 38 # 33

elif wheel_position == "Right":
    ard_pi_4 = 38 # 33
    ard_pi_5 = 37 # 38

GPIO.setup(ard_pi_1,GPIO.IN)
GPIO.setup(ard_pi_2,GPIO.IN)
GPIO.setup(ard_pi_3,GPIO.IN)
GPIO.setup(ard_pi_4,GPIO.IN)
GPIO.setup(ard_pi_5,GPIO.IN)

Food_pod_retrieval = 11 # BNC output on the Feather
GPIO.setup(Food_pod_retrieval, GPIO.IN)


#set pin inputs from running wheel rotary encoder
clk=12
GPIO.setup(clk,GPIO.IN)
clkLastState=GPIO.input(clk)

# set pin outputs to arduino
Pi_RFID = 15#16
Pi_exit = 16
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
choice_flag=False
counter=0
cycle=1200 #cycle on running wheel gives approx this many counts
run_flag=False
food_flag=False
flag_two_animals=False
flag_animals_left = False
task_complete_flag = False
entry_flag = False
sequence_index = 0
food_clk_end = 0
food_clk_start = 0

save = SaveData()
buzzer = Buzzer()

while True:
    MODE = check_bridge() 
    while True:
        if MODE == 1:
            print("\nMODE 1\n")
            clean_tag = RFID_readtag("RFID1")
            animaltag = RFID_datacheck(clean_tag)
            entry_flag = RFID_sequential_check(animaltag)

            if not entry_flag:
                # MODE is already equal to 1
                break

            if entry_flag:
                # trigger arduino to open servo1
                print('Sending Pi_RFID pulse to Arduino')
                GPIO.output(Pi_RFID,True) # start signal = high

                MODE = 2

            
        if MODE == 2 and GPIO.input(ard_pi_1): 
            print("\nMODE 2\n")
            
            GPIO.output(Pi_RFID,False)
            
            #check if animal matches before start to weigh it
            print("Waiting for animal to be confirmed")
            while True:
                clean_tag = RFID_readtag("RFID2")
                animaltag = RFID_datacheck(clean_tag)
                same_animal = RFID_sequential_check(animaltag)

                if not same_animal:
                    MODE = 0
                    break
                        
                elif same_animal:
                    #Append data
                    save.append_event("+", "", "START", animaltag, wheel_position, FED_position)
                    MODE = 3
                    choice_flag=False
                    break
    
        if MODE == 3:
            # Starting weighing the animal once its identity is confirmed
            two_animals = acquire_weight(animaltag)
            if two_animals:
                MODE = 0
            
            if not two_animals:
                GPIO.output(Pi_RFID,True) # open door 2
                MODE = 4
            
                
                
        if MODE == 4 and GPIO.input(ard_pi_2) and not choice_flag: 
            #append run wheel here
            print("\ntrial start\n")

            # only append BB2 for the first time the animal entersf the maze
            if event_list["Type"] == ["START"]:
                save.append_event("*", "", "BB2", animaltag, wheel_position, FED_position)
            
            if food_flag:
                print("appending food pod data")
                cycles_str = round(counter/cycle,4)
                save.append_event(cycles_str, "", "Food_log", animaltag, wheel_position, FED_position)
            
            if run_flag:
                print("appending running wheel data")
                cycles_str = round(counter/cycle,4)
                save.append_event(cycles_str, "", "Run_log", animaltag, wheel_position, FED_position)
            #start camera capture/opto
            GPIO.output(Pi_capture_1,True)
            choice_flag=True
            run_flag=False
            food_flag=False
            counter=0
            food_clk_end=0
            
            
        if MODE == 4 and GPIO.input(ard_pi_3): #animal going back home
            save.append_event("-", "", "END", animaltag, wheel_position, FED_position)
            task_complete_flag = True
            MODE = 0
            
        if MODE ==0:
            buzzer.buzz(True)
            animal_left = exit_mode()
            if animal_left:
                GPIO.output(Pi_RFID,False)
                GPIO.output(Pi_exit,False)
                GPIO.output(Pi_end,False)
                GPIO.output(Pi_capture_1,False)
                buzzer.buzz(False)
                
                if task_complete_flag:
                    sequence_index = (sequence_index + 1) % len(sequence_list) # works for two animals
                    task_complete_flag = False
                break
                        
        if MODE == 4 and GPIO.input(ard_pi_4) and choice_flag: #log food pod
            save.append_event("*", "", "BB4", animaltag, wheel_position, FED_position)
            food_clk_start = time.process_time()
            # arduino sends pulse to FED
            print("\nfood pod\n")
            
            choice_flag=False
            food_flag=True
            limit=cycle

        if MODE == 4 and GPIO.input(ard_pi_5) and choice_flag: #log a maze event running wheel
            print("\nrunning wheel\n")
            save.append_event("*", "", "BB3", animaltag, wheel_position, FED_position)
            
            choice_flag=False
            run_flag=True
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
            print("Appending food retrieval") 
            save.append_event("", food_clk_end, "Food_retrieval", animaltag, wheel_position, FED_position)
            time.sleep(1) #Necessary because otherwise appends 10 data points ms apart

    # reset variables
    entry_flag = False
    flag_animals_left = False
    flag_two_animals=False
    
    print("finally")
