# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import re
from os import listdir
from os.path import isfile, join
from email.parser import Parser

# Parameter:
#folder_path = '/home/anna/Scrivania/Mail/mail'
folder_path = '/home/anna/Scrivania/Mail/mail'

mail_sent = []
for address in open('/home/anna/Scrivania/Mail/mail.csv', 'r'):
    mail_sent.append(address.strip().replace('\t', ''))
    
# Function:
def clean(all_mail):
    ''' Remove not necessary mail
    '''
    res = []
    for email in all_mail:
        if email in mail_sent and email not in res:
            res.append(email)       
    return res        

for mail_file in [f for f in listdir(folder_path)]:
    mail_fullfile = join(folder_path, mail_file)
    message = Parser().parse(open(mail_fullfile, 'r'))
    state = 'Not delivered'
    
    # Extract list of mail:
    all_mail = clean(re.findall(r'[\w\.-]+@[\w\.-]+', message.as_string()))

    # Extract mail description:    
    mail = message['from']
    try:
        mail_description = mail.split('"')[1]
    except:
        mail_description = mail
    
    # Extract mail:    
    try:    
       mail_address = mail.split("<")[1].split(">")[0]
    except:
       mail_address = mail
    subject = message['subject'].replace('\n','').replace('\r','')

    # Check if is our SMTP server (so delay)       
    if 'Recapito ritardato' in subject or 'Delayed' in subject:
        state = 'Delayed' 

    #  Now the header items can be accessed as a dictionary:
    print 'Sate: %s| File: %s| To: %s| From: ("%s" <%s>)| Mails: %s|Subject: %s' % (
        state,
        mail_file,
        message['to'],
        mail_description,
        mail_address,
        all_mail,
        subject,
        )
