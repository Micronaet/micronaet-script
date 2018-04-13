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

header = [
    '_ARTIP', '_ARCOD', '_ARDES', '_ARAGG', '_ARALT',
    '_ARANN', '_ARSOS', '_ARNDS(1)', '_ARNDE(1)', '_ARNDT(1)',
    '_ARNDS(2)', '_ARNDE(2)', '_ARNDT(2)', '_ARDTC', '_ARDTA',
    '_ARDSL(1)', '_ARDSL(2)', '_ARDSL(3)', '_ARDSL(4)', '_ARDSL(5)',
    '_ARDSL(6)', '_ARDSL(7)', '_ARDSL(8)', '_ARDSL(9)', '_ARIVA',
    '_ARUM1', '_ARUM2', '_ARDEC', '_ARKOEPTA', '_ARCON',
    '_ARSTA', '_ARSTN', '_ARTCO', '_ARSTR', '_ARVST',
    '_ARVUL', '_ARVUP', '_ARSST', '_ARCUL', '_ARCUP',
    '_ARRIC', '_ARCOS', '_ARSCO', '_ARSCQ', '_ARLIS',
    '_ARTPR', '_ARIMB', '_ARQPR', '_ARQPA', '_ARPRZ(1)',
    '_ARPRZ(2)', '_ARPRZ(3)', '_ARPRZ(4)', '_ARPRZ(5)', '_ARPRZ(6)',
    '_ARPRZ(7)', '_ARPRZ(8)', '_ARPRZ(9)',  '_AREXG', '_AREXA',
    '_AREXB', '_AREXC', '_ARMFTCPS', '_ARDBP', '_ARDBV',
    '_ARCAR', '_ARDBA', '_ARCTG', '_ARFRM', 'CALENDPROD',
    '_ARPRE', '_ARTMO', '_ARVMO', '_ARSMO', '_ARAMO',
    '_ARRRO', '_ARRST', '_ARTDE', '_ARFOR(1)', '_ARGGR(1)',
    '_ARLOT(1)', '_ARFPR(1)', '_ARCOF(1)', '_ARQTA(1,1)', '_ARQTA(1,2)', 
    '_ARQTA(1,3)', '_ARVAL(1)', '_ARSCQ(1,1)', '_ARSCQ(1,2)', '_ARSCQ(1,3)', 
    '_ARSCQ(1,4)', '_ARFOR(2)', '_ARGGR(2)', '_ARLOT(2)', '_ARFPR(2)', 
    '_ARCOF(2)', '_ARQTA(2,1)', '_ARQTA(2,2)', '_ARQTA(2,3)', '_ARVAL(2)', 
    '_ARSCQ(2,1)', '_ARSCQ(2,2)', '_ARSCQ(2,3)', '_ARSCQ(2,4)', '_ARFOR(3)', 
    '_ARGGR(3)', '_ARLOT(3)', '_ARFPR(3)', '_ARCOF(3)', '_ARQTA(3,1)', 
    '_ARQTA(3,2)', '_ARQTA(3,3)', '_ARVAL(3)', '_ARSCQ(3,1)', '_ARSCQ(3,2)', 
    '_ARSCQ(3,3)', '_ARSCQ(3,4)', 'SCOSULIST1', 'SCOSULIST2', 'SCOSULIST3', 
    'SCOSULIST4', 'SCOSULIST5', 'SCOSULIST6', 'SCOSULIST7', 'SCOSULIST8', 
    'SCOSULIST9', 'PRZSULIST1', 'PRZSULIST2', 'PRZSULIST3', 'PRZSULIST4', 
    'PRZSULIST5', 'PRZSULIST6', 'PRZSULIST7', 'PRZSULIST8', 'PRZSULIST9', 
    '_ARVEX', '_ARPPER', '_ARPRIT', '_ARPCAS', '_ARPMES', 
    '_ARINO', '_ARIMA', '_ARIKM', '_ARIUS', '_ARIDU', 
    '_ARIKU', '_ARIPR', '_ARIPA', '_ARRDT', '_ARRRI', 
    '_ARRTL', '_ARRSA', 'CODAGEN1', 'CONDAGE1', 'TIPPROV1', 
    'FORMULA1', 'CODAGEN2', 'CONDAGE2', 'TIPPROV2', 'FORMULA2', 
    'CODAGEN3', 'CONDAGE3', 'TIPPROV3', 'FORMULA3', 'CODAGEN4', 
    'CONDAGE4', 'TIPPROV4', 'FORMULA4', 'CODAGEN5', 'CONDAGE5', 
    'TIPPROV5', 'FORMULA5', 'CODAGEN6', 'CONDAGE6', 'TIPPROV6', 
    'FORMULA6', 'CODAGEN7', 'CONDAGE7', 'TIPPROV7', 'FORMULA7', 
    'CODAGEN8', 'CONDAGE8', 'TIPPROV8', 'FORMULA8', 'CODAGEN9', 
    'CONDAGE9', 'TIPPROV9', 'FORMULA9', 'GRPMERCE', 'NATURA', 
    '_ARPRIT1', '_ARIMM', '_ARCAT', '_ARICO', '_ARIVS', 
    '_ARAGR', 'MINFATT', 'MAXFATT', 'ARGSI', '_ARFOR(4)', 
    '_ARGGR(4)', '_ARLOT(4)', '_ARFPR(4)', '_ARCOF(4)', '_ARQTA(4,1)', 
    '_ARQTA(4,2)', '_ARQTA(4,3)', '_ARVAL(4)', '_ARSCQ(4,1)', '_ARSCQ(4,2)', 
    '_ARSCQ(4,3)', '_ARSCQ(4,4)', '_ARFOR(5)', '_ARGGR(5)', '_ARLOT(5)', 
    '_ARFPR(5)', '_ARCOF(5)', '_ARQTA(5,1)', '_ARQTA(5,2)', '_ARQTA(5,3)', 
    '_ARVAL(5)', '_ARSCQ(5,1)', '_ARSCQ(5,2)', '_ARSCQ(5,3)', '_ARSCQ(5,4)', 
    '_ARFOR(6)', '_ARGGR(6)', '_ARLOT(6)', '_ARFPR(6)', '_ARCOF(6)', 
    '_ARQTA(6,1)', '_ARQTA(6,2)', '_ARQTA(6,3)', '_ARVAL(6)', '_ARSCQ(6,1)', 
    '_ARSCQ(6,2)', '_ARSCQ(6,3)', '_ARSCQ(6,4)', '_ARFOR(7)',
    '_ARGGR(7)', '_ARLOT(7)', '_ARFPR(7)', '_ARCOF(7)', '_ARQTA(7,1)', 
    '_ARQTA(7,2)', '_ARQTA(7,3)', '_ARVAL(7)', '_ARSCQ(7,1)', '_ARSCQ(7,2)', 
    '_ARSCQ(7,3)', '_ARSCQ(7,4)', '_ARFOR(8)', '_ARGGR(8)', '_ARLOT(8)', 
    '_ARFPR(8)', '_ARCOF(8)', '_ARQTA(8,1)', '_ARQTA(8,2)', '_ARQTA(8,3)', 
    '_ARVAL(8)', '_ARSCQ(8,1)', '_ARSCQ(8,2)', '_ARSCQ(8,3)', '_ARSCQ(8,4)', 
    '_ARFOR(9)', '_ARGGR(9)', '_ARLOT(9)', '_ARFPR(9)', '_ARCOF(9)', 
    '_ARQTA(9,1)', '_ARQTA(9,2)', '_ARQTA(9,3)', '_ARVAL(9)', '_ARSCQ(9,1)', 
    '_ARSCQ(9,2)', '_ARSCQ(9,3)', '_ARSCQ(9,4)', 'SCOSULIST10', 'SCOSULIST11', 
    'SCOSULIST12', 'SCOSULIST13', 'SCOSULIST14', 'SCOSULIST15', 'SCOSULIST16', 
    'SCOSULIST17', 'SCOSULIST18', 'PRZSULIST10', 'PRZSULIST11', 'PRZSULIST12', 
    'PRZSULIST13', 'PRZSULIST14', 'PRZSULIST15', 'PRZSULIST16', 'PRZSULIST17', 
    'PRZSULIST18', 'CODAGEN10', 'CONDAGE10', 'TIPPROV10', 'FORMULA10', 
    'CODAGEN11', 'CONDAGE11', 'TIPPROV11', 'FORMULA11', 'CODAGEN12', 
    'CONDAGE12', 'TIPPROV12', 'FORMULA12', 'CODAGEN13', 'CONDAGE13', 
    'TIPPROV13', 'FORMULA13', 'CODAGEN14', 'CONDAGE14', 'TIPPROV14', 
    'FORMULA14', 'CODAGEN15', 'CONDAGE15', 'TIPPROV15', 'FORMULA15', 
    'CODAGEN16', 'CONDAGE16', 'TIPPROV16', 'FORMULA16', 'CODAGEN17', 
    'CONDAGE17', 'TIPPROV17', 'FORMULA17', 'CODAGEN18', 'CONDAGE18', 
    'TIPPROV18', 'FORMULA18',
    ]
    
# -----------------------------------------------------------------------------
# Parameters:
# -----------------------------------------------------------------------------
end_line = '\n\r'
row_start = 0
code_limit = 16
name_limit = 64
price_decimal = 3
currency_id = 11

current_path = os.path.dirname(__file__)
file_csv = os.path.join(current_path, 'CSV', 'anar_arc.csv')

filename_xls = '601.00055.xls'
file_xls = os.path.join(
    current_path,
    'XLS', 
    filename_xls,
    )
supplier_code = ''.join(
   filename_xls.split('.')[:-1]
   )

no_line_text = ('CODICE CATALOGO', )

# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
# Conversion function for CSV file:
def csv_float(value, price_decimal=3):
    if not value or type(value) != float:
        value = 0.0
        
    mask = '%%20.%sf' % price_decimal
    return (mask % value).strip().replace('.', ',')

def csv_uom(value):
    return (value or '').upper()

def csv_vat(value):
    return int(value)

def csv_text(value, limit):
    return value[:limit]

def get_code(value):
    if type(value) == float:
        return '%s' % int(value)
    elif value:
        return value.strip()
    else:
        return ''

def get_ascii_name(value):
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
    
# -----------------------------------------------------------------------------
# Load origin name from XLS
# -----------------------------------------------------------------------------
try:
   WB = xlrd.open_workbook(file_xls)
except:
   print '[ERROR] Cannot read XLS file: %s' % file_xls
   sys.exit()
WS = WB.sheet_by_index(0)

# -----------------------------------------------------------------------------
# Load pricelist and create CSV
# -----------------------------------------------------------------------------
pricelist_db = {}
i = 0

# Open output file and write header:
f_csv = open(file_csv, 'w')
f_csv.write(';'.join(header) + end_line)
print u'%s. [INFO] File da importare: %s [Tot.: %s]' % (i, file_xls, WS.nrows)

for row in range(row_start, WS.nrows):
    i += 1
    
    # Col read:
    default_code = get_code(WS.cell(row, 0).value)
    if not default_code:
        print u'%s. [WARNING] Saltata riga senza codice' % i
        continue        
        
    name = get_ascii_name(WS.cell(row, 1).value)
    name_csv = csv_text(name, name_limit)
    name1 = name_csv[:28]
    name2 = name_csv[28:]
    
    price = WS.cell(row, 2).value
    vat = WS.cell(row, 3).value
    uom = WS.cell(row, 4).value
    
    # Test if is data line:
    if default_code in no_line_text:
        print u'%s. [WARNING] Saltata riga di intestazione: %s' % (
            i, default_code)
        continue        
    if not price or type(price) != float:
        print u'%s. [WARNING] Saltata riga senza prezzo' % i
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
        csv_float(price, price_decimal), #_ARSST',
        '', #_ARCUL',
        '', #_ARCUP',       
        '', #_ARRIC',
        '', #_ARCOS',
        '', #_ARSCO',
        '', #_ARSCQ',
        '', #_ARLIS',       
        '1', #_ARTPR',
        '', #_ARIMB',
        '', #_ARQPR',
        '', #_ARQPA',
        '', #_ARPRZ(1)',       
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
        '', #_ARFPR(1)',
        '', #_ARCOF(1)',
        '', #_ARQTA(1,1)',
        '', #_ARQTA(1,2)',        
        '', #_ARQTA(1,3)',
        '', #_ARVAL(1)',
        '', #_ARSCQ(1,1)',
        '', #_ARSCQ(1,2)',
        '', #_ARSCQ(1,3)',        
        '', #_ARSCQ(1,4)',
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
        end_line,
        ]

    
    f_csv.write(u'A;%s;%s;%s;%20s%s;%s;%8s%s;%s;%s;%s;%7s%s;%32s%s;%251s%s' % (
        #csv_text(default_code, code_limit),
        #name1,
        #name2,
        ';' * 20,
        #csv_vat(vat),
        #csv_uom(uom),
        ';' * 8, 
        #currency_id,
        #currency_id,
        #currency_id,
        #csv_float(price, price_decimal),
        ';' * 7,
        #'1',
        ';' * 32,
        #supplier_code,
        ';' * 251,
        end_line,
        ))
     
    # Check error:    
    error = u''    
    if len(default_code) > code_limit:
        error += u'[Codice troncato]'
    if len(name) > name_limit:    
        error += u'[Nome troncato]'
    
    # Write log line:
    print u'%s. [%s] Riga importata: %s 	%s' % (
        i, 
        u'WARNING' if error else u'INFO', 
        default_code,
        error,
        )
                
