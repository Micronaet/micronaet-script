#!/usr/bin/python
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
import ConfigParser
import thread
import base64

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from datetime import datetime

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )

class MicronaetWebService():
    ''' Start XMLRPC Handler
        Config file in parameters
    '''
    # -------------------------------------------------------------------------
    #                               PRIVATE METHODS:
    # -------------------------------------------------------------------------
    def _log_data(self, event, mode='INFO'):
        ''' Log data on file:
        '''
        # ---------------------------------------------------------------------
        # Chose log registry file:
        # ---------------------------------------------------------------------
        if not self._file_log:
            # Open log file for service session:
            self._file_log = open(self._filename_log, 'a+')
        
        # ---------------------------------------------------------------------
        # Write event:
        # ---------------------------------------------------------------------
        self._file_log.write('%s. [%s] %s%s' % (
            datetime.now(),
            mode.upper(),
            event,
            self._return,
            ))
        self._file_log.flush()        
        return True
    
    def _shutdown_thread(self, ):
        ''' Hidden procedure for close RDP server
        '''
        # Close server:
        message = 'RDP Server shutdown in progress...'
        print message
        self._log_data(message)
        
        self._server.shutdown()

        message = 'RDP Server shutdown done!'
        print message
        self._log_data(message)

        # Close log file:
        try:
            self._file_log.close()
        except:
            pass    

    # -------------------------------------------------------------------------
    #                                METHODS:
    # -------------------------------------------------------------------------
    def remote_shutdown(self, ):
        ''' Procedure to close server via XMLRPC
        '''
        thread.start_new_thread(self._shutdown_thread, ())
        return True

        
    def execute(self, operation, parameter=None):
        ''' Execute method for call function (saved in ODOO)
            operation: name of operation (searched in odoo xmlrpc.operation obj
            parameter: dict with extra parameter
                > input_file_string: text of input file

            @return: dict with parameter:
                error: if there's an error during operation
                result_string_file: output file returned as a string
        '''
        if parameter is None:  
            parameter = {}
            
        res = {
            'esit': True,
            'comment': '',
            }

        # ---------------------------------------------------------------------
        #                      CASE: OPERATION: 
        # ---------------------------------------------------------------------
        if operation == 'ping':
            # Demo operation used to test echo response from RPC
            res['comment'] = 'Server is up'
            self._log_data('Call [ping]')
            return res
            
        # ---------------------------------------------------------------------                
        # Launch command
        # ---------------------------------------------------------------------                
        elif operation == 'file': # Get binary file
            try:
                filename = parameter.get('filename')      
                
                import pdb; pdb.set_trace()
                f_in = open(filename, 'rb')
                binary_data = f_in.read()
                res['file'] = base64.b64encode(binary_data)
                f_in.close()
                
            except:
                res['esit'] = False
                res['comment'] += 'Cannot access filename passed as context'
            return res
            
        elif operation == 'batch': # Launch remote command:
            command = parameter.get('command')
            self._log_data('Call [batch] >> command: %s' % command)
            batch_path = os.path.dirname(os.path.realpath(__file__))
            
            # -----------------------------------------------------------------
            # Launch invoice:
            # -----------------------------------------------------------------
            if command == 'invoice':
                try:
                    batch_command = os.path.join(
                        self._batch_path, '%s.bat' % command)
                    if not os.path.isfile(batch_command):
                        res['esit'] = False
                        res['comment'] += u'Batch command not found: %s!' % (
                            batch_command,
                            )
                        return res
                        
                    os.system(batch_command) # Launch sprix
                    res['comment'] += u'Command launched: %s' % batch_command
                    return res
                except:
                    res['esit'] = False
                    res['comment'] += \
                        u'Error launch command %s' % batch_command
                    return res

            # -----------------------------------------------------------------
            # XXX invoice:
            # -----------------------------------------------------------------
            # TODO 
            
            # -----------------------------------------------------------------
            # Launch error:
            # -----------------------------------------------------------------
            else:        
                res['esit'] = False
                res['comment'] += u'Unknow command parameter: %s' % command
                self._log_data('Unknown call [batch] >> command: %s' % command, 
                    mode='error')
                return res
        return True
    
    def __init__(self, config_file):
        ''' Start XMLRPC reading config file for parameter
        '''        
        # ---------------------------------------------------------------------
        # A. Service configuration: .\service.cfg       
        # ---------------------------------------------------------------------
        config = ConfigParser.ConfigParser()
        current_path = os.path.dirname(os.path.realpath(__file__))  
        config.read([os.path.join(current_path, 'service.cfg')])
        self._root_path = config.get('path', 'root')
        self._batch_path = os.path.join(self._root_path, 'rdp', 'batch')
        self._log_path = os.path.join(self._root_path, 'rdp', 'log')
        self._filename_log = os.path.join(self._log_path, 'rdp.log')
        self._file_log = False
        self._return = '\r\n'

        # Create batch path if not present:
        try:
            os.system('mkdir "%s"' % self._batch_path)
        except:
            message = 'RDP Batch Folder creation error: %s' % self._batch_path
            print message
            self._log_data(message, mode='error')

        # Create log path if not present:
        try:
            os.system('mkdir "%s"' % self._log_path)
        except:
            message = 'RDP Log Folder creation error: %s' % self._log_path
            print message
            self._log_data(message, mode='error')

        # ---------------------------------------------------------------------
        # B. RDP Configuration: (file passed)
        # ---------------------------------------------------------------------
        config = ConfigParser.ConfigParser()
        self._config_file = config_file        
        config.read([self._config_file])        
        
        # ---------------------------------------------------------------------
        #                          XMLRPC server:
        # ---------------------------------------------------------------------
        try:
            xmlrpc_host = config.get('XMLRPC', 'host') 
            xmlrpc_port = eval(config.get('XMLRPC', 'port'))
        except:
            message = 'Config file not present: %s' % self._config_file 
            print message
            self._log_data(message, mode='error')
            return 
            
        # ---------------------------------------------------------------------
        #                             Create server:
        # ---------------------------------------------------------------------
        self._server = SimpleXMLRPCServer(
            (xmlrpc_host, xmlrpc_port), 
            requestHandler=RequestHandler,
            )
        self._server.register_introspection_functions()

        # Register exported functions:        
        self._server.register_function(self.remote_shutdown, 'remote_shutdown')
        self._server.register_function(self.execute, 'execute')
        
        # ---------------------------------------------------------------------
        # Hello string:
        # ---------------------------------------------------------------------
        print 'Micronaet: XMLRPC Server started on: %s port %s' % (
            xmlrpc_host, xmlrpc_port)
        print 'Config file: %s' % self._config_file
        print 'Waiting for calls...'
        
        # ---------------------------------------------------------------------
        # Forever loop:
        # ---------------------------------------------------------------------
        self._server.serve_forever()

if __name__ == '__main__':  
    if len(sys.argv) == 2:
        WebService = MicronaetWebService(sys.argv[1])
    else:
        print 'Launch passing config.cfg fullpath'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
