# Created by: Robin M. Givens
# Date: August 3, 2020

# Example of using the getPersonToGroupNetworkX method to draw the 
# person-to-group network using the Fruchterman-Reingold algorithm in Matplotlib
# through NetworkX, and getBinPersonToPersonNetworkX method to draw the
# person-to-person network with the same parameters.

# Example shows how naming the nodes in a particular way allows you to draw them
# with different styles.

from network import Network
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

files = ['test1.csv', 'test2.csv', 'test3.csv']


# colors chosen from https://htmlcolorcodes.com/ Color Picker
blue =   '#2471A3'
orange = '#CA6F1E'
darkG =  '#566573'
medG =   '#808B96'
lightG = '#ABB2B9'
red =    '#A93226'
yellow = '#F9E79F'
green =  '#7DCEA0'
vLight = '#EAECEE'



def drawPersonToGroup(files, seed=999999):
    net = Network(files).getPersonToGroupNetworkX()
    
    # separate out person sets, group sets
    set1 = []   # person set 1
    set2 = []   # person set 2
    set3 = []   # group set 1
    set4 = []   # group set 2
    
    for n in net:
        start = n[0]
        end = n[len(n)-1]
        
        if start in 'ABCDEFHI':
            set1.append(n)
        elif start in 'JKLMNOP':
            set2.append(n)
        elif start == 'G':
            if end == 'G':
                set1.append(n)
            elif end in '1357':
                set3.append(n)
            else:
                set4.append(n)
        
    # networkx.drawing.layout.spring_layout is Fruchterman-Reingold algorithm
    positions = nx.spring_layout(net, k=(7/24), seed=seed)    
    
    
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set2, node_size=50, linewidths=0.5, node_color = orange, edgecolors=darkG)
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set1, node_size=50, linewidths=0.5, node_color = blue, edgecolors=darkG)
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set3, node_size=50, node_shape = 's', linewidths=0.5, node_color=green, edgecolors=darkG)
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set4, node_size=50, node_shape = 's', linewidths=0.5, node_color=yellow, edgecolors=darkG)
    nx.draw_networkx_edges(net, pos=positions, edge_color=lightG, width=0.75)    
    
    
def drawPersonToPerson(files, seed=999999):
    net = Network(files).getBinPersonToPersonNetworkX()
    
    # separate out person sets
    set1 = []   # person set 1
    set2 = []   # person set 2 
    
    for n in net:
        start = n[0]
        if start in 'ABCDEFGHI':
            set1.append(n)
        else:
            set2.append(n)
        
    # networkx.drawing.layout.spring_layout is Fruchterman-Reingold algorithm
    positions = nx.spring_layout(net, k=(3/4), seed=seed)    
    
    
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set2, node_size=50, linewidths=0.5, node_color = orange, edgecolors=darkG)
    nx.draw_networkx_nodes(net, pos=positions, nodelist=set1, node_size=50, linewidths=0.5, node_color = blue, edgecolors=darkG)
    nx.draw_networkx_edges(net, pos=positions, edge_color=lightG, width=0.75) 
    
    
    
drawPersonToGroup(files)
#drawPersonToPerson(files)