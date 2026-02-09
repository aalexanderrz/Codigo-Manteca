import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Now we have to generate our preliminary conditions like possible positions
t = np.linspace(0,2*np.pi,13)
r0 = 1
xp = r0*np.cos(t)
yp = r0*np.sin(t)
fig, ax = plt.subplots(figsize=(5,5))
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.5,1.5)
ax.set_yticklabels([])
ax.set_xticklabels([])
#ax.scatter(xp,yp)
#Now we want to be able to generate one of the possible 12 positions.
T0 = np.random.randint(0,12)*(t[1]-t[0])
#Once we are here, we want to be able to move to the next position
#We would also like to keep track of our journey, so let's create an empty list and a max amount of steps
n = 20
statesx = np.zeros(n)
statesy = np.zeros(n)
statesx[0] = r0*np.cos(T0)
statesy[0] = r0*np.sin(T0)
phi = 30*np.pi/180
for i in range(1,n):
    statesx[i] = r0*np.cos(i*phi)
    statesy[i] = r0*np.sin(i*phi)
    '''
    j = np.random.randint(1,3)
    match j:
        case 1:
            statesx[i] = statesx[i-1]*np.cos(phi)-statesy[i-1]*np.sin(phi)
            statesy[i] = statesx[i-1]*np.sin(phi)+statesy[i]*np.cos(phi)
        case 2:
            statesx[i] = statesx[i-1]*np.cos(phi)+statesy[i-1]*np.sin(phi)
            statesy[i] = -statesx[i-1]*np.sin(phi)+statesy[i-1]*np.cos(phi)
    '''
#Now we animate
point = ax.plot([],[],'o')

def animate(frame):
    point.set_data(statesx[frame],statesy[0])
    return point

animation = FuncAnimation(
    fig=fig,func=animate,frames=n,interval=333
)
plt.show()
