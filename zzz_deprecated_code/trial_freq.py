import pandas as pd
import matplotlib.axes as ax
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('0220082200D5DF_weight.csv')
print(df)

x = df['Date']
y = df['Time']

df.Date = pd.to_datetime(df.Date)
df.Time = pd.to_datetime(df.Time)


# plot
plt.scatter(x, y, s =100, c = 'red')


# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
