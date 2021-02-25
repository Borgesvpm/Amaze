from datetime import datetime
import os
import sys
import time

def file_creation():
    f=open(animal_num + ".txt", "a+")
    short_hand = input("What is the animal's shorthand (e.g. LONG_WHITE, LEFT_CUT)? ")
    rfid = input("What is the animal's RFID tag? (it should contain 14 characters) ")

    f.write("File created on " + str(datetime.now() ))
    f.write("\n")
    f.write("Animal number: " + animal_num)
    f.write("\n")
    f.write("Short hand: " + short_hand)
    f.write("\n")
    f.write("RFID tag: " + rfid)
    f.write("\n")
    f.write("\n")

    print("File created sucessfully. Restart program to append data. ")
    time.sleep(2)

def user_comment():
    f=open(animal_num + ".txt", "a+")

    while True:
        user_input = input("Write down any comments related to the session or type 'q' to quit. \n")
        if user_input.lower() == "q":
            print("Goodbye!")
            time.sleep(2)
            break
        else:
            f.write(str(datetime.now() ))
            f.write("\n")
            f.write(user_input)
            f.write("\n")
            f.write("\n")


flag = 0
animal_num = input("What is the number of the animal? ")

if not os.path.isfile(animal_num + ".txt"):
    print("This animal currently does not have a file.")
    resp_user = input("Would you like to create one? Press 'y' for yes or anything else for no. \n")
    if resp_user.lower() == "y":
        file_creation()
    else:
        print("No problem, goodbye! ")
else:
    user_comment()
