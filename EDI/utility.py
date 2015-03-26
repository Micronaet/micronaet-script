# -*- coding: utf-8 -*-
###############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

# Constant (for log):
DATETIME_FORMAT = "%Y%m%d_%H%M%S"
DATETIME_FORMAT_LOG = "%Y/%m/%d %H:%M:%S"

# -----------------------------------------------------------------------------
#                                  Utility:
# -----------------------------------------------------------------------------
def log_event(comment, log_type='info'):
    ''' Log on file the operations
    '''
    log_file.write("[%s] %s >> %s\n" % (
        log_type,
        datetime.now().strftime(DATETIME_FORMAT_LOG),
        comment, 
        ))
    return True    

def new_file(invoice):
    ''' Operation for get new file:
    '''
    out_filename = join(output_folder, invoice)
    log_event("Output on file: %s" % out_filename)
    return open(out_filename, 'w') 

