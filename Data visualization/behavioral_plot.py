import pandas as pd
import os
from matplotlib import pyplot as plt

os.chdir(r'\\scistor.vu.nl\shares\BETA-NeuroSciences-Hypo\lof\Documents\data')

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


if __name__ == "__main__":
    c = Behavioral_plot([189003, 189004, 189005])
    c.RotationPlot()
    c.TimeDiff_SS()
    c.WeightPlot()