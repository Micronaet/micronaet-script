# -*- coding: utf-8 -*-
###############################################################################
#
# ODOO (ex OpenERP) 
# Open Source Management Solution
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
import os
import sys
import xlrd
import shutil
import ConfigParser
from datetime import datetime

current_path = os.path.dirname(__file__)

# -----------------------------------------------------------------------------
# Parameters from config file:
# -----------------------------------------------------------------------------
# Open file:
cfg_file = os.path.join(current_path, 'mexal.cfg')
config = ConfigParser.ConfigParser()
config.read([cfg_file])

# Read data:
newline = eval(config.get('parameter', 'newline'))
row_start = eval(config.get('parameter', 'row_start'))
code_limit = eval(config.get('parameter', 'code_limit'))
name_limit = eval(config.get('parameter', 'name_limit'))
name_split = eval(config.get('parameter', 'name_split'))
price_decimal = eval(config.get('parameter', 'price_decimal'))
currency_id = str(config.get('parameter', 'currency_id'))

out_csv = config.get('file', 'out_csv')

# -----------------------------------------------------------------------------
# Calculated paremeters:
# -----------------------------------------------------------------------------
# CSV:
file_csv = os.path.join(current_path, 'CSV', out_csv)

# Log:
path_log = os.path.join(current_path, 'LOG')
path_log_xls = os.path.join(path_log, 'XLS')
file_log = os.path.join(path_log, 'conversioni.txt')
f_log = open(file_log, 'a')

# XLS:
path_xls = os.path.join(current_path, 'XLS')
path_done_xls = os.path.join(path_xls, 'FATTI')

# File:
no_line_text = ('CODICE CATALOGO', )
header = [
    '_ARTIP',
    '_ARCOD',
    '_ARDES',
    '_ARAGG',
    '_ARALT',
    '_ARANN',
    '_ARSOS',
    '_ARNDS(1)',
    '_ARNDE(1)',
    '_ARNDT(1)',
    '_ARNDS(2)',
    '_ARNDE(2)',
    '_ARNDT(2)',
    '_ARDTC',
    '_ARDTA',
    '_ARDSL(1)',
    '_ARDSL(2)',
    '_ARDSL(3)',
    '_ARDSL(4)',
    '_ARDSL(5)',
    '_ARDSL(6)',
    '_ARDSL(7)',
    '_ARDSL(8)',
    '_ARDSL(9)',
    '_ARIVA',
    '_ARUM1',
    '_ARUM2',
    '_ARDEC',
    '_ARKOEPTA',
    '_ARCON',
    '_ARSTA',
    '_ARSTN',
    '_ARTCO',
    '_ARSTR',
    '_ARVST',
    '_ARVUL',
    '_ARVUP',
    '_ARSST',
    '_ARCUL',
    '_ARCUP',
    '_ARRIC',
    '_ARCOS',
    '_ARSCO',
    '_ARSCQ',
    '_ARLIS',
    '_ARTPR',
    '_ARIMB',
    '_ARQPR',
    '_ARQPA',
    '_ARPRZ(1)',
    '_ARPRZ(2)',
    '_ARPRZ(3)',
    '_ARPRZ(4)',
    '_ARPRZ(5)',
    '_ARPRZ(6)',
    '_ARPRZ(7)',
    '_ARPRZ(8)',
    '_ARPRZ(9)',
     '_AREXG',
    '_AREXA',
    '_AREXB',
    '_AREXC',
    '_ARMFTCPS',
    '_ARDBP',
    '_ARDBV',
    '_ARCAR',
    '_ARDBA',
    '_ARCTG',
    '_ARFRM',
    'CALENDPROD',
    '_ARPRE',
    '_ARTMO',
    '_ARVMO',
    '_ARSMO',
    '_ARAMO',
    '_ARRRO',
    '_ARRST',
    '_ARTDE',
    '_ARFOR(1)',
    '_ARGGR(1)',
    '_ARLOT(1)',
    '_ARFPR(1)',
    '_ARCOF(1)',
    '_ARQTA(1,1)',
    '_ARQTA(1,2)',
    '_ARQTA(1,3)',
    '_ARVAL(1)',
    '_ARSCQ(1,1)',
    '_ARSCQ(1,2)',
    '_ARSCQ(1,3)',
    '_ARSCQ(1,4)',
    '_ARFOR(2)',
    '_ARGGR(2)',
    '_ARLOT(2)',
    '_ARFPR(2)',
    '_ARCOF(2)',
    '_ARQTA(2,1)',
    '_ARQTA(2,2)',
    '_ARQTA(2,3)',
    '_ARVAL(2)',
    '_ARSCQ(2,1)',
    '_ARSCQ(2,2)',
    '_ARSCQ(2,3)',
    '_ARSCQ(2,4)',
    '_ARFOR(3)',
    '_ARGGR(3)',
    '_ARLOT(3)',
    '_ARFPR(3)',
    '_ARCOF(3)',
    '_ARQTA(3,1)',
    '_ARQTA(3,2)',
    '_ARQTA(3,3)',
    '_ARVAL(3)',
    '_ARSCQ(3,1)',
    '_ARSCQ(3,2)',
    '_ARSCQ(3,3)',
    '_ARSCQ(3,4)',
    'SCOSULIST1',
    'SCOSULIST2',
    'SCOSULIST3',
    'SCOSULIST4',
    'SCOSULIST5',
    'SCOSULIST6',
    'SCOSULIST7',
    'SCOSULIST8',
    'SCOSULIST9',
    'PRZSULIST1',
    'PRZSULIST2',
    'PRZSULIST3',
    'PRZSULIST4',
    'PRZSULIST5',
    'PRZSULIST6',
    'PRZSULIST7',
    'PRZSULIST8',
    'PRZSULIST9',
    '_ARVEX',
    '_ARPPER',
    '_ARPRIT',
    '_ARPCAS',
    '_ARPMES',
    '_ARINO',
    '_ARIMA',
    '_ARIKM',
    '_ARIUS',
    '_ARIDU',
    '_ARIKU',
    '_ARIPR',
    '_ARIPA',
    '_ARRDT',
    '_ARRRI',
    '_ARRTL',
    '_ARRSA',
    'CODAGEN1',
    'CONDAGE1',
    'TIPPROV1',
    'FORMULA1',
    'CODAGEN2',
    'CONDAGE2',
    'TIPPROV2',
    'FORMULA2',
    'CODAGEN3',
    'CONDAGE3',
    'TIPPROV3',
    'FORMULA3',
    'CODAGEN4',
    'CONDAGE4',
    'TIPPROV4',
    'FORMULA4',
    'CODAGEN5',
    'CONDAGE5',
    'TIPPROV5',
    'FORMULA5',
    'CODAGEN6',
    'CONDAGE6',
    'TIPPROV6',
    'FORMULA6',
    'CODAGEN7',
    'CONDAGE7',
    'TIPPROV7',
    'FORMULA7',
    'CODAGEN8',
    'CONDAGE8',
    'TIPPROV8',
    'FORMULA8',
    'CODAGEN9',
    'CONDAGE9',
    'TIPPROV9',
    'FORMULA9',
    'GRPMERCE',
    'NATURA',
    '_ARPRIT1',
    '_ARIMM',
    '_ARCAT',
    '_ARICO',
    '_ARIVS',
    '_ARAGR',
    'MINFATT',
    'MAXFATT',
    'ARGSI',
    '_ARFOR(4)',
    '_ARGGR(4)',
    '_ARLOT(4)',
    '_ARFPR(4)',
    '_ARCOF(4)',
    '_ARQTA(4,1)',
    '_ARQTA(4,2)',
    '_ARQTA(4,3)',
    '_ARVAL(4)',
    '_ARSCQ(4,1)',
    '_ARSCQ(4,2)',
    '_ARSCQ(4,3)',
    '_ARSCQ(4,4)',
    '_ARFOR(5)',
    '_ARGGR(5)',
    '_ARLOT(5)',
    '_ARFPR(5)',
    '_ARCOF(5)',
    '_ARQTA(5,1)',
    '_ARQTA(5,2)',
    '_ARQTA(5,3)',
    '_ARVAL(5)',
    '_ARSCQ(5,1)',
    '_ARSCQ(5,2)',
    '_ARSCQ(5,3)',
    '_ARSCQ(5,4)',
    '_ARFOR(6)',
    '_ARGGR(6)',
    '_ARLOT(6)',
    '_ARFPR(6)',
    '_ARCOF(6)',
    '_ARQTA(6,1)',
    '_ARQTA(6,2)',
    '_ARQTA(6,3)',
    '_ARVAL(6)',
    '_ARSCQ(6,1)',
    '_ARSCQ(6,2)',
    '_ARSCQ(6,3)',
    '_ARSCQ(6,4)',
    '_ARFOR(7)',
    '_ARGGR(7)',
    '_ARLOT(7)',
    '_ARFPR(7)',
    '_ARCOF(7)',
    '_ARQTA(7,1)',
    '_ARQTA(7,2)',
    '_ARQTA(7,3)',
    '_ARVAL(7)',
    '_ARSCQ(7,1)',
    '_ARSCQ(7,2)',
    '_ARSCQ(7,3)',
    '_ARSCQ(7,4)',
    '_ARFOR(8)',
    '_ARGGR(8)',
    '_ARLOT(8)',
    '_ARFPR(8)',
    '_ARCOF(8)',
    '_ARQTA(8,1)',
    '_ARQTA(8,2)',
    '_ARQTA(8,3)',
    '_ARVAL(8)',
    '_ARSCQ(8,1)',
    '_ARSCQ(8,2)',
    '_ARSCQ(8,3)',
    '_ARSCQ(8,4)',
    '_ARFOR(9)',
    '_ARGGR(9)',
    '_ARLOT(9)',
    '_ARFPR(9)',
    '_ARCOF(9)',
    '_ARQTA(9,1)',
    '_ARQTA(9,2)',
    '_ARQTA(9,3)',
    '_ARVAL(9)',
    '_ARSCQ(9,1)',
    '_ARSCQ(9,2)',
    '_ARSCQ(9,3)',
    '_ARSCQ(9,4)',
    'SCOSULIST10',
    'SCOSULIST11',
    'SCOSULIST12',
    'SCOSULIST13',
    'SCOSULIST14',
    'SCOSULIST15',
    'SCOSULIST16',
    'SCOSULIST17',
    'SCOSULIST18',
    'PRZSULIST10',
    'PRZSULIST11',
    'PRZSULIST12',
    'PRZSULIST13',
    'PRZSULIST14',
    'PRZSULIST15',
    'PRZSULIST16',
    'PRZSULIST17',
    'PRZSULIST18',
    'CODAGEN10',
    'CONDAGE10',
    'TIPPROV10',
    'FORMULA10',
    'CODAGEN11',
    'CONDAGE11',
    'TIPPROV11',
    'FORMULA11',
    'CODAGEN12',
    'CONDAGE12',
    'TIPPROV12',
    'FORMULA12',
    'CODAGEN13',
    'CONDAGE13',
    'TIPPROV13',
    'FORMULA13',
    'CODAGEN14',
    'CONDAGE14',
    'TIPPROV14',
    'FORMULA14',
    'CODAGEN15',
    'CONDAGE15',
    'TIPPROV15',
    'FORMULA15',
    'CODAGEN16',
    'CONDAGE16',
    'TIPPROV16',
    'FORMULA16',
    'CODAGEN17',
    'CONDAGE17',
    'TIPPROV17',
    'FORMULA17',
    'CODAGEN18',
    'CONDAGE18',
    'TIPPROV18',
    'FORMULA18',    
    ]

# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
# Conversion function for CSV file:
def now():
    ''' Return datetime string
    '''
    now = '%s' % datetime.now()
    return now.replace('/', '_').replace(':', '-').split('.')[0]
    
def csv_float(value, price_decimal=3):
    ''' Return string from float passed (decimal is a parameter)
    '''
    if not value or type(value) != float:
        value = 0.0
        
    mask = '%%20.%sf' % price_decimal
    return (mask % value).strip().replace('.', ',')

def csv_uom(value):
    ''' String conversion of UM
    '''
    return (value or '').upper()

def csv_vat(value):
    ''' VAT conversion in string
    '''
    return str(int(value))

def csv_text(value, limit):
    ''' CSV limited text (for write in file)
    '''
    return value[:limit]

def get_code(value):
    ''' String data code (manage float problem)
    '''
    if type(value) == float:
        return '%s' % int(value)
    elif value:
        return value.strip()
    else:
        return ''

def get_ascii_name(value):
    ''' Clean extra ascii char and remove it (or replace managed char)
    '''
    if not value:
        return ''
        
    res = ''
    for c in value.strip():
        if c == ';':
            res += ','
        elif ord(c) < 127:
            res += c
        elif c == u'\xb0': # °
            res += 'o'
        else:
            pass
    return res        

def file_log_data(f_log, event, mode='INFO', newline='\n\r'):
    ''' Log data in event format
    '''
    f_log.write('[%s] %s: %s%s' % (mode, datetime.now(), event, newline))
    return True

# -----------------------------------------------------------------------------
# Read all files in XLS folder:
# -----------------------------------------------------------------------------
# SINGLE FILE: Open output file and write header:
f_csv = open(file_csv, 'w')
f_csv.write(';'.join(header) + newline)
for root, dirs, files in os.walk(path_xls):
    for filename_xls in files:
        is_error = False
        default_discount = False
        discount_category = False
        f_split = filename_xls.split('.')
        if len(f_split) != 3 or \
                not f_split[0].isdigit() or \
                not f_split[1].isdigit() or \
                len(f_split[0]) != 3 or \
                len(f_split[1]) != 5 or \
                f_split[2].lower() not in ('xls' or 'xlsx'):
            file_log_data(
               f_log, 
               'Formato errato: %s (usare: 000.00000.xls)' % file_xls, 
               mode='ERROR',
               newline=newline,
               )
            continue    
                
        file_xls = os.path.join(path_xls, filename_xls)
        done_file_xls = os.path.join(
            path_done_xls, 
            '%s.%s' % (now(), filename_xls),
            )
        file_log_xls = os.path.join(path_log_xls, '%s.%s.txt' % (
            filename_xls, now()))
        f_log_xls = open(file_log_xls, 'w')

        supplier_code = ''.join(f_split[:-1])   
        try:
           WB = xlrd.open_workbook(file_xls)
           file_log_data(
               f_log, 
               'Aperto file XLS: %s' % file_xls, 
               newline=newline)
        except:
            is_error = True
            file_log_data(
               f_log, 
               'File XLS non leggibile: %s' % file_xls, 
               mode='ERROR',
               newline=newline,
               )
            continue
        WS = WB.sheet_by_index(0)

        # ---------------------------------------------------------------------
        # Load pricelist and create CSV
        # ---------------------------------------------------------------------
        i = 0

        file_log_data(
            f_log_xls, 
            u'%s. File da importare: %s [Tot.: %s]' % (i, file_xls, WS.nrows),   
            newline=newline,
            )
        for row in range(row_start, WS.nrows):
            i += 1
            
            # -----------------------------------------------------------------
            # Read columns from pricelist XLS:
            # -----------------------------------------------------------------
            default_code = get_code(WS.cell(row, 0).value)
            if not default_code:
                file_log_data(
                    f_log_xls, 
                    u'%s. Saltata riga senza codice' % i,
                    mode='WARNING',
                    newline=newline,
                    )
                continue        
                
            name = get_ascii_name(WS.cell(row, 1).value)
            price = WS.cell(row, 2).value
            vat = WS.cell(row, 3).value
            uom = WS.cell(row, 4).value
            
            if default_discount == False:
                discount = WS.cell(row, 5).value # Supplier discount values
                if discount:
                    default_discount = discount
                else:
                    default_discount = ''

            if discount_category == False:
                discount_category = str(
                    WS.cell(row, 6).value or '').rstrip('.0')

            # Transform data read:
            name_csv = csv_text(name, name_limit)
            name1 = name_csv[:name_split]
            name2 = name_csv[name_split:]
            
            # Test if is data line:
            if default_code in no_line_text:
                file_log_data(
                    f_log_xls, 
                    u'%s. Saltata riga intestazione: %s' % (i, default_code),
                    mode='WARNING',
                    newline=newline,
                    )
                continue        
            if not price or type(price) != float:
                file_log_data(
                    f_log_xls, 
                    u'%s. Saltata riga senza prezzo' % i,
                    mode='WARNING',
                    newline=newline,
                    )
                continue

            record = [
                'A', #_ARTIP',
                csv_text(default_code, code_limit), #_ARCOD',
                name1, #_ARDES',
                name2, #_ARAGG',
                '', #_ARALT',       
                '', #_ARANN',
                '', #_ARSOS',
                '', #_ARNDS(1)',
                '', #_ARNDE(1)',
                '', #_ARNDT(1)',       
                '', #_ARNDS(2)',
                '', #_ARNDE(2)',
                '', #_ARNDT(2)',
                '', #_ARDTC',
                '', #_ARDTA',       
                '', #_ARDSL(1)',
                '', #_ARDSL(2)',
                '', #_ARDSL(3)',
                '', #_ARDSL(4)',
                '', #_ARDSL(5)',       
                '', #_ARDSL(6)',
                '', #_ARDSL(7)',
                '', #_ARDSL(8)',
                '', #_ARDSL(9)',
                csv_vat(vat), #_ARIVA',       
                csv_uom(uom), #_ARUM1',
                '', #_ARUM2',
                '', #_ARDEC',
                '', #_ARKOEPTA',
                '', #_ARCON',       
                '', #_ARSTA',
                '', #_ARSTN',
                '', #_ARTCO',
                '', #_ARSTR',
                currency_id, #_ARVST',       
                currency_id, #_ARVUL',
                currency_id, #_ARVUP',
                '', #_ARSST',
                '', #_ARCUL',
                '', #_ARCUP',       
                '', #_ARRIC',
                '', #_ARCOS',
                discount_category, #_ARSCO',
                '', #_ARSCQ',
                '', #_ARLIS',       
                '1', #_ARTPR',
                '', #_ARIMB',
                '', #_ARQPR',
                '', #_ARQPA',
                csv_float(price, price_decimal), #_ARPRZ(1)',       
                '', #_ARPRZ(2)',
                '', #_ARPRZ(3)',
                '', #_ARPRZ(4)',
                '', #_ARPRZ(5)',
                '', #_ARPRZ(6)',       
                '', #_ARPRZ(7)',
                '', #_ARPRZ(8)',
                '', #_ARPRZ(9)',
                '', #_AREXG',
                '', #_AREXA',       
                '', #_AREXB',
                '', #_AREXC',
                '', #_ARMFTCPS',
                '', #_ARDBP',
                '', #_ARDBV',       
                '', #_ARCAR',
                '', #_ARDBA',
                '', #_ARCTG',
                '', #_ARFRM',
                '', #CALENDPROD',       
                '', #_ARPRE',
                '', #_ARTMO',
                '', #_ARVMO',
                '', #_ARSMO',
                '', #_ARAMO',       
                '', #_ARRRO',
                '', #_ARRST',
                '', #_ARTDE',
                supplier_code, #_ARFOR(1)',
                '', #_ARGGR(1)',       
                '', #_ARLOT(1)',
                csv_float(price, price_decimal), #_ARFPR(1)',
                '', #_ARCOF(1)',
                '', #_ARQTA(1,1)',
                '', #_ARQTA(1,2)',        
                '', #_ARQTA(1,3)',
                '', #_ARVAL(1)',
                '', #_ARSCQ(1,1)',
                '', #_ARSCQ(1,2)',
                '', #_ARSCQ(1,3)',        
                default_discount, #_ARSCQ(1,4)',
                '', #_ARFOR(2)',
                '', #_ARGGR(2)',
                '', #_ARLOT(2)',
                '', #_ARFPR(2)',        
                '', #_ARCOF(2)',
                '', #_ARQTA(2,1)',
                '', #_ARQTA(2,2)',
                '', #_ARQTA(2,3)',
                '', #_ARVAL(2)',        
                '', #_ARSCQ(2,1)',
                '', #_ARSCQ(2,2)',
                '', #_ARSCQ(2,3)',
                '', #_ARSCQ(2,4)',
                '', #_ARFOR(3)',        
                '', #_ARGGR(3)',
                '', #_ARLOT(3)',
                '', #_ARFPR(3)',
                '', #_ARCOF(3)',
                '', #_ARQTA(3,1)',        
                '', #_ARQTA(3,2)',
                '', #_ARQTA(3,3)',
                '', #_ARVAL(3)',
                '', #_ARSCQ(3,1)',
                '', #_ARSCQ(3,2)',        
                '', #_ARSCQ(3,3)',
                '', #_ARSCQ(3,4)',
                '', #SCOSULIST1',
                '', #SCOSULIST2',
                '', #SCOSULIST3',        
                '', #SCOSULIST4',
                '', #SCOSULIST5',
                '', #SCOSULIST6',
                '', #SCOSULIST7',
                '', #SCOSULIST8',        
                '', #SCOSULIST9',
                '', #PRZSULIST1',
                '', #PRZSULIST2',
                '', #PRZSULIST3',
                '', #PRZSULIST4',        
                '', #PRZSULIST5',
                '', #PRZSULIST6',
                '', #PRZSULIST7',
                '', #PRZSULIST8',
                '', #PRZSULIST9',        
                '', #_ARVEX',
                '', #_ARPPER',
                '', #_ARPRIT',
                '', #_ARPCAS',
                '', #_ARPMES',        
                '', #_ARINO',
                '', #_ARIMA',
                '', #_ARIKM',
                '', #_ARIUS',
                '', #_ARIDU',        
                '', #_ARIKU',
                '', #_ARIPR',
                '', #_ARIPA',
                '', #_ARRDT',
                '', #_ARRRI',        
                '', #_ARRTL',
                '', #_ARRSA',
                '', #CODAGEN1',
                '', #CONDAGE1',
                '', #TIPPROV1',        
                '', #FORMULA1',
                '', #CODAGEN2',
                '', #CONDAGE2',
                '', #TIPPROV2',
                '', #FORMULA2',        
                '', #CODAGEN3',
                '', #CONDAGE3',
                '', #TIPPROV3',
                '', #FORMULA3',
                '', #CODAGEN4',        
                '', #CONDAGE4',
                '', #TIPPROV4',
                '', #FORMULA4',
                '', #CODAGEN5',
                '', #CONDAGE5',        
                '', #TIPPROV5',
                '', #FORMULA5',
                '', #CODAGEN6',
                '', #CONDAGE6',
                '', #TIPPROV6',        
                '', #FORMULA6',
                '', #CODAGEN7',
                '', #CONDAGE7',
                '', #TIPPROV7',
                '', #FORMULA7',        
                '', #CODAGEN8',
                '', #CONDAGE8',
                '', #TIPPROV8',
                '', #FORMULA8',
                '', #CODAGEN9',        
                '', #CONDAGE9',
                '', #TIPPROV9',
                '', #FORMULA9',
                '', #GRPMERCE',
                '', #NATURA',        
                '', #_ARPRIT1',
                '', #_ARIMM',
                '', #_ARCAT',
                '', #_ARICO',
                '', #_ARIVS',        
                '', #_ARAGR',
                '', #MINFATT',
                '', #MAXFATT',
                '', #ARGSI',
                '', #_ARFOR(4)',        
                '', #_ARGGR(4)',
                '', #_ARLOT(4)',
                '', #_ARFPR(4)',
                '', #_ARCOF(4)',
                '', #_ARQTA(4,1)',        
                '', #_ARQTA(4,2)',
                '', #_ARQTA(4,3)',
                '', #_ARVAL(4)',
                '', #_ARSCQ(4,1)',
                '', #_ARSCQ(4,2)',        
                '', #_ARSCQ(4,3)',
                '', #_ARSCQ(4,4)',
                '', #_ARFOR(5)',
                '', #_ARGGR(5)',
                '', #_ARLOT(5)',        
                '', #_ARFPR(5)',
                '', #_ARCOF(5)',
                '', #_ARQTA(5,1)',
                '', #_ARQTA(5,2)',
                '', #_ARQTA(5,3)',        
                '', #_ARVAL(5)',
                '', #_ARSCQ(5,1)',
                '', #_ARSCQ(5,2)',
                '', #_ARSCQ(5,3)',
                '', #_ARSCQ(5,4)',        
                '', #_ARFOR(6)',
                '', #_ARGGR(6)',
                '', #_ARLOT(6)',
                '', #_ARFPR(6)',
                '', #_ARCOF(6)',        
                '', #_ARQTA(6,1)',
                '', #_ARQTA(6,2)',
                '', #_ARQTA(6,3)',
                '', #_ARVAL(6)',
                '', #_ARSCQ(6,1)',        
                '', #_ARSCQ(6,2)',
                '', #_ARSCQ(6,3)',
                '', #_ARSCQ(6,4)',
                '', #_ARFOR(7)',       
                '', #_ARGGR(7)',
                '', #_ARLOT(7)',
                '', #_ARFPR(7)',
                '', #_ARCOF(7)',
                '', #_ARQTA(7,1)',        
                '', #_ARQTA(7,2)',
                '', #_ARQTA(7,3)',
                '', #_ARVAL(7)',
                '', #_ARSCQ(7,1)',
                '', #_ARSCQ(7,2)',        
                '', #_ARSCQ(7,3)',
                '', #_ARSCQ(7,4)',
                '', #_ARFOR(8)',
                '', #_ARGGR(8)',
                '', #_ARLOT(8)',        
                '', #_ARFPR(8)',
                '', #_ARCOF(8)',
                '', #_ARQTA(8,1)',
                '', #_ARQTA(8,2)',
                '', #_ARQTA(8,3)',        
                '', #_ARVAL(8)',
                '', #_ARSCQ(8,1)',
                '', #_ARSCQ(8,2)',
                '', #_ARSCQ(8,3)',
                '', #_ARSCQ(8,4)',        
                '', #_ARFOR(9)',
                '', #_ARGGR(9)',
                '', #_ARLOT(9)',
                '', #_ARFPR(9)',
                '', #_ARCOF(9)',        
                '', #_ARQTA(9,1)',
                '', #_ARQTA(9,2)',
                '', #_ARQTA(9,3)',
                '', #_ARVAL(9)',
                '', #_ARSCQ(9,1)',        
                '', #_ARSCQ(9,2)',
                '', #_ARSCQ(9,3)',
                '', #_ARSCQ(9,4)',
                '', #SCOSULIST10',
                '', #SCOSULIST11',        
                '', #SCOSULIST12',
                '', #SCOSULIST13',
                '', #SCOSULIST14',
                '', #SCOSULIST15',
                '', #SCOSULIST16',        
                '', #SCOSULIST17',
                '', #SCOSULIST18',
                '', #PRZSULIST10',
                '', #PRZSULIST11',
                '', #PRZSULIST12',        
                '', #PRZSULIST13',
                '', #PRZSULIST14',
                '', #PRZSULIST15',
                '', #PRZSULIST16',
                '', #PRZSULIST17',        
                '', #PRZSULIST18',
                '', #CODAGEN10',
                '', #CONDAGE10',
                '', #TIPPROV10',
                '', #FORMULA10',        
                '', #CODAGEN11',
                '', #CONDAGE11',
                '', #TIPPROV11',
                '', #FORMULA11',
                '', #CODAGEN12',        
                '', #CONDAGE12',
                '', #TIPPROV12',
                '', #FORMULA12',
                '', #CODAGEN13',
                '', #CONDAGE13',        
                '', #TIPPROV13',
                '', #FORMULA13',
                '', #CODAGEN14',
                '', #CONDAGE14',
                '', #TIPPROV14',        
                '', #FORMULA14',
                '', #CODAGEN15',
                '', #CONDAGE15',
                '', #TIPPROV15',
                '', #FORMULA15',        
                '', #CODAGEN16',
                '', #CONDAGE16',
                '', #TIPPROV16',
                '', #FORMULA16',
                '', #CODAGEN17',        
                '', #CONDAGE17',
                '', #TIPPROV17',
                '', #FORMULA17',
                '', #CODAGEN18',
                '', #CONDAGE18',        
                '', #TIPPROV18',
                '', #FORMULA18',
                ]            
            f_csv.write(u';'.join(record) + newline)

            # Check error:    
            error = u''    
            if len(default_code) > code_limit:
                error += u'[Codice troncato]'
            if len(name) > name_limit:    
                error += u'[Nome troncato da %s a %s]' % (
                    len(name), name_limit)
            
            # Write log line:
            file_log_data(
                f_log_xls, 
                u'%s. Riga importata: %s %s' % (i, default_code, error),
                mode=u'WARNING' if error else u'INFO', 
                newline=newline,
                )
                
        file_log_data(
            f_log, 
            'Chiuso file XLS [Righe lette: %s]: %s' % (file_xls, i), 
            newline=newline)
        
        # ---------------------------------------------------------------------
        # History the file:   
        # ---------------------------------------------------------------------
        if not is_error:
            shutil.move(file_xls, done_file_xls)
            file_log_data(
                f_log, 
                'Storicizzato il file in: %s' % done_file_xls, 
                newline=newline,
                )
        else:       
            file_log_data(
                f_log, 
                'Errore elaborando il file non storicizzato: %s' % file_xls, 
                newline=newline,
                )
        # Close mono file log:   
        f_log_xls.close()
f_log.close()
