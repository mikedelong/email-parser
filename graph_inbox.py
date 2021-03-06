import csv
import logging
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
logging_level = logging.INFO
logger.setLevel(logging_level)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging_level)
logger.debug('started')

known_names_file = './known_names.csv'
with open(known_names_file, mode='r') as input_file:
    reader = csv.reader(input_file, delimiter=';')
    known_names = {row[0]: row[1] for row in reader if len(row) > 0}
logger.info(known_names)

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# "6" refers to the index of a folder - in this case, the inbox.
folder_index = 6
inbox = outlook.GetDefaultFolder(folder_index)

# todo break this into a data-reading, offline-document section
# todo and a processing section
messages = inbox.Items
# build a graph out of the list of messages
records = list()

for message in messages:
    try:
        sender = message.sendername
        tos = message.to
        cc = message.cc
        recipients = [item.strip() for item in ';'.join([tos, cc]).split(';')]
        recipients = [item for item in recipients if len(item) > 0]
        record = ';'.join([sender] + recipients)
        records.append(record)
    except AttributeError as attributeError:
        logger.warning(attributeError)
    except Exception as error:
        logger.warning(error)

# before we go on let's write the records as ragged CSV
records_file = './records.csv'
with open(records_file, 'w', encoding='utf-8') as output_file:
    for record in records:
        output_file.write('%s\n' % record)

string_of_interest = 'xxx'
G = nx.Graph()
for record in records:
    items = record.split(';')
    sender = items[0]
    if sender in known_names.keys():
        canonical_name = known_names[sender]
        logger.debug('substituting %s for %s as sender' % (canonical_name, sender))
        sender = canonical_name
    recipients = items[1:]
    for recipient in recipients:
        if recipient in known_names.keys():
            canonical_name = known_names[recipient]
            logger.debug('substituting %s for %s as recipient' % (canonical_name, recipient))
            recipient = canonical_name
        if string_of_interest in sender.lower():
            logger.info(sender)
        if string_of_interest in recipient.lower():
            logger.info(recipient)
        if sender not in G:
            G.add_node(sender)
        if recipient not in G:
            G.add_node(recipient)
        G.add_edge(sender, recipient)
        logger.debug('sender: [%s] %d recipient: [%s] %d' % (sender, len(sender), recipient, len(recipient)))
    if len(items) == 1:
        logger.warning('singleton: %s' % sender)

# todo add an initial layout to get repeatable results
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
                         colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right'),
                         line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

markers_are_names = True
markers_are_counts = False
if markers_are_counts:
    for node, neighbors in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(neighbors))
        node_info = '# of connections: ' + str(len(neighbors))
        node_trace['text'].append(node_info)
elif markers_are_names:
    nodes = G.nodes()
    for node, neighbors in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(neighbors))
        node_info = nodes[node]
        node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(title='<br>Inbox network graph made with Python/Plotly', titlefont=dict(size=16),
                           showlegend=False, hovermode='closest', margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

offline.plot(fig, filename='networkx.html')

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
