# https://codehandbook.org/how-to-read-email-from-gmail-using-python/


import email
import imaplib
import logging


# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

def read_email_from_gmail(arg_smtp_server, arg_from_email, arg_from_pwd, arg_logger):
    try:
        mail = imaplib.IMAP4_SSL(arg_smtp_server)
        mail.login(arg_from_email, arg_from_pwd)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    arg_logger.debug('From : ' + email_from)

                    arg_logger.debug('Subject : ' + email_subject)

    except Exception as e:
        arg_logger.warning(str(e))


# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

ORG_EMAIL = "@gmail.com"
# todo get this from a config file
FROM_EMAIL = "yourEmailAddress" + ORG_EMAIL
# todo get this from a config file
FROM_PWD = "yourPassword"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

read_email_from_gmail(SMTP_SERVER, FROM_EMAIL, FROM_PWD, logger)

logger.debug('finished')
