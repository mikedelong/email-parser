import logging
import time
import win32com.client
import os

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


dir_path = os.path.dirname(os.path.realpath(__file__))
current_file = dir_path + r"/example.msg"

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
try:
    message = outlook.OpenSharedItem(current_file)
    logger.debug('sender name: %s' , message.SenderName)
    logger.debug('sender address: %s' , message.SenderEmailAddress)
    logger.debug('sent on: %s ', message.SentOn)
    logger.debug('sent to: %s', message.To)
    logger.debug('CC: %s', message.CC)
    logger.debug('BCC: %s', message.BCC)
    logger.debug('Subject: %s', message.Subject)

    # msg.Body

except AttributeError as attributeError:
    logger.warning(attributeError)
except Exception as this_exception:
    logger.warning(this_exception)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
