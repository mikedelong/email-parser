import csv
import logging
import time

from fuzzywuzzy import fuzz

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

entities = set()
for record in records:
    items = record.split(';')
    for item in items:
        entities.add(item)

entities = list(entities)
logger.info(entities)
logger.info('we have %d unique entities.' % len(entities))

tokens = ['@', '(', ')', '.', '_', ',', '/', '-', ':']
for left_entity in entities:
    for token in tokens:
        left_entity = left_entity.replace(token, ' ')
    for right_entity in entities:
        for token in tokens:
            right_entity = right_entity.replace(token, ' ')
        if left_entity != right_entity:
            how_similar = fuzz.ratio(left_entity, right_entity)
            if how_similar > 90:
                logger.info('%f [%s] [%s]' % (how_similar, left_entity, right_entity))

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
