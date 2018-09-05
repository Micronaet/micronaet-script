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

import webservice

from datetime import datetime


class PySvc(win32serviceutil.ServiceFramework):  
    ''' Class for manage Microsoft Service
    '''
    # -------------------------------------------------------------------------
    #                                  INSTANCE DATA:
    # -------------------------------------------------------------------------
    # Service name (use with net start / stop
    _svc_name_ = 'Micronaet Listner Service'
    
    # Service name in Service Control Manager (SCM)    
    _svc_display_name_ = 'Micronaet WebService'
    
    # Help text in SCM
    _svc_description_ = 'This service open a XMLRPC listner for remote call'

    # -------------------------------------------------------------------------
    #                                  PRIVATE METHOD:
    # -------------------------------------------------------------------------
    def _create_setup_file(self, ):
        ''' Create config file if not present in data path
        '''
        if not os.path.isfile(self._setup_file):
            setup_file = open(self._setup_file, 'w')
            setup_file.write('[XMLRPC]%shost: localhost%sport: 8000' % (
                self._return,
                self._return,
                ))
            setup_file.close()
            self._log_data('Create empty config file: %s%s' % (
                self._setup_file, self._return))
        return True
        
    def _log_data(self, event, mode='INFO', registry='activity', close=False):
        ''' Log data on file:
        '''
        # ---------------------------------------------------------------------
        # Chose log registry file:
        # ---------------------------------------------------------------------
        if registry == 'activity':
            if not self._file_activity:
                # Open log file for service session:
                self._file_activity = open(self._log_activity, 'a+')
            current_log = self._file_activity
        else: # service registry
            if not self._file_service:
                # Open log file for service session:
                self._file_service = open(self._log_service, 'a+')
            current_log = self._file_service
 
        # ---------------------------------------------------------------------
        # Write event:
        # ---------------------------------------------------------------------
        current_log.write('%s. [%s] %s%s' % (
            datetime.now(),
            mode.upper(),
            event,
            self._return,
            ))
        current_log.flush()
        
        # ---------------------------------------------------------------------
        # Closing check:
        # ---------------------------------------------------------------------
        if close:
            try:
                current_log.close()
            except:
                pass # TODO Log closing error?
        return True

    def _init(self, ):
        ''' Initial setup (launched both init and start service)
        '''
        # ---------------------------------------------------------------------
        # Parameters:
        # ---------------------------------------------------------------------
        # Return:
        self._return = '\r\n'
        
        # Root folder:
        self._root_path = 'C:\\Micronaet\\Micronaet Listner Service' # TODO
        #self._root_path = os.path.join(
        #    'C:\\',
        #    'Micronaet',
        #    self._svc_name_, 
        #    ))

        #os.path.expanduser(
        print 'Root folder: %s' % self._root_path
         
        # Configuration:        
        self._setup_file = os.path.join(self._root_path, 'service.cfg')
        print 'Config file: %s' % self._setup_file
        
        # Log:
        self._log_path = os.path.join(self._root_path, 'log')        
        self._log_service = os.path.join(self._log_path, 'service.log')
        self._log_activity = os.path.join(self._log_path, 'activity.log')
        print 'Log file Service: %s Activity: %s' % (
            self._log_service,
            self._log_activity,
            )
        
        # Handle file:
        self._file_service = False
        self._file_activity = False
        
        # Millisecond for waiting:
        self._wait_ms = 5000
        
        # Create path if not present:
        try:
            os.system('mkdir "%s"' % self._log_path) # create also root folder
        except:
            print 'Error creating folder structure: %s' % self._log_path

        # ---------------------------------------------------------------------
        # Config file:
        # ---------------------------------------------------------------------
        # Create empty if not present:
        self._create_setup_file()

        # ---------------------------------------------------------------------
        # Log install event:
        # ---------------------------------------------------------------------
        self._log_data('Instance %s service%sLog path: %s%sConfig: %s' % (
            self._svc_name_, self._return, self._log_path,
            self._return, self._setup_file), 
            registry='service',
            )

    # -------------------------------------------------------------------------
    #                            CONSTRUCTOR:
    # -------------------------------------------------------------------------
    def __init__(self, args):
        ''' Constructor, init method
        '''
        # Setup instance:
        self._init()
          
        # ---------------------------------------------------------------------
        # Windows intallation:
        # ---------------------------------------------------------------------
        # Launch ancherstor init procedure:            
        win32serviceutil.ServiceFramework.__init__(self, args)

        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    # -------------------------------------------------------------------------
    #                            PUBLIC METHODS:
    # -------------------------------------------------------------------------
    def SvcDoRun(self):        
        ''' Start service method
        '''
        # Reload instance:
        self._init()

        response = None        

        # Log operation:
        self._log_data('Start Listner Service', registry='service')

        # ---------------------------------------------------------------------
        #                     START WEBSERVICE:
        # ---------------------------------------------------------------------
        self._web_service = webservice.MicronaetWebService(self._setup_file)

        # ---------------------------------------------------------------------
        #                        RUNNING LOOP:
        # ---------------------------------------------------------------------
        # If the stop event hasn't been fired keep looping  
        while response != win32event.WAIT_OBJECT_0:  
            # Stop for X millisecond and listen for stop event
            response = win32event.WaitForSingleObject(
                self.hWaitStop, 
                self._wait_ms,
                )  

    def SvcStop(self):  
        ''' Shutting down service:
        '''
        # Tell the SCM shutting down event:
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        # Raise the stop event  
        win32event.SetEvent(self.hWaitStop)

        # ---------------------------------------------------------------------
        #                          STOP WEBSERVICE:
        # ---------------------------------------------------------------------
        try:
            # Terminate XMLRPC loop:
            self._web_service.remote_shutdown()
            
            self._log_data(
                'Stop Listner Service', 
                registry='service', 
                close=True,
                )
        except:
            self._log_data(
                'Error stopping listener', 
                mode='error',
                registry='service', 
                close=True,
                )
            

if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
