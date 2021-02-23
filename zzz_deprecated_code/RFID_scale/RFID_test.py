import serial
ser = serial.Serial()
ser.port = '/dev/ttyUSB1' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()

while True:
    try:
        ser_bytes = ser.readline()
        print(str(ser_bytes))
    except:
        print("Keyboard Interrupt")
        break
    