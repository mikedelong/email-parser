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

count = 0
for message in messages:
    try:
        subject = message.Subject
        date = message.SentOn
        sender_address = message.Sender.GetExchangeUser().PrimarySmtpAddress if message.SenderEmailType == 'EX' else \
            message.SenderEmailAddress
        logger.info('%s %s %s' % (subject, date, sender_address))
        count += 1
    except AttributeError as attributeError:
        logger.warning(attributeError)
    except Exception as error:
        logger.warning(error)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
