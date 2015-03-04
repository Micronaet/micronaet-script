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

cfg_file = os.path.join(os.path.expanduser("~"), "etl", "Fiam", "openerp.cfg")
   
# Set up parameters (for connection to Open ERP Database) *********************
config = ConfigParser.ConfigParser()
config.read([cfg_file]) # if file is in home dir add also: , os.path.expanduser('~/.openerp.cfg')])
dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint
separator = config.get('dbaccess', 'separator') # test

# XMLRPC connection for autentication (UID) and proxy 
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

FileInput = sys.argv[1]

lines = csv.reader(open(FileInput, 'rb'), delimiter=separator)
counter = 0
try:
    for line in lines:
        if counter < 0:  # jump n lines of header 
           counter += 1
        else: 
            if len(line): # jump empty lines
               counter += 1 
               error = "Importing line" 
               ref = Prepare(line[0])
               name = Prepare(line[1]).title()
               uom = Prepare(line[2]).title()
               taxes_id = Prepare(line[3])
               ref2 = Prepare(line[4]) # TODO where put it?               
               linear_length = PrepareFloat(line[14])   # Lunghezza lineare
               volume = PrepareFloat(line[15])   # Volume M3
               weight = PrepareFloat(line[16])   # Peso (lordo?) TODO vedere se e' netto

               active = True

               item = sock.execute( # search current ref
                   dbname, uid, pwd, 'product.product', 'search', [
                       ('default_code', '=', ref)])

               name = "[%s] %s" % (ref[0:6].replace(' ', ''), name)
                 
               data = {
                   'active': active, # for GPB purpose
                   'name': name,
                   'default_code': ref,
                   'sale_ok': True,
                   'purchase_ok': True,
                   #'uom_id': uom_id,    
                   #'uom_po_id': uom_id, 
                   'type': 'product',    
                   'supply_method': 'produce',
                   #'standard_price': bug_start_value,
                   'list_price': 0.0,
                   'procure_method': 'make_to_order', 
                   'description_sale': name, # preserve original name (not code + name)<<<<<<<<<
                   #'name_template': name,    
                   #'description': description,
                   #'description_spurchase'
                   #'lst_price' 
                   #'seller_qty'   
                   }
 
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
               
except:
    print '>>> [ERROR] Error importing articles!'
    raise #Exception("Errore di importazione!") # Scrivo l'errore per debug

