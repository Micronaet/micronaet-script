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
import barcode
# pip install pyBarcode


# Parameters:
ean12_file = 'ean_fiam.csv'
ean13_file = 'ean_fiam_13.csv'
ean_12_f = open(ean12_file, 'r')
ean_13_f = open(ean13_file, 'w')

EAN = barcode.get_barcode_class('ean13')

i = 0
for row in ean_12_f:
    ean12 = row.strip().split(';')[-1]
    if len(ean12) != 12:
        print 'Not EAN:', ean12
        continue
    else:
        i += 1
        ean = EAN(ean12)
        ean13 = ean.ean
        ean_13_f.write('%s%s\n' % (
            row.strip(),
            ean13[12],
            ))
        #print ean12, ean13, ean13[12]
        
        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
