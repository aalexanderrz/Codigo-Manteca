import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Leer los datos estadísticos
df = pd.read_csv("resultados_frecuencias_estadistico.csv")

frecuencias = df["Frecuencia (Hz)"]
ch1_promedio = df["CH1_Max_Promedio (V)"]
ch2_promedio = df["CH2_Max_Promedio (V)"]
ch1_std = df["CH1_Max_Std (V)"]
ch2_std = df["CH2_Max_Std (V)"]

# 2. Cálculos de Ganancia Lineal y su error
ganancia_lineal = ch2_promedio / ch1_promedio
error_relativo = ((ch2_std / ch2_promedio)**2 + (ch1_std / ch1_promedio)**2)**0.5
error_ganancia_lineal = ganancia_lineal * error_relativo

# 3. Cálculos de Ganancia en Decibelios (dB) y su error
ganancia_db = 20 * np.log10(ganancia_lineal)
error_ganancia_db = (20 / np.log(10)) * error_relativo

# --- (Pasos 1, 2 y 3 se mantienen igual) ---

# 3.5 ENCONTRAR LA FRECUENCIA DE CORTE (-3 dB)
# Calculamos la ganancia máxima y el umbral de corte
ganancia_max_db = ganancia_db.max()
nivel_corte_db = ganancia_max_db - 3.0

# Encontramos el índice del dato experimental que está MÁS CERCA de ese nivel de corte
# np.abs() saca el valor absoluto de la diferencia, y .argmin() nos da la posición del menor error
idx_corte = (np.abs(ganancia_db - nivel_corte_db)).argmin()

# Extraemos la frecuencia y ganancia de ese punto
fc_estimada = frecuencias.iloc[idx_corte]
ganancia_fc = ganancia_db.iloc[idx_corte]

# Velocidad de caída por mínimos cuadrados
sxy = 0
sx = 0
xbar = frecuencias.mean()
ybar = ganancia_db.mean()
for i in range(len(frecuencias)):
        sxy = (frecuencias[i] - xbar) * (ganancia_db[i] - ybar)
        #print(sxy)
        sx = (frecuencias[i] - xbar)**2
        #print(sx)
m = sxy / sx

print(f"Ganancia Máxima: {ganancia_max_db:.2f} dB")
print(f"Nivel de Corte Teórico: {nivel_corte_db:.2f} dB")
print(f"Frecuencia de Corte Estimada (punto más cercano): {fc_estimada} Hz a {ganancia_fc:.2f} dB")
print(f"La razón de atenuación estimada es: {m:.5f} dB/Hz")

"""
# 4. Crear la figura con 2 subgráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
fig.suptitle("Respuesta en Frecuencia del Circuito", fontsize=16, y=0.95)

# --- Gráfica Superior: Ganancia Lineal (Se mantiene igual) ---
ax1.errorbar(frecuencias, ganancia_lineal, yerr=error_ganancia_lineal, fmt='-o', color='purple', 
             ecolor='gray', capsize=5, label='Ganancia Lineal ($V_{out}/V_{in}$)')
ax1.set_ylabel("Ganancia Lineal", fontsize=12)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(loc="upper right")

# --- Gráfica Inferior: Ganancia en dB (Modificada con el corte) ---
ax2.errorbar(frecuencias, ganancia_db, yerr=error_ganancia_db, fmt='-o', color='teal', 
             ecolor='gray', capsize=5, label='Ganancia en dB')

# AGREGAMOS LAS LÍNEAS DE CORTE
# Línea horizontal para el umbral de -3dB
ax2.axhline(nivel_corte_db, color='red', linestyle='--', alpha=0.7, label=f'Umbral -3 dB ({nivel_corte_db:.2f} dB)')
# Línea vertical para la frecuencia de corte encontrada
ax2.axvline(fc_estimada, color='orange', linestyle='--', alpha=0.7, label=f'$f_c$ aprox: {fc_estimada} Hz')
# Un punto grande resaltando la intersección en nuestros datos
ax2.plot(fc_estimada, ganancia_fc, 'ro', markersize=8)

ax2.set_xlabel("Frecuencia (Hz) [Escala Logarítmica]", fontsize=12)
ax2.set_ylabel("Magnitud (dB)", fontsize=12)
ax2.set_xscale('log') 
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.legend(loc="lower left") # Moví la leyenda para que no estorbe las líneas

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
"""
# 4. Crear la figura con 2 subgráficos (2 filas, 1 columna)
# sharex=True permite que ambos gráficos compartan el mismo eje de frecuencias
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
fig.suptitle("Respuesta en Frecuencia del Circuito", fontsize=16, y=0.95)

# --- Gráfica Superior: Ganancia Lineal ---
ax1.plot(frecuencias, ganancia_lineal, color='red', marker = '^', label='Ganancia ($V_{out}/V_{in}$)')
ax1.set_ylabel("Ganancia", fontsize=12)
ax1.grid(True, which="both", alpha=0.5)
ax1.legend(loc="upper right")

# --- Gráfica Inferior: Ganancia en dB ---
ax2.plot(frecuencias, ganancia_db, color='green', 
            marker = '^', label='Ganancia en dB')
ax2.set_xlabel("Frecuencia (Hz)", fontsize=12)
ax2.set_ylabel("Ganancia (dB)", fontsize=12)
ax2.set_xscale('log') # Aplicamos escala logarítmica al eje X compartido
ax2.grid(True, which="both", alpha=0.5)
ax2.legend(loc="upper right")

# Ajustar el espaciado para que no se superpongan los textos
plt.tight_layout()
plt.subplots_adjust(top=0.9) # Damos un pequeño margen para el título principal
#plt.savefig("plot_lab.png")
plt.show()