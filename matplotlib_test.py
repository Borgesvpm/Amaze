import matplotlib.pyplot as plt

x = [1,2,3]
y = [6,2,4]
x2 = [1,2,3]
y2 = [10,4,9]

plt.plot(x,y,label='first line')
plt.plot(x2,y2,label='second line')
plt.xlabel('Time (s)')
plt.ylabel('Weight reading')
plt.title('Real-Time\nWeight Data')
plt.legend()
plt.show()