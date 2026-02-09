import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10,10,100)
y = x**3+5*x**2-x-5
plt.plot(x,y)
plt.show()