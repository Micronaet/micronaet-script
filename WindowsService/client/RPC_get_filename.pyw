#!/usr/bin/python
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
import os
import sys
import xmlrpclib
import time
import base64
from Tkinter import *

def message_window(text):
    ''' Open Standard message for output
    '''
    root = Tk()
    frame = Frame(root)
    frame.pack()
    label = Label(frame, text=text)
    label.pack()
    quitButton = Button(frame, text='OK', command=frame.quit)
    quitButton.pack()
    root.mainloop()
    
try:
    # -------------------------------------------------------------------------
    # Command parameters:
    # -------------------------------------------------------------------------
    text = '''
[INFO]
Sintassi errata, utilizzare:
python RCP_call.py <IP RDP Server> <Porta RDP Server> <server file> <client file>
ex.:   
python RCP_call.py 192.168.1.100 7000 c:\micronaet\server.xlsx c:\client\client.xlsx
'''
    hostname = sys.argv[1]
    port = sys.argv[2]
    filename = sys.argv[3]
    output = sys.argv[4]

    # -------------------------------------------------------------------------
    # RDP Operation:
    # -------------------------------------------------------------------------
    text = '[ERRORE]\nNessuna risposta del server\nverificare il servizio!'
    sock = xmlrpclib.ServerProxy(
        'http://%s:%s/RPC2' % (hostname, port), allow_none=True)
    reply = sock.execute('file', {'filename': filename})
    
    if not reply.get('esit', False):
        message_window('[ERRORE] Nessun file di ritorno dalla procedura')
        sys.exit()

    text = '[ERRORE] Non riesco a salvare il file in locale'
    f_bin = open(output, 'wb')
    import pdb; pdb.set_trace()
    binary = base64.decodestring(reply.get('file'))
    f_bin.write(binary)
    
    # XXX XLSX file will be opened from batch
    
except:
    print text
    message_window(text)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
