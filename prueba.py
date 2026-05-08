import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.constants as cte

n = 10
x = np.linspace(-0.999, 0.999, 1000)
x1 = np.linspace(-10, -0.1, 1000)
x2 = np.linspace(0.1, 10, 1000)
fun = sp.special.hermite(n)
y1 = 1 / (np.pi * np.sqrt(1 - x ** 2))
y2 = (1 / (2 ** n * sp.special.factorial(n))) * fun(x1) ** 2 * np.exp(- x1 ** 2 / (2))
y22 = (1 / (2 ** n * sp.special.factorial(n))) * fun(x2) ** 2 * np.exp(- x2 ** 2 / 2)
plt.plot(x, y1, label = r"\rho_{CL}(x)")
plt.plot(x, y2, label = r"\rho_{QM}(x)")
plt.plot(x, y22)
plt.legend()
plt.xlim(-1.01,1.01)
plt.show()