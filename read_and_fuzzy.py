import csv
import logging
import time

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

import fuzzywuzzy

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
    known_names = {row[0]: row[1] for row in reader}
logger.info(known_names)

records_file = './records.csv'

with open(records_file, 'r', encoding='utf-8') as input_file:
    records = input_file.readlines()
# strip off trailing newlines as appropriate
records = [item.strip() for item in records]


elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
