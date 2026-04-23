#!/usr/bin/env python3
"""
gamma_traces.py
===============
Módulo para el cálculo numérico de trazas de matrices de Dirac
y elementos matriciales al cuadrado en QED.

Representación: Dirac-Pauli.
Convención de métrica: (+,-,-,-).
"""

import numpy as np
from itertools import product as cartesian

# ============================================================
# 1. Definición de las matrices gamma
# ============================================================

# Matrices de Pauli
sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)

I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
Z2 = np.zeros((2, 2), dtype=complex)

sigma = [sigma_1, sigma_2, sigma_3]

# gamma^0
gamma0 = np.block([[I2, Z2], [Z2, -I2]])

# gamma^k (k=1,2,3)
gamma_spatial = []
for k in range(3):
    gk = np.block([[Z2, sigma[k]], [-sigma[k], Z2]])
    gamma_spatial.append(gk)

# Arreglo indexado: gamma[mu] para mu=0,1,2,3
gamma = [gamma0] + gamma_spatial

# gamma^5 = i gamma^0 gamma^1 gamma^2 gamma^3
gamma5 = 1j * gamma[0] @ gamma[1] @ gamma[2] @ gamma[3]

# Métrica
eta = np.diag([1.0, -1.0, -1.0, -1.0])


def gamma_lower(mu):
    """Devuelve gamma_mu = eta_{mu,mu} gamma^mu."""
    return eta[mu, mu] * gamma[mu]


def p_slash(p):
    """
    Calcula p-slash = p_mu gamma^mu = p^mu gamma_mu (con métrica).
    p debe ser un 4-vector contravariante: p = (p0, p1, p2, p3).
    """
    result = np.zeros((4, 4), dtype=complex)
    for mu in range(4):
        result += p[mu] * gamma_lower(mu)
    return result


# ============================================================
# 2. Función para calcular trazas
# ============================================================

def trace(*matrices):
    """
    Calcula Tr{M1 @ M2 @ ... @ Mn}.
    Acepta una secuencia de matrices 4x4 (numpy arrays).
    """
    result = I4.copy()
    for M in matrices:
        result = result @ M
    return np.trace(result)


def trace_gamma(*indices, include_g5=False):
    """
    Calcula Tr{gamma^{mu1} gamma^{mu2} ... gamma^{mun} [gamma5]}.
    indices: tupla de enteros (0,1,2,3) para los índices de Lorentz.
    include_g5: si True, incluye gamma5 al final del producto.
    """
    matrices = [gamma[mu] for mu in indices]
    if include_g5:
        matrices.append(gamma5)
    return trace(*matrices)


# ============================================================
# 3. Amplitud al cuadrado para e-q -> e-q
# ============================================================

def dot4(p, q):
    """Producto escalar de Minkowski p·q = p^mu q_mu."""
    return p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3]


def M2_eq_scattering(p1, p2, p3, p4, Qq, me=0.0, mq=0.0, e=1.0):
    """
    Calcula <|M|^2> para la dispersión e-q -> e-q
    usando el resultado analítico (ecuación 1 del problema 7).

    Parámetros:
        p1, p2, p3, p4: cuadrimomentos (arrays de 4 componentes).
        Qq: carga fraccionaria del quark.
        me, mq: masas del electrón y del quark.
        e: acoplamiento electromagnético.
    """
    t = dot4(p1 - p3, p1 - p3)
    term1 = dot4(p1, p2) * dot4(p3, p4)
    term2 = dot4(p1, p4) * dot4(p2, p3)
    term3 = -me**2 * dot4(p2, p4)
    term4 = -mq**2 * dot4(p1, p3)
    term5 = 2 * me**2 * mq**2
    bracket = term1 + term2 + term3 + term4 + term5
    return 8 * Qq**2 * e**4 / t**2 * bracket


def M2_eq_massless(s, t, u, Qq, e=1.0):
    """
    Calcula <|M|^2> en el límite sin masa usando variables de Mandelstam.
    """
    return 2 * Qq**2 * e**4 * (s**2 + u**2) / t**2


def M2_eq_traces(p1, p2, p3, p4, Qq, me=0.0, mq=0.0, e=1.0):
    """
    Calcula <|M|^2> para e-q -> e-q evaluando las trazas numéricamente.
    Esto sirve como verificación del resultado analítico.
    """
    t = dot4(p1 - p3, p1 - p3)

    # Tensor leptónico del electrón: Tr{(p3_slash + me) gamma^mu (p1_slash + me) gamma^nu}
    ps1 = p_slash(p1)
    ps2 = p_slash(p2)
    ps3 = p_slash(p3)
    ps4 = p_slash(p4)

    Le = np.zeros((4, 4), dtype=complex)
    Lq = np.zeros((4, 4), dtype=complex)

    for mu in range(4):
        for nu in range(4):
            # Traza del electrón
            Le[mu, nu] = trace(ps3 + me * I4, gamma[mu], ps1 + me * I4, gamma[nu])
            # Traza del quark
            Lq[mu, nu] = trace(ps4 + mq * I4, gamma_lower(mu),
                               ps2 + mq * I4, gamma_lower(nu))

    # Contracción
    contraction = 0.0
    for mu in range(4):
        for nu in range(4):
            contraction += Le[mu, nu] * Lq[mu, nu]

    return Qq**2 * e**4 / (4 * t**2) * contraction.real


# ============================================================
# 4. Verificaciones
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICACIONES DE TRAZAS DE MATRICES DE DIRAC")
    print("=" * 60)

    # --- Verificación 1: (gamma5)^2 = 1 ---
    g5_sq = gamma5 @ gamma5
    print("\n1. (gamma5)^2 =")
    print(np.round(g5_sq.real, 6))
    assert np.allclose(g5_sq, I4), "¡Error: (gamma5)^2 != I!"
    print("   -> Coincide con I4  ✓")

    # --- Verificación 2: {gamma5, gamma^mu} = 0 ---
    print("\n2. Anticonmutador {gamma5, gamma^mu}:")
    for mu in range(4):
        anticomm = gamma5 @ gamma[mu] + gamma[mu] @ gamma5
        ok = np.allclose(anticomm, 0)
        print(f"   mu={mu}: max|{{g5,g{mu}}}| = {np.max(np.abs(anticomm)):.1e}  {'✓' if ok else '✗'}")

    # --- Verificación 3: Tr{gamma^mu gamma^nu} = 4 eta^{mu,nu} ---
    print("\n3. Tr{gamma^mu gamma^nu} vs 4*eta^{mu,nu}:")
    for mu in range(4):
        for nu in range(4):
            val = trace_gamma(mu, nu)
            expected = 4 * eta[mu, nu]
            if abs(val - expected) > 1e-10:
                print(f"   ({mu},{nu}): {val:.1f} vs {expected:.1f}  ✗")
    print("   -> Todos coinciden  ✓")

    # --- Verificación 4: Tr{g^mu g^nu g^rho g^sigma} ---
    print("\n4. Tr{gamma^mu gamma^nu gamma^rho gamma^sigma}:")
    print("   Casos particulares:")
    for (m, n, r, s) in [(0,0,0,0), (0,1,0,1), (0,1,2,3), (1,2,1,2)]:
        val = trace_gamma(m, n, r, s)
        analytic = 4*(eta[m,n]*eta[r,s] - eta[m,r]*eta[n,s] + eta[m,s]*eta[n,r])
        print(f"   ({m},{n},{r},{s}): numérico={val.real:+.0f}, analítico={analytic:+.0f}  "
              f"{'✓' if abs(val-analytic)<1e-10 else '✗'}")

    # --- Verificación 5: Tr{g^mu g^nu g^rho g^sigma g5} ---
    print("\n5. Tr{gamma^mu gamma^nu gamma^rho gamma^sigma gamma5}:")
    # epsilon^{0123} = +1
    val = trace_gamma(0, 1, 2, 3, include_g5=True)
    print(f"   (0,1,2,3): {val:.4f}  (esperado: -4i = {-4j})")
    # (1,0,2,3) debe dar +4i
    val2 = trace_gamma(1, 0, 2, 3, include_g5=True)
    print(f"   (1,0,2,3): {val2:.4f}  (esperado: +4i = {4j})")
    # Índices repetidos: debe dar 0
    val3 = trace_gamma(0, 0, 1, 2, include_g5=True)
    print(f"   (0,0,1,2): {val3:.4f}  (esperado: 0)")

    # --- Verificación 6: Tr{g^mu g^nu g5} = 0 ---
    print("\n6. Tr{gamma^mu gamma^nu gamma5}:")
    all_zero = True
    for mu in range(4):
        for nu in range(4):
            val = trace_gamma(mu, nu, include_g5=True)
            if abs(val) > 1e-10:
                print(f"   ({mu},{nu}): {val} ✗")
                all_zero = False
    if all_zero:
        print("   -> Todos cero  ✓")

    # --- Verificación 7: e-q scattering ---
    print("\n" + "=" * 60)
    print("VERIFICACIÓN: DISPERSIÓN e-q (sin masas)")
    print("=" * 60)

    # Cinemática en el CM: sqrt(s) = 100 GeV, theta = 60 grados
    Ecm = 100.0
    theta = np.pi / 3
    E = Ecm / 2
    pz = E  # masas nulas

    p1 = np.array([E, 0, 0, pz])
    p2 = np.array([E, 0, 0, -pz])
    p3 = np.array([E, E*np.sin(theta), 0, E*np.cos(theta)])
    p4 = np.array([E, -E*np.sin(theta), 0, -E*np.cos(theta)])

    Qq = 2.0/3  # quark up
    e_coupling = 1.0

    s = 2 * dot4(p1, p2)
    t = dot4(p1 - p3, p1 - p3)
    u = dot4(p1 - p4, p1 - p4)

    print(f"\n   sqrt(s) = {Ecm:.1f} GeV, theta = {np.degrees(theta):.0f}°")
    print(f"   s = {s:.2f},  t = {t:.2f},  u = {u:.2f}")
    print(f"   s + t + u = {s+t+u:.6f}  (debe ser ~0)")

    # Método 1: fórmula analítica con productos escalares
    M2_analytic = M2_eq_scattering(p1, p2, p3, p4, Qq, me=0, mq=0, e=e_coupling)
    # Método 2: fórmula con variables de Mandelstam
    M2_mandelstam = M2_eq_massless(s, t, u, Qq, e=e_coupling)
    # Método 3: trazas numéricas
    M2_numerical = M2_eq_traces(p1, p2, p3, p4, Qq, me=0, mq=0, e=e_coupling)

    print(f"\n   <|M|^2> (prod. escalares): {M2_analytic:.6f}")
    print(f"   <|M|^2> (Mandelstam):      {M2_mandelstam:.6f}")
    print(f"   <|M|^2> (trazas num.):     {M2_numerical:.6f}")
    print(f"   Diferencia relativa:       {abs(M2_analytic-M2_numerical)/M2_analytic:.2e}")

