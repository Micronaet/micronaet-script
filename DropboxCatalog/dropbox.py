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
import shutil
from config import (input_folders, dropbox_path, file_replace_char,
    folder_replace_char, product_part
    ) # Micronaet: configuration file
from datetime import datetime, timedelta

# Database elements:
product_db = {}
folder_db = {}
case_db = {} # Check product case different elements

# Check elements:
error = [] # Error database
warning = [] # Warning database
info = [] #Info database
log = [] # Log database
log_sym = [] # Log database for symlinks

# -----------------------------------------------------------------------------
#                                 UTILITY:
# -----------------------------------------------------------------------------
def clean_char(name, replace_char):
    ''' Clean name with replate list of elements
    '''
    for (find, replace) in replace_char:
        name = name.replace(find, replace)
    return name.strip() # Clean extra spaces

# -----------------------------------------------------------------------------
#                           READ ALL INPUT FOLDERS:
# -----------------------------------------------------------------------------
tot = 0
for (key, path, extension, walk) in input_folders:
    # XXX walk for now is not used
    
    path = os.path.expanduser(path)
    if key in folder_db:
        error.append('KEY not unique: %s jump folder %s' % (key, path))
        continue
    else:
        folder_db[key] = path

    for root, dirs, files in os.walk(path):
        for f in files:
            tot += 1    

            # -----------------------------------------------------------------
            # Check estension:
            # -----------------------------------------------------------------
            ext = (f.split('.')[-1]).upper()
            if extension and ext not in extension:
                log.append('%s. Estension %s not used: %s' % (i, ext, f))
                continue
            
            # -----------------------------------------------------------------
            # Generate product / folder name
            # -----------------------------------------------------------------
            product = f[:product_part]
            if product not in product_db:
                product_db[product] = {}                
            if key not in product_db[product]:
                product_db[product][key] = []
                
            # File to symlink:    
            product_db[product][key].append(f)    

            # -----------------------------------------------------------------
            # Check case problem:
            # -----------------------------------------------------------------
            product_upper = product.upper()
            if product_upper in case_db:
                if product != case_db[product_upper]:
                    error.append('Case error product %s now %s' % (
                        product, case_db[product_upper]))
            else:
                case_db[product_upper] = product                

            # Log insert:                
            log.append('File used %s [Key: %s]' % (f, key))

# -----------------------------------------------------------------------------
#                            CREATE SYMLINKS:
# -----------------------------------------------------------------------------
# Destination root folder:
dropbox_path = os.path.expanduser(dropbox_path)

# TODO write log file:
# Read all product and key elements:
tot = 0
import pdb; pdb.set_trace()
for product in product_db:
    for key in product_db[product]:
        # ---------------------------------------------------------------------
        # DESTINATION: Folder
        # ---------------------------------------------------------------------
        # 1. Generate name:        
        product_folder = os.path.join(
            dropbox_path, 
            clean_char(product, folder_replace_char), # change char
            )        
        
        # 2. Create if not present:
        if not demo:
            os.system('mkdir -p "%s"' % product_folder)
        
        for f in product_db[product][key]:
            tot += 1
            # ORIGIN: Filename:
            origin = os.path.join(
                folder_db[key], # Origin folder for that key
                f,
                )

            # DESTINATION: Filename
            name = clean_char(
                '%s_%s' % (key, f), # Filename for destination
                file_replace_char, # Replace list
                )

            destination = os.path.join(
                dropbox_path,
                product_folder, # Product folder
                name.strip(),
                )
            
            # Symlink operations:     
            if not demo:
                os.symlink(origin, destination)
            log_sym.append('origin: %s destination: %s' % (
                origin, destination)) 

print log_sym                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
