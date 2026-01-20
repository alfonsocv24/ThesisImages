#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 19:30:58 2026

@author: alfonsocabezonvizoso
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
import numpy as np
import random

def get_lipid_style(lipid_name):
    styles = {
        'PC': {'color': '#5DA5DA', 'label': 'PC'},
        'PS': {'color': '#60BD68', 'label': 'PS'},
        'PE': {'color': '#7A7A7A', 'label': 'PE'},
        'PG': {'color': '#F15854', 'label': 'PG'},
    }
    return styles.get(lipid_name, {'color': 'gray', 'label': '?'})

def draw_curly_tail(ax, head_x, head_y, angle_rad, length=2.0, thickness=1.2, leaflet_type='outer'):
    t = np.linspace(0, length, 20)
    
    if leaflet_type == 'outer':
        direction = -1 
    else:
        direction = 1

    amp = 0.17
    freq = 5
    
    offset_x1 = -0.15 
    tail1_u = t * direction 
    tail1_v = offset_x1 + (np.sin(t * freq) * amp)
    
    offset_x2 = 0.15
    tail2_u = t * direction
    tail2_v = offset_x2 + (np.sin(t * freq + 2) * amp)

    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    
    t1_x = head_x + (tail1_u * cos_a - tail1_v * sin_a)
    t1_y = head_y + (tail1_u * sin_a + tail1_v * cos_a)
    
    t2_x = head_x + (tail2_u * cos_a - tail2_v * sin_a)
    t2_y = head_y + (tail2_u * sin_a + tail2_v * cos_a)

    ax.plot(t1_x, t1_y, color='#444444', lw=thickness, zorder=1) 
    ax.plot(t2_x, t2_y, color='#444444', lw=thickness, zorder=1)

def draw_membrane_final():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # =============================================================================
    # ADJUST DISTANCE BETWEEN LEAFLETS
    # =============================================================================
    r_outer = 15
    inter_leaflet_gap = 5.5
    r_inner = r_outer - inter_leaflet_gap
    # =============================================================================


    # =============================================================================
    # ADJUST HEAD AND TAIL SIZE
    # =============================================================================
    head_radius = 0.55
    tail_len = 2.5          
    tail_thickness = 3.5 
    sign_size = 30       
    # =============================================================================

    
    # =============================================================================
    # ADJUST LIPID COUNTS
    # =============================================================================
    num_lipids_outer = 62
    num_lipids_inner = 42
    # =============================================================================


    # =============================================================================
    # ADJUST ROTATION ANGLES (New!)
    # =============================================================================
    # Rotate the entire ring in degrees. 
    # Use this to align lipids or create staggering.
    rotation_outer = 0      
    rotation_inner = 17     # Try changing this to stagger the inner ring
    # =============================================================================


    # Create base angles and apply rotation
    angles_outer = np.linspace(0, 2*np.pi, num_lipids_outer, endpoint=False)
    angles_outer += np.radians(rotation_outer) # Apply rotation

    angles_inner = np.linspace(0, 2*np.pi, num_lipids_inner, endpoint=False)
    angles_inner += np.radians(rotation_inner) # Apply rotation


    mammalian_outer_dist = ['PC']*80 + ['PE']*20
    mammalian_inner_dist = ['PE']*40 + ['PS']*60
    bacterial_outer_dist = ['PE']*45 + ['PG']*45 + ["PC"]*10
    bacterial_inner_dist = ['PE']*45 + ['PG']*45 + ["PC"]*10

    # --- DRAW OUTER LEAFLET ---
    for theta in angles_outer:
        # Normalize angle to 0-360 for consistent domain checking
        deg = np.degrees(theta) % 360
        
        # Determine Mammalian (Left) vs Bacterial (Right)
        # 90 to 270 is Left
        is_mammalian = 90 <= deg <= 270
        
        if is_mammalian:
            lipid_choice = random.choice(mammalian_outer_dist)
        else:
            lipid_choice = random.choice(bacterial_outer_dist)
            
        style = get_lipid_style(lipid_choice)
        
        draw_curly_tail(ax, r_outer*np.cos(theta), r_outer*np.sin(theta), theta, 
                        length=tail_len, thickness=tail_thickness, leaflet_type='outer')
        
        circle = patches.Circle((r_outer*np.cos(theta), r_outer*np.sin(theta)), radius=head_radius, 
                                facecolor=style['color'], edgecolor='black', zorder=10)
        ax.add_patch(circle)
        
        if style['label'] in ['PS', 'PG']:
             dist = r_outer + head_radius + 0.4 
             ax.text(dist*np.cos(theta), dist*np.sin(theta), "-", 
                     ha='center', va='center', fontsize=sign_size, fontweight='bold')

    # --- DRAW INNER LEAFLET ---
    for theta in angles_inner:
        deg = np.degrees(theta) % 360
        is_mammalian = 90 <= deg <= 270
        
        if is_mammalian:
            lipid_choice = random.choice(mammalian_inner_dist)
        else:
            lipid_choice = random.choice(bacterial_inner_dist)
            
        style = get_lipid_style(lipid_choice)
        
        draw_curly_tail(ax, r_inner*np.cos(theta), r_inner*np.sin(theta), theta, 
                        length=tail_len, thickness=tail_thickness, leaflet_type='inner')
        
        circle = patches.Circle((r_inner*np.cos(theta), r_inner*np.sin(theta)), radius=head_radius, 
                                facecolor=style['color'], edgecolor='black', zorder=10)
        ax.add_patch(circle)
        
        if style['label'] in ['PS', 'PG']:
             dist = r_inner - head_radius - 0.4
             ax.text(dist*np.cos(theta), dist*np.sin(theta), "-", 
                     ha='center', va='center', fontsize=sign_size, fontweight='bold')

    ax.plot([0, 0], [20, -18], color='black', lw=3, zorder=5, ls = "--")
    
    plt.text(-8, 19, "Mammalian Membrane", fontsize=22, ha='center', fontweight='bold')
    plt.text(8, 19, "Bacterial Membrane", fontsize=22, ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig("LipidBilayerComparison.png", dpi = 300, transparent = True)

if __name__ == "__main__":
    draw_membrane_final()