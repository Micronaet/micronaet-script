import imaplib
import sys

#copy from
f_server = 'imap.gmail.com'
f_username = 'f1@gmail.com'
f_password = 'pwd'
f_box_name = 'Inbox'

#copy to
t_server = 'imap.gmail.com'
t_username = 'f2@gmail.com'
t_password = 'pwd'
t_box_name = 'Sent'

To = imaplib.IMAP4_SSL(t_server) 
To.login(t_username, t_password)
print 'Logged into mail server'

From = imaplib.IMAP4_SSL(t_server)
From.login(t_username, t_password)
print 'Logged into archive'

From.select(f_box_name)  #open box which will have its contents copied
print 'Fetching messages...'
typ, data = From.search(None, 'ALL')  #get all messages in the box
msgs = data[0].split()

sys.stdout.write(" ".join(['Copying', str(len(msgs)), 'messages']))

for num in msgs: #iterate over each messages id number
    typ, data = From.fetch(num, '(RFC822)')
    sys.stdout.write('.')
    To.append(t_box_name, None, None, data[0][1]) #add a copy of the message to the archive box specified above
    From.expunge() # delete marked
    

'''
import imaplib

#copy from
from_server = {
    'server': '1.1.1.1',
    'username': 'j@example.com',
    'password': 'pass',
    'box_names': ['Sent', 'Sent Messages']}

#copy to
to_server = {
    'server': '2.2.2.2',
    'username': 'archive',
    'password': 'password',
    'box_name': 'Sent'}

def connect_server(server):
    conn = imaplib.IMAP4_SSL(server['server']) 
    conn.login(server['username'], server['password'])
    print 'Logged into mail server @ %s' % server['server']
    return conn

def disconnect_server(server_conn):
    out = server_conn.logout()

if __name__ == '__main__':
    From = connect_server(from_server)
    To = connect_server(to_server)

    for box in from_server['box_names']:
        box_select = From.select(box, readonly = False)  #open box which will have its contents copied
        print 'Fetching messages from \'%s\'...' % box
        resp, items = From.search(None, 'ALL')  #get all messages in the box
        msg_nums = items[0].split()
        print '%s messages to archive' % len(msg_nums)

        for msg_num in msg_nums:
            resp, data = From.fetch(msg_num, "(FLAGS INTERNALDATE BODY.PEEK[])") # get email
            message = data[0][1] 
            flags = imaplib.ParseFlags(data[0][0]) # get flags
            flag_str = " ".join(flags)
            date = imaplib.Time2Internaldate(imaplib.Internaldate2tuple(data[0][0])) #get date
            copy_result = To.append(to_server['box_name'], flag_str, date, message) # copy to archive

            if copy_result[0] == 'OK': 
                del_msg = From.store(msg_num, '+FLAGS', '\\Deleted') # mark for deletion

        ex = From.expunge() # delete marked
        print 'expunge status: %s' % ex[0]
        if not ex[1][0]: # result can be ['OK', [None]] if no messages need to be deleted
            print 'expunge count: 0'
        else:
            print 'expunge count: %s' % len(ex[1])

    disconnect_server(From)
    disconnect_server(To)
'''
