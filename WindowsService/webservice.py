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
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import ConfigParser
import thread

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )

class MicronaetWebService():
    ''' Start XMLRPC Handler
        Config file in parameters
    '''
    # -------------------------------------------------------------------------
    #                                METHODS:
    # -------------------------------------------------------------------------
    def remote_shutdown(self, ):
        thread.start_new_thread(self.shutdown_thread, ())

    def remote_thread(self, ):
        self._server.shutdown()
        
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
            'status': 'ok', # else 'ko'
            'comment': '',
            }

        # ---------------------------------------------------------------------
        #                      CASE: OPERATION: 
        # ---------------------------------------------------------------------
        if operation == 'lauch':
            command = parameter.get('command')
            try:
                os.system(command) # Launch sprix
                res['comment'] += u'Command launched: %s\n' % command
                return res
            except:
                res['status'] = 'ko'
                res['comment'] += u'Error launch shell command\n'
                return res
        # XXX elif
    
    def __init__(self, config_file):
        ''' Start XMLRPC reading config file for parameter
        '''        
        # ---------------------------------------------------------------------
        #                       Reading config parameters:
        # ---------------------------------------------------------------------
        self._config_file = config_file
        
        config = ConfigParser.ConfigParser()
        config.read([self._config_file])

        # XMLRPC server:
        try:
            xmlrpc_host = config.get('XMLRPC', 'host') 
            xmlrpc_port = eval(config.get('XMLRPC', 'port'))
        except:
            print 'Error file not present: %s' % self._config_file    
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
        
        # Forever loop:
        self._server.serve_forever()

if __name__ == '__main__':  
    WebService = MicronaetWebService('setup.cfg')        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
