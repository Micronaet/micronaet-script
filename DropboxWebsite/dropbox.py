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
import shutil
import parameters # Micronaet: configuration file
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
samba_path = parameters.samba_path
dropbox_path = parameters.dropbox_path

print '''
Setup parameters: 
    ODOO: Connection: %s:%s DB %s utente: %s
    Demo: %s
    Samba folders: %s
    Dropbox path: %s
    ''' % (
        odoo_server, 
        odoo_port, 
        odoo_database, 
        odoo_user,
        
        demo,
        samba_path,
        dropbox_path,
        )

# -----------------------------------------------------------------------------
#                                 UTILITY:
# -----------------------------------------------------------------------------
def get_modify_date(fullname):
    ''' Return modify date for file
    '''
    modify_date = datetime.fromtimestamp(
        os.stat(fullname).st_mtime).strftime('%Y-%m-%d')
    return modify_date        

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
    
# Pool used:
product_pool = odoo.model('product.product.web.server')
product_ids = product_pool.search([
    ('connector_id.wordpress', '=', True),
    ])

# Check elements:
#error = [] # Error database
#warning = [] # Warning database
#info = [] # Info database
#log = [] # Log database
#log_sym = [] # Log database for symlinks
#product_odoo = {}

# Only if new file (check how):
dropbox_root_path = os.path.expanduser(dropbox_path)
samba_root_path = os.path.expanduser(samba_path)

# -----------------------------------------------------------------------------
# Save current files (Dropbox folder):
# -----------------------------------------------------------------------------
current_files = []
for root, folders, files in os.walk(dropbox_root_path):
    for f in files:
        current_files.append(
            os.path.join(root, f)
    break # only first folder! 

# -----------------------------------------------------------------------------
# Logg on all product image selected:
# -----------------------------------------------------------------------------
for product in product_pool.browse(product_ids):
    for image in product.image_ids:      
        image_id = image.id
        code = image.album_id.code        
        samba_relative_path = image.album_id.path # TODO dropbox_path
        filename = product.filename
        
        origin = os.path.(samba_relative_path, filename)
        destination = os.path.(dropbox_root_path, '%s.%s' % (code, filename))
        
        if destination in current_files:
            current_files.remove(destination)
        
        # Create symlink:
        try:
            os.symlink(origin, destination)
            log_sym.append('CREATO: origin: %s destination: %s' % (
                origin, destination))
        except:
            log_sym.append('ERRORE: origin: %s destination: %s' % (
                origin, destination))
                
        # Find dropbox link:
        
        # Save dropbox link:
    
os.system('chmod 777 "%s" -R' % dropbox_path)

for filename in current_files:
    os.rm(filename)

# file_modify = get_modify_date(fullname)
# os.system('mkdir -p "%s"' % product_folder)
        
print 'End operation'                        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
