import logging
import time
import win32com.client
import os
import pandas

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

# use the local directory
dir_path = os.path.dirname(os.path.realpath(__file__))
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

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


        except AttributeError as attributeError:
            logger.warning(attributeError)
        except Exception as this_exception:
            logger.warning(this_exception)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
