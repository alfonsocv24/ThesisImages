#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:07:27 2025

@author: alfonsocabezonvizoso
"""


from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import sys
import networkx as nx
import graphein.molecule as gm
import argparse
import matplotlib.pyplot as plt

# =============================================================================
'''Define user inputs'''
parser = argparse.ArgumentParser(description='CYCLOPEp ML')
parser.add_argument('-s', '--smile', help='Smile of the molecule',
                    action='store', type = str, default='O=C(N(C1=O)C)N(C2=C1N(C=N2)C)C')
parser.add_argument('-n', '--name', help='Name for the molecule',
                    action='store', type = str, default="caffeine")
args = parser.parse_args()
# =============================================================================

atom_color = {'C' : 'black', 'O' : 'red', 'N' : 'blue', 'H' : 'gray'}

def smi2xyz(smi : str, name : str):
    '''
    This function takes the smile of a molecule and creates an xyz file.

    Parameters
    ----------
    smi : str
        SMILE string of a molecule.
        
    name : str
        Name for the molecule

    Returns
    -------
    None.

    '''
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDG()
    params.randomSeed = 0  # or any fixed integer
    AllChem.EmbedMolecule(mol, params)
    # AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)
    Chem.rdmolfiles.MolToXYZFile(mol, f'{name}.xyz')
    return mol

mol = smi2xyz(args.smile, args.name)

params_to_change = {'add_hs' : True}
config = gm.MoleculeGraphConfig(**params_to_change) # Initializ MoleculeGraphConfig object to control configuration of graph
# print(config.dict())
# sys.exit()
graph = gm.construct_graph(smiles=args.smile, config=config)
nodes = graph.nodes
new_nodes = [node.split(':')[0] for node in nodes]
colors = [atom_color[atom] for atom in new_nodes]
new_nodes = [new_nodes[i] + f'{i+1}' for i in range(len(nodes))]
mapping = dict(zip(nodes,new_nodes))
graph = nx.relabel_nodes(graph, mapping)

conf = mol.GetConformer()
positions = {new_nodes[i] : [conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y]
             for i in range(len(new_nodes))}
print(positions)
positions['H22'][0] += 0.25
positions['H22'][1] += 0.7

positions['H15'][0] -= 0.45
positions['H15'][1] -= 0.4

positions['H19'][0] += 0.7
positions['H19'][1] -= 0.35

positions['H21'][1] -= 0.4

nx.draw(graph, pos = positions, with_labels = True, node_size = 600, width = 2,
        node_color = colors, font_color = 'white', edgecolors = 'black')
# nx.draw_networkx_nodes(graph, pos = nx.spring_layout(graph), nodelist=Hs, node_color = 'black')
plt.savefig(f'graph_{args.name}.png', dpi = 300, transparent = True)
# print(graph.nodes)
sys.exit()
# graph.graph["rdmol"]
Draw.MolToFile(Chem.MolFromSmiles(args.smile), f'{args.name}.png', size = (600,600))

