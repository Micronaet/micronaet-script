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
from Tkinter import *

try:
    # -------------------------------------------------------------------------
    # Command parameters:
    # -------------------------------------------------------------------------
    hostname = sys.argv[1]
    port = sys.argv[2]
    launch_command = sys.argv[3]
except:
    # Open window message:    
    root = Tk()
    frame = Frame(root)
    frame.pack()
    label = Label(frame, text='''
        [INFO] Launch syntax error, use:
            python ./RCP_call.py <IP RDP Server> <Port RDP Server> <command>
            
            ex.:   
            python ./RCP_call.py 192.168.1.100 7000 invoice
            ''')
    label.pack()
    quitButton = Button(frame, text="OK", command=frame.quit)
    quitButton.pack()
    root.mainloop()
    sys.exit()
    
try:
    # -------------------------------------------------------------------------
    # RDP Operation:
    # -------------------------------------------------------------------------
    sock = xmlrpclib.ServerProxy(
        'http://%s:%s/RPC2' % (hostname, port), allow_none=True)
    print '[INFO] %s' % sock.execute('batch', {'command': launch_command})
except:
    print '[ERROR] Server not reply'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
