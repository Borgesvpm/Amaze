from RFID import RFID
import serial
import RPi.GPIO as GPIO
class OpenScale:
    ys = [] #store weight list
    weight_list = {
        "Weight_Mean": [],
        "Weight_Median": [],
        "Weight_Mode": [],
        "Weight_Max_Mode": [],
        "Date_Time": []
        }
    def __init__(self, port = '/dev/ttyUSB0', weight_data = [], animaltag = "test"):
        self.port = port
        self.weight_data = weight_data
        self.animaltag = animaltag
        

    def acquire_weight(self, num_readings):
        serOS = serial.Serial()
        serOS.port = self.port
        serOS.open()
        serOS.flush()

        for x in range(8): # chuck eight lines of garbage 
            line=serOS.readline()
            print(line)

        for x in range(num_readings): # read num_readings lines * speed of acquisition
            line=serOS.readline()
            print(line)
            # fixing string and converts to float
            line_as_list = line.split(b',')
            relProb = line_as_list[0]
            relProb_as_list = relProb.split(b'\n') # byte to new lines (string format)
            relProb_float = float(relProb_as_list[0])
            relProb_grams = relProb_float*1000 # kg to g
            if relProb_grams > 34:
                serOS.close()
                print("TWO ANIMALS ON BRIDGE")
                flag_two_animals = True
            else:
                relProb_grams = round(relProb_grams,3)
                OpenScale.ys.append(relProb_grams)
        serOS.close()

    def wait_animals_left(self):
        Pi_end = 13
        ard_pi_3 = 37
        data_zeros = [] #store weights here
        serOS = serial.Serial()
        serOS.port = self.port
        serOS.open()
        serOS.flush()

        for x in range(8): # chuck two lines 
            line=serOS.readline()
            print(line)
        for x in range(100000):
            
            line=serOS.readline()
            print(line)
            
            line_as_list = line.split(b',')
            relProb = line_as_list[0]
            relProb_as_list = relProb.split(b'\n')
            relProb_float = float(relProb_as_list[0])
            relProb_float = relProb_float*1000
            
            if relProb_float < 1:
                GPIO.output(Pi_end,True)
                print("load cell clear sent to ARD")
            else:
                GPIO.output(Pi_end,False)
                    
            if not GPIO.input(ard_pi_3):    
                serOS.close()
                print("ARD said to stop. Load cell and BB5 clear")
                
                flag_animals_left = True
                return flag_animals_left
                


    def weight_stats(self):
        import statistics as stats

        # mean 
        weight_data_mean = stats.mean(OpenScale.ys)
        # median
        weight_data_median = stats.median(OpenScale.ys)
        # mode
        try:
            weight_data_mode = stats.mode(OpenScale.ys)
        except:
            weight_data_mode = "NO MODE"
            
        # mode max
        try:
            weight_data_max_mode = stats.multimode(OpenScale.ys)
            weight_data_max_mode = weight_data_max_mode[-1] # largest of modes
        except:
            weight_data_max_mode = "NO MAX_MODE"

        #appending data to database
        OpenScale.append_weight(weight_data_mean, weight_data_median, weight_data_mode, weight_data_max_mode)

        #clean up variables
        OpenScale.ys = []

    def append_weight(self, weight_data_mean=[], weight_data_median=[], 
                        weight_data_mode=[], weight_data_max_mode=[]):
        """
        It uses the weight_list variable dictionary list to create a structured .csv file.
        Whenever the function is called, datetime.now() is ran to update the current date and time.
        If the RFID tag has been seen before, the data is appended to the existing file.
        If the RFID tag has never been seen before, a new file is created.
        CSV output looks like:
        Weight Date_Time
        3.4    2021-02-20 14:03:00.228348
        4.3    2021-02-20 15:02:51.248299
        2.5    2021-02-21 12:25:40.663348
        """

        from datetime import datetime
        import pandas as pd
        import os

        tr = RFID()
        animaltag = tr.datacheck()

        OpenScale.weight_list.update({'Weight_Mean': [weight_data_mean]})
        OpenScale.weight_list.update({'Weight_Median': [weight_data_median]})
        OpenScale.weight_list.update({'Weight_Mode': [weight_data_mode]})
        OpenScale.weight_list.update({'Weight_Max_Mode': [weight_data_max_mode]})
        OpenScale.weight_list.update({'Date_Time': [datetime.now()]})
        
        df_w = pd.DataFrame(OpenScale.weight_list)
        print(df_w)

        if not os.path.isfile(animaltag + "_weight.csv"):
            df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
        else:
            df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)
        
    def test_data(self, num_rows):
        import random
        from time import sleep
        self.animaltag = input("What is the name of the test file? ")
        
        for i in range(num_rows):
            self.weight_data = random.uniform(15, 20)
            
            print(self.weight_data)
            OpenScale.append_weight(self,self.weight_data)
            sleep(random.randint(1,3))
            
if __name__ == "__main__":
    sc = OpenScale()
    sc.acquire_weight(10)
    