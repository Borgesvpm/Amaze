class BeamBreak:
    def __init__(self):
        pass
    def setup(self):
        pass

class RFID:
    def __init__(self):
        pass
    def rawstring(self):
        pass
    def test(self):
        pass


class OpenScale:
    from datetime import datetime
    import pandas as pd
    import os
    
    weight_list = {
    "Weight": [],
    "Date_Time": []
    }

    animaltag = "TEST1234"

    def __init__(self):
        pass
    def acquire_weight(self, num_readings):
        import serial
        import statistics as stats
        openscale = [] #store weight list
        serOS = serial.Serial()
        serOS.port = "COM15"
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
            openscale.append(relProb_grams) # appends to list
        serOS.close()

        try:
            weight_data = stats.mode(openscale) # average of data points
        except:
            weight_data = stats.median(openscale)
        weight_data = round(weight_data,2) # two digits of precision
        #appending data to database
        return weight_data
    def append_weight(self, weight_data):
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
        OpenScale.weight_list.update({'Weight': [weight_data]})
        weight_list.update({'Date_Time': [datetime.now()]})
        
        df_w = pd.DataFrame(weight_list)
        print(df_w)

        if not os.path.isfile(animaltag + "_weight.csv"):
            df_w.to_csv(animaltag + "_weight.csv", encoding="utf-8-sig", index=False)
        else:
            df_w.to_csv(animaltag + "_weight.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)


class Servo:
    pass


class RunningWheel:
    pass


class FoodPod:
    pass


weight = OpenScale()
x = weight.acquire_weight(10)
print(x)