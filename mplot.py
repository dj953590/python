import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,5,11)
y = x**2

plt.plot(x,y)
plt.show()

plt.subplot(1,2,1)
plt.plot(x,y,'r')
plt.subplot(1,2,2)

plt.plot(y,x,'b')
plt.show()

#using the oop for doing the plotting

x = np.linspace(0,10,100)
y = np.sqrt(x)

fig = plt.figure()
# first 2 number is the south west point, 3 - width, 4 - height
axes = fig.add_axes([0.1,0.1,0.8,0.8])
axes.plot(x,y)
fig

fig.savefig('myplot.pdf')


