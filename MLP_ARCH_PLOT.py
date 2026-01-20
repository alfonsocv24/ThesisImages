#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 18:30:57 2026

@author: alfonsocabezonvizoso
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

def draw_mlp(layer_sizes, layer_colors):
    """
    Draws a Multilayer Perceptron with specific styling.
    
    Parameters:
    - layer_sizes: List of integers representing neurons per layer.
    - layer_colors: List of strings for the outline color of each layer.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Configuration
    v_spacing = 1.0   # Vertical space between neurons
    h_spacing = 2.0   # Horizontal space between layers
    neuron_radius = 0.3
    
    # Store coordinates of neurons to draw connections later
    # Structure: layers_coords[layer_index][neuron_index] = (x, y)
    layers_coords = []


    # 1. Calculate Coordinates
    for i, n in enumerate(layer_sizes):
        layer_nodes = []
        layer_x = i * h_spacing
        
        # Center the neurons vertically
        # y = spacing * (node_index - (total_nodes - 1) / 2)
        for j in range(n):
            layer_y = v_spacing * (j - (n - 1) / 2)
            layer_nodes.append((layer_x, layer_y))
        
        layers_coords.append(layer_nodes)

    # 2. Draw Connections (Lines)
    # We draw these first so they appear behind the neurons (zorder=1)
    for i in range(len(layers_coords) - 1):
        curr_layer = layers_coords[i]
        next_layer = layers_coords[i + 1]
        
        for p1 in curr_layer:
            for p2 in next_layer:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                        color='black', alpha=0.4, linewidth=2, zorder=1)

    # 3. Draw Neurons (Circles)
    # We draw these second so they appear on top of lines (zorder=2)
    for i, layer_nodes in enumerate(layers_coords):
        color = layer_colors[i]
        for x, y in layer_nodes:
            # Create the circle patch
            circle = Circle((x, y), radius=neuron_radius, 
                            facecolor='white', edgecolor=color, 
                            linewidth=4, zorder=2)
            ax.add_patch(circle)

    # 4. Add Layer Labels at the TOP - zorder=3 (front)
    
    # Find the highest y-coordinate occupied by any neuron
    max_layer_size = max(layer_sizes)
    # The top neuron is at index (n-1). Using the formula from step 1:
    max_y_coord = v_spacing * ((max_layer_size - 1) - (max_layer_size - 1) / 2)

    # Determine y-position for labels (above the highest neuron + radius + padding)
    label_y_pos = max_y_coord + neuron_radius + 0.5
    
    # Font styling - changed 'va' to 'bottom' so text sits on the line
    font_style = {'fontsize': 30, 'fontweight': 'bold', 'ha': 'center', 'va': 'bottom'}

    # Input Layer Label (centered horizontally over the first layer)
    ax.text(layers_coords[0][0][0], label_y_pos, "Input Layer", 
            color=layer_colors[0], **font_style)

    # Hidden Layers Label (centered horizontally between the two hidden layers)
    hidden_center_x = (layers_coords[1][0][0] + layers_coords[2][0][0]) / 2
    ax.text(hidden_center_x, label_y_pos, "Hidden Layers", 
            color='black', **font_style)

    # Output Layer Label (centered horizontally over the last layer)
    ax.text(layers_coords[-1][0][0], label_y_pos, "Output Layer", 
            color=layer_colors[-1], **font_style) 

    # 4. Final Plot Styling
    ax.set_aspect('equal')
    plt.axis('off')  # Turn off axis lines and labels
    # plt.title("Multilayer Perceptron Architecture", fontsize=15)
    plt.tight_layout()
    plt.savefig("MLP_architecture.png", transparent = True, dpi = 300)
    plt.show()

# --- Configuration based on user request ---
# Architecture: 4 Input, 8 Hidden, 6 Hidden, 1 Output
mlp_layers = [3, 6, 4, 1]

# Colors: Forestgreen (Input), Black (Hidden 1), Black (Hidden 2), Red (Output)
mlp_colors = ['forestgreen', 'black', 'black', 'red']

# Generate the plot
draw_mlp(mlp_layers, mlp_colors)