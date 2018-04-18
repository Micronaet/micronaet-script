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
# -----------------------------------------------------------------------------
# ODOO Connection:
# -----------------------------------------------------------------------------
odoo_server = 'localhost'
odoo_port = 8069
odoo_user = 'admin'
odoo_password = 'password'
odoo_database = 'dbname'

# -----------------------------------------------------------------------------
# Setup demo mode
# -----------------------------------------------------------------------------
demo = True

# -----------------------------------------------------------------------------
# Folder are a list of element for manage input folders:
# -----------------------------------------------------------------------------
#     (KEY, PATH, ESTENSION, WALK)
#
#     > KEY: start name of output dropbox file (must be unique!)
#     > PATH: Path of the folder
#     > Estension: list of valid estension (no case check) XXX always uppercase
#     > Walk subfolder element

input_folders = [
    ('CHROMA', '~/company/chroma', [
        # UPPER CASE!!!
        ], False),
    ('ENVIRONMENT', '~/company/environment', [
        # UPPER CASE!!!
        ], False),
    ]

# -----------------------------------------------------------------------------
# Drobbox root folder:
# -----------------------------------------------------------------------------
dropbox_path = '~/dropbox/product'

# -----------------------------------------------------------------------------
# List of 2 elements tuple for replate in dropbox filename some char
# -----------------------------------------------------------------------------
# For filename:
file_replace_char = [
    ('_', ' '),
    ]
# For folder product name:    
folder_replace_char = [
    ('_', ' '),
    ]

# -----------------------------------------------------------------------------
# Product name beginning char to consider:
# -----------------------------------------------------------------------------
# Es. 127TX_ANBIBES.001.jpeg >> 127TX_ANBIBE (Folder that will be created)
product_part = 12 # Folder product name
parent_part = 3 # Folder parent name (if all numeric)

no_family_name = 'NON CLASSIFICATO'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
