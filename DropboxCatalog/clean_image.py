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
name_done = []
name_duplicated = []
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
            if len(part) > 3:
                log.append('File with dot extra: %s' % f)
                continue
                
            name = '.'.join(part[:-1]) # Take only first block at first dot!                
            ext = part[-1]
            
            if not name:
                log.append('No image file: %s' % f)
                continue

            # -----------------------------------------------------------------
            # 1. Case problem in Extension (lower not jpeg:
            # -----------------------------------------------------------------
            if ext == ext.lower() and ext.lower() != 'jpeg':
                new_extension = ext # remain the same
            else:
                # Clean case error:
                new_extension = ext.lower()
                
                # Remove jpeg files:
                if new_extension == 'jpeg':
                    new_extension = 'jpg'

            # -----------------------------------------------------------------
            # 2. Case problem in name:
            # -----------------------------------------------------------------
            if name == name.upper():   
                new_name = name    
            else:
                new_name = name.upper()

            # -----------------------------------------------------------------
            # 3. SX >> .001 change     or S.jpg >>> .jpg
            # -----------------------------------------------------------------
            if new_name[13:14] == 'S':                
                extra_s = new_name[14:]
                if extra_s.is_digit():
                    new_name = '%s.%03d' % (
                        new_name[:13],
                        int(extra_s), # XXX < 3 char
                        ) 
                elif not extra_s:
                    new_name = new_name[:-1] # Remove S
                else:
                    log.append('No SX format: %s' % f)
                    continue
                
            # -----------------------------------------------------------------
            # 4. "NOME 1.jpg" >>> NOME.001.jpg
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # 5. + JUMPED
            # -----------------------------------------------------------------


            # TODO case not managed: _COPIA, S1-0, NOME(1).jpg
            
            # -----------------------------------------------------------------
            # LAST. " " >>> "_"
            # -----------------------------------------------------------------


            # -----------------------------------------------------------------
            # END: Rename procedure:
            # -----------------------------------------------------------------        
            new_name = '%s.%s' % (new_name, new_extension)
            if new_name in name_done:
                name_duplicated.append(new_name) # XXX no rename duplicated!
                continue
            else:
                if demo:
                    # Log operation:
                    print 'Old: %s, new: %s' % (f, new_name)
                else:    
                    # Rename operation:
                    shutil.move(
                        os.path.join(root, f),
                        os.path.join(root, new_name),
                        )                    
                name_done.append(new_name)
        break
print 'Done elements: \n\n%s' % (ext_done, )            

if ext_duplicated:
    print 'Duplicated elements: \n\n%s' % (ext_duplicated, )            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
