import logging
import os
import time

import networkx as nx
import plotly.offline as offline
import win32com.client
from plotly.graph_objs import Data
from plotly.graph_objs import Figure
from plotly.graph_objs import Layout
from plotly.graph_objs import Line
from plotly.graph_objs import Marker
from plotly.graph_objs import Scatter
from plotly.graph_objs import XAxis
from plotly.graph_objs import YAxis

start_time = time.time()

# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

# use the messages subfolder of the local directory
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path + '\\messages\\'
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

records = list()
for file_name in os.listdir(dir_path):
    if file_name.endswith(".msg"):

        current_file = os.path.join(dir_path, file_name)
        logger.debug(current_file)
        try:
            message = outlook.OpenSharedItem(current_file)
            record = (message.SenderName, message.SenderEmailAddress, message.SentOn, message.To,
                      message.CC, message.BCC, message.Subject, message.Body)
            logger.debug('sender name: %s', record[0])
            logger.debug('sender address: %s', record[1])
            logger.debug('sent on: %s ', record[2])
            logger.debug('sent to: %s', record[3])
            logger.debug('CC: %s', record[4])
            logger.debug('BCC: %s', record[5])
            logger.debug('Subject: %s', record[6])
            logger.debug('Body: %s', record[7])
            records.append(record)
        except AttributeError as attributeError:
            logger.warning(attributeError)
        except Exception as this_exception:
            logger.warning(this_exception)

# build a graph out of the records array
G = nx.Graph()
for record in records:
    recipients = [item.strip() for item in ';'.join([record[3], record[4]]).split(';')]
    for recipient in recipients:
        if record[0] not in G:
            G.add_node(record[0])
        if recipient not in G:
            G.add_node(recipient)
        G.add_edge(record[0], recipient)
        logger.debug('%s %s' % (record[0], recipient))

pos = nx.spring_layout(G)
nx.set_node_attributes(G, 'pos', pos)

logger.debug(G.nodes())

edge_trace = Scatter(hoverinfo='none', line=Line(width=0.5, color='#888'), mode='lines', x=[], y=[])

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                     marker=Marker(
                         showscale=True,
                         # colorscale options
                         # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                         # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                         colorscale='YIGnBu', reversescale=True, color=[], size=10,
                         colorbar=dict(thickness=15, title='Node Connections', xanchor='left',
                                       titleside='right'),
                         line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

markers_are_names = True
markers_are_counts = False
if markers_are_counts:
    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# of connections: ' + str(len(adjacencies))
        node_trace['text'].append(node_info)
elif markers_are_names:
    nodes = G.nodes()
    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = nodes[node]
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

offline.plot(fig, filename='networkx.html')

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
