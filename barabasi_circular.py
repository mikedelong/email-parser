import matplotlib.pyplot as plt
import networkx as nx

options_2 = {
 'with_labels': False,
 'node_color': 'grey',
 'node_size': 10,
 'linewidths': 0,
 'width': 0.1,
}

node_count = 10
graph = nx.barabasi_albert_graph(node_count, 3)

layout = nx.circular_layout(graph)
nx.draw(graph, layout, node_size = 10)

plt.show()