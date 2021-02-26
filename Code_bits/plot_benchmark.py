from matplotlib import pyplot as plt
from datetime import datetime

ys = []

# start while loop
start = datetime.now() #start of loop
# your code here
end = datetime.now() #end of loop

datapoint = (end-start) 
datapoint_float = datapoint.total_seconds()
ys.append(datapoint_float)

# Example measuring performance of the entire code

ys = []

start = datetime.now() #start of loop
for i in range(1000):
    print(i)
end = datetime.now() #end of loop

datapoint = (end-start) 
datapoint_float = datapoint.total_seconds()
ys.append(datapoint_float)

# Example measuring performance of every loop

ys = []


for i in range(1000):
    start = datetime.now() #start of loop
    print(i)
    end = datetime.now() #end of loop

    datapoint = (end-start) 
    datapoint_float = datapoint.total_seconds()
    ys.append(datapoint_float)

# plotting performance of every loop

x = range(len(ys))
plt.scatter(x,ys,color="#6c3376", linewidth=0.1)

plt.show()
plt.savefig("benchmark.png")