"""
╔══════════════════════════════════════════════════════════════════════╗
║              EXAMEN SIMULACRO — FÍSICA COMPUTACIONAL                 ║
║                         FCL1109 · 2026                               ║
╠══════════════════════════════════════════════════════════════════════╣
║  Duración : 1 hora 30 minutos                                        ║
║  Permitido: fcl1109.py (como fc), numpy (uso básico), matplotlib     ║
║  Archivos : datos_decaimiento.csv, senal_ruido.csv                   ║
║                                                                      ║
║  Instrucciones generales:                                            ║
║  - Cada problema indica lo que se debe calcular, graficar o          ║
║    imprimir.                                                         ║
║  - Use print() para reportar resultados numéricos.                   ║
║  - Guarde todas las gráficas con plt.savefig().                      ║
║  - Comente brevemente cada paso de su código.                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import matplotlib.pyplot as plt
import fcl1109 as fc

# ====================================================================
# PROBLEMA 1 — Potencial de Lennard-Jones          (25 pts · ~20 min)
# ====================================================================
#
# El potencial de Lennard-Jones modela la interacción entre dos átomos
# neutros:
#
#          V(r) = 4ε [ (σ/r)^12  −  (σ/r)^6 ]
#
# con  ε = 0.0103 eV  y  σ = 3.40 Å  (parámetros del argón).
#
# a) Defina la función V(r).
#
# b) Use Newton-Raphson para encontrar la distancia de equilibrio r_eq,
#    es decir, el punto donde la fuerza F(r) = −dV/dr = 0.
#    (Sugerencia: busque la raíz de F(r) con x₀ = 3.5 Å.)
#    Imprima r_eq con al menos 6 decimales.
#
# c) Calcule la segunda derivada V''(r_eq) usando derivada_enesima.
#    Esto equivale a la "constante de resorte" efectiva κ del enlace.
#    Imprima κ en eV/Å².
#
# d) Grafique V(r) en el rango r ∈ [3.0, 7.0] Å.
#    Marque con un punto rojo la posición de equilibrio (r_eq, V(r_eq)).
#    Etiquete los ejes y guarde la gráfica como "p1_lennard_jones.png".
#

#parámetros constantes
e = 0.0103 #eV
s = 3.40 #Armstrong
x0 = 3.5 #Armstrong
h = 1e-6 #para derivada central


#a)
"""
#definición de potencial
def V(r):
    return 4 * e * ((s / r) ** 12 - (s / r) ** 6)

#b)

def F(r):
    dfdr = fc.derivada_central(V, r, h)
    return dfdr

root = fc.newton_raphson(F, x0, h, 1e-6, 10)

print(f'La raíz para la fuerza es: {root:.6}, la cual fue encontrada con una toleracia de {1e-3} y una cantidad máxima de {10} iteraciones.')

#c)

segunda = fc.derivada_enesima(F, root, 2)

print(f'El valor de la constane de resorte fue de {segunda:.3} ev/A²')

#d)

r = np.linspace(3.0, 7.0, 1000)
potencial = V(r)
plt.plot(r, potencial, label="V(r)", color='green')
plt.scatter(root, V(root), label=r'$r_{eq}$', color='red')
plt.legend()
plt.xlabel(r'r')
plt.ylabel('V(r)')
plt.grid()
plt.show()
"""



# --- Escriba su código aquí ---


# ====================================================================
# PROBLEMA 2 — Distribución de Maxwell-Boltzmann   (25 pts · ~20 min)
# ====================================================================
#
# La distribución de rapideces de Maxwell-Boltzmann es:
#
#      f(v) = 4π · (m / 2πkT)^(3/2) · v² · exp(−mv² / 2kT)
#
# Use:  m = 6.63 × 10⁻²⁶ kg  (argón),  T = 300 K,
#       k_B = 1.381 × 10⁻²³ J/K.
#
# a) Defina f(v) y verifique que está normalizada, es decir, que
#    ∫₀^∞ f(v) dv = 1 usando integral_impropia.
#    Imprima el resultado.
#
# b) Calcule la rapidez más probable v_p (donde f(v) es máxima)
#    usando Newton-Raphson sobre f'(v) = 0.
#    (Sugerencia: x₀ = 300 m/s.)
#    Imprima v_p y compárelo con el valor analítico v_p = √(2kT/m).
#
# c) Calcule la probabilidad de que una partícula tenga rapidez
#    v > 600 m/s, es decir P = ∫₆₀₀^∞ f(v) dv.
#    Imprima P.
#
# d) Grafique f(v) en el rango v ∈ [0, 1000] m/s.
#    Sombree (con plt.fill_between) la región v > 600 m/s.
#    Marque v_p con una línea vertical punteada.
#    Guarde como "p2_maxwell.png".
#


"""
#definición de constantes
m = 6.63e-26 #kg
T = 300 #K
k = 1.381e-23 #J/K
eps = 1e-6
x0 = 300 #m/s
#a)vpoints

def f(v):
    return np.pi * 4 * (m / ( 2 * np.pi * k * T)) ** (3/2) * (v ** 2) * np.exp((- m * (v**2))/ (2 * k * T))
#f(v) = 4π · (m / 2πkT)^(3/2) · v² · exp(−mv² / 2kT)

integral = fc.integral_impropia(f, 0, np.inf, 100000)
print(f'\nEl resultado de la integral normalizada es {integral}')

#b)
def df(v):
    return fc.derivada_enesima(f, v, 1)

vprob = fc.newton_raphson(df, x0, h, 1e-6, 100000)
anal = np.sqrt((2 * k * T) / m)

print(f'La velocidad con mayor probabilidad fue calculada como {vprob:.3} m/s, que se compara con el valor analítico de {anal:.3}')

#c)

prob600 = fc.integral_impropia(f, 600, np.inf, 100000)
print(f'La probabilidad de que la velocidad sea mayor que 600 m/s es de {prob600:.3}')
# --- Escriba su código aquí ---

#d)
vpoints = np.linspace(0, 1000, 10000)
escotv = np.linspace(vprob, 1000, 10000)
denscot = f(escotv)
densidad = np.pi * 4 * (m / ( 2 * np.pi * k * T)) ** (3/2) * (vpoints ** 2) * np.exp((- m * (vpoints**2))/ (2 * k * T))

plt.plot(vpoints, densidad)
plt.xlim(min(vpoints), max(vpoints))
plt.ylim(min(densidad), max(densidad))
plt.plot((vprob, vprob), (min(densidad), max(densidad)), '--')
plt.fill_between(escotv, denscot)
plt.show()
"""

# ====================================================================
# PROBLEMA 3 — Oscilador armónico amortiguado      (25 pts · ~25 min)
# ====================================================================
#
# Un oscilador amortiguado obedece la ecuación:
#
#      d²x/dt² + 2γ dx/dt + ω₀² x = 0
#
# con  ω₀ = 2π rad/s  (frecuencia natural)  y  γ = 0.3 s⁻¹ (amortiguamiento).
#
# Condiciones iniciales:  x(0) = 1.0 m ,  v(0) = dx/dt(0) = 0 m/s.
#
# a) Reescriba la EDO de segundo orden como un sistema de dos EDOs
#    de primer orden:
#        dx/dt = v
#        dv/dt = −2γv − ω₀²x
#    Defina la función f(t, estado) que recibe t y estado = [x, v]
#    y devuelve [dx/dt, dv/dt].
#
# b) Integre desde t = 0 hasta t = 15 s usando rk4 con dt = 0.01.
#    Almacene los arreglos de t, x(t) y v(t).
#
# c) En una misma figura con dos subplots (uno encima del otro):
#      - Arriba: x(t) vs t.  Superponga la solución analítica:
#            x_a(t) = e^{−γt} [cos(ω_d · t) + (γ/ω_d) sin(ω_d · t)]
#        donde  ω_d = √(ω₀² − γ²).
#      - Abajo: v(t) vs t.
#    Guarde como "p3_oscilador.png".
#
# d) Imprima el error máximo |x_numérico − x_analítico| en todo el
#    intervalo.
#

"""
#constantes
omega = 2 * np.pi #rad/s
gamma = 0.3 #s⁻1
t0 = 0
tf = 15
dt = 0.01
x0 = np.array([1.0, 0], float)
wd = np.sqrt(omega ** 2 + gamma ** 2)

#a)

def f(t, x):
    dxdt = x[1]
    dvdt = - 2 * gamma * x[1] - omega ** 2 * x[0]
    return np.array([dxdt, dvdt], float)

#b)

tpoints = np.arange(t0, tf, dt)
xpoints = np.zeros(len(tpoints))
vpoints = np.zeros(len(tpoints))
anal = np.exp(- gamma * tpoints) * (np.cos(wd * tpoints) + (gamma / wd) * np.sin(wd * tpoints))

for i in range(len(tpoints)):
    xpoints[i] = x0[0]
    vpoints[i] = x0[1]

    x0 = fc.rk4(tpoints[i], dt, x0, f)

#c)

fig, ax = plt.subplots(2,1, figsize = (4, 10))
ax[0].plot(tpoints, anal, label = 'anal', alpha = 0.5)
ax[0].plot(tpoints, xpoints, label = 'nume', linestyle = '--')
ax[0].legend()
ax[1].plot(tpoints, vpoints)
plt.show()

error = abs(anal - xpoints)
plt.plot(tpoints, error)
plt.show()
"""
# --- Escriba su código aquí ---


# ====================================================================
# PROBLEMA 4 — Ajuste de datos + Análisis de Fourier (25 pts · ~25 min)
# ====================================================================
#
# ── Parte A: Ajuste de decaimiento radiactivo (15 pts) ──
#
# El archivo "datos_decaimiento.csv" contiene mediciones (t, N, σ)
# de la actividad de una muestra radiactiva.
#
# El modelo es:  N(t) = N₀ · e^{−λt}
# Linealizando:  ln(N) = ln(N₀) − λt   →   Y = a₀ + a₁·t
#
# a) Cargue los datos. Calcule Y = ln(N) y la incertidumbre propagada
#    σ_Y = σ / |N|.
#
# b) Construya la matriz normal A (2×2) y el vector b (2×1) para
#    el ajuste lineal ponderado Y = a₀ + a₁·t, y resuelva con
#    minimos_cuadrados. Extraiga N₀ = e^{a₀} y λ = −a₁.
#    Imprima N₀ y λ.
#
# c) Calcule χ² y χ²/ν (con ν = N_datos − 2).
#    Imprima ambos valores.
#
# d) Grafique: datos con barras de error + curva ajustada N₀·e^{−λt}.
#    Incluya en la gráfica el valor de N₀, λ y χ²/ν como texto.
#    Guarde como "p4a_decaimiento.png".
#
#
"""
datos = np.loadtxt("datos_decaimiento.csv", delimiter = ',', skiprows = 1)
t = datos[:, 0]
N = datos[:, 1]
sigma = datos[:, 2]
Y = np.log(N)
incert = sigma / N
S = Sx = Sxx = Sy = Sxy = 0
for i in range(len(N)):
    sigmoid = 1 / sigma[i] ** 2
    S += 1 / sigmoid
    Sx += t[i] / sigmoid
    Sxx += t[i] ** 2 / sigmoid
    Sy += Y[i] / sigmoid
    Sxy += t[i] * Y[i] / sigmoid

A = np.array([[S, Sx], [Sx, Sxx]])
b = np.array([Sy, Sxy])
cof = fc.minimos_cuadrados(A, b)
tpoints = np.linspace(t[0], t[len(t) - 1], len(t))
fit = np.exp(cof[0] + cof[1] * tpoints)
chi = fc.chi_cuadrada(Y, fit, sigma)
chichi = chi / (len(t) - 2)
plt.errorbar(t, N, yerr = sigma, label = "data")
plt.plot(tpoints, fit, label = "fit", linestyle = '--')
plt.legend()
plt.show()
"""
# ── Parte B: Análisis espectral de una señal (10 pts) ──
#
# El archivo "senal_ruido.csv" contiene una señal V(t) muestreada
# uniformemente con dt = 0.01 s (128 puntos).
#
# e) Cargue los datos. Calcule la FFT de la señal V usando fc.fft().
#
# f) Construya el eje de frecuencias:  freq_k = k / (N·dt)  para
#    k = 0, 1, ..., N/2.
#    Grafique |FFT[k]| vs frecuencia (solo la mitad positiva, k=0..N/2).
#
# g) Identifique las dos frecuencias dominantes (los dos picos más altos
#    excluyendo k=0). Imprima sus valores en Hz.
#    Guarde la gráfica como "p4b_espectro.png".
#

datos = np.loadtxt("senal_ruido.csv", delimiter = ',', skiprows = 1)
t = datos[:, 0]
V = datos[:, 1]

furry = fc.fft(V)
k = np.zeros(len(t) // 2 + 1)
mag = np.zeros(len(t) // 2 + 1)

for i in range(len(t) // 2 + 1):
    k[i] = i / (len(t) * 0.01)
    mag[i] = np.abs(furry[i])
plt.stem(k, mag)
plt.show()

indices = []
maximo = max(mag)


for l in range(1, len(mag)):
    if mag[l] == maximo:
        indices.append(l)
        narray = np.delete(mag, l)
        for j in range(0, len(narray)):
            if narray[j] ==  max(narray):
                indices.append(j + 1)

# --- Escriba su código aquí ---

ind1 = indices[0]
ind2 = indices[1]

print(f'Las frecuencias de mayor aporte son: {k[ind1]} y {k[ind2]} Hz')

print("\n" + "=" * 50)
print("  FIN DEL EXAMEN — Verifique sus gráficas y salidas")
print("=" * 50)