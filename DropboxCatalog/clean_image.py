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
import parameters # Micronaet: configuration file
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# Parameters:
# -----------------------------------------------------------------------------
demo = True #parameters.demo  # TODO change
input_folders = parameters.input_folders

print '''
Setup parameters: 
    Demo: %s
    Input folders: %s
    ''' % (
        demo,
        input_folders,
        )

# Check elements:
error = [] # Error database
warning = [] # Warning database
info = [] #Info database
log = [] # Log database

# -----------------------------------------------------------------------------
#                           READ ALL INPUT FOLDERS:
# -----------------------------------------------------------------------------
ext_done = []
ext_duplicated = []

name_done = []
name_duplicated = []
import pdb; pdb.set_trace()
for (key, path, extension, walk) in input_folders:
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.startswith('.'):
                log.append('Temp file not used: %s' % f)
                continue
            if '.' not in f:
                log.append('No dot in filename, so no ext.: %s' % f)
                continue
                
            # -----------------------------------------------------------------
            # Parse filename:
            # -----------------------------------------------------------------
            part = f.split('.')
            if len(part) > 2:
                log.append('File with dot extra: %s' % f)
                
            name = '.'.join(part[:-1]) # Take only first block at first dot!                
            ext = part[-1]
            
            if not name:
                log.append('No image file: %s' % f)
                continue

            # -----------------------------------------------------------------
            # Case problem in Extension:
            # -----------------------------------------------------------------
            if ext == ext.lower():          
                new_extension = ext # remain the same
            else:
                # Clean case error:
                log.append('Rename extension %s file: %s' % (ext, f))
                new_extension = ext.lower()
                
                # Remove jpeg files:
                if new_extension == 'jpeg':
                    new_extension = 'jpg'
                new_name = '%s.%s' % (name, new_extension)
                if new_name in ext_done:
                    ext_duplicated.append(new_name) # XXX no rename!
                else:
                    shutil.move(
                        os.path.join(root, f),
                        os.path.join(root, new_name),
                        )                    
                    ext_done.append(new_name)

            # -----------------------------------------------------------------
            # Case problem in name:
            # -----------------------------------------------------------------
            if name != name.upper():          
                # Clean case error:
                log.append('Rename %s file: %s' % (name, f))
                new_name = name.upper()
                
                # Remove jpeg files:
                new_name = '%s.%s' % (new_name, new_extension)
                if new_name in name_done:
                    name_duplicated.append(new_name) # XXX no rename!
                else:
                    if demo:
                        print 'Da %s A %s' % (
                            os.path.join(root, f),
                            os.path.join(root, new_name),
                            )
                    else:
                        shutil.move(
                            os.path.join(root, f),
                            os.path.join(root, new_name),
                            )                    
                        name_done.append(new_name)

print 'Done elements: \n\n%s' % (ext_done, )            

if ext_duplicated:
    print 'Duplicated elements: \n\n%s' % (ext_duplicated, )            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
