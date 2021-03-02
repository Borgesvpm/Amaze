import serial
class RFID:
    def __init__(self, port="COM14"):
        self.port = port
        try:
            self.RFID = serial.Serial(port, baudrate=9600)
            self.RFID.flushInput()

        except IOError as e:
            print("Could not open serial port ", port, " please make sure the tag reader is properly connected.")
            print("Specific error is:")
            print(e)
            exit()

    def clear_buffer(self):
        """
        Clears the serial buffer for the serialport used by the tagReader
        """
        self.RFID.flushInput()
        
    def raw_tag(self):
        import serial
        serRFID = serial.Serial()
        serRFID.port = self.port
        serRFID.open()
        serRFID.flush() # waits for transmission of outgoing serial data to be completed
        ser2 = serRFID.readline() # RFID string
        print(ser2)

    def read_tag(self):
        """
        Reads a hexidecimal RFID tag from the serial port using a blocking read and returns the decimal equivalent

        RFID Tag is 16 characters: STX(02h) DATA (10 ASCII) CHECK SUM (2 ASCII) CR LF ETX(03h)
        1 char of junk, 10 of hexadecimal data, 2 of hexadecimal check sum, 3 of junk

        :returns decimal value of RFID tag
        :raises IOError: if serialPort not read
        raises ValueError: if checksum or conversion from hex to decimal fails

        """
        junk     = self.RFID.read(1)
        tag      = self.RFID.read(10)
        checksum = self.RFID.read(2)
        junk2    = self.RFID.read(3)

        return str(int(tag, 16)) # transform from hexadecimal to a number
        """
        if animaltag == "0220082200B2B8":
            print("Animal 119010")
        elif animaltag == "02200822005359":
            print("Animal 119011")
        elif animaltag == "02200822004248":
            print("Animal 119012")
        """

    def test(self):
        pass

if __name__ == "__main__":
    tr = RFID()

    try:
        print("Press CTRL+C to terminate program. Scan a tag to see its ID.")
        print("Waiting for tag...")
        while True:
            tag = tr.read_tag()
            print("Tag was: ", str(tag))

    except KeyboardInterrupt:
        print("Hope the tags worked well! :)")