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

# Installation with pip:
# pip install wmi
# download pywin32 from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
# pip install pywin32-22'.1-cè27-cp27m-win32.whl # this version for win7 pro

# Change position:
# http://stackoverflow.com/questions/25257274/python-3-4-importerror-no-module-named-win32api

import os
import wmi

c = wmi.WMI ()
for process in c.Win32_Process ():
  print process.ProcessId, process.Name
  
os.system('taskkill /im make.exe')
