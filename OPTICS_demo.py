#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 18:20:55 2025

@author: alfonsocabezonvizoso
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
from sklearn.cluster import OPTICS
from sklearn.datasets import make_blobs
from matplotlib import gridspec

# Generate sample data
n_samples = 500
random_state = 42
X, _ = make_blobs(
    n_samples=n_samples,
    centers=[[0, 0], [5, 5], [0, 5]],
    cluster_std=[0.5, 0.5, 0.5],
    random_state=random_state
)

# Run OPTICS
optics_model = OPTICS(min_samples=10, xi=0.05, min_cluster_size=0.05)
optics_model.fit(X)

# Extract reachability and ordering
ordering = optics_model.ordering_
reachability = optics_model.reachability_[ordering]
space = np.arange(len(X))

# Extract predecessor (for spanning tree)
predecessors = optics_model.predecessor_

# Cluster labels and colors
labels = optics_model.labels_
labels_ordered = labels[ordering]
cluster_colors = {0: 'indianred', 1: 'royalblue', 2: 'black'}

# Create figure with GridSpec
fig = plt.figure(figsize=(14, 12))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])


# Top-left: scatter plot
ax0 = fig.add_subplot(gs[0, 0])
ax0.scatter(X[:, 0], X[:, 1], s=15, c = 'gray')
# ax0.set_xlabel('Feature 0')
# ax0.set_ylabel('Feature 1')
ax0.set_title('Input data for OPTICS', fontsize = 20)
# ax0.grid(True, linestyle='--', alpha=0.5)

# Top-right: spanning tree
ax1 = fig.add_subplot(gs[0, 1])
for idx, pred in enumerate(predecessors):
    if pred != -1:
        ax1.plot(
            [X[idx, 0], X[pred, 0]],
            [X[idx, 1], X[pred, 1]],
            linewidth=2.5, c = 'green', alpha = 0.2
        )
# Scatter points colored by cluster
for lbl, color in cluster_colors.items():
    mask = labels == lbl
    ax1.scatter(X[mask, 0], X[mask, 1], s=30, color=color, label=f'Cluster {lbl}')
# ax1.scatter(X[:, 0], X[:, 1], s=15)
# ax1.set_xlabel('Feature 0')
# ax1.set_ylabel('Feature 1', fontsize = 18)
ax1.set_title('OPTICS Spanning Tree', fontsize = 20)
# ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(fontsize = 16)

# Bottom (spanning both cols): reachability plot colored by cluster
ax2 = fig.add_subplot(gs[1, :])
ax2.plot(space, reachability, color = 'green', alpha = 0.3)
for lbl, color in cluster_colors.items():
    mask = labels_ordered == lbl
    ax2.scatter(space[mask], reachability[mask], s=30, color=color, label=f'Cluster {lbl}')
ax2.set_xlabel('OPTICS indexing', fontsize = 18)
ax2.set_ylabel('Reachability distance', fontsize = 18)
ax2.set_title('OPTICS Reachability Plot', fontsize = 20)
# ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(fontsize = 16)

for i in [ax0, ax1, ax2]:
    i.tick_params(direction = 'in', labelsize = 16)

fig.tight_layout()

# Display the combined plot
plt.savefig('OPTICS_demo.png', dpi = 300)
