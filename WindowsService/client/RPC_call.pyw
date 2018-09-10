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
try:
    from Tkinter import *
    graphic = True
except:
    graphic = False

def message_window(text):
    ''' Open Standard message for output
    '''
    if not graphic:
        print '[TEXT] %s' % text
        return

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
    hostname = sys.argv[1]
    port = sys.argv[2]
    launch_command = sys.argv[3]
except:
    text = '''
[INFO]
Sintassi errata, utilizzare:
python RCP_call.py <IP RDP Server> <Porta RDP Server> <comando>
ex.:   
python RCP_call.py 192.168.1.100 7000 invoice
'''
    print text
    message_window(text)
    sys.exit()
    
try:
    # -------------------------------------------------------------------------
    # RDP Operation:
    # -------------------------------------------------------------------------
    sock = xmlrpclib.ServerProxy(
        'http://%s:%s/RPC2' % (hostname, port), allow_none=True)
    reply = sock.execute('batch', {'command': launch_command})
    text = reply.get('comment', '???')
    print text
    if not reply.get('esit', False):
        message_window('[ERRORE]\n%s' % text)
    
except:
    text = '[ERRORE]\nNessuna risposta del server\nverificare il servizio!'
    print text
    message_window(text)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
