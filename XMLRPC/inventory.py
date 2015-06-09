#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os
import sys
import xmlrpclib
import csv
import ConfigParser

# Function: *******************************************************************
def Prepare(valore):  
    # For problems: input win output ubuntu; trim extra spaces
    #valore=valore.decode('ISO-8859-1')
    valore=valore.decode('cp1252')
    valore=valore.encode('utf-8')
    return valore.strip()

def PrepareDate(valore):
    if valore: # TODO test correct date format
       return valore
    else:
       return time.strftime("%d/%m/%Y")

def PrepareFloat(valore):
    valore=valore.strip() 
    if valore: # TODO test correct date format       
       return float(valore.replace(",","."))
    else:
       return 0.0   # for empty values

# Start main code *************************************************************
if len(sys.argv) != 2 :
   print """
         *** Syntax Error! ***
         *  Use the command with this syntax: python ./articoli_ETL.py nome_file.csv 
         *********************
         """ 
   sys.exit()

cfg_file = os.path.join(os.path.expanduser("~"), "openerp.cfg")

# Set up parameters (for connection to Open ERP Database) *********************
config = ConfigParser.ConfigParser()
config.read([cfg_file]) # if file is in home dir add also: , os.path.expanduser('~/.openerp.cfg')])
dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint
separator = config.get('dbaccess', 'separator') # test
inventory_id = 2 # TODO change

# XMLRPC connection for autentication (UID) and proxy 
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

FileInput = sys.argv[1]

lines = csv.reader(open(FileInput, 'rb'), delimiter=separator)

counter = 0
#import pdb; pdb.set_trace()
for line in lines:
    if len(line): # jump empty lines
       counter += 1 
       ref = Prepare(line[0])
       qty = PrepareFloat(line[1])

       product_id = sock.execute( # search current ref
           dbname, uid, pwd, 'product.product', 'search', [
               ('default_code', '=', ref)])
       if not product_id:
           print counter, ". [ERROR]Product code not found:", ref        
           continue
       
       line_id = sock.execute( # search current ref
           dbname, uid, pwd, 'stock.inventory.line', 'search', [
               ('product_id', '=', product_id[0]),
               ('inventory_id', '=', inventory_id)
               ])
       if not line_id:
           print counter, ". [ERROR] Line not found in inventory:", ref        
           continue
       
       # Update line:        
       sock.execute( 
           dbname, 
           uid, 
           pwd, 
           'stock.inventory.line', 
           'write', 
           line_id[0],
           {'product_qty': qty, }
           )
       print counter, ". [INFO] Line updated", ref, qty    

