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
from os.path import isfile, join
from datetime import datetime, timedelta
from utility import *

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

# Char to split csv file:
slit_char = config.get(company, 'split_char')

# file to log:
log_file = config.get(company, 'log_file_name')

# Folder with file to split:
input_folder = config.get(company, 'path_in')

# File converted:
output_file = config.get(company, 'split_file_out')

# folder where save input_file after elaboration:
history_folder = config.get(company, 'path_history')

# Output file:
order_mask = config.get(company, 'split_mask')  # Mask file:

jump_element = config.get(company, 'split_jump_cols')
max_element = config.get(company, 'split_max_cols')

# -----------------------------------------------------------------------------
#                                  Start procedure:
# -----------------------------------------------------------------------------
log_file = open(log_file, 'w')
import pdb; pdb.set_trace()
log_event("Start converting on file: %s" % input_file)
try:
    # TODO loop on folder: 
    # for file in input_folder
    input_file = "/home/thebrush/Scrivania/ordini.csv" # TODO
    in_file = open(input_file, 'r')
    i = 0
    for line in in_file:
        i += 1 
        if not line: # Jump empty lines:
            log_event("Empty line [%s] (jumped)" % i, 'warning')
            continue
        line = line.strip() # remove extra space
        line = line.split(slit_char) # convert in list

        if len(line) != max_element:
            log_event("Column error %s instead of %s (jumped)" % (
                len(line),
                max_element,
                ), 'error')
            continue
        dict_line = {}
        j = 0
        for item in line:            
            format_line[str(j)] = item
            j += 1
                
        # Formatting and writingstring:        
        out_file.write(order_mask % (dict_line,)

    # Close file:
    out_file.close()         
    in_file.close()
        
    # History current converted file:
    history_filename = join(
        history_folder, 
        datetime.now().strftime(DATETIME_FORMAT),
        )

    os.rename(input_file, history_filename, )
    log_event("Historized file: %s" % history_filename)
        
    # Log:
    log_event("End converting\n")
    log_file.close()
except:
    log_event("Error converting: %s\n" % (sys.exc_info(), ), 'error')
    sys.exit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

