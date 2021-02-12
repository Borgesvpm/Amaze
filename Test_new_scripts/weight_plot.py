import pandas as pd
from datetime import datetime   
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('0220082200D5DF_weight.csv')
print (df)

x = df['Time']
y = df['Weight']

# plot
plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
