import pandas as pd
from matplotlib import pyplot as plt

class Behavioral_plot:
    def __init__(self):
        pass

    def RotationPlot(self):
        import pandas as pd
        from datetime import datetime, timedelta
        from matplotlib import pyplot as plt
        from matplotlib import dates as mpl_dates
        import matplotlib.lines as mlines

        df = pd.read_csv("189003_events.csv")

        df['Date_Time']  = pd.to_datetime(df['Date_Time'])
        df['Date_column'] = pd.to_datetime(df['Date_Time']).dt.date
        df['Time_column'] = pd.to_datetime(df['Date_Time']).dt.time

        #df=df.replace(to_replace="+",value=0)
        #df=df.replace(to_replace="-",value=0)
        unique_dates = pd.unique(df["Date_column"])
        print(unique_dates)
        #print(pd.unique(df["Date_column"])[0])
        #unique_indices = pd.Index.unique(df["Date_column"])

        #for key, value in df.items() :
        #    print (key)

        plt.style.use("seaborn")

        for i in unique_dates:
            plt.figure()
            # get index of datapoints per day
            for counter, val in enumerate(df["Date_column"]):
                if df["Rotation"][counter] == "+":
                    df["Rotation"][counter] = 0
                    plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker=".", c="k")
                elif df["Rotation"][counter] == "-":
                    df["Rotation"][counter] = 0
                    plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="_", c="r")
                elif df["Type"][counter] == "Run":
                    plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="D", c="g")
                elif df["Type"][counter] == "Food":
                    plt.scatter(df["Date_Time"][counter],float(df["Rotation"][counter]),marker="*", c="b")
        
        plt.gcf().autofmt_xdate()

        black_dot = mlines.Line2D([], [], color='black', marker=".", label="Session start")
        red_line = mlines.Line2D([], [], color='red', marker="_", label="Session end")
        green_diamond = mlines.Line2D([], [], color='green', marker="D", label="Running wheel")
        blue_star = mlines.Line2D([], [], color='blue', marker="*", label="Food pod")

        date_format = mpl_dates.DateFormatter("%b %d, %H:%M:%S")
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', 
        ncol=2, mode="expand", borderaxespad=0.)
        plt.title("Behavioral output")
        plt.xlabel("Date and Time")
        plt.ylabel("Rotation")
        plt.legend(handles=[black_dot, red_line, green_diamond, blue_star])
        plt.tight_layout()

        plt.show()
        # plot all data point in the day
            
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
        
        df = pd.read_csv("189003_events.csv")
        animalsh = str(189003)

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

                if event_type[i+1] == "Session start":
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

        plt.title(animalsh)
        plt.xlabel("Date and Time")
        plt.ylabel("Time between events (s)")

        plt.tight_layout()

        plt.show()

    def WeightPlot(self):
        import pandas as pd
        import datetime
        from datetime import datetime as dt, timedelta
        from matplotlib import pyplot as plt
        from matplotlib import dates as mpl_dates
        import matplotlib.lines as mlines
        
        df = pd.read_csv("189003_weight.csv")
        animalsh = str(189003)

        date_time  = pd.to_datetime(df['Date_Time'])
        weight_mode = df["Weight_Mode"]
        weight_median = df["Weight_Median"]
        plt.style.use("seaborn")

        for i, val in enumerate(date_time):
            if weight_mode[i] == "NO MODE":
                plt.scatter(date_time[i], float(weight_median[i]),marker="o", c="b")
            elif float(weight_mode[i]) == 0.0:
                continue  
            else:
                plt.scatter(date_time[i], float(weight_mode[i]),marker="*", c="g")
                

        plt.gcf().autofmt_xdate()

        date_format = mpl_dates.DateFormatter("%b %d, %H:%M:%S")
        plt.gca().xaxis.set_major_formatter(date_format)

        plt.title(animalsh)
        plt.xlabel("Date and Time")
        plt.ylabel("Time between events (s)")

        plt.tight_layout()

        plt.show()


if __name__ == "__main__":
    c = Behavioral_plot()
    c.TimeDiff()