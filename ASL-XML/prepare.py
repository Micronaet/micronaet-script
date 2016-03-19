#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
# Developer: Nicola Riolini @thebrush (<https://it.linkedin.com/in/thebrush>)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

# -----------------------------------------------------------------------------
#                                LIBRARY
# -----------------------------------------------------------------------------
import os
import sys
import xlrd
import base64
import ConfigParser
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
#                              Parameters
# -----------------------------------------------------------------------------
# Config file:
cfg_file = 'asl.cfg' # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)


# Log
log_file = os.path.expanduser(config.get('log', 'log_file'))
log = eval( config.get('log', 'log'))

# Fixed data:
proprietario_dict = {
    'codiceRegione': config.get('proprietario', 'codiceRegione'),
    'codiceAsl': config.get('proprietario', 'codiceAsl'),
    'codiceSSA': config.get('proprietario', 'codiceSSA'),
    'cfProprietario': config.get('proprietario', 'cfProprietario'),
    }

# Mask used:    
xml_mask = '''
    <?xml version='1.0' encoding='UTF-8'?>
    <precompilata xsi:noNamespaceSchemaLocation='730_precompilata_new.xsd' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
       ||proprietario||
       ||documentoSpesa||
    </precompilata>
    '''

proprietario = '''
       <proprietario>
           <codiceRegione>%(codiceRegione)s</codiceRegione>
           <codiceAsl>%(codiceAsl)s</codiceAsl>
           <codiceSSA>%(codiceSSA)s</codiceSSA>
           <cfProprietario>%(cfProprietario)s</cfProprietario>
       </proprietario>''' % (proprietario_dict)

# Parameters (files to open):
xls_file = os.path.expanduser(config.get('xls', 'input'))
xml_path = os.path.expanduser(config.get('xml', 'path'))
xml_file = '%(codiceRegione)s_%(codiceAsl)s_%(codiceSSA)s_730.XML' % (
    proprietario)

xml_mask = xml_mask.replace('||proprietario||', proprietario)

documentoSpesa_mask = '''
    <documentoSpesa>
        <idSpesa>
            <pIva>00000000000</pIva>   <!--numerico totale 11-->  
            <dataEmissione>2016-01-01</dataEmissione>   <!--AAAA-MM-DD -->
            <numDocumentoFiscale>
                <dispositivo>1</dispositivo>   <!--1 >> 999--> 
                <numDocumento>-</numDocumento>   <!-- a-z A-Z 0-9 _ . / \ - da 1 a 20  -->
            </numDocumentoFiscale>
        </idSpesa>       
       
        <dataPagamento>2016-01-01</dataPagamento>
        <flagPagamentoAnticipato>1</flagPagamentoAnticipato>       
        <flagOperazione>I</flagOperazione>   <!--I(nser.) V(ariaz) R(imb.) C(ancell.)-->
        <cfCittadino>aaaaaaaaaaaaa</cfCittadino>   <!--stringa max 256 -->
        
        <voceSpesa>   <!--senza limiti-->
           <tipoSpesa>TK</tipoSpesa>   <!--TK(ticket) FC(farmaco) FV(veterinario) AS(spese sanitarie) SR(spese prestazioni assistenza) CT(cure terminali) PI(protesica) IC(chirurgia estetica) AA(altro) -->
           <flagTipoSpesa>1</flagTipoSpesa>   <!--facoltativi   1(ticket) 2(intramoenia)-->
            <importo>00000.01</importo>   <!-- max 5 . max 2 (sempre >0)-->
        </voceSpesa>
        <voceSpesa>
           <tipoSpesa>FC</tipoSpesa>
           <flagTipoSpesa>2</flagTipoSpesa>
           <importo>0.01</importo>
        </voceSpesa>       
    </documentoSpesa>   
    '''

# -----------------------------------------------------------------------------
#                                    MAIN
# -----------------------------------------------------------------------------
error_alert = False

 
try:
    # -------------------------------------------------------------------------
    #                              LOG FILES:
    # -------------------------------------------------------------------------
    error = 'Error opening log files:'
    
    # Open log files:
    log_f = open(log_log_file, 'w')
    xml_f = open(log_log_file, 'w')

    book = xlrd.open_workbook(xls_file)
    sheet = book.sheet_by_index(0) # first
    row = 0
    max_col = 2
    col_convert = {
        0: 'nome',
        1: 'cognome',        
        }
    col_range = range(0, max_col)
    go = True
    spese = ''
    while go:                
        if sheet.cell(row, col) == '':
            break # end loop when no data in first line
            
        data_spesa = {}
        for col in col_range:
            data_spesa[col_convert[row]] = sheet.cell(row, col)
        spese += documentoSpesa_mask % (data_spesa)    
        
    xml_mask.replace('documentoSpesa', spese)        
except:
    pass
xml_f.write(xml_mask) 
   
log_f.close()
xml_f.close()                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
