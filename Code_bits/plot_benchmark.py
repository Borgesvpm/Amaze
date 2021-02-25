from matplotlib import pyplot as plt

x = [4,5,6]
y = range(len(x))
plt.scatter(x,y,color="#6c3376", linewidth=3)

plt.show()
plt.savefig("benchmark.png")