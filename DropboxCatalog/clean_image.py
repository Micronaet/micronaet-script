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
import pdb; pdb.set_trace()
for (key, path, extension, walk) in input_folders:
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        for f in files:
            rename_file = False
            
            if f.startswith('.'):
                log.append('NO|Temp file not used|%s|' % f)
                continue
            if '.' not in f:
                log.append('NO|No extension (no .)|%s|' % f)
                continue
                
            # -----------------------------------------------------------------
            # Parse filename:
            # -----------------------------------------------------------------
            part = f.split('.')
            if len(part) > 3:
                log.append('NO|File with extra dot|%s|' % f)
                continue
            
            prefix = ''    
            name = '.'.join(part[:-1]) # Take only first block at first dot!                
            ext = part[-1]
            
            if not name:
                log.append('NO|No image file|%s|' % f)
                continue

            # -----------------------------------------------------------------
            # 1. Case problem in Extension (lower not jpeg:
            # -----------------------------------------------------------------
            if ext == ext.lower() and ext.lower() != 'jpeg':
                new_extension = ext # remain the same
            else:
                rename_file = True
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
                rename_file = True
                new_name = name.upper()

            if new_name[:2] in ('ST', 'MT'):
                prefix = new_name[:2]
                new_name = new_name[2:] # remove prefix for analysis extra value

            # -----------------------------------------------------------------
            # 3. SX >> .001 change     or S.jpg >>> .jpg
            # -----------------------------------------------------------------
            if new_name[13:14] == 'S':                
                rename_file = True
                extra_s = new_name[14:]
                if extra_s.isdigit():
                    new_name = '%s.%03d' % (
                        new_name[:13].strip('_'),
                        int(extra_s), # XXX < 3 char
                        ) 
                elif not extra_s:
                    new_name = new_name[:-1] # Remove S
                else:
                    log.append('NO|No SX format|%s|' % f)
                    continue
                
            # -----------------------------------------------------------------
            # 4. "NOME (1).jpg" >>> NOME.001.jpg
            # -----------------------------------------------------------------
            if '(' in new_name and ')' in new_name:
                extra_s = new_name[13:]                
                extra_s = extra_s.replace('(', '').replace(')', '').strip()
                if extra_s.isdigit():
                    rename_file = True
                    new_name = '%s.%03d' % (
                        new_name[:13].strip('_'), # Remove extra _
                        int(extra_s), # XXX < 3 char
                        ) 

            # -----------------------------------------------------------------
            # 5. "NOME 1.jpg" >>> NOME.001.jpg
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # 6. + JUMPED
            # -----------------------------------------------------------------
            if '+' in new_name or '-' in new_name:
                log.append('NO|Jumped more product (+ or -)|%s|' % f)
                continue

            # -----------------------------------------------------------------
            # 7. + JUMPED
            # -----------------------------------------------------------------
            if 'COPIA' in new_name:
                log.append('NO|Jumped COPIA product|%s|' % f)
                continue

            # TODO case not managed: _COPIA, S1-0, NOME(1).jpg
            
            # -----------------------------------------------------------------
            # LAST. " " >>> "_"
            # -----------------------------------------------------------------
            if ' ' in new_name:
                rename_file = True
                new_name = new_name.replace(' ', '_')
                
            # -----------------------------------------------------------------
            # END: Rename procedure:
            # -----------------------------------------------------------------        
            if not rename_file:
                log.append('NO|No rename operation|%s|' % f)
                continue
                
            new_name = new_name.strip('_')
            new_name = '%s%s.%s' % (prefix, new_name, new_extension)
            from_file = os.path.join(root, f)
            to_file = os.path.join(root, new_name)
            if os.path.isfile(to_file):
                log.append('NO|Duplicated name|%s|%s' % (f, new_name))
                continue
            
            if demo:
                # Log operation:
                log.append('YES|RENAMED|%s|%s' % (f, new_name))
            else:    
                # Rename operation:
                pass#shutil.move(from_file, to_file)
        break

f_log = open('./log.csv', 'w')
for item in sorted(log):
    f_log.write('%s\n' % item)
f_log.close()    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
