import matplotlib.pyplot as plt
import networkx as nx

import networkx as nx
import plotly.offline as offline
from plotly.graph_objs import Data
from plotly.graph_objs import Figure
from plotly.graph_objs import Layout
from plotly.graph_objs import Line
from plotly.graph_objs import Marker
from plotly.graph_objs import Scatter
from plotly.graph_objs import XAxis
from plotly.graph_objs import YAxis

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
nx.set_node_attributes(graph, 'pos', layout)

edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in graph.edges():
    x0, y0 = graph.node[edge[0]]['pos']
    x1, y1 = graph.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in graph.nodes():
    x, y = graph.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for node, adjacencies in enumerate(graph.adjacency_list()):
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = '# of connections: ' + str(len(adjacencies))
    node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                 title='<br>Network graph made with Python',
                 titlefont=dict(size=16),
                 showlegend=False,
                 hovermode='closest',
                 margin=dict(b=20, l=5, r=5, t=40),

                 # annotations=[dict(
                 #     text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                 #     showarrow=False,
                 #     xref="paper", yref="paper",
                 #     x=0.005, y=-0.002)],
                 xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                 yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig, filename='barabasi.html')
