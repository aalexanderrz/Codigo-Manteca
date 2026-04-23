#!/usr/bin/env python3
"""
running_alpha.py
================
Genera la gráfica de alpha^{-1}(Q) vs Q para la constante
de estructura fina en QED, incluyendo contribuciones de
leptones y quarks ligeros.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Constantes
alpha_0 = 1.0 / 137.036  # alpha(0)
MZ = 91.1876  # GeV

# Masas de los fermiones cargados (GeV)
m_e = 0.000511
m_mu = 0.10566
m_tau = 1.7768
m_u = 0.002   # quark u (masa constituyente efectiva ~ escala QCD, pero usamos corriente)
m_d = 0.005   # quark d
m_s = 0.095   # quark s
m_c = 1.275   # quark c
m_b = 4.18    # quark b
m_t = 173.0   # quark top

# Cargas eléctricas al cuadrado (en unidades de e)
# leptones: Q=1, quarks u,c,t: Q=2/3, quarks d,s,b: Q=1/3
# Factor de color Nc=3 para quarks

fermions = [
    # (nombre, masa, Q^2 * Nc)
    ("e",   m_e,   1.0),
    ("mu",  m_mu,  1.0),
    ("tau", m_tau, 1.0),
    ("u",   m_u,   3 * (2/3)**2),
    ("d",   m_d,   3 * (1/3)**2),
    ("s",   m_s,   3 * (1/3)**2),
    ("c",   m_c,   3 * (2/3)**2),
    ("b",   m_b,   3 * (1/3)**2),
]


def delta_alpha_fermion(Q, mf, NcQ2):
    """
    Contribución de un fermión a Delta alpha, usando la fórmula a 1 lazo
    con un corte suave en el umbral.

    Para Q >> 2*mf:
        Delta alpha_f = (alpha/3pi) * NcQ2 * [ln(Q^2/mf^2) - 5/3]

    Para Q < 2*mf: contribución suprimida.
    """
    if Q < 1e-6:
        return 0.0

    ratio = Q**2 / mf**2
    if ratio < 4:
        # Por debajo del umbral: contribución suprimida
        # Usamos la forma exacta a 1 lazo con beta = sqrt(1 - 4mf^2/Q^2)
        # que se vuelve imaginaria por debajo del umbral (región space-like
        # vs time-like). Para Q^2 > 0 (space-like), la contribución real es:
        beta2 = 1 - 4 * mf**2 / Q**2
        if beta2 < 0:
            beta = np.sqrt(-beta2)
            # Fórmula analítica para la región subumbral
            da = (alpha_0 / (3 * np.pi)) * NcQ2 * (
                -5/3 + 4*mf**2/Q**2
                + (1 - 2*mf**2/Q**2) * 2*beta * np.arctan(1/beta)
            )
        else:
            beta = np.sqrt(beta2)
            da = (alpha_0 / (3 * np.pi)) * NcQ2 * (
                -5/3 + 4*mf**2/Q**2
                + (1 - 2*mf**2/Q**2) * beta * np.log((1+beta)/(1-beta+1e-30))
            )
        return max(da, 0.0)
    else:
        # Formula logarítmica estándar (válida para Q >> 2mf)
        return (alpha_0 / (3 * np.pi)) * NcQ2 * (np.log(ratio) - 5/3)


def alpha_running(Q):
    """Calcula alpha(Q) sumando las contribuciones de todos los fermiones."""
    Delta = 0.0
    for name, mf, NcQ2 in fermions:
        Delta += delta_alpha_fermion(Q, mf, NcQ2)

    # Evitar polo de Landau
    denom = 1.0 - Delta
    if denom <= 0.01:
        return alpha_0 / 0.01
    return alpha_0 / denom


# Generar datos
Q_values = np.logspace(-4, np.log10(500), 1000)  # de 0.1 MeV a 500 GeV
alpha_inv = np.array([1.0 / alpha_running(Q) for Q in Q_values])

# Valor en el polo Z
alpha_MZ = alpha_running(MZ)
print(f"alpha^{{-1}}(0)   = {1/alpha_0:.3f}")
print(f"alpha^{{-1}}(M_Z) = {1/alpha_MZ:.1f}")
print(f"alpha(M_Z) = 1/{1/alpha_MZ:.1f}")

# ============================================================
# Gráfica
# ============================================================

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(Q_values, alpha_inv, linewidth=1.8, color = 'limegreen')

# Marcar el polo Z
ax.axvline(x=MZ, color='red', linestyle='--', linewidth=0.8, alpha=0.7)
ax.annotate(
    rf'$M_Z = {MZ:.1f}$ GeV' + f'\n' + rf'$\alpha^{{-1}} \approx {1/alpha_MZ:.1f}$',
    xy=(MZ, 1/alpha_MZ), xytext=(200, 132),
    arrowprops=dict(arrowstyle='->', color='red', lw=1.2),
    fontsize=11, color='red',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='red', alpha=0.8)
)

# Marcar umbrales de leptones
threshold_labels = [
    (2*m_e, r'$2m_e$', 0.002),
    (2*m_mu, r'$2m_\mu$', 0.25),
    (2*m_tau, r'$2m_\tau$', 4.5),
    (2*m_c, r'$2m_c$', 3.0),
    (2*m_b, r'$2m_b$', 10.0),
]

for thresh, label, xpos in threshold_labels:
    ax.axvline(x=thresh, color='gray', linestyle=':', linewidth=0.6, alpha=0.5)
    ypos = 1.0 / alpha_running(thresh)
    ax.annotate(label, xy=(thresh, ypos),
                xytext=(thresh*1.5, ypos + 1.5),
                fontsize=9, color='gray',
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.6))

# Línea horizontal en 137
ax.axhline(y=137.036, color='green', linestyle='--', linewidth=0.6, alpha=0.5)
ax.text(0.0003, 137.5, r'$\alpha^{-1}(0) = 137.036$', fontsize=9, color='green')

ax.set_xscale('log')
ax.set_xlabel(r'$Q$ [GeV]', fontsize=14)
ax.set_ylabel(r'$\alpha^{-1}(Q)$', fontsize=14)
ax.set_title(r'Evolución de la constante de estructura fina $\alpha^{-1}(Q)$', fontsize=14)
ax.set_xlim(1e-4, 500)
ax.set_ylim(125, 138)
ax.tick_params(labelsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('running_alpha.pdf', dpi=150)
plt.savefig('running_alpha.png', dpi=150)
print("\nGráfica guardada: running_alpha.pdf / running_alpha.png")
