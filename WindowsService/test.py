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

sock = xmlrpclib.ServerProxy(
    'http://localhost:7000/RPC2', allow_none=True)

print sock
print sock.execute('ping')
sock.remote_shutdown()
print 'Wait 1 sec...'
time.sleep(1)
try:
    print sock.execute('ping')
except:    
    print 'Server is down'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
