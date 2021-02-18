import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('0220082200D5DF_weight.csv')
print(df)

df.Date_and_Time = pd.to_datetime(df.Date_and_Time)

x = df['Date_and_Time']
y = df['Weight']

df.info()

#grp_date = df.groupby("Date")
#weights_by_date = pd.DataFrame(grp_date.size(), columns=['num_sessions'])
#print(weights_by_date)

# plot
plt.plot(x,y,linestyle="",marker="o")
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
