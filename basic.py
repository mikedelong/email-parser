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
    logger.debug('sender : ' + message.SenderName)
except Exception as this_exception:
    logger.warning(this_exception)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
