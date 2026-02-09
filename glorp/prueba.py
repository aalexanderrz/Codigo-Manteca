import numpy as np
import matplotlib.pyplot as plt

x1 = np.linspace(-3,3,100)
x2 = np.linspace(-3,3,100)
x1_v, x2_v = np.meshgrid(x1,x2)
P = np.exp(-x1_v**2-x2_v**2)*(x2_v-x1_v)**2
plt.contour(x1_v, x2_v, P, levels = 30)
plt.colorbar()
plt.show()
