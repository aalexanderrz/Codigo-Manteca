#ejercicio 3.1 del libro Monte Carlo

import numpy as np
import matplotlib.pyplot as plt
import time #Dios por alguna razón

#registrar tiempo de inicio
start_time = time.time()

#código grueso, por qué está tan grueso
#:3c
estados = []
intentos = 1000000
trayectoriax = []
trayectoriay = []

for j in range(intentos):
    n = np.random.randint(0,21)
    r = np.zeros((n,2))
    tcontadorx = 0
    tcontadory = 0
    for i in range (1,n):
        eleccion = np.random.randint(0,4)
        match eleccion:
            case 0:
                r[i][0] = r[i-1][0] + 1
                r[i][1] = r[i-1][1]
                tcontadorx += 1
            case 1:
                r[i][0] = r[i-1][0]
                r[i][1] = r[i-1][1] + 1
                tcontadory += 1
            case 2:
                r[i][0] = r[i-1][0] - 1
                r[i][1] = r[i-1][1]
                tcontadorx += 1
            case 3:
                r[i][0] = r[i-1][0]
                r[i][1] = r[i-1][1] - 1
                tcontadory += 1
    trayectoriax.append(tcontadorx)
    trayectoriay.append(tcontadory)
    estados.append(r)
avgx = np.mean(trayectoriax)
avgy = np.mean(trayectoriay)
print(f'El promedio de la distancia recorrida fue {avgx:.4} para x y {avgy:.4} para y')
end_time = time.time()
tiempo = end_time - start_time
print(f'el tiempo DE ejecución: {tiempo:.4}s')

fig, ax = plt.subplots()
ax.grid()
for l in range(intentos):
    ax.plot(estados[l][:,0],estados[l][:,1])

plt.show()

#registrar el tiempo final de ejecución


#calcular y mostrar el tiempo


