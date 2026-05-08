import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

#Constantes
G = 1
m1 = 1
m2 = 2 * m1
m3 = 3 * m1

#funciones
def r(x1, x2):
    return np.sqrt( (x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2 + (x1[2] - x2[2]) ** 2)

def f(x1, x2, x3, v1, v2, v3):
    ddr1ddt = -G * m1 * m2 * x1 / r(x1, x2) ** 3
    dxdt1 = v1
   