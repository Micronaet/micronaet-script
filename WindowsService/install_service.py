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
import win32service  
import win32serviceutil  
import win32event  
import servicemanager  
  
filename = 'c:\\git\\Services\\test.dat'  
import pdb; pdb.set_trace()
class PySvc(win32serviceutil.ServiceFramework):  
    # you can NET START/STOP the service by the following name  
    _svc_name_ = "Python Service"  
    # this text shows up as the service name in the Service  
    # Control Manager (SCM)  
    _svc_display_name_ = "Python Service as test"  
    # this text shows up as the description in the SCM  
    _svc_description_ = "This service writes stuff to a file"  
      
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self,args)  
        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    # core logic of the service     
    def SvcDoRun(self):  
        ''' Start procedure RUN method
        ''' 
        import pdb; pdb.set_trace()
        f = open(filename, 'w+')  
        rc = None  
          
        # if the stop event hasn't been fired keep looping  
        while rc != win32event.WAIT_OBJECT_0:  
            f.write('TEST DATA\n')  
            f.flush()  
            # block for 5 seconds and listen for a stop event  
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)  
              
        f.write('SHUTTING DOWN\n')  
        f.close()  
      
    # called when we're being shut down      
    def SvcStop(self):  
        # tell the SCM we're shutting down  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        # fire the stop event  
        win32event.SetEvent(self.hWaitStop)  
          
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
