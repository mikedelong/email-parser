# import pyzmail

import logging
import time
# import sys
import win32com.client
import os

# http://mypy.pythonblogs.com/12_mypy/archive/1253_workaround_for_python_bug_ascii_codec_cant_encode_character_uxa0_in_position_111_ordinal_not_in_range128.html
# reload(sys)
# sys.setdefaultencoding("utf8")

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

current_file = '.\example.msg'
# with open(current_file, 'rb') as fp:
#     message = pyzmail.message_from_file(fp)

dir_path = os.path.dirname(os.path.realpath(__file__))
logger.debug(dir_path)

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg = outlook.OpenSharedItem(dir_path + r"/example.msg")

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
