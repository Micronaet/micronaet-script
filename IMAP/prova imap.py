#!/usr/bin/python26

import imaplib

imap_host = 'imap.gmail.com'
imap_user = 'pradeep@gmail.com'
imap_pass = 'xXxxXxx'

## connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)

## login to server
imap.login(imap_user, imap_pass)

## get status for the mailbox (folder) INBOX
status, response = imap.status('INBOX', "(UNSEEN)")

print status

unreadcount = int(response[0].split()[2].strip(').,]'))
print unreadcount


## create a new sub-folder inside a folder
status, create_response = imap.create('Archives.July')

## list folders
status, folder_list = imap.list()

## list sub-folders
status, sub_folder_list = imap.list(directory='Social NW Mails')

## select a specific folder
status, data = imap.select('INBOX')

## search a folder, returns the matched message-ids in CSV
status, msg_ids = imap.search(None, '(SUBJECT "Your Monthly Statement")')

## fetching a message, first we'll see how to fetch just headers
## first arg is the message id, next are flags
status, msg_header = imap.fetch('1', '(BODY.PEEK[HEADER])')

## fecthing full message
status, msg_full = imap.fetch('1', '(RFC822)')

## moving/copying messages around folders
status, msg_ids = imap.copy(msg_ids, 'Archives.July')
status, msg_ids = imap.move(msg_ids, 'Unimportant')

## last but not the least, closing & logging out
imap.close()
imap.logout()



#http://en.wikipedia.org/wiki/Internet_Message_Access_Protocol#Advantages_over_POP
