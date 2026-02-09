#we have our constants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
sigma = 10
beta = 8/3
rho = 28
time = 5


def rk4single(fun,dt,t0,y0):
    f1 = fun(t0, y0)
    f2 = fun(t0 + dt / 2 , y0 + (dt/2) * f1)
    f3 = fun(t0 + dt / 2, y0 + (dt/2) * f2)
    f4 = fun(t0 + dt, y0 + f3 * dt)
    yout = y0 + (dt/6)*(f1+2*f2+2*f3+f4)
    return yout

def lorenz(t,state):
    x, y, z = state
    dy =[sigma * (y - x),
         x * (rho - z) - y,
         x * y - beta * z]
    return np.array(dy)

#initial condition
y0 = [np.random.randint(-10,10),np.random.randint(-10,10),np.random.randint(-10,10)]
y1 = [np.random.randint(-10,10)+0.1,np.random.randint(-10,10)+0.1,np.random.randint(-10,10)+0.1]
#compute trajectory
dt = 0.01
T = 50
num_time_pts = int(T/dt)
t = np.linspace(0,T,num_time_pts)

Y = np.zeros((3,num_time_pts))
Z = np.zeros((3,num_time_pts))
Y[:,0] = y0
Z[:,0] = y1
yin = y0
yin1 = y1

for i in range(num_time_pts-1):
    yout = rk4single(lorenz,dt,t[i],yin)
    yout1 = rk4single(lorenz,dt,t[i],yin1)
    Y[:,i+1] = yout
    Z[:,i+1] = yout1
    yin = yout
    yin1 = yout1

fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
attractor, = ax.plot(Y[0,:],Y[1,:],Y[2,:],'b', color='red')
attractor1, = ax.plot(Z[0,:],Z[1,:],Z[2,:], 'b')

def animated(frame):
    attractor.set_data(Y[0,:frame],Y[1,:frame])
    attractor.set_3d_properties(Y[2,:frame])
    attractor1.set_data(Z[0,:frame],Z[1,:frame])
    attractor1.set_3d_properties(Z[2,:frame])
    return attractor, attractor1

animation = anim.FuncAnimation(fig=fig,func=animated,frames=num_time_pts,interval=25)
plt.show()