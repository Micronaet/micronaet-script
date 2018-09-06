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
import time

import webservice
import xmlrpclib
import ConfigParser

from datetime import datetime


class PySvc(win32serviceutil.ServiceFramework):  
    ''' Class for manage Microsoft Service
    '''
    # -------------------------------------------------------------------------
    #                                  INSTANCE DATA:
    # -------------------------------------------------------------------------
    # Service name (use with net start / stop
    _svc_name_ = 'Micronaet Listener Service'
    
    # Service name in Service Control Manager (SCM)    
    _svc_display_name_ = 'Micronaet Web Service'
    
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
            setup_file.write('[XMLRPC]%shost: 0.0.0.0%sport: 7000' % (
                self._return,
                self._return,
                ))
            setup_file.close()
            self._log_data('Create empty config file: %s%s' % (
                self._setup_file, self._return))
        return True
        
    def _log_data(self, event, mode='INFO', registry='activity'):
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
        self._root_path = 'C:\\Micronaet\\Micronaet Listener Service' # TODO
        #self._root_path = os.path.join(
        #    'C:\\',
        #    'Micronaet',
        #    self._svc_name_, 
        #    ))

        print 'Root folder: %s' % self._root_path
         
        # Configuration:        
        self._setup_file = os.path.join(self._root_path, 'service.cfg')
        print 'Config file: %s' % self._setup_file

        self._webserver_command = 'start %s "%s"' % (
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'webservice.py',
                ),
            self._setup_file,
            ) 
        print 'Web Server: %s' % self._webserver_command
        
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

        # Read from config file port used from XMLRPC:
        config = ConfigParser.ConfigParser()
        config.read([self._setup_file])
        self._xmlrpc_port = eval(config.get('XMLRPC', 'port'))

        # XMLRPC server:            
        self._xmlrpc_address = 'http://localhost:%s/RPC2' % self._xmlrpc_port

        # ---------------------------------------------------------------------
        # Log install event:
        # ---------------------------------------------------------------------
        self._log_data(
            'Instance %s%s    Log path: %s%s    Config: %s [localhost:%s]' % (
                self._svc_name_, self._return, self._log_path,
                self._return, self._setup_file, self._xmlrpc_port), 
                registry='service',
                )
        self._log_data('Web Server command: %s' % self._webserver_command)    

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

        # Log operation:
        self._log_data('Start RPC Service', registry='service')

        # START WEBSERVICE:        
        os.system(self._webserver_command) # Launch indipendent task:

        # RUNNING LOOP:
        # If the stop event hasn't been fired keep looping  
        #check_every = 1 # 20 times
        #i = 0

        self._sock = False
        response = None
        while response != win32event.WAIT_OBJECT_0:
            ''''i += 1
            
            # Check working service:
            if i > check_every:
                try:
                    i = 0
                    if not self._sock:
                        self._sock = xmlrpclib.ServerProxy(
                            self._xmlrpc_address, allow_none=True)
                    self._sock.execute('ping') # Check operation
                    self._log_data('Server is up') # TODO remove
                except:
                    self._log_data(u'Server is down from remote %s' % (
                        sys.exc_info()
                        ))
                    #os.system('net stop %s' % self._svc_name_) # is better mode?
            '''
            self._log_data('Server is up: %s' % self._xmlrpc_address)
            # Stop for X millisecond and listen for stop event
            response = win32event.WaitForSingleObject(
                self.hWaitStop, 
                self._wait_ms,
                )  

    def SvcStop(self):  
        ''' Shutting down service:
        '''
        # ---------------------------------------------------------------------
        #                          STOP OPERATION:
        # ---------------------------------------------------------------------
        # Terminate web server:
        try:
            sock = xmlrpclib.ServerProxy(
                self._xmlrpc_address, 
                allow_none=True,
                )
            sock.remote_shutdown()
            time.sleep(1)
            
            self._log_data(
                'Shutdown RPC Service %s' % self._xmlrpc_address,
                registry='service', 
                )
        except:
            self._log_data(
                'Cannot stop RPC: %s [%s]' % (
                    self._xmlrpc_address,
                    sys.exc_info()),
                mode='error',
                registry='service', 
                )
                
        # Close log file        
        try:
            self._file_service.close()
        except:
            pass # Service unavailable
        try:
            self._file_activity.close()
        except:
            pass # Service unavailable

        # Service stop part:
        try:
            # Tell the SCM shutting down event:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            
            # Raise the stop event  
            win32event.SetEvent(self.hWaitStop)
        except:
            pass # Service unavailable
            

if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
