from RFID import RFID
class Maze:
    event_list = {
        "Rotation": [],
        "Type" : [],
        "Date_Time": []
        }
    def __init__(self):
        pass

    def append_event(self, cycles_str=[],event_type=[]):
        from datetime import datetime
        import pandas as pd
        import os
        tr = RFID()
        animaltag = tr.datacheck()
        """
        It uses the event_list dictionary list to create a structured .csv file.
        Whenever the function is called, datetime.now() is ran to update the current date and time.
        If the RFID tag has been seen before, the data is appended to the existing file.
        If the RFID tag has never been seen before, a new file is created.
        CSV output looks like:
        Rotation  Type  Date_Time
        +         START 2021-02-20 14:03:00.228348
        5.225     Food  2021-02-20 14:04:02.724573
        2.652     Run   2021-02-20 14:05:52.846536
        -         END   2021-02-21 14:07:23.543257
        """
        Maze.event_list.update({'Rotation': [cycles_str]})
        Maze.event_list.update({'Type': [event_type]})
        Maze.event_list.update({'Date_Time': [datetime.now()]})
        
        df_e = pd.DataFrame(Maze.event_list)
        print(df_e)

        if not os.path.isfile(animaltag + "_events.csv"):
            df_e.to_csv(animaltag + "_events.csv", encoding="utf-8-sig", index=False)
        else:
            df_e.to_csv(animaltag + "_events.csv", mode="a+", header=False, encoding="utf-8-sig", index=False)