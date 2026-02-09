import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#La idea es aplicar la idea del punto movible a un objeto sobre un círculo (reloj) y parar una vez ha
#cubierto todos los 12 números

#creamos los parámetros para el círculo que representará al reloj
r = 1
t = np.linspace(0,2*np.pi,13)
rplot = np.full((13),r)

label = ['12','11','10','9','8','7','6','5','4','3','2','1','']

#creemos el algoritmo para movernos
n = 50 #número de pasos
p = 1 #tamaño de paso
estado1 = np.zeros(n) # creamos el contenedor de las posiciones
restado = np.full((n),r) #radios de los estados
estado01 = np.random.randint(0,12)*p*np.pi/6
estado1[0] = estado01
estado02 = np.random.randint(0,12)*p*np.pi/6
estado2 = np.zeros(n)
for i in range(1,n):
    kaj = np.random.randint(1,3) #generador del movimiento
    daj = np.random.randint(1,3)
    match kaj:
        case 1:
            estado1[i] = estado1[i-1]+p*np.pi/6 #movimiento hacia la izquierda
        case 2:
            estado1[i] = estado1[i-1]-p*np.pi/6 #movimiento hacia la derecha
            kaj = np.random.randint(1,3) #generador del movimiento
    match daj:
        case 1:
            estado2[i] = estado2[i-1]+p*np.pi/6 #movimiento hacia la izquierda
        case 2:
            estado2[i] = estado2[i-1]-p*np.pi/6 #movimiento hacia la derecha

#ploteamos el reloj

fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
#ax.scatter(t,rplot,markersize=3)
ax.set_xticks(t)
ax.set_xticklabels(label)
ax.set_yticklabels([])
ax.set_theta_zero_location('N')
papa, = ax.plot(estado1,restado,'o')
mama, = ax.plot(estado2,restado,'o')
#animamos
time = 15e3 #tiempo de animación en ms
intv = int(time/n) #intervalo necesario entre los frames
def animate(frame):
    papa.set_data([estado1[frame]],[restado[frame]])
    mama.set_data([estado2[frame]],[restado[frame]])
    return papa, mama

animation = FuncAnimation(fig=fig,func=animate,frames=n,interval=intv)
plt.show()