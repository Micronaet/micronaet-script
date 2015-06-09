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

import erppeek

f_out = 'inventory.csv'
f = open(f_out, 'w')

odoo = erppeek.Client(
    'http://localhost:18069', 
    db='database', 
    user='admin', 
    password='password')

inventory = odoo.model('stock.inventory.line')
inventory_ids = inventory.search([])
for item in inventory.browse(inventory_ids):
    f.write("%s;%s\n") % (
        item.id,
        item.product_id.name,
        )
f.close()        
