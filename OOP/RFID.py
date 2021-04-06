import serial
class RFID:
    animaltag = []
    clean_tag = 0
    def __init__(self, port='/dev/ttyUSB2'):
    #def __init__(self, port='/dev/ttyUSB1'):
        self.port = port
        try:
            self.RFID = serial.Serial(port, baudrate=9600)
            self.RFID.flushInput()

        except IOError as e:
            print("Could not open serial port ", port, " please make sure the tag reader is properly connected.")
            print("Specific error is:")
            print(e)
            exit()
        
    def raw_tag(self):
        serRFID = serial.Serial()
        serRFID.port = self.port
        serRFID.open()
        serRFID.flush() # waits for transmission of outgoing serial data to be completed
        ser2 = serRFID.readline() # RFID string
        print(ser2)

    def read_tag(self):
        global tag
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

        RFID.clean_tag = str(int(tag, 16)) # transform from hexadecimal to a number                
        return RFID.clean_tag

    def datacheck(self):
        if RFID.clean_tag == "137575399499":
            RFID.animaltag = "189005"
            print("Animal in: LONG_WHITE. ID: 189005")
            return RFID.animaltag
    
        elif RFID.clean_tag == "137575399602":
            RFID.animaltag = "189004"
            print("Animal in: SHORT_WHITE. ID: 189004")
            return RFID.animaltag
    
        elif RFID.clean_tag == "137575399650":
            RFID.animaltag = "189003"
            print("Animal in: NO_WHITE. ID: 189003")
            return RFID.animaltag
        
        elif RFID.clean_tag == "137575399500":
            RFID.animaltag = "Test"
            print("This is a test RFID.")
            return RFID.animaltag
        
        elif RFID.clean_tag == "137575399614":
            RFID.animaltag = "Test2"
            print("This is a test RFID.")
            return RFID.animaltag
        
        elif RFID.clean_tag == "137575399426":
            RFID.animaltag = "Test3"
            print("This is a test RFID.")
            return RFID.animaltag
        
        else:
            pass

    def sequential_check_old(self):
        global previous_animal
        global current_animal
        global prevent_entry_flag
        global animaltag
        
        if previous_animal != animaltag:
            previous_animal = animaltag
            print("Different animal from previous session")
            return
        
        if previous_animal == animaltag:
            print("This is the same animal from previous session")
            print("Entry prevented")
            prevent_entry_flag = True

    def sequential_check(self):
        global prevent_entry_flag
        global allow_entry_flag
        
        global sequence_index
        sequence_index = 0
        
        #sequence_list = ["137575399499", "137575399602", "137575399650"] #short_white included
        #sequence_list = ["137575399499", "137575399650"] #short_white excluded
        sequence_list = ["137575399426", "137575399426", "137575399426"] #test tag3
        
        if sequence_list[sequence_index] == self.clean_tag:
            print("Animal matches sequence")
            print("Entry allowed")
            prevent_entry_flag = False
            return prevent_entry_flag
        
        if sequence_list[sequence_index] != self.clean_tag:
            print("Animal does not match sequence")
            print("Next animal in line is " + sequence_list[sequence_index])
            print("Entry prevented")
            prevent_entry_flag = True
            return prevent_entry_flag

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
            tr.datacheck()
            print(tr.animaltag)

    except KeyboardInterrupt:
        print("Hope the tags worked well! :)")