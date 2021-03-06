import csv
import difflib
import logging
import time

from fuzzywuzzy import fuzz

# start the clock
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
logger.info('known names pairs: %s' % known_names)

ignore_tokens_file = './tokens_to_ignore.csv'
with open(ignore_tokens_file, mode='r') as input_file:
    reader = csv.reader(input_file, delimiter=';')
    ignore_tokens = {row[0] for row in reader if len(row) > 0}
logger.info('tokens to ignore: [%s]' % ignore_tokens)

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
original_entities = entities.copy()
for token in ['@', '(', ')', '[', ']', '.', '_', ',', '/', '-', ':']:
    entities = [entity.replace(token, ' ') for entity in entities]

entities = [entity.replace('  ', ' ') for entity in entities]
entities = [entity.strip() for entity in entities]
for token in ignore_tokens:
    entities = [entity.replace(token, '') for entity in entities]
entities = [' '.join(entity.split(' ')[:3]).strip() for entity in entities]
logger.info(entities)

near_match_count = 0
for le in entities:
    left_entity = le.lower()
    for re in entities:
        right_entity = re.lower()
        if left_entity != right_entity:
            how_similar = fuzz.ratio(left_entity, right_entity)
            if how_similar > 78:
                logger.info('%d [%s] [%s]' % (how_similar, le, re))
                near_match_count += 1
            if how_similar > 93:
                # https://stackoverflow.com/questions/17904097/python-difference-between-two-strings
                for index, substring in enumerate(difflib.ndiff(left_entity, right_entity)):
                    if substring[0] == ' ':
                        continue
                    elif substring[0] == '-':
                        logger.info(u'Delete "{}" from position {}'.format(substring[-1], index))
                    elif substring[0] == '+':
                        logger.info(u'Add "{}" to position {}'.format(substring[-1], index))
logger.info('we have %d unique entities and %d near matches.' % (len(entities), near_match_count))
elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
