import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

theta = np.linspace(-np.pi, np.pi, 10000)
phi = np.linspace(-2*np.pi, 2 * np.pi, 10000)
tv, pv = np.meshgrid(theta,phi)
phase = pv

fig, ax = plt.subplots()

def animate(frame):
    phase = frame + pv 
    ax.clear()
    ax.contourf(pv,tv,phase)
    
animation = FuncAnimation(fig, animate,frames=100,interval=33)
plt.show()
