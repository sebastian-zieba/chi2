import numpy as np
import matplotlib.pyplot as plt

#y = kx + d

k = 1.234
d = -43.21

x = np.linspace(-100,100,10000)
y = k * x + d + np.random.randn(len(x))
y_err = [1]*len(x)
plt.scatter(x,y, s=1)
plt.plot(x, k*x+d, c='r')
plt.plot(x, k*x+d+1, c='r', ls='--')
plt.plot(x, k*x+d-1, c='r', ls='--')
plt.show()

np.savetxt('datalist.txt', list(zip(x,y,y_err)))
