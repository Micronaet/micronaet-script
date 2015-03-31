#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import os
import sys

#error = []
converter = {}
converter_chg = {}
for f in ('1.log', '2.log'):
    file_input = os.path.expanduser(os.path.join(".", f))
    f_in = open(file_input, 'r')
    continue_next = False
    i = 0
    for row in f_in:
        i += 1
        if continue_next:
            continue_next = False            
            items = row.split(',')
            if len(items) != 3 or not filename:
                continue        
            
            #order_supplier = items[1].replace("'", "").strip() 
            order_company = items[2].replace("]", "").replace("'", "").strip()
            if order_company in converter:
                if order_company in converter_chg:
                    print "Error, multi-importation order:", filename, row
                else:    
                    converter_chg[order_company] = filename
            else:
                converter[order_company] = filename
            filename = False

        if 'Divisione file:' in row:
            filename = row.split('>')[-1].strip()
            continue_next = True
    f_in.close()  
    
# Read file from Mexal:
orders = {}
for line in open(mexal_file, 'r'):
    # Parse line:
    line = line.split(";")
    ddt = line[0].strip()
    article = line[1].strip()
    order = line[2].strip()
    counter = line[3].strip()

    if order not in orders:
        orders[order] = {}
    
    orders[order][article] = (ddt, counter)

order_file = {}
for order in orders:
    if order in converter:
       print "Error order not found in file:", order
       continue

    # Check if file exist:    
    filename = os.path.join(".", "history", order[0])
    if not os.path.isfile(filename):
        print filename, "non esiste"
        
    order_file[order] = {}
    for row in open(filename, 'r'):    
        article = row[2356:2391].strip()
        info = row[2356:2391].strip() # TODO 
    
        order_file[order][article] = info

result = open("result.csv", "w")
for order in orders: # mexal order imported
    for article in orders[order]:
        if article in order_file[order]:
            print order_file[order][article]
            #result.write
        else: # Articolo non trovato
            print article, "non trovato nell'ordine", order
 
