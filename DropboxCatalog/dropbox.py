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
import erppeek
#import xmlrpclib
import shutil
import parameters # Micronaet: configuration file
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# -----------------------------------------------------------------------------
# Parameters:
# -----------------------------------------------------------------------------
rsync_mask = 'rsync -avh "%s" "%s"'

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
month = parameters.month

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

def get_modify_date(fullname):
    ''' Return modify date for file
    '''
    modify_date = datetime.fromtimestamp(
        os.stat(fullname).st_mtime).strftime('%Y-%m-%d')
    #create_date = datetime.fromtimestamp(
    #    os.stat(fullname).st_ctime).strftime('%Y-%m-%d')    
    #if create_date > modify_date:
    #    return create_date
    #else:
    return modify_date        

def get_now_less_month(month):
    ''' Return date now
    '''
    return (datetime.now() + relativedelta(months=month)
        ).strftime('%Y-%m-%d')
    
# -----------------------------------------------------------------------------
#                           ODOO operation:
# -----------------------------------------------------------------------------
odoo = erppeek.Client(
    'http://%s:%s' % (
        odoo_server, odoo_port), 
    db=odoo_database,
    user=odoo_user,
    password=odoo_password,
    )

# Dropbox recent excluded:
excluded_recent = []
product_pool = odoo.model('product.product')
product_ids = product_pool.search([
    ('no_dropbox', '=', True),
    ('default_code', '!=', False),
    ])
for product in product_pool.browse(product_ids):
    excluded_recent.append(product.default_code)
    
# Read family database
family_pool = odoo.model('product.template')
family_ids = family_pool.search([
    ('is_family', '=', True),
    ])
for family in family_pool.browse(family_ids):
    if not family.family_list:
        print 'Family list not present for: %s' % family.name 
        continue
    for parent in family.family_list.split('|'):
        family_db[parent] = clean_ascii(family.dropbox or family.name)
        if len(parent) not in parent_char:
            parent_char.append(len(parent))
        
# -----------------------------------------------------------------------------
#                           READ ALL INPUT FOLDERS:
# -----------------------------------------------------------------------------
# Folder for modify:
recent_modify = [] # (from_path, name)
from_month = get_now_less_month(month)

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
            fullname = os.path.join(root, f)
            product_db[product][key].append((fullname, f))
            
            # -----------------------------------------------------------------
            # New product management:
            # -----------------------------------------------------------------
            file_modify = get_modify_date(fullname)
            if file_modify >= from_month:
                recent_modify.append((
                    key, file_modify[:7], fullname, f))

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
                dropbox_path, 
                key,
                family_name, 
                found_parent or folder_parent, 
                folder_name,
                )
        else:
            if found_parent:
                product_folder = os.path.join(
                    dropbox_path, 
                    key,
                    family_name, 
                    found_parent, 
                    folder_name,
                    )
            else:        
                product_folder = os.path.join(
                    dropbox_path, 
                    key,
                    family_name, 
                    folder_name,
                    )

        # 2. Create if not present:
        if not demo:
            os.system('mkdir -p "%s"' % product_folder)
        
        for origin, f in product_db[product][key]:
            tot += 1
            # DESTINATION: Filename
            #name = '%s_%s' % (
            name = '%s' % (
                #key, 
                clean_char(
                    f, 
                    file_replace_char, # Replace list
                    ),
                ) # Filename for destination
            destination = os.path.join(
                dropbox_path,
                product_folder, # Product folder
                name,
                )
            
            # Symlink operations:     
            if demo:
                log_sym.append('DEMO origin: %s destination: %s' % (
                    origin, destination)) 
            else:    
                try:
                    # os.symlink(origin, destination)
                    # shutil.copy(origin, destination)
                    os.system(rsync_mask % (origin, destination))
                    log_sym.append('CREATO: origin: %s destination: %s' % (
                        origin, destination))
                except:  # TODO used?
                    log_sym.append('PRESENTE: origin: %s destination: %s' % (
                        origin, destination))

# -----------------------------------------------------------------------------                        
# Recent file management:
# -----------------------------------------------------------------------------
recent_folder = os.path.join(dropbox_path, 'RECENT')

# -----------------------------------------------------------------------------
# Load all files present in dropbox_path folder (also recent):
# -----------------------------------------------------------------------------
old_file = []
new_file = []
for root, folders, files in os.walk(recent_folder):
    for f in files:
        old_file.append(os.path.join(root, f))

# Loop the new image:
for key, file_month, origin, f in recent_modify:
    # Evaluate exclusion:
    code = f.split('.')[0].replace('_', ' ')
    if code in excluded_recent:
        log_sym.append('RECENT Excluded: %s' % code)
        continue

    # B. Create first level + month folder:
    this_folder = os.path.join(recent_folder, key, file_month)
    os.system('mkdir -p "%s"' % this_folder)

    # Create symlink:
    name = '%s' % clean_char(f, file_replace_char)
    destination = os.path.join(this_folder, name)
    new_file.append(destination)

    # Symlink operations:
    if demo:
        log_sym.append('RECENT origin: %s destination: %s' % (
            origin, destination)) 
    else:
        try:
            # os.symlink(origin, destination)
            # shutil.copy(origin, destination)
            os.system(rsync_mask % (origin, destination))
            log_sym.append('RECENT CREATO: origin: %s destination: %s' % (
                origin, destination))
        except:  # TODO used?   
            log_sym.append('RECENT ESISTENTE: origin: %s destination: %s' % (
                origin, destination))

# -----------------------------------------------------------------------------
# Remove unused files:
# -----------------------------------------------------------------------------
for destination in (set(old_file) - set(new_file)):
    os.remove(destination)    

os.system('chmod 777 "%s" -R' % dropbox_path)

if demo:
    print log_sym                
print 'End operation'                        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
