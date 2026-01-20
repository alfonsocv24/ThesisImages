#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 13:19:28 2026

@author: alfonsocabezonvizoso
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

def draw_leap_frog_diagram_v5():
    
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm" 
    })
    # 1. Setup Figure
    # Increased width to allow equations to fit without overlapping
    fig, ax = plt.subplots(figsize=(16, 6))

    # 2. Draw the Timeline
    # Main horizontal line
    # ax.plot([-0.8, 3.4], [0, 0], 'k-', lw=3)
    # Arrow at the end
    ax.annotate("", xy=(3.55, 0), xytext=(-0.8, 0),
                arrowprops=dict(arrowstyle="->", lw=3, color='k'))
    # Label 't'
    ax.text(3.6, 0, r"$t$", fontsize=26, va='center', ha='left')

    # PARAMETERS
    rad = -0.85           # Curvature of arcs
    arc_y_base = 0.05    # Arcs start slightly above line
    label_y_offset = 0.52 # "x" and "v" labels above arcs
    
    # Alternating heights for equations below the line
    y_eq_x = -0.17       # Position equations (Row 1 - closer)
    y_eq_v = -0.05       # Velocity equations (Row 2 - further)
    
    tick_len = 0.04      # Length of the small ticks on the timeline
    
    color_x = 'black'
    color_v = 'firebrick'

    # ==========================
    # 3. Handle X (Position)
    # ==========================
    # We want arcs for intervals: [0,1], [1,2], [2,3]
    # We want labels/ticks at: 0, 1, 2, 3
    
    # Draw Arcs
    x_arc_starts = [0, 1.0, 2.0]
    for start in x_arc_starts:
        end = start + 1.0
        # Draw Arc
        arc = patches.FancyArrowPatch((start, arc_y_base), (end, arc_y_base),
                                      connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="->", mutation_scale=20, 
                                      color=color_x, lw=2)
        ax.add_patch(arc)
        # Label 'x' above arc
        mid = (start + end) / 2
        ax.text(mid, label_y_offset, "r", ha='center', fontsize=24, color=color_x, weight='bold')

    # Draw Ticks and Equations for X
    # Points: 0, 1, 2, 3
    x_points = [0, 1, 2, 3]
    for i, t in enumerate(x_points):
        # Tick mark
        ax.plot([t, t], [0, -tick_len], color="black", lw=3)
        
        # Equation Label
        if i == 0:
            txt = r"$r(t)$"
        elif i == 1:
            txt = r"$r(t + \Delta t)$"
        else:
            txt = r"$r(t + " + str(i) + r"\Delta t)$"
            
        ax.text(t, y_eq_x, txt, ha='center', va='top', fontsize=22, color=color_x)

    # ==========================
    # 4. Handle V (Velocity)
    # ==========================
    # We want arcs for intervals: [-0.5, 0.5], [0.5, 1.5], [1.5, 2.5]
    # We want labels/ticks at: -0.5, 0.5, 1.5, 2.5
    
    # Draw Arcs
    v_arc_starts = [-0.5, 0.5, 1.5]
    for start in v_arc_starts:
        end = start + 1.0
        # Draw Arc
        arc = patches.FancyArrowPatch((start, arc_y_base), (end, arc_y_base),
                                      connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="->", mutation_scale=20, 
                                      color=color_v, lw=2)
        ax.add_patch(arc)
        # Label 'v' above arc
        mid = (start + end) / 2
        ax.text(mid, label_y_offset, "v", ha='center', fontsize=24, color=color_v, weight='bold')

    # Draw Ticks and Equations for V
    # Points: -0.5, 0.5, 1.5, 2.5
    v_points = [-0.5, 0.5, 1.5, 2.5]
    for i, t in enumerate(v_points):
        # Tick mark
        ax.plot([t, t], [0, -tick_len], color=color_v, lw=3)
        
        # Equation Label
        # i=0 -> -1/2, i=1 -> +1/2, i=2 -> +3/2, i=3 -> +5/2
        if i == 0:
            sign = "-"
            num = "1"
        else:
            sign = "+"
            num = str(2*i - 1)
            
        txt = r"$v(t " + sign + r" \frac{" + num + r"}{2}\Delta t)$"
        
        ax.text(t, y_eq_v, txt, ha='center', va='top', fontsize=22, color=color_v)

    # 5. Clean up
    ax.set_xlim(-1.0, 4.0)
    ax.set_ylim(-0.8, 1.5) # Expanded bottom limit to fit staggered text
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig("LeapFrogIntegrator", dpi = 300, transparent = True)

if __name__ == "__main__":
    draw_leap_frog_diagram_v5()