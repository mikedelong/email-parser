# https://plot.ly/python/network-graphs/

# import plotly.plotly as py
# from plotly.graph_objs import *

import networkx as nx

G = nx.random_geometric_graph(200, 0.125)
pos = nx.get_node_attributes(G, 'pos')

dmin = 1
ncenter = 0
for n in pos:
    x, y = pos[n]
    d = (x - 0.5) ** 2 + (y - 0.5) ** 2
    if d < dmin:
        ncenter = n
        dmin = d

p = nx.single_source_shortest_path_length(G, ncenter)
