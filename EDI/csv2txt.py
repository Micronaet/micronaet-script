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

import sys
import os
import ConfigParser
from os.path import isfile, join, expanduser
from os import listdir
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
#                                   Parameters:
# -----------------------------------------------------------------------------
# Config file:
cfg_file = "openerp.cfg" # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

company = "SAR" # default company is SAR

# From / to position of order number: (not used)
#from_char = config.get(company, 'split_from_char')
#to_char = config.get(company, 'split_to_char')

cr = eval(config.get('general', 'return'))

# Char to split csv file:
split_char = config.get(company, 'split_char')

# file to log:
log_file = os.path.expanduser(config.get(company, 'log_file_name'))

# Folder with file to split:
input_folder = os.path.expanduser(config.get(company, 'path_csv'))
output_folder = os.path.expanduser(config.get(company, 'path_in')) # in for imp

# folder where save input_file after elaboration:
history_folder = os.path.expanduser(config.get(company, 'path_history'))

# Output file:
field_type = config.get(company, 'split_field_type').replace("(", "%(")  # Mask file:
max_element = eval(config.get(company, 'split_max_cols'))

# -----------------------------------------------------------------------------
#                                  Utility:
# -----------------------------------------------------------------------------
# Constant (for log):
DATETIME_FORMAT = "%Y%m%d_%H%M%S"
DATETIME_FORMAT_LOG = "%Y/%m/%d %H:%M:%S"

def log_event(comment, log_type='info'):
    ''' Log on file the operations
    '''
    log_file.write("[%s] %s >> %s\n" % (
        log_type,
        datetime.now().strftime(DATETIME_FORMAT_LOG),
        comment, 
        ))
    return True    

def new_file(invoice):
    ''' Operation for get new file:
    '''
    out_filename = join(output_folder, invoice)
    log_event("Output on file: %s" % out_filename)
    return open(out_filename, 'w') 
    
# -----------------------------------------------------------------------------
#                                  Start procedure:
# -----------------------------------------------------------------------------
log_file = open(log_file, 'w')
# Create mask:
order_mask = ""
i = 0
end_col = "" # TODO parametrize (used for debug)

fields = {}
for item in field_type.split('|'):
    t = item[:1].lower()
    fields[i] = item # save for trunk operations
    if t == "s": # string
        if fields[i][1:2] == ">":
           start = 2
           sign= ""
        elif fields[i][1:2] == ("<"):
           start = 2
           sign= "-"
        else: # left align
           start = 1    
           sign= "-"

        order_mask += "%s(%s)%s%ss%s" % ("%", i, sign, item[start:], end_col)
    elif t == "f": # fload
        order_mask += "%s(%s)%sf%s" % ("%", i, item[1:], end_col)
    elif t == "x": # jump line
        pass # Jump field
    else:
        log_event(
            'Field format error, start with %s (correct: X, F, S)' % f, 
            'error')
    i += 1
order_mask += cr

split_count = 0
previous_order = False
date_part = datetime.now().strftime("%Y%m%d")

for file_name in [
        f for f in listdir(input_folder) if isfile(
            join(input_folder, f))]:
    try:
        error = "Error file not exist"
        input_file = expanduser(join(input_folder, file_name)) 
        
        log_event("Start converting: %s" % input_file)

        # Input file:
        in_file = open(input_file, 'r')
        
        error = "Error converting elements"
        i = 0
        for line in in_file:
            i += 1 
            line = line.strip() # remove extra space
            line = line.replace("°", ".") # Problem with symbol
            if not line: # Jump empty lines:
                #log_event("Empty line [%s] (jumped)" % i, 'warning')
                continue
            line = line.split(split_char) # convert in list
            
            if len(line) != max_element:
                log_event("File %s Column error %s instead of %s (jumped)" % (
                    input_file,
                    len(line),
                    max_element,
                    ), 'error')                
                break # TODO test jump file!!!    

            order_ref = line[1]                
            # Split file if necessary:
            if not previous_order or previous_order != order_ref:
                previous_order = order_ref
                try:
                    out_file.close()
                except:
                    pass # no error if file is not present
                # order ref is name
                output_file = expanduser(join(
                    output_folder, "%s_%s.asc" % (date_part, order_ref)))
                out_file = open(output_file, 'w')
                log_event("New output file: %s" % output_file)

            dict_line = {}            
            j = 0
            for item in line:            
                t = fields[j][:1].lower()
                if t == "s": # trunk at char
                    dict_line[str(j)] = item[:int(fields[j][1:])] 
                elif t == "f":
                    dict_line[str(j)] = float(item.replace(",", "."))
                j += 1
            
            # Formatting and writingstring:        
            out_file.write(order_mask % dict_line)

        # Close file:
        out_file.close()         
        in_file.close()
            
        # History current converted file:
        history_filename = join(
            history_folder, 
            "%s_%s" % (
                datetime.now().strftime(DATETIME_FORMAT),
                file_name,
                ),
            )
        os.rename(input_file, history_filename)
        log_event("Historized file: %s > %s" % (
            input_file,
            history_filename, ))
    except:
        log_event("Error converting: %s [%s]\n" % (
            error, 
            sys.exc_info(), 
            ), 'error')
            
log_event("End converting\n")
log_file.close()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
