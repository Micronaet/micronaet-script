#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import ConfigParser
from os.path import isfile, join
from datetime import datetime, timedelta


# -----------------------------------------------------------------------------
#                                   Parameters:
# -----------------------------------------------------------------------------
# Config file:
cfg_file = "openerp.cfg" # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

try:
    company = sys.argv[1]
except:
    company = "SDX" # default company

# Constant:
DATETIME_FORMAT = "%Y%m%d_%H%M%S"
DATETIME_FORMAT_LOG = "%Y/%m/%d %H:%M:%S"

# From / to position of invoice number:
from_char = config.get(company, 'split_from_char')
to_char = config.get(company, 'split_to_char')

# file to log:
log_file = config.get(company, 'split_log')

# file to split:
input_file = config.get(company, 'split_file_in')

# folder to save splitted file:
output_folder = config.get(company, 'split_out')

# folder where save input_file after elaboration:
history_folder = config.get(company, 'split_history')

# Output file:
invoice_mask = config.get(company, 'split_mask')  # Mask file:

# -----------------------------------------------------------------------------
#                                  Utility:
# -----------------------------------------------------------------------------
log_file = open(log_file, 'w')
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
log_event("Start splitting on file: %s" % input_file)
old_invoice = False # for break file
try:
    in_file = open(input_file, 'r')
    i = 0
    for line in in_file:
        # Jump empty lines:
        if not line:
            log_event("Empty line [%s] (jumped)" % i, 'warning')
            continue
            
        # Read invoice number:    
        invoice = invoice_mask % int(line[from_char:to_char].strip()) # Read # invoice 
                
        # ---------------------------------------------------------------------
        #                            First time:
        # ---------------------------------------------------------------------
        if not old_invoice: 
            old_invoice = invoice
            out_file = new_file(invoice)
            i = 0
            
        # ---------------------------------------------------------------------
        #                            Break time:
        # ---------------------------------------------------------------------
        if old_invoice != invoice: 
            out_file.close()
            old_invoice = invoice                     
            log_event("Line write on file = %s" % i)
            out_file = new_file(invoice)
            i = 0
            
        i += 1            
        out_file.write(line)
    else:        
        log_event("Line write on file = %s" % i)

        # Close file:
        out_file.close()         
        in_file.close()
        
        # History:
        history_filename = join(
            history_folder, 
            datetime.now().strftime(DATETIME_FORMAT),
            )

        os.rename(input_file, history_filename, )
        log_event("Historized file: %s" % history_filename)
        
        # Log:
        log_event("End splitting\n")
        log_file.close()
except:
    log_event("Error splitting: %s\n" % (sys.exc_info(), ), 'error')
    sys.exit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

