#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 12:18:39 2026

@author: alfonsocabezonvizoso
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_final_pbc_updates():
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm" 
    })
    fig, ax = plt.subplots(figsize=(12, 12))
    
    
    # --------------------------
    # 1. Setup Simulation Domain
    # --------------------------
    L = 1.0  # Box length
    
    # Particle Positions (Central Box)
    pos = np.array([
        [0.65, 0.90], # Particle A: Leaving top
        [0.25, 0.50], # Particle B: Center Left
        [0.45, 0.75]  # Particle C: Center
    ])
    
    # Velocities
    vel = np.array([
        [0.05, 0.25],  # Velocity for A
        [0.10, -0.05],
        [-0.10, 0.15]
    ])
    
    # Colors
    colors = ['#084594', '#2171b5', '#9ecae1']
    
    # Global Boundaries of the 3x3 visualization for wrapping logic
    Y_MAX = 2.0  # Top of the j=1 row
    Y_MIN = -1.0 # Bottom of the j=-1 row
    
    # --------------------------
    # 2. Draw Grid & Particles
    # --------------------------
    grid_range = [-1, 0, 1]
    
    # Separate loop for boxes to handle z-order explicitly
    # Draw Replica Boxes FIRST (zorder=0)
    for i in grid_range:
        for j in grid_range:
            shift = np.array([i*L, j*L])
            is_center = (i == 0 and j == 0)
            
            if not is_center:
                rect = patches.Rectangle((shift[0], shift[1]), L, L, 
                                         linewidth=1.0,
                                         edgecolor='#bdc3c7',
                                         facecolor='none',
                                         linestyle='--',
                                         zorder=0) # Replicas at the bottom
                ax.add_patch(rect)

    # Draw Central Box LAST (zorder=1)
    # This ensures solid black lines overwrite the dashed grey lines of neighbors
    rect_center = patches.Rectangle((0, 0), L, L, 
                             linewidth=2.5,
                             edgecolor='black',
                             facecolor='none',
                             linestyle='-',
                             zorder=1) # Center box on top of replicas
    ax.add_patch(rect_center)

    # Draw Particles and Vectors
    for i in grid_range:
        for j in grid_range:
            shift = np.array([i*L, j*L])
            is_center = (i == 0 and j == 0)
            
            for k in range(len(pos)):
                p = pos[k] + shift
                v = vel[k]
                
                # Style
                alpha = 1.0 if is_center else 0.4
                zorder = 10 if is_center else 5
                
                # Draw Particle Circle
                circle = patches.Circle(p, 0.06, 
                                        facecolor=colors[k], 
                                        edgecolor='none', 
                                        alpha=alpha, 
                                        zorder=zorder)
                ax.add_patch(circle)
                
                # --- VECTOR HANDLING (Wrapped logic from previous turn) ---
                start_p = p
                end_p = p + v
                draw_standard = True
                
                # Check for Global Boundary Crossing (Top Replicas j=1, Particle k=0)
                if k == 0 and j == 1: 
                    if end_p[1] > Y_MAX:
                        draw_standard = False
                        # 1. Draw cut vector (Start to Boundary)
                        dy = v[1]
                        dx = v[0]
                        if dy != 0:
                            t = (Y_MAX - start_p[1]) / dy
                            intersect_x = start_p[0] + t * dx
                            intersect_p = np.array([intersect_x, Y_MAX])
                            
                            ax.plot([start_p[0], intersect_x], [start_p[1], Y_MAX],
                                    color='black', alpha=alpha, zorder=zorder, linewidth=1)
                            
                            # 2. Draw wrapped tip in Bottom Row (j=-1)
                            rem_start = np.array([intersect_x, Y_MIN])
                            rem_end   = rem_start + (end_p - intersect_p)
                            
                            ax.arrow(rem_start[0], rem_start[1], 
                                     rem_end[0] - rem_start[0], rem_end[1] - rem_start[1],
                                     head_width=0.03, head_length=0.04,
                                     fc='black', ec='black', alpha=alpha, zorder=zorder,
                                     length_includes_head=True)
                            
                            # 3. Draw Ghost at the wrapped position
                            # ghost_circle = patches.Circle(rem_end, 0.06, 
                            #           facecolor='none', edgecolor=colors[0], 
                            #           linestyle=':', linewidth=2, zorder=12)
                            # ax.add_patch(ghost_circle)

                if draw_standard:
                    ax.arrow(p[0], p[1], v[0], v[1], 
                             head_width=0.03, head_length=0.04, 
                             fc='black', ec='black', 
                             alpha=alpha, zorder=zorder, 
                             length_includes_head=True)

    # --------------------------
    # 3. Central Mechanism Annotation & Text
    # --------------------------
    p_main = pos[0] # Top of central box
    v_main = vel[0]
    p_bottom = p_main + np.array([0, -1.0]) # Particle in bottom box
    
    # Ghost 1: Leaving Top
    future_pos_top = p_main + v_main
    ghost_top = patches.Circle(future_pos_top, 0.06, 
                               facecolor='none', edgecolor=colors[0], 
                               linestyle=':', linewidth=2, zorder=12)
    ax.add_patch(ghost_top)
    
    # Ghost 2: Re-entering Bottom
    future_pos_bottom = p_bottom + v_main
    ghost_bottom = patches.Circle(future_pos_bottom, 0.06, 
                                  facecolor='none', edgecolor=colors[0], 
                                  linestyle=':', linewidth=2, zorder=12)
    ax.add_patch(ghost_bottom)
    
    # Connection Line
    ax.plot([p_main[0], p_bottom[0]], [p_main[1], p_bottom[1]], 
            color='#d62728', linestyle=':', linewidth=2, zorder=2)

    # --- NEW: TEXT ANNOTATIONS ---
    # 1. r(t) next to the particle leaving the main cell
    # Position: p_main
    ax.text(p_main[0] + 0.08, p_main[1], r"$r(t)$", 
            fontsize=20, color='black', verticalalignment='center')
    
    # 2. r(t + Delta t) next to the ghost particle entering the main cell
    # Position: future_pos_bottom (This is the ghost re-entering)
    ax.text(future_pos_bottom[0] - 0.49, future_pos_bottom[1], r"$r(t + \Delta t)$", 
            fontsize=18, color='black', verticalalignment='center')

    # --------------------------
    # 4. Final Formatting
    # --------------------------
    ax.set_xlim(-1.5, 2.5)
    ax.set_ylim(-1.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    
    # plt.tight_layout()
    plt.savefig('pbc_image.png', dpi=300)#, bbox_inches='tight', pad_inches=0)
    plt.show()

draw_final_pbc_updates()