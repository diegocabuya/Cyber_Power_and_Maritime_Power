#!/usr/bin/env python3
"""Extended robustness analysis of MP_norm (second review round, IEEE Access, Access-2026-53526).

Companion script of the article "Cyber Power as a Structural Variable of Maritime Power: A Normalized
Multiplicative Model for Multidomain Assessment of Maritime Power". It regenerates every number added in
the second revision, including Table 8:

  A. Level 1, Colombian scenario: threshold of the Significant level with maritime security fixed at 0.24;
     alternative positive transformations of the maritime security rank; Proposition 1 with unequal core
     weights lambda_k (mean one), including gamma and alpha above one.
  B. Level 1: distributions and dependence. The independent uniform sampling of Table 7 is repeated with
     triangular distributions and with an equicorrelated Gaussian copula (rho = 0.3 and 0.6).
  C. Level 2: uncertainty in the internal parameters (weights w_i, w_1-w_3, a_1-a_3, beta, mu, delta) and
     in the sub-indicators, with group Sobol' indices (Jansen's estimator for S_T; Saltelli et al. 2010
     with the output centered for S_i) and 95% bootstrap intervals, in three hypothetical designs: sub-indicators within +-0.10 or
     +-0.20 of the Level 1 value of their component, and sub-indicators uniform on [0.01, 1].
  D. Aggregation rules: on the same Level 2 draws, components and levels under the proposed rules (naval
     power normalized), the unnormalized naval-power product, all-geometric and all-arithmetic rules.

Fixed seeds; requires numpy. Reference output: robustness_round2_output.txt

    python3 verification/robustness_round2.py
"""
import math
import warnings
import sys

import numpy as np

np.seterr(all="ignore")   # spurious macOS BLAS warnings in matmul (copula); the correlations were checked separately

M_L1 = 200_000     # draws per Level 1 scenario (B)
N_BOOT = 200        # bootstrap resamples of the Sobol' indices (C)
M_L2 = 50_000      # Sobol' base rows per Level 2 design (C); 2 + 14 groups -> 800,000 evaluations
REF = {"MI": 0.60, "NP": 0.55, "SW": 0.48, "MS": 0.24, "CP": 0.40}
KEYS = ("MI", "NP", "SW", "MS", "CP")
A0, G0 = 0.55, 0.70
NIVELES = ("Critical", "Low", "Moderate", "Significant", "High")
CORTES = np.array([0.20, 0.40, 0.60, 0.80])   # half-open intervals (a, b]: (0,.2], (.2,.4], ...


def pm(MI, NP, SW, MS, CP, a, g, c=(1.0, 1.0, 1.0)):
    """MP_norm with relative core weights lambda (mean one) and n_eff = 3 + g + a."""
    n = 3 + g + a
    s = c[0] * np.log(MI) + c[1] * np.log(NP) + c[2] * np.log(SW) + g * np.log(MS) + a * np.log(CP)
    return np.exp(s / n)


def nivel(y):
    return np.searchsorted(CORTES, y, side="left")   # y <= .20 -> 0, ... ; > .80 -> 4


def reparto(y):
    k = np.bincount(nivel(y), minlength=5) / len(y)
    return {NIVELES[i]: k[i] for i in range(5)}


def fmt_reparto(r):
    return "  ".join(f"{k} {100 * v:5.1f} %" for k, v in r.items() if v >= 0.0005)


salida = []


def out(s=""):
    print(s)
    salida.append(s)


# ---------------------------------------------------------------- A. Level 1, Colombian scenario
out("A. LEVEL 1 -- COLOMBIAN SCENARIO (alpha 0.55, gamma 0.70)")
P0 = float(pm(*[REF[k] for k in KEYS], A0, G0))
G = (REF["MI"] * REF["NP"] * REF["SW"] * REF["MS"] ** G0) ** (1 / (3 + G0))
out(f"  MP_norm = {P0:.4f}   G = {G:.4f}   CP = {REF['CP']:.2f}")
n = 3 + G0 + A0
k_ms = REF["MS"] ** (G0 / n)
x_sig = (0.60 / k_ms) ** (n / (3 + A0))
out(f"  MS fixed at 0.24: with the other four equal to x, MP_norm = 0.60 when x = {x_sig:.4f}")
out(f"  MS fixed at 0.24 and the other four at 0.90: MP_norm = {float(pm(.9, .9, .9, .24, .9, A0, G0)):.4f} (Significant)")
for nom, v in (("MI, NP and SW at 0.80, CP 0.40", dict(MI=.8, NP=.8, SW=.8, MS=.24, CP=.40)),
               ("MI, NP and SW at 0.85, CP 0.40", dict(MI=.85, NP=.85, SW=.85, MS=.24, CP=.40)),
               ("MI, NP, SW and CP at 0.75", dict(MI=.75, NP=.75, SW=.75, MS=.24, CP=.75))):
    y = float(pm(*[v[k] for k in KEYS], A0, G0))
    out(f"    {nom}: MP_norm = {y:.4f} ({NIVELES[int(nivel(np.array([y]))[0])]})")
out(f"  Only MS raised to 1 (rest fixed): MP_norm = {float(pm(.6, .55, .48, 1.0, .4, A0, G0)):.4f}")

out("\n  Transformation of the MS rank (r = 75, N = 99) into the domain (0,1]:")
N_, r_ = 99, 75
eps = 0.01
TRANS = (("max{eps, (N-r)/(N-1)}, eps = 0.01 (adopted)", max(eps, (N_ - r_) / (N_ - 1))),
         ("(N-r+1)/N", (N_ - r_ + 1) / N_),
         ("(N-r+0.5)/N (mid-rank)", (N_ - r_ + 0.5) / N_),
         ("eps + (1-eps)(N-r)/(N-1)", eps + (1 - eps) * (N_ - r_) / (N_ - 1)),
         ("share / sample maximum, 0.59/2.38", 0.59 / 2.38))
for nom, ms in TRANS:
    y = float(pm(.6, .55, .48, ms, .4, A0, G0))
    out(f"    {nom:<46} MS = {ms:.4f}   MP_norm = {y:.4f} ({NIVELES[int(nivel(np.array([y]))[0])]})")
out(f"    last-ranked state (r = N): (N-r)/(N-1) = 0 ; adopted = {eps}; (N-r+1)/N = {1 / N_:.4f}")

out("\n  Proposition 1 with unequal core weights lambda (mean one), 200,000 draws:")
rng = np.random.default_rng(20261109)
M = 200_000
X = rng.uniform(0.01, 1.0, (5, M))
a = rng.uniform(0.01, 3.0, M)
g = rng.uniform(0.01, 3.0, M)        # gamma and alpha above 1 included: the proposition does not bound them
c = rng.dirichlet(np.ones(3), M).T * 3
P = pm(*X, a, g, c)
Gc = np.exp((c[0] * np.log(X[0]) + c[1] * np.log(X[1]) + c[2] * np.log(X[2]) + g * np.log(X[3])) / (3 + g))
w = a / (3 + g + a)
err_id = np.max(np.abs(P - Gc ** (1 - w) * X[4] ** w))
lo, hi = np.minimum(Gc, X[4]), np.maximum(Gc, X[4])
err_cota = max(np.max(lo - P), np.max(P - hi), 0.0)
h = 1e-6
dnum = (pm(*X, a + h, g, c) - pm(*X, a - h, g, c)) / (2 * h)
mask = np.abs(X[4] - Gc) > 1e-4
signo_ok = np.mean(np.sign(dnum[mask]) == np.sign((X[4] - Gc)[mask]))
om = np.vstack([c[0], c[1], c[2], g, a]) / (3 + g + a)
el_err = 0.0
for k in range(5):
    Xu, Xd = X.copy(), X.copy()
    Xu[k] *= 1 + 1e-5
    Xd[k] *= 1 - 1e-5
    el = (np.log(pm(*Xu, a, g, c)) - np.log(pm(*Xd, a, g, c))) / (np.log(1 + 1e-5) - np.log(1 - 1e-5))
    el_err = max(el_err, float(np.max(np.abs(el - om[k]))))
out(f"    identity G^(1-w)CP^w: {err_id:.1e}   bounds: {err_cota:.1e}   sign dMP/dalpha = sign(CP-G): "
    f"{100 * signo_ok:.3f} %   elasticity = omega_k: {el_err:.1e}")
out(f"    sum of omegas: {np.max(np.abs(om.sum(0) - 1)):.1e}  (n_eff = 3 + gamma + alpha also with unequal lambda)")
out("    With normalized AHP weights omega_k (positive, adding up to 1) and omega_bar the mean of the three core weights:")
out("    lambda_k = omega_k/omega_bar, gamma = omega_MS/omega_bar, alpha = omega_CP/omega_bar  ->  all > 0 by construction;")
ej = np.array([0.24, 0.22, 0.20, 0.20, 0.14])
ob = ej[:3].mean()
out(f"    example omega = {ej.tolist()}: lambda = {np.round(ej[:3] / ob, 3).tolist()}, gamma = {ej[3] / ob:.3f}, "
    f"alpha = {ej[4] / ob:.3f}, n_eff = {3 + ej[3] / ob + ej[4] / ob:.3f}")

# ---------------------------------------------------------------- B. Level 1: distributions and dependence
out("\nB. LEVEL 1 -- DISTRIBUTIONS AND DEPENDENCE (Colombian scenario; alpha, gamma ~ U[0.10, 1])")


def marg(u, ref, d, forma):
    lo, hi = max(0.01, ref - d), ref + d
    if forma == "uniform":
        return lo + (hi - lo) * u
    m = (ref - lo) / (hi - lo)              # triangular with mode at the scenario value
    return np.where(u < m, lo + np.sqrt(u * (hi - lo) * (ref - lo)), hi - np.sqrt((1 - u) * (hi - lo) * (hi - ref)))


def cupula(rho, M, rng):
    from scipy.stats import norm
    S = np.full((5, 5), rho) + (1 - rho) * np.eye(5)
    Z = rng.standard_normal((M, 5)) @ np.linalg.cholesky(S).T
    return norm.cdf(Z).T


resB = {}
for d in (0.10, 0.20):
    out(f"  components +-{d:.2f}")
    for nom, forma, rho in (("uniform, independent (Table 7)", "uniform", 0.0),
                            ("triangular, independent", "triangular", 0.0),
                            ("uniform, copula rho = 0.3", "uniform", 0.3),
                            ("uniform, copula rho = 0.6", "uniform", 0.6)):
        rng = np.random.default_rng(20261110 + int(100 * d) + int(10 * rho) + (forma == "triangular"))
        U = rng.uniform(size=(5, M_L1)) if rho == 0 else cupula(rho, M_L1, rng)
        Xs = [marg(U[i], REF[k], d, forma) for i, k in enumerate(KEYS)]
        a = rng.uniform(0.10, 1.0, M_L1)
        g = rng.uniform(0.10, 1.0, M_L1)
        y = pm(*Xs, a, g)
        p5, p50, p95 = np.percentile(y, [5, 50, 95])
        r = reparto(y)
        bajo = np.mean(np.argmin(np.vstack(Xs), axis=0) == 3)
        resB[(d, nom)] = (p50, p5, p95, r, bajo)
        out(f"    {nom:<34} median {p50:.3f}  [P5 {p5:.3f}, P95 {p95:.3f}]   {fmt_reparto(r)}   MS lowest {100 * bajo:.1f} %")

# ---------------------------------------------------------------- C and D. Level 2
out("\nC. LEVEL 2 -- INTERNAL PARAMETERS AND SUB-INDICATORS (hypothetical scenario; group Sobol' indices)")
DELTA0, CDIP0 = 0.25, 0.30
C_CP = REF["CP"] / (1 + DELTA0 * CDIP0)     # CS, CD, RC centered so that CP = 0.40 with delta 0.25 and CDip 0.30
CENTRO = {"MI": [REF["MI"]] * 18, "NP": [REF["NP"]] * 3, "SW": [REF["SW"]] * 3, "MS": [REF["MS"]] * 3,
          "CP": [C_CP] * 3 + [CDIP0]}
GRUPOS = ("x_MI", "x_NP", "x_SW", "x_MS", "x_CP", "w_i", "mu", "w_1-3", "a_1-3", "beta", "delta", "alpha", "gamma")
PARAM_L2 = ("w_i", "mu", "w_1-3", "a_1-3", "beta", "delta")


def muestra(M, diseno, d, rng):
    S = {}
    for comp, cent in CENTRO.items():
        cent = np.array(cent)[:, None]
        if diseno == "dispersed":
            v = rng.uniform(0.01, 1.0, (len(cent), M))
        else:
            v = rng.uniform(np.maximum(0.01, cent - d), np.minimum(1.0, cent + d), (len(cent), M))
        S["x_" + comp] = v
    S["w_i"] = rng.dirichlet(np.ones(18), M).T
    S["mu"] = rng.uniform(0.5, 1.5, (1, M))
    S["w_1-3"] = rng.dirichlet(np.ones(3), M).T
    S["a_1-3"] = rng.dirichlet(np.ones(3), M).T
    S["beta"] = rng.dirichlet(np.ones(3), M).T
    S["delta"] = rng.uniform(0.0, 0.5, (1, M))
    S["alpha"] = rng.uniform(0.10, 1.0, (1, M))
    S["gamma"] = rng.uniform(0.10, 1.0, (1, M))
    return S


def componentes(S, regla="proposed"):
    xmi, xnp, xsw, xms, xcp = S["x_MI"], S["x_NP"], S["x_SW"], S["x_MS"], S["x_CP"]
    mu = S["mu"][0]
    wa, aa, b, dl = S["w_1-3"], S["a_1-3"], S["beta"], S["delta"][0]
    geo = lambda x, w: np.exp((w * np.log(x)).sum(0) / w.sum(0))
    ari = lambda x, w: (w * x).sum(0) / w.sum(0)
    wnp = np.vstack([np.ones_like(mu), np.ones_like(mu), mu])
    amp = 1 + dl * xcp[3]
    if regla == "proposed":
        return (ari(xmi, S["w_i"]), geo(xnp, wnp), geo(xsw, wa), geo(xms, aa), np.minimum(1, ari(xcp[:3], b) * amp))
    if regla == "NP product":
        return (ari(xmi, S["w_i"]), xnp[0] * xnp[1] * xnp[2] ** mu, geo(xsw, wa), geo(xms, aa),
                np.minimum(1, ari(xcp[:3], b) * amp))
    if regla == "all geometric":
        return (geo(xmi, S["w_i"]), geo(xnp, wnp), geo(xsw, wa), geo(xms, aa), np.minimum(1, geo(xcp[:3], b) * amp))
    if regla == "all arithmetic":
        return (ari(xmi, S["w_i"]), ari(xnp, wnp), ari(xsw, wa), ari(xms, aa), np.minimum(1, ari(xcp[:3], b) * amp))
    raise ValueError(regla)


def f(S, regla="proposed"):
    comp = componentes(S, regla)
    return pm(*comp, S["alpha"][0], S["gamma"][0]), comp


def mezclar(A, B, grupos):
    C = dict(A)
    for gname in grupos:
        C[gname] = B[gname]
    return C


resC, resD = {}, {}
for diseno, d in (("balanced", 0.10), ("balanced", 0.20), ("dispersed", None)):
    etiqueta = f"sub-indicators +-{d:.2f} around the value of their component" if d else "sub-indicators uniform on [0.01, 1]"
    rng = np.random.default_rng(20261111 + (int(100 * d) if d else 99))
    A = muestra(M_L2, diseno, d, rng)
    B = muestra(M_L2, diseno, d, rng)
    fA, compA = f(A)
    fB, _ = f(B)
    media = np.concatenate([fA, fB]).mean()
    V = np.concatenate([fA, fB]).var()
    out(f"  {etiqueta}")
    y = np.concatenate([fA, fB])
    p5, p50, p95 = np.percentile(y, [5, 50, 95])
    out(f"    MP_norm median {p50:.3f}  [P5 {p5:.3f}, P95 {p95:.3f}]   {fmt_reparto(reparto(y))}")
    filas = []
    for gname in GRUPOS + ("Level 2 (all internal parameters)",):
        grp = PARAM_L2 if gname.startswith("Level 2") else (gname,)
        fAB, _ = f(mezclar(A, B, grp))
        st = np.mean((fA - fAB) ** 2) / (2 * V)
        s1 = np.mean((fB - media) * (fAB - fA)) / V
        # bootstrap of S_T: the base rows are resampled, with no new model evaluations
        rb = np.random.default_rng(7)
        stb = []
        for _ in range(N_BOOT):
            i = rb.integers(0, M_L2, M_L2)
            stb.append(np.mean((fA[i] - fAB[i]) ** 2) / (2 * np.concatenate([fA[i], fB[i]]).var()))
        lo, hi = np.percentile(stb, [2.5, 97.5])
        filas.append((gname, s1, st, (hi - lo) / 2))
    for gname, s1, st, hw in filas:
        out(f"    {gname:<42} S_i {s1:6.3f}   S_T {st:6.3f}   CI95 +-{hw:.3f}")
    out(f"    largest half-width of the 95% bootstrap CI of S_T: {max(r[3] for r in filas):.3f}")
    resC[(diseno, d)] = dict(p50=p50, p5=p5, p95=p95, rep=reparto(y), filas=filas)

    # D. aggregation rules on the same draws
    out("    D. aggregation rules (same draws A):")
    yA, cA = fA, compA
    nivA, bajoA = nivel(yA), np.argmin(np.vstack(cA), axis=0)
    medias = "  ".join(f"{k} {np.mean(v):.3f}" for k, v in zip(KEYS, cA))
    out(f"      proposed       component means: {medias}   median MP {np.median(yA):.3f}")
    for regla in ("NP product", "all geometric", "all arithmetic"):
        yR, cR = f(A, regla)
        cambio_nivel = np.mean(nivel(yR) != nivA)
        cambio_bajo = np.mean(np.argmin(np.vstack(cR), axis=0) != bajoA)
        np_bajo = np.mean(np.argmin(np.vstack(cR), axis=0) == 1)
        medias = "  ".join(f"{k} {np.mean(v):.3f}" for k, v in zip(KEYS, cR))
        out(f"      {regla:<14} means: {medias}   median MP {np.median(yR):.3f}   "
            f"level differs {100 * cambio_nivel:5.1f} %   lowest component differs {100 * cambio_bajo:5.1f} %   "
            f"NP lowest {100 * np_bajo:5.1f} %")
        resD[(diseno, d, regla)] = dict(cambio_nivel=cambio_nivel, cambio_bajo=cambio_bajo, np_bajo=np_bajo,
                                        mnp=float(np.mean(cR[1])), med=float(np.median(yR)))
    resD[(diseno, d, "proposed")] = dict(np_bajo=float(np.mean(bajoA == 1)), mnp=float(np.mean(cA[1])),
                                         med=float(np.median(yA)))
    out(f"      proposed: NP lowest {100 * resD[(diseno, d, 'proposed')]['np_bajo']:.1f} %")

with open(__file__.replace("robustness_round2.py", "robustness_round2_output.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(salida) + "\n")
