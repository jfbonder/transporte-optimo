# -*- coding: utf-8 -*-
"""Genera las tres ilustraciones de la portada (notas/portada-{I,II,III}.pdf).

   Requiere POT: pip install pot


   portada-I   : el mapa monótono (acoplamiento comonótono, líneas que no se cruzan)
   portada-II  : la geodésica de Wasserstein (interpolación por desplazamiento)
   portada-III : baricentro entrópico de tres formas (Sinkhorn convolucional)

Salida: notas/portada-{I,II,III}.pdf
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
import ot
import pathlib

DEST = pathlib.Path(__file__).resolve().parent.parent / "notas"

ICNAVY = "#013274"
ICCYAN = "#029BDF"
ICMAG  = "#E2017B"
DMRED  = "#A8000C"

CM = 1 / 2.54
FIGSIZE = (5.1 * CM, 4.6 * CM)        # el tamaño exacto que ocupa en la portada


def normal(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def cuantil(x, f, u):
    """Pseudoinversa de la función de distribución de la densidad f sobre la grilla x."""
    F = np.cumsum(f) * (x[1] - x[0])
    F /= F[-1]
    return np.interp(u, F, x)


# ----------------------------------------------------------------- densidades
x = np.linspace(-5.5, 5.5, 4000)
f_mu = 0.58 * normal(x, -2.5, 0.52) + 0.42 * normal(x, -0.6, 0.40)
f_nu = 0.5 * normal(x, 2.0, 1.00) + 0.5 * normal(x, 3.4, 0.55)
f_mu /= np.trapezoid(f_mu, x)
f_nu /= np.trapezoid(f_nu, x)


# ============================================================ I. mapa monótono
fig, ax = plt.subplots(figsize=FIGSIZE)

esc = 0.80 / max(f_mu.max(), f_nu.max())
y_mu, y_nu = 1.0, 0.0

ax.fill_between(x, y_mu, y_mu + esc * f_mu, color=ICCYAN, alpha=0.55, lw=0)
ax.plot(x, y_mu + esc * f_mu, color=ICNAVY, lw=1.1)
ax.fill_between(x, y_nu, y_nu - esc * f_nu, color=ICMAG, alpha=0.45, lw=0)
ax.plot(x, y_nu - esc * f_nu, color=ICMAG, lw=1.1)

u = (np.arange(1, 15) - 0.5) / 14
for q0, q1 in zip(cuantil(x, f_mu, u), cuantil(x, f_nu, u)):
    ax.plot([q0, q1], [y_mu, y_nu], color=ICNAVY, lw=0.75, alpha=0.5,
            solid_capstyle="round")

sop_mu = x[f_mu > 1e-3]; sop_nu = x[f_nu > 1e-3]
ax.plot([sop_mu[0], sop_mu[-1]], [y_mu, y_mu], color=ICNAVY, lw=0.7, alpha=0.7)
ax.plot([sop_nu[0], sop_nu[-1]], [y_nu, y_nu], color=ICMAG, lw=0.7, alpha=0.7)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-0.86, 1.86)
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(DEST / "portada-I.pdf", transparent=True)
plt.close(fig)


# ===================================================== II. geodésica de W_2
fig, ax = plt.subplots(figsize=FIGSIZE)

uu = np.linspace(1e-4, 1 - 1e-4, 3000)
Qmu, Qnu = cuantil(x, f_mu, uu), cuantil(x, f_nu, uu)
fmu_Q = np.interp(Qmu, x, f_mu)
fnu_Q = np.interp(Qnu, x, f_nu)

ts = np.linspace(0, 1, 5)
cmap = LinearSegmentedColormap.from_list("ic", [to_rgb(ICCYAN), to_rgb(ICNAVY), to_rgb(ICMAG)])

paso = 0.55
for k, t in enumerate(ts[::-1]):
    xt = (1 - t) * Qmu + t * Qnu
    dxt = (1 - t) / np.maximum(fmu_Q, 1e-9) + t / np.maximum(fnu_Q, 1e-9)
    rho = 1.0 / dxt
    base = paso * k
    col = cmap(1 - k / (len(ts) - 1))
    ax.fill_between(xt, base, base + rho, color="white", lw=0, zorder=2 * k)
    ax.fill_between(xt, base, base + rho, color=col, alpha=0.35, lw=0, zorder=2 * k)
    ax.plot(xt, base + rho, color=col, lw=1.3, zorder=2 * k + 1,
            solid_capstyle="round")

ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-0.05, paso * (len(ts) - 1) + 1.05)
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(DEST / "portada-II.pdf", transparent=True)
plt.close(fig)


# ============================================== III. baricentro entrópico
n = 72
gx, gy = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))


def normaliza(a):
    a = a.astype(float)
    return a / a.sum()


disco = normaliza(((gx - 0.5) ** 2 + (gy - 0.5) ** 2 < 0.37 ** 2))
cuadrado = normaliza((np.abs(gx - 0.5) < 0.33) & (np.abs(gy - 0.5) < 0.33))
tri = normaliza((gy - 0.10 > 0) & (gy - 0.10 < 1.75 * (gx - 0.08)) &
                (gy - 0.10 < 1.75 * (0.92 - gx)))

A = np.stack([disco, cuadrado, tri])
bar = ot.bregman.convolutional_barycenter2d(A, reg=0.0016,
                                            weights=np.ones(3) / 3,
                                            numItermax=20000, stopThr=1e-11)

cmap_in = LinearSegmentedColormap.from_list("nav", ["white", to_rgb(ICNAVY)])
cmap_bar = LinearSegmentedColormap.from_list("mag", ["white", to_rgb(ICMAG)])

fig = plt.figure(figsize=FIGSIZE)
# tres entradas en los vértices y el baricentro en el centro
pos_in = [(0.00, 0.57, 0.33, 0.33), (0.67, 0.57, 0.33, 0.33), (0.335, 0.00, 0.33, 0.33)]
for (l, b, w, h), img in zip(pos_in, A):
    a = fig.add_axes([l, b, w, h])
    a.imshow(img, cmap=cmap_in, origin="lower", interpolation="bilinear")
    a.axis("off")

a = fig.add_axes([0.285, 0.30, 0.43, 0.43])
a.imshow(bar, cmap=cmap_bar, origin="lower", interpolation="bilinear")
a.axis("off")
fig.savefig(DEST / "portada-III.pdf", transparent=True)
plt.close(fig)

print("listas:", *(p.name for p in sorted(DEST.glob("portada-*.pdf"))))
