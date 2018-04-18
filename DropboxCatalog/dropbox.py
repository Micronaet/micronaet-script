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
#import erppeek
import xmlrpclib
import shutil
import parameters # Micronaet: configuration file
from datetime import datetime, timedelta


# -----------------------------------------------------------------------------
# Parameters:
# -----------------------------------------------------------------------------
# ODOO connection:
odoo_server = parameters.odoo_server
odoo_port = parameters.odoo_port
odoo_user = parameters.odoo_user
odoo_password = parameters.odoo_password
odoo_database = parameters.odoo_database

# Dropbox:
demo = parameters.demo
input_folders = parameters.input_folders
dropbox_path = parameters.dropbox_path
file_replace_char = parameters.file_replace_char
folder_replace_char = parameters.folder_replace_char
product_part = parameters.product_part
parent_part = parameters.parent_part
no_family_name = parameters.no_family_name

print '''
Setup parameters: 
    ODOO: Connection: %s:%s DB %s utente: %s
    Demo: %s
    Input folders: %s
    Dropbox path: %s
    File replace char: %s
    Folder replace char: %s
    Product part: %s    
    ''' % (
        odoo_server, 
        odoo_port, 
        odoo_database, 
        odoo_user,
        
        demo,
        input_folders,
        dropbox_path,
        file_replace_char,
        folder_replace_char,
        product_part,        
        )

# Database elements:
product_db = {}
folder_db = {}
family_db = {}
parent_char = [] # len of parent in family list
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
def clean_ascii(name):
    ''' Replace not ascii char
    '''
    res = ''
    for c in name:
        if ord(c) < 127:
            res += c
        else:
            res += '_'
    return res

def clean_char(name, replace_char):
    ''' Clean name with replate list of elements
    '''
    for (find, replace) in replace_char:
        name = name.replace(find, replace)
    return name.strip() # Clean extra spaces

# -----------------------------------------------------------------------------
#                           ODOO operation:
# -----------------------------------------------------------------------------
# Connect with ODOO
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (odoo_server, odoo_port))
uid = sock.login(odoo_database, odoo_user, odoo_password)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (odoo_server, odoo_port))

family_ids = sock.execute(
    odoo_database, uid, odoo_password, 
    'product.template', 'search', [
        ('is_family', '=', True),
        ]) 

for family in sock.execute(odoo_database, uid, odoo_password, 
        'product.template', 'read', family_ids, [
            'name', 'family_list', 'dropbox']):
    family_name = clean_ascii(family['dropbox'] or family['name'])
    for parent in family['family_list'].split('|'):
        family_db[parent] = family_name
        if len(parent) not in parent_char:
            parent_char.append(len(parent))

#odoo = erppeek.Client(
#    'http://%s:%s' % (
#        odoo_server, odoo_port), 
#    db=odoo_database,
#    user=odoo_user,
#    password=odoo_password,
#    )
    
# Read family database
#family_pool = odoo.model('product.template')
#family_ids = family_pool.search([
#    ('is_family', '=', True),
#    ])
#for family in family_pool.browse(family_ids):
#    for parent in family.family_list.split('|'):
#        family_db[parent] = family.name
#        if len(parent) not in parent_char:
#            parent_char.append(len(parent))
        
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

            if f.startswith('.'):
                log.append('Temp file not used: %s' % f)
                continue
            if '.' not in f:
                log.append('No dot in filename, so no ext.: %s' % f)
                continue
                
            # -----------------------------------------------------------------
            # Check estension:
            # -----------------------------------------------------------------
            part = f.split('.')
            if len(part) > 3:
                log.append('File with dot extra: %s' % f)
            name = part[0].upper() # Take only first block at first dot!                
            ext = part[-1].upper()
            
            if not name:
                log.append('No product folder: %s' % f)
                continue

            if extension and ext not in extension:
                log.append('Estension %s not used: %s' % (ext, f))
                continue
            
            # -----------------------------------------------------------------
            # Generate product / folder name
            # -----------------------------------------------------------------
            product = name[:product_part]
            if product not in product_db:
                product_db[product] = {}
            if key not in product_db[product]:
                product_db[product][key] = []
                
            # File to symlink:    
            product_db[product][key].append((
                os.path.join(root, f),
                f,
                ))    

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
        # TODO check walk clause here!!!
        # if not walk: 
        #     break
        break # Only first folder

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
        folder_name = clean_char(product, folder_replace_char) # change char
        folder_parent = folder_name[:parent_part]
        
        # ---------------------------------------------------------------------
        # Check family:
        # ---------------------------------------------------------------------
        family_name = no_family_name
        found_parent = False
        for l in sorted(parent_char, reverse=True):
            family_parent = folder_name[:l]
            if family_parent in family_db:
                family_name = family_db[family_parent]
                found_parent = family_parent
                break
        
        if folder_parent.isdigit() or found_parent:
            product_folder = os.path.join(
                dropbox_path, family_name, 
                found_parent or folder_parent, 
                folder_name,
                )
        else:
            if found_parent:
                product_folder = os.path.join(
                    dropbox_path, family_name, folder_name)
            else:        
                product_folder = os.path.join(
                    dropbox_path, family_name, found_parent, folder_name)
        
        # 2. Create if not present:
        if not demo:
            os.system('mkdir -p "%s"' % product_folder)
        
        for origin, f in product_db[product][key]:
            tot += 1
            # DESTINATION: Filename
            name = '%s_%s' % (key, clean_char(
                f, 
                file_replace_char, # Replace list
                )) # Filename for destination
            try:    
                destination = os.path.join(
                    dropbox_path,
                    product_folder, # Product folder
                    name,
                    )
            except:
                import pdb; pdb.set_trace()        
            
            # Symlink operations:     
            if demo:
                log_sym.append('DEMO origin: %s destination: %s' % (
                    origin, destination)) 
            else:    
                try:
                    os.symlink(origin, destination)
                    log_sym.append('CREATO: origin: %s destination: %s' % (
                        origin, destination))
                except:
                    log_sym.append('PRESENTE: origin: %s destination: %s' % (
                        origin, destination))
print log_sym                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
