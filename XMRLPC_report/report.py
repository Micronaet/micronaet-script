#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import xmlrpclib
import ConfigParser
import time
import base64

cfg_file = os.path.join(os.path.expanduser('openerp.cfg'))
   
# Set up parameters (for connection to Open ERP Database) *********************
config = ConfigParser.ConfigParser()
config.read([cfg_file]) # if file is in home dir add also: , os.path.expanduser('~/.openerp.cfg')])
dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint

# XMLRPC connection for autentication (UID) and proxy 
import pdb; pdb.set_trace()
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)

#sock = xmlrpclib.ServerProxy(
#    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)
    
sock_report = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/report' % (server, port), allow_none=True)

ids = 1
model = 'sale.order'
# 'report.webkitstatus'
report_id = 518
"""sock_report.report(
    dbname, uid, pwd, model, ids, {
        'model': model, 
        'id': [ids],
        'report_type': 'webkit',
        'data': {},
        })"""

#time.sleep(5)
state = False
attempt = 0

while not state:
    report = sock.report_get(dbname, uid, pwd, report_id)
    state = report['state']
    if not state:
        time.sleep(1)
    attempt += 1
    if attempt > 200:
        print 'Printing aborted, too long delay !'

    string_pdf = base64.decodestring(report['result'])
    file_pdf = open('/tmp/file.pdf','w')
    file_pdf.write(string_pdf)
    file_pdf.close()
"""
item = sock.execute( # search current ref
   dbname, uid, pwd, 'product.product', 'search', [
       ('default_code', '=', ref)])

name = "[%s] %s" % (ref[0:6].replace(' ', ''), name)
 

if item: # update
   try:
       modify_id = sock.execute(
           dbname, uid, pwd, 'product.product', 'write', 
           item, data)
       product_id = item[0]
   except:
       print "[ERROR] Modify product, current record:", data
   print "[INFO]", counter, "Already exist: ", ref, name
else: # create
   if not active:
       print "[WARN]", counter, "Not active, jumped: ", ref, name
       continue # no recreate if not active
       
   try:
       product_id = sock.execute(
           dbname, uid, pwd, 'product.product', 'create', data) 
   except:
       print "[ERROR] Create product, current record:", data
   print "[INFO]", counter, "Insert: ", ref, name
"""
