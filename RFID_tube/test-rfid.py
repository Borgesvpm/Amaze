import serial
import time

#initialize serial port for RFID
serRFID = serial.Serial()
serRFID.port = 'COM14' #Arduino serial port
serRFID.baudrate = 9600
serRFID.open()

def read_RFID():
    ser_string = serRFID.readline()
    ser_string = str(ser_string)

    if len(ser_string) > 5: 
        # fixing animal tag 
        ind = ser_string.find("x")
        global animaltag
        animaltag = ser_string[len(ser_string)-19:len(ser_string)-5]
        print(animaltag)
        del ser_string

RFID_list = []

while True:
    read_RFID()
    if not animaltag in RFID_list:
        # read RFID and put it in a list
        RFID_list.append(animaltag)
        print(RFID_list)

        if len(RFID_list) >= 2: # check if list has 2 elements
            print(f"two animals")
            t1 = time.time()
            while True:
                read_RFID()
                print(f"animal {animaltag} is the winner!")
            break






# if so, trigger countdown
# read RFIDs, the last one to pass is the winner