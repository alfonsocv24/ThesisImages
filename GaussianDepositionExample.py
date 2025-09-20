#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 18:06:26 2025

@author: alfonsocabezonvizoso
"""
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm

# # 1) Asymmetric double‐well: tilt term +0.3*x makes the left well deeper.
# def V_base(x):
#     return (x**2 - 1)**2 - 0.5 + 0.3*x

# # 2) Domain and metadynamics params
# x = np.linspace(-3, 3, 800)
# n_steps = 20
# gamma = 0.1
# sigma = 0.3

# # 3) Toy CV trajectory: half the Gaussians in each well (avoid barrier)
# np.random.seed(0)
# pos_left  = np.random.normal(-1.0, 0.2, n_steps//2)
# pos_right = np.random.normal( 1.0, 0.2, n_steps//2)
# cv_positions = np.hstack([pos_left, pos_right])
# np.random.shuffle(cv_positions)

# # 4) Colormap
# colors = cm.plasma(np.linspace(0,1,n_steps))

# # 5) Plot
# plt.figure(figsize=(7,4.5))

# # Thick black base potential
# V0 = V_base(x)
# plt.plot(x, V0-0.05, 'k', lw=3, label='Base potential')

# # Accumulate Gaussians (only in wells) and overplot
# V_acc = V0.copy()
# for pos, col in zip(cv_positions, colors):
#     V_acc += gamma * np.exp(-0.5*((x - pos)/sigma)**2)
#     plt.plot(x, V_acc, color=col, lw=1.2)

# # Cosmetics
# plt.xlim(-1.8, 1.8)
# plt.ylim(-1.2, 1.8)
# plt.xlabel('Collective variable $x$')
# plt.ylabel('Potential $V(x)$')
# plt.title('Gaussian deposition in Metadynamics')
# # plt.grid('--', alpha=0.4)
# plt.tick_params(direction = 'in')
# plt.tight_layout()

# # Uncomment to save:
# plt.savefig('GaussianDeposition.png', dpi = 300, transparent = True)

# plt.show()

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
from matplotlib import cm

# --- 1) Define an asymmetric double‑well ---
def V_base(x):
    # two minima at ±1, left one ~0.3 deeper
    return (x**2 - 1)**2 - 0.5 + 0.3*x

# --- 2) Grid + metadynamics params ---
x       = np.linspace(-3, 3, 1000)
n_steps = 10
gamma   = 0.1    # bump height
sigma   = 0.3     # bump width

# --- 3) Toy “trajectory” crossing the barrier ---
np.random.seed(0)
walk_left   = np.random.normal(-1.0, 0.01, 10)
walk_mid1   = np.random.normal(-0.5, 0.01, 2)
walk_center = np.random.normal( 0.0, 0.05, 0)
walk_mid2   = np.random.normal( 0.5, 0.05, 0)
walk_right  = np.random.normal( 1.0, 0.01, 5)
cv_positions = np.hstack([walk_left, walk_mid1, walk_center, walk_mid2, walk_right])

# --- 4) Colormap for each step ---
colors = cm.plasma(np.linspace(0, 1, len(cv_positions)))

# --- 5) Plot the buildup ---
plt.figure(figsize=(8, 5))

# base potential in thick black
V0 = V_base(x)
plt.plot(x, V0, 'k', lw=3, label='Base potential')

# accumulate Gaussians & overplot each Vₙ(x)
V_acc = V0.copy()
for pos, col in zip(cv_positions, colors):
    V_acc += gamma * np.exp(-0.5 * ((x - pos) / sigma) ** 2)
    plt.plot(x, V_acc, color=col, lw=1.2)

# Cosmetics
plt.xlim(-1.8, 1.8)
plt.ylim(-1.2, 1.8)
plt.xlabel('Collective variable $x$')
plt.ylabel('Potential $V(x)$')
plt.title('Gaussian deposition in Metadynamics')
# plt.grid('--', alpha=0.4)
plt.tick_params(direction = 'in')
# # Uncomment to save:
plt.savefig('GaussianDeposition.png', dpi = 300, transparent = True)

plt.show()





