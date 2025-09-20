#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 15:09:09 2025

@author: alfonsocabezonvizoso
"""

# Re-import libraries after code execution state reset
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
from sklearn.decomposition import PCA

# Generate synthetic 2D data with some correlation
np.random.seed(42)
mean = [0, 0]
cov = [[3, 2], [2, 2]]  # Covariance matrix with correlation
x, y = np.random.multivariate_normal(mean, cov, 400).T
data = np.vstack((x, y)).T
print(len(x))
# Fit PCA
pca = PCA(n_components=2)
pca.fit(data)
components = pca.components_
mean_point = pca.mean_

# Recreate the plot with arrows at the end of the principal component lines
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(data[:, 0], data[:, 1], s = 60, c = 'black', alpha=0.5, label='Original data')

# Plot principal components as arrows
pc_component = 1
colors = ['red', 'blue']
for length, vector in zip(pca.explained_variance_, components):
    v = vector * 3 * np.sqrt(length)
    ax.arrow(mean_point[0], mean_point[1], v[0], v[1],
             width=0.1, head_width=0.3, head_length=0.3,
             fc=colors[pc_component-1], ec=colors[pc_component-1], label=f'PC{pc_component}')
    pc_component += 1

# Axes settings
ax.set_aspect('equal')
ax.tick_params(direction = 'in', labelsize = 16)
ax.set_ylabel('Y-axis', fontsize = 18)
ax.set_xlabel('X-axis', fontsize = 18)
# ax.axhline(0, color='grey', lw=1)
# ax.axvline(0, color='grey', lw=1)
ax.set_title('PCA applied to 2D data', fontsize = 20)
ax.legend(fontsize = 16)
plt.grid(True, linestyle = '--')
plt.tight_layout()
plt.savefig('PCA_demonstration.png', transparent = True, dpi = 300)
