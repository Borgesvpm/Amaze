import pandas as pd
import os
from matplotlib import pyplot as plt

#os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')

class Behavioral_plot:

    def __init__(self, animalID):
        self.animalID = animalID

    def RotationPlot(self):
        import pandas as pd
        from datetime import datetime, timedelta
        from matplotlib import pyplot as plt
        from matplotlib import dates as mpl_dates
        import matplotlib.lines as mlines

        for animal in self.animalID:
            os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            df = pd.read_csv(str(animal) + "_events.csv")

            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            #df=df.replace(to_replace="+",value=0)
            #df=df.replace(to_replace="-",value=0)
            unique_dates = pd.unique(date)
            print(unique_dates)
            #print(pd.unique(df["Date_column"])[0])
            #unique_indices = pd.Index.unique(df["Date_column"])

            #for key, value in df.items() :
            #    print (key)

            plt.style.use("seaborn")

            for u_date in unique_dates:
                fig = plt.figure()
                # get index of datapoints per day
                for counter, val in enumerate(date):
                    date_string = u_date.strftime('%Y%m%d')
                    if date[counter] == u_date:
                        if df["Type"][counter] == "Session start" or df["Type"][counter] == "START":
                            plt.scatter(date_time[counter],0,marker="|", c="r", s= 10**7, alpha = 0.1)
                        elif df["Type"][counter] == "END":
                            plt.scatter(date_time[counter],0,marker="|", c="k", s= 10**7, alpha = 0.1)
                        elif df["Type"][counter] == "Run" or df["Type"][counter] == "Run_log":
                            plt.scatter(date_time[counter],float(df["Rotation"][counter]),marker="D", c="g", s=15)
                        elif df["Type"][counter] == "Food" or df["Type"][counter] == "Food_log":
                            plt.scatter(date_time[counter],float(df["Rotation"][counter]),marker="*", c="b")
            
                plt.gcf().autofmt_xdate()

                black_dot = mlines.Line2D([], [], color='red', marker="|", alpha = 0.1, label="Session start")
                red_line = mlines.Line2D([], [], color='black', marker="|", alpha = 0.1, label="Session end")
                green_diamond = mlines.Line2D([], [], color='green', marker="D", label="Running wheel")
                blue_star = mlines.Line2D([], [], color='blue', marker="*", label="Food pod")

                date_format = mpl_dates.DateFormatter("%b %d, %H:%M:%S")
                plt.gca().xaxis.set_major_formatter(date_format)
                plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', 
                ncol=2, mode="expand", borderaxespad=0.)
                plt.title("Behavioral output")
                plt.xlabel("Date and Time")
                plt.ylabel("Rotation (number of revolutions)")
                plt.legend(handles=[black_dot, red_line, green_diamond, blue_star])
                plt.tight_layout()
                
                # plot all data point in the day
                os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
                plt.savefig(str(animal) + '_rotation_plot_' + date_string + '.png', bbox_inches='tight')
                plt.close(fig)    # close the figure window
                """
                fig, ax = plt.subplots()
                data_tuples = zip(df["Date_Time"],df["Rotation"])
                plt.scatter(*zip(*data_tuples)) 

                plt.show()
                print(df)
                """
            #plt.scatter(df["Date_Time"],df["Rotation"],color="#6c3376", linewidth=0.1)

            #plt.savefig(user_input + ".png")

    def TimeDiff(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        from matplotlib import pyplot as plt
        from matplotlib import dates as mpl_dates
        import matplotlib.lines as mlines
        
        df = pd.read_csv(str(self.animalID) + "_events.csv")

        date_time  = pd.to_datetime(df['Date_Time'])
        date = pd.to_datetime(df['Date_Time']).dt.date
        time = pd.to_datetime(df['Date_Time']).dt.time
        unique_dates = pd.unique(date)
        event_type = df["Type"]

        plt.style.use("seaborn")

        dates = []
        y = []

        init_date = datetime.date(1, 1, 1)
        
    
        for _ in unique_dates:
            plt.figure()
            for i in range(len(date_time)-1):
                t1 = time[i]
                t2 = time[i+1]
                datetime2 = dt.combine(init_date, t2)
                datetime1 = dt.combine(init_date, t1)
                time_elapsed = datetime2 - datetime1
                seconds = time_elapsed.total_seconds()

                if event_type[i+1] == "Session start" or event_type[i+1] == "START":
                    plt.scatter(date_time[i],seconds,marker="o", c="k")
                elif event_type[i+1] == "BB2":
                    plt.scatter(date_time[i],seconds,marker=".", c="k")
                elif event_type[i+1] == "Run":
                    plt.scatter(date_time[i],seconds,marker="D", c="g")
                elif event_type[i+1] == "BB3":
                    plt.scatter(date_time[i],seconds,marker=".", c="g")
                elif event_type[i+1] == "Food":
                    plt.scatter(date_time[i],seconds,marker="*", c="b")
                elif event_type[i+1] == "BB4":
                    plt.scatter(date_time[i],seconds,marker=".", c="b")
                elif event_type[i+1] == "END":
                    plt.scatter(date_time[i],seconds,marker="_", c="r")
                elif event_type[i+1] == "BB5":
                    plt.scatter(date_time[i],seconds,marker=".", c="r")
        


        #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="_", c="r")

        #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="D", c="g")

        #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="*", c="b")
        
        #plt.plot_date(dates, y) #  linestyle='solid'

        black_dot = mlines.Line2D([], [], color='black', marker="o", label="Session start")
        red_line = mlines.Line2D([], [], color='red', marker="_", label="Session end")
        green_diamond = mlines.Line2D([], [], color='green', marker="D", label="Running wheel")
        blue_star = mlines.Line2D([], [], color='blue', marker="*", label="Food pod")
        circle = mlines.Line2D([], [], color='black', marker=".", label="Beam Break")
        plt.legend(handles=[black_dot, red_line, green_diamond, blue_star])

        plt.gcf().autofmt_xdate()

        date_format = mpl_dates.DateFormatter("%b %d, %H:%M:%S")
        plt.gca().xaxis.set_major_formatter(date_format)

        plt.title(str(self.animalID))
        plt.xlabel("Date and Time")
        plt.ylabel("Time between events (s)")

        plt.tight_layout()

        plt.show()

    def TimeDiff_SS(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os

        for animal in self.animalID:
            os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            df = pd.read_csv(str(animal) + "_events.csv")

            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            event_type = df["Type"]

            plt.style.use("seaborn")

            dates = []
            y = []

            init_date = datetime.date(1, 1, 1)

            print(unique_dates)
            

            for u_date in unique_dates:
                fig = plt.figure()
                for i in range(len(date_time)-1):
                    t1 = time[i]
                    t2 = time[i+1]
                    datetime2 = dt.combine(init_date, t2)
                    datetime1 = dt.combine(init_date, t1)
                    time_elapsed = datetime2 - datetime1
                    seconds = time_elapsed.total_seconds()
                    date_string = u_date.strftime('%Y%m%d')
                    
                    if date[i] == u_date:

                        if i == 1:
                            plt.scatter(date_time[i],0,marker="|", c="r", s= 10**7, alpha = 0.1)

                        if event_type[i+1] == "Session start" or event_type[i+1] == "START":
                            plt.scatter(date_time[i],0,marker="|", c="r", s= 10**7, alpha = 0.1)
                        elif event_type[i+1] == "BB2":
                            plt.scatter(date_time[i],seconds,marker=".", c="r")
                        elif event_type[i+1] == "Run" or event_type[i+1] == "Run_log":
                            plt.scatter(date_time[i],seconds,marker="*", c="g", s=40)
                        elif event_type[i+1] == "BB3":
                            plt.scatter(date_time[i],seconds,marker=".", c="g")
                        elif event_type[i+1] == "Food" or event_type[i+1] == "Food_log":
                            plt.scatter(date_time[i],seconds,marker="*", c="b", s=40)
                        elif event_type[i+1] == "BB4":
                            plt.scatter(date_time[i],seconds,marker=".", c="b")
                        elif event_type[i+1] == "END":
                            plt.scatter(date_time[i],0,marker="|", c="k", s= 10**7, alpha = 0.1)
                        elif event_type[i+1] == "BB5":
                            plt.scatter(date_time[i],seconds,marker=".", c="k")

                #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="_", c="r")

                #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="D", c="g")

                #plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="*", c="b")
                
                #plt.plot_date(dates, y) #  linestyle='solid'

                black_dot = mlines.Line2D([], [], color='red', marker="|", alpha = 0.1, label="Session start")
                red_line = mlines.Line2D([], [], color='black', marker="|", alpha = 0.1, label="Session end")
                green_diamond = mlines.Line2D([], [], color='green', marker="*", label="Running wheel start")
                green_circle = mlines.Line2D([], [], color='green', marker=".", label="Running wheel logged")
                blue_star = mlines.Line2D([], [], color='blue', marker="*", label="Food pod start")
                blue_circle = mlines.Line2D([], [], color='blue', marker=".", label="Food pod logged")
                plt.legend(handles=[black_dot, red_line, green_diamond, green_circle,
                                    blue_star, blue_circle])

                plt.gcf().autofmt_xdate()

                date_format = mdates.DateFormatter("%b %d, %H:%M:%S")
                plt.gca().xaxis.set_major_formatter(date_format)

                plt.title(str(animal))
                plt.xlabel("Date and Time")
                plt.ylabel("Time between events (s)")

                plt.tight_layout()

                os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
                plt.savefig(str(animal) + '_time_events_' + date_string + '.png', bbox_inches='tight')
                plt.close(fig)    # close the figure window


    def WeightPlot(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        from matplotlib import pyplot as plt
        from matplotlib import dates as mpl_dates
        import matplotlib.lines as mlines
        
        for animal in self.animalID:
            os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            df = pd.read_csv(str(animal) + "_weight.csv")

            date_time  = pd.to_datetime(df['Date_Time'])
            weight_mode = df["Weight_Mode"]
            weight_median = df["Weight_Median"]
            plt.style.use("seaborn")

            label_added1 = False
            label_added2 = False

            for i, val in enumerate(date_time):
                if weight_mode[i] == "NO MODE":
                    if float(weight_median[i]) > 17 and not label_added1: 
                        plt.scatter(date_time[i], float(weight_median[i]),marker="o", c="b",label="Median")
                        label_added1= True
                    else:
                        if float(weight_median[i]) > 17:
                            plt.scatter(date_time[i], float(weight_median[i]),marker="o", c="b")
                elif float(weight_mode[i]) < 17 or float(weight_mode[i])> 24:
                    continue  
                else:
                    if not label_added2:
                        plt.scatter(date_time[i], float(weight_mode[i]),marker="*", c="g", label="Mode")
                        label_added2 = True
                    else:
                        print(date_time[i])
                        print(weight_mode[i])
                        plt.scatter(date_time[i], float(weight_mode[i]),marker="*", c="g")
                    

            plt.gcf().autofmt_xdate()

            date_format = mpl_dates.DateFormatter("%b %d, %H:%M:%S")
            plt.gca().xaxis.set_major_formatter(date_format)

            plt.title(str(animal))
            plt.xlabel("Date and Time")
            plt.ylabel("Weight (g)")
            plt.legend()

            plt.tight_layout()

            os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + '_weight' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

    def DecisionSwitch(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os

        

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]
                    switch_index_list.append(i+2)
            return switch_index_list


        def DetectFirstBlockOfEachDay():
            first_block = []

            date = pd.to_datetime(df['Date_Time']).dt.date
            unique_dates = pd.unique(date)
            ind_dates = 0

            for i,val in enumerate(date):
                try:
                    if val == unique_dates[ind_dates]:
                        print(i +2)
                        first_block.append(i+2)
                        ind_dates += 1
                except:
                    return first_block

        def DetectSessionPreviousToSwitch():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 3
                        list_event_type_val.append(tmp_val)
                except:
                    pass
            print(list_event_type_val)
            return list_event_type_val

        def TimeElapsedBetweenEvents(index, number_of_elements):
            y = []

            init_date = datetime.date(1, 1, 1)

            for i in range(index,index+number_of_elements):
                t1 = time[i]
                t2 = time[i+1]
                datetime2 = dt.combine(init_date, t2)
                datetime1 = dt.combine(init_date, t1)
                time_elapsed = datetime2 - datetime1
                seconds = time_elapsed.total_seconds()
                y.append(seconds)
            return y

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            non_switch_index_list = DetectFirstBlockOfEachDay()
            switch_index_list = DetectSwitch()

            switch_list = []
            switch_event =[]
            for i, elem in enumerate(switch_index_list):
                list_time = TimeElapsedBetweenEvents(elem, 7)
                list_event = EventType(elem, 7)
                switch_list.append(list_time)
                switch_event.append(list_event)
                print(list_time)
                print(list_event)

            non_switch_list = []
            non_switch_event = []
            for i, elem in enumerate(non_switch_index_list):
                list_time_non = TimeElapsedBetweenEvents(elem, 7)
                list_event_non = EventType(elem, 7)
                non_switch_list.append(list_time_non)
                non_switch_event.append(list_event_non)

            for i, val in enumerate(switch_list):
                # Plotting
                fig = plt.figure(figsize = (10, 5))
                plt.style.use("seaborn")

                # creating the bar plot previous to switch
                plt.subplot(1, 2, 1)
                temp_x =  [i for i in range(len(list_event_non))]
                print(temp_x)
                plt.bar(temp_x, non_switch_list[i], color ='maroon',
                        width = 0.4)
                plt.xticks(temp_x, non_switch_event[i])

                plt.xlabel("Trial Type")
                plt.ylabel("Time (seconds)")
                plt.title("Decisions immediately before left-right switch " + str(animal) + "_" + str(i+1))


                # creating the bar plot switched
                plt.subplot(1, 2, 2)
                temp_x =  [i for i in range(len(list_event))]
                print(temp_x)
                plt.bar(temp_x, switch_list[i], color ='maroon',
                        width = 0.4)
                plt.xticks(temp_x, switch_event[i])

                plt.xlabel("Trial Type")
                plt.ylabel("Time (seconds)")
                plt.title("Decisions immediately after left-right switch " + str(animal) + "_" + str(i+1))

                plt.tight_layout()

                #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
                plt.savefig(str(animal) + '_decision_timing_' + str(i+1) + '.png', bbox_inches='tight')
                plt.close()    # close the figure window

    def ThreeDecisionBeforeAndAfter(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os
        import numpy as np

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]

                    switch_index_list.append(i+2)
                    print(i+2)

                    #if date[i-1] == date[i]: # does not append if switch happened between days
                    #    switch_index_list.append(i+2)
                    #    print(i+2)

            print(' ')
            return switch_index_list

        def DetectSessionPreviousToSwitch(detect_switch_list):
            i = 3
            previous_index_list = []

            for val in detect_switch_list:
                while True:
                    if event_type[val - i] == "START":
                        print(val-i+2)
                        print("hi")
                        previous_index_list.append(val-i+2)
                        break
                    i += 1
            
            return previous_index_list
            

        def DetectSessionPreviousToSwitch_old():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 2
                        list_event_type_val.append(tmp_val)
                        print(tmp_val)
                except:
                    pass
            return list_event_type_val

        def ThreeChoicesBeforeSwitch(list_before_switch):
            num_food = 0
            num_run = 0

            for elem in list_before_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 3:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 3:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def ThreeChoicesAfterSwitch(list_after_switch):
            num_food = 0
            num_run = 0

            for elem in list_after_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 3:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 3:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            
            switch_index_list = DetectSwitch()
            non_switch_index_list = DetectSessionPreviousToSwitch(switch_index_list)


            after_list = []
            for i, elem in enumerate(switch_index_list):
                list_event = EventType(elem, 10)
                print(list_event)
                after_list.append(ThreeChoicesAfterSwitch(list_event))

            print(after_list)
            after_mean = np.nanmean(after_list,axis = 0)
            print(after_mean)
            after_std = np.nanstd(after_list,axis = 0)
            print(after_std)

            before_list = []
            for i, elem in enumerate(non_switch_index_list):
                list_event_non = EventType(elem, 10)
                print(list_event_non)
                before_list.append(ThreeChoicesBeforeSwitch(list_event_non))
                
            print(before_list)
            before_mean = (np.nanmean(before_list, axis = 0))
            print(before_mean)
            before_std = (np.nanstd(before_list, axis = 0))
            print(before_std)

            x_values = ["Run", "Food"]

            # Plotting
            fig = plt.figure(figsize = (10, 5))
            plt.style.use("seaborn")

            # creating the bar plot previous to switch
            plt.subplot(1, 2, 1)
            plt.bar(x_values, before_mean, color = (0.2, 0.4, 0.6, 0.6),
                    width = 0.4)
            plt.errorbar(x_values, before_mean, before_std, fmt=' ', ecolor='black', capsize=5)

            plt.xlabel("Trial Type")
            plt.ylabel("Choice Type")
            plt.title("Decisions before left-right switch" + str(animal) + "_")


            # creating the bar plot switched
            plt.subplot(1, 2, 2)
            plt.bar(x_values, after_mean, color = (0.6, 0.4, 0.2, 0.6),
                    width = 0.4)
            plt.errorbar(x_values, after_mean, after_std, fmt=' ', ecolor='black', capsize=5)

            plt.xlabel("Trial Type")
            plt.ylabel("Choice Type")
            plt.title("Decisions after left-right switch" + str(animal) + "_")

            plt.tight_layout()

            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + '_three_decisions' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

    def FirstDecisionBeforeAndAfterLineAverage(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os
        import numpy as np

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]

                    switch_index_list.append(i+2)
                    print(i+2)

                    #if date[i-1] == date[i]: # does not append if switch happened between days
                    #    switch_index_list.append(i+2)
                    #    print(i+2)

            print(' ')
            return switch_index_list

        def DetectSessionPreviousToSwitch(detect_switch_list):
            i = 4
            previous_index_list = []

            for val in detect_switch_list:
                while True:
                    if event_type[val - i] == "START":
                        print(val-i+2)
                        previous_index_list.append(val-i+2)
                        i=4
                        break
                    i += 1
            
            return previous_index_list
            
            

        def DetectSessionPreviousToSwitch_old():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 2
                        list_event_type_val.append(tmp_val)
                        print(tmp_val)
                except:
                    pass
            return list_event_type_val

        def ThreeChoicesBeforeSwitch(list_before_switch):
            num_food = 0
            num_run = 0

            for elem in list_before_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def ThreeChoicesAfterSwitch(list_after_switch):
            num_food = 0
            num_run = 0

            for elem in list_after_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            
            switch_index_list = DetectSwitch()
            non_switch_index_list = DetectSessionPreviousToSwitch(switch_index_list)


            after_list = []
            for i, elem in enumerate(switch_index_list):
                list_event = EventType(elem, 10)
                print(list_event)
                after_list.append(ThreeChoicesAfterSwitch(list_event))

            print(after_list)
            after_mean = np.nanmean(after_list,axis = 0)
            print(after_mean)
            after_std = np.nanstd(after_list,axis = 0)
            print(after_std)

            before_list = []
            for i, elem in enumerate(non_switch_index_list):
                list_event_non = EventType(elem, 10)
                print(list_event_non)
                before_list.append(ThreeChoicesBeforeSwitch(list_event_non))
                
            print(before_list)
            before_mean = (np.nanmean(before_list, axis = 0))
            print(before_mean)
            before_std = (np.nanstd(before_list, axis = 0))
            print(before_std)

            x_values = [0, 1]

            # Plotting
            fig = plt.figure(figsize = (10, 5))
            plt.style.use("seaborn")

            # creating the bar plot previous to switch
            b = plt.plot([x - 0.02 for x in x_values], [before_mean[0], after_mean[0]], color = (0.2, 0.4, 0.6, 0.6), marker='.', markersize=20, label="Run")
            (_, caps, _) = plt.errorbar([x - 0.02 for x in x_values], before_mean, before_std, ecolor=(0.2, 0.4, 0.6, 0.6), capsize=10, elinewidth=3, markeredgewidth=3, fmt=' ')

            a = plt.plot([x + 0.02 for x in x_values], [before_mean[1], after_mean[1]], color = (0.6, 0.4, 0.2, 0.6), marker='.', markersize=20, label="Food")
            (_, caps, _) = plt.errorbar([x + 0.02 for x in x_values], after_mean, after_std, ecolor=(0.6, 0.4, 0.2, 0.6), capsize=10, elinewidth=3, markeredgewidth=3, fmt=' ')

            plt.ylabel("Choice Type (%)")
            plt.title("First decision before and after switching" + str(animal) + "_")
            plt.legend()

            plt.xticks([0, 1], ['Before', 'After'], rotation=20)  # Set text labels and properties.)

            plt.tight_layout()

            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + '_three_decisions_line' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

    def FirstDecisionBeforeAndAfterLineSingle(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os
        import numpy as np

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]

                    switch_index_list.append(i+2)
                    print(i+2)

                    #if date[i-1] == date[i]: # does not append if switch happened between days
                    #    switch_index_list.append(i+2)
                    #    print(i+2)

            print(' ')
            return switch_index_list

        def DetectSessionPreviousToSwitch(detect_switch_list):
            i = 4
            previous_index_list = []

            for val in detect_switch_list:
                while True:
                    if event_type[val - i] == "START":
                        print(val-i+2)
                        previous_index_list.append(val-i+2)
                        i=4
                        break
                    i += 1
            
            return previous_index_list
            
            

        def DetectSessionPreviousToSwitch_old():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 2
                        list_event_type_val.append(tmp_val)
                        print(tmp_val)
                except:
                    pass
            return list_event_type_val

        def ThreeChoicesBeforeSwitch(list_before_switch):
            num_food = 0
            num_run = 0

            for elem in list_before_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print(elem)
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def ThreeChoicesAfterSwitch(list_after_switch):
            num_food = 0
            num_run = 0

            for elem in list_after_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            
            switch_index_list = DetectSwitch()
            non_switch_index_list = DetectSessionPreviousToSwitch(switch_index_list)


            after_list = []
            for i, elem in enumerate(switch_index_list):
                list_event = EventType(elem, 10)
                print(list_event)
                after_list.append(ThreeChoicesAfterSwitch(list_event))

            before_list = []
            for i, elem in enumerate(non_switch_index_list):
                list_event_non = EventType(elem, 10)
                print(list_event_non)
                before_list.append(ThreeChoicesBeforeSwitch(list_event_non))

            x_values = [0, 1]

            
            print(before_list)
            print(after_list)

            y = []
            for i in range(len(before_list)):
                y.append([before_list[i][0], after_list[i][0]])

            print(y)

            # Plotting
            fig = plt.figure(figsize = (10, 5))
            plt.style.use("seaborn")

            # creating the bar plot previous to switch
            for i, val in enumerate(before_list):
                plt.plot([(x + 0.02 * i) for x in x_values], y[i], marker='.', markersize=20, label="Day "+ str(i+1))

            plt.ylabel("Choice Type (%)")
            plt.title("First decision before and after switching" + str(animal) + "_")
            plt.legend()

            plt.xticks([0, 1], ['Before', 'After'], rotation=20)  # Set text labels and properties.)
            plt.yticks([0, 1], ['Run', 'Food'], rotation=20)  # Set text labels and properties.)
            plt.tight_layout()

            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + 'day_decision' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

    def FirstDecisionBeforeAndAfterTime(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os
        import numpy as np

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]

                    switch_index_list.append(i+2)
                    print(i+2)

                    #if date[i-1] == date[i]: # does not append if switch happened between days
                    #    switch_index_list.append(i+2)
                    #    print(i+2)

            print(' ')
            return switch_index_list

        def DetectSessionPreviousToSwitch(detect_switch_list):
            i = 4
            previous_index_list = []

            for val in detect_switch_list:
                while True:
                    if event_type[val - i] == "START":
                        print(val-i+2)
                        previous_index_list.append(val-i+2)
                        i=4
                        break
                    i += 1
            
            return previous_index_list
            

        def DetectSessionPreviousToSwitch_old():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 2
                        list_event_type_val.append(tmp_val)
                        print(tmp_val)
                except:
                    pass
            return list_event_type_val

        def ThreeChoicesBeforeSwitch(list_before_switch):
            num_food = 0
            num_run = 0

            for elem in list_before_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def ThreeChoicesAfterSwitch(list_after_switch):
            num_food = 0
            num_run = 0

            for elem in list_after_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        def TimeElapsedBetweenEvents(index, number_of_elements):
            y = []

            init_date = datetime.date(1, 1, 1)

            for i in range(index,index+number_of_elements):
                t1 = time[i+3]
                print("hi")
                print(i+3)
                datetime1 = dt.combine(init_date, t1)
                j = 1
                while True:
                    if event_type[i+3+j] == "Food_log" or event_type[i+3+j] == "Run_log":
                        t2 = time[i+3+j]
                        datetime2 = dt.combine(init_date, t2)
                        print("hello")
                        print(i+3+j)
                        break
                    else:
                        j += 1
                
                time_elapsed = datetime2 - datetime1
                seconds = time_elapsed.total_seconds()
                    
                y.append(seconds)

            return y

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            
            switch_index_list = DetectSwitch()
            print(switch_index_list)
            non_switch_index_list = DetectSessionPreviousToSwitch(switch_index_list)
            print(non_switch_index_list)


            after_list = []
            after_time_list = []
            for i, elem in enumerate(switch_index_list):
                list_event = EventType(elem, 10)
                print(list_event)
                after_list.append(ThreeChoicesAfterSwitch(list_event))
                print(elem)
                after_time_list.append(TimeElapsedBetweenEvents(elem-1, 1))
                print(after_time_list)

            before_list = []
            before_time_list = []
            for i, elem in enumerate(non_switch_index_list):
                list_event_non = EventType(elem, 10)
                print(list_event_non)
                before_list.append(ThreeChoicesBeforeSwitch(list_event_non))
                print(elem)
                before_time_list.append(TimeElapsedBetweenEvents(elem-1, 1))
                print(before_time_list)

            x_values = [0, 1]

            
            print(before_list)
            print(after_list)

            y = []
            for i in range(len(before_list)):
                y.append([before_time_list[i][0], after_time_list[i][0]])

            print(y)
            df_y = pd.DataFrame(y)
            df_y.to_csv(str(animal) + "_tabular_data.csv", encoding="utf-8-sig", index=False)

            # Plotting
            fig = plt.figure(figsize = (10, 5))
            plt.style.use("seaborn")

            # creating the bar plot previous to switch
            for i, val in enumerate(before_list):
                plt.plot([(x + 0.02 * i) for x in x_values], y[i], marker='.', markersize=20, label="Day "+ str(i+1))

            plt.ylabel("Time between choice (food or run) and return to maze (BB2)")
            plt.title("First decision before and after switching" + str(animal) + "_")
            plt.legend()

            plt.xticks([0, 1], ['Before', 'After'], rotation=20)  # Set text labels and properties.)
            plt.tight_layout()

            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + 'day_decision_time' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

    def FirstDecisionBeforeAndAfterLineAverage2(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        import matplotlib
        from matplotlib import pyplot as plt        
        import numpy as np
        import matplotlib.patches as patches
        import matplotlib.dates as mdates
        import matplotlib.lines as mlines
        import matplotlib.axes as axes
        from matplotlib.patches import Rectangle
        import os
        import numpy as np
        import scipy.stats

        def DetectSwitch():
            switch_index_list = []
            previous_position = wheel_position[0]

            for i, val in enumerate(event_type):
                if wheel_position[i] != previous_position:
                    previous_position = wheel_position[i]

                    switch_index_list.append(i+2)
                    print(i+2)

                    #if date[i-1] == date[i]: # does not append if switch happened between days
                    #    switch_index_list.append(i+2)
                    #    print(i+2)

            print(' ')
            return switch_index_list

        def DetectSessionPreviousToSwitch(detect_switch_list):
            i = 4
            previous_index_list = []

            for val in detect_switch_list:
                while True:
                    if event_type[val - i] == "START":
                        print(val-i+2)
                        previous_index_list.append(val-i+2)
                        i=4
                        break
                    i += 1
            
            return previous_index_list
            

        def DetectSessionPreviousToSwitch_old():
            previous_position = wheel_position[0]
            list_event_type_val = []
            list_event_type_ind = [] 
            for i,val in enumerate(event_type):
                if val == "START" or val == "Session Start":
                    list_event_type_ind.append(i)
            for i, val in enumerate(list_event_type_ind):
                try:
                    if wheel_position[list_event_type_ind[i+1]] != previous_position:
                        previous_position = wheel_position[i]
                        tmp_val = list_event_type_ind[i] + 2
                        list_event_type_val.append(tmp_val)
                        print(tmp_val)
                except:
                    pass
            return list_event_type_val

        def ThreeChoicesBeforeSwitch(list_before_switch):
            num_food = 0
            num_run = 0

            for elem in list_before_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def ThreeChoicesAfterSwitch(list_after_switch):
            num_food = 0
            num_run = 0

            for elem in list_after_switch:
                #print(elem)
                if elem == "BB3":
                    num_run += 1
                if elem == "BB4":
                    num_food += 1
                if num_run + num_food >= 1:
                    break
                if elem == "END":
                    break

            if num_run + num_food >= 1:
                print("done\n")
                return [num_run, num_food]
            else:
                print("did not reach three choices")
                return [float('NaN'), float('NaN')]

        def EventType(index, number_of_elements):
            event_list = []
            event_type = df['Type']

            for i in range(index,index+number_of_elements):
                event_list.append(event_type[i])
                
            return event_list

        def TimeElapsedBetweenEvents(index, number_of_elements):
            y = []

            init_date = datetime.date(1, 1, 1)

            for i in range(index,index+number_of_elements):
                t1 = time[i+3]
                print("hi")
                print(i+3)
                datetime1 = dt.combine(init_date, t1)
                j = 1
                while True:
                    if event_type[i+3+j] == "Food_log" or event_type[i+3+j] == "Run_log":
                        t2 = time[i+3+j]
                        datetime2 = dt.combine(init_date, t2)
                        print("hello")
                        print(i+3+j)
                        break
                    else:
                        j += 1
                
                time_elapsed = datetime2 - datetime1
                seconds = time_elapsed.total_seconds()
                
                if seconds < 1000:
                    y.append(seconds)
                else:
                    y.append(float('NaN'))

            return y

        for animal in self.animalID:
            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')
            os.chdir(r'C:\Users\Administrator2\Documents\GitHub\Amaze\Data visualization')
            df = pd.read_csv(str(animal) + "_events.csv")
            date_time  = pd.to_datetime(df['Date_Time'])
            date = pd.to_datetime(df['Date_Time']).dt.date
            time = pd.to_datetime(df['Date_Time']).dt.time
            unique_dates = pd.unique(date)
            wheel_position = df["Wheel_Position"]
            event_type = df['Type']

            
            switch_index_list = DetectSwitch()
            print(switch_index_list)
            non_switch_index_list = DetectSessionPreviousToSwitch(switch_index_list)
            print(non_switch_index_list)


            after_list = []
            after_time_list = []
            for i, elem in enumerate(switch_index_list):
                list_event = EventType(elem, 10)
                print(list_event)
                after_list.append(ThreeChoicesAfterSwitch(list_event))
                print(elem)
                after_time_list.append(TimeElapsedBetweenEvents(elem-1, 1))
                print(after_time_list)

            before_list = []
            before_time_list = []
            for i, elem in enumerate(non_switch_index_list):
                list_event_non = EventType(elem, 10)
                print(list_event_non)
                before_list.append(ThreeChoicesBeforeSwitch(list_event_non))
                print(elem)
                before_time_list.append(TimeElapsedBetweenEvents(elem-1, 1))
                print(before_time_list)

            


            y = []
            for i in range(len(before_list)):
                y.append([before_time_list[i][0], after_time_list[i][0]])

            

            df_y = pd.DataFrame(y)
            df_y.to_csv(str(animal) + "_tabular_data.csv", encoding="utf-8-sig", index=False)

            # Statistics
            print(after_time_list)
            after_mean = np.nanmean(after_time_list,axis = 0)
            print(after_mean)
            after_std = np.nanstd(after_time_list,axis = 0)
            print(after_std)

            print(before_time_list)
            before_mean = np.nanmean(before_time_list,axis = 0)
            print(before_mean)
            before_std = np.nanstd(before_time_list,axis = 0)
            print(before_std)

            # T-test
            t_stat, p_value = scipy.stats.ttest_ind(before_time_list, after_time_list, nan_policy ="omit")
            print(t_stat)
            print(p_value)

            # Plotting
            x_values = [0, 1]
            fig = plt.figure(figsize = (10, 5))
            plt.style.use("seaborn")

            # creating the bar plot previous to switch
            b = plt.plot(x_values[0], before_mean, color = (0.2, 0.4, 0.6, 0.6), marker='.', markersize=20, label="Run")
            (_, caps, _) = plt.errorbar(x_values[0], before_mean, before_std, ecolor=(0.2, 0.4, 0.6, 0.6), capsize=10, elinewidth=3, markeredgewidth=3, fmt=' ')

            a = plt.plot(x_values[1], after_mean, color = (0.6, 0.4, 0.2, 0.6), marker='.', markersize=20, label="Food")
            (_, caps, _) = plt.errorbar(x_values[1], after_mean, after_std, ecolor=(0.6, 0.4, 0.2, 0.6), capsize=10, elinewidth=3, markeredgewidth=3, fmt=' ')

            plt.ylabel("Time between choice (food or run) and return (BB2)")
            plt.title("First decision before and after switching" + str(animal) + "_")
            plt.legend()

            plt.xticks([0, 1], ['Before', 'After'], rotation=20)  # Set text labels and properties.)
            
            #annotation
            plt.text(0.2, 0.2, 'T-test: ' + str(t_stat))
            plt.text(0.8, 0.8, 'P-value: ' + str(p_value))

            plt.tight_layout()

            #os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data\Figures')
            plt.savefig(str(animal) + '_time_stats' + '.png', bbox_inches='tight')
            plt.close()    # close the figure window

if __name__ == "__main__":
    c = Behavioral_plot([189003, 189004, 189005])
    #c.FirstDecisionBeforeAndAfterTime()
    #c.FirstDecisionBeforeAndAfterLineSingle()
    c.FirstDecisionBeforeAndAfterLineAverage2()
    #c.DecisionSwitch()
    #c.RotationPlot()
    #c.TimeDiff_SS()
    #c.WeightPlot()