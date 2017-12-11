# https://stackoverflow.com/questions/5077625/reading-e-mails-from-outlook-with-python-through-mapi

import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# "6" refers to the index of a folder - in this case,
# the inbox. You can change that number to reference
# any other folder
folder_index = 6
inbox = outlook.GetDefaultFolder(folder_index)
messages = inbox.Items
for message in messages:
    print(message.sendername)

print('We have %d messages in all.' % len(messages))
