import logging
import time

import pythoncom
import win32com.client
import email.generator
import email.policy

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
# https://stackoverflow.com/questions/31619012/extract-senders-email-address-from-outlook-exchange-in-python-using-win32
# todo figure out how to write email messages to a file with all headers
for message in messages:
    try:
        subject = message.Subject
        date = message.SentOn
        sender_address = message.Sender.GetExchangeUser().PrimarySmtpAddress if message.SenderEmailType == 'EX' else \
            message.SenderEmailAddress
        logger.info('%s %s %s' % (subject, date, sender_address))
        filename = './messages/{}.msg'.format(count)
        message.SaveAs(filename)

        count += 1
    except AttributeError as attributeError:
        logger.warning(attributeError)
    except pythoncom.com_error as comError:
        logger.warning(comError)
        logger.warning(vars(comError))
        logger.warning(comError.args)
        hr, msg, exc, arg = comError.args
        logger.warning(comError)
    except Exception as error:
        logger.warning(error)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
