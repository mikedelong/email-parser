# https://codehandbook.org/how-to-read-email-from-gmail-using-python/

import configparser
import email
import imaplib
import logging


def read_email_from_gmail(arg_smtp_server, arg_from_email, arg_from_pwd, arg_logger, arg_mailbox):
    try:
        mail = imaplib.IMAP4_SSL(host=arg_smtp_server, port=993)
        mail.login(arg_from_email, arg_from_pwd)
        mail.select(arg_mailbox)

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


# get configuration from config file
config = configparser.ConfigParser()
config.read('config.ini')

# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

logger.debug(config)

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = config['DEFAULT']['username'] + ORG_EMAIL
FROM_PWD = config['DEFAULT']['password']
SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993

if True:
    read_email_from_gmail(SMTP_SERVER, FROM_EMAIL, FROM_PWD, logger, 'inbox')

logger.debug('finished')
