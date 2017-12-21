import logging
import time

import win32com.client

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


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# "6" refers to the index of a folder - in this case, the inbox.
folder_index = 6
inbox = outlook.GetDefaultFolder(folder_index)
messages = inbox.Items

for message in messages:
    try:
        subject = message.Subject
        date = message.SentOn
        logger.info('%s %s' % (subject, date))
    except AttributeError as attributeError:
        logger.warning(attributeError)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
