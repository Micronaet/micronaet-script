#!environment python
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
import barcode

# Parameters:
file_ean = 'ean.csv'
ean_part = '8000001'

eans = []
double = 0
for ean in open(file_ean, 'r'):
    if ean.startswith(ean_gpb):
        ean_code = ean[7:12]
        if ean_code in eans:
            double += 1
        else:   
            eans.append(ean_code)

free = 0
EAN = barcode.get_barcode_class('ean13')
for i in range(1, 100000):
    ean_code = '%05d' % i
    if ean_code in eans:
        continue
        
    free += 1    
    ean12 = '%s%s' % (ean_part, ean_code)
    ean = EAN(ean12)
    ean13 = ean.get_fullcode()
    print ean13

print 'Used: %s - Double: %s - Free %s' % (
    len(eans),
    double,
    free,
    )
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

