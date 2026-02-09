import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

a = 1
r = a/2
ac, aq = 0, 0
t = np.linspace(0,2*np.pi,100)
tama = 1000
charliex = r - a*np.random.uniform(0,1,size=tama)
charliey = r - a*np.random.uniform(0,1,size=tama)
for i in range(tama):
    if (np.linalg.norm([charliex[i],charliey[i]])<=r):
        ac = ac + 1
        aq = aq + 1
    else: 
        aq = aq + 1
print(4*ac/aq)
fig, ax = plt.subplots(figsize=(6,6))

ax.plot(r*np.cos(t),r*np.sin(t),color='red',linewidth=3)
puntos, = ax.plot(charliex,charliey,'o')


def animate(frame):
    puntos.set_data(charliex[:10*frame],charliey[:10*frame])
    return puntos

animation = FuncAnimation(fig=fig,func=animate,frames=tama,interval=33)
#animation.save('animation.gif',writer='pillow',fps=30)
plt.show()



