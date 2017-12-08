import matplotlib.pyplot as plt
import networkx as nx

options_2 = {
 'with_labels': False,
 'node_color': 'grey',
 'node_size': 10,
 'linewidths': 0,
 'width': 0.1,
}

graph = nx.barabasi_albert_graph(100, 3)
# nx.draw_circular(G, **options_2)

nx.draw_circular(graph, node_size = 10)

plt.show()