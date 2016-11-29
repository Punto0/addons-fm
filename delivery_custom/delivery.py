# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import time
from openerp.osv import fields,osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval

_logger = logging.getLogger(__name__)

class delivery_carrier(osv.osv):
    _name = "delivery.carrier"
    _inherit = "delivery.carrier"
    _description = "Carrier"
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Transport Company', required=False, help="The partner that is doing the delivery service."),
        'product_id': fields.many2one('product.product', 'Delivery Product', required=False),
    }

    def create(self, cr, uid, vals, context=None):
        vals['product_id'] = self.pool.get('product.product').search(cr, uid, [('name','=','Generic Transport')])[0]
        vals['partner_id'] = self.pool.get('res.users').browse(cr,uid,uid,context=context).company_id.partner_id.id
        res_id = super(delivery_carrier, self).create(cr, uid, vals, context=context)
        self.create_grid_lines(cr, uid, [res_id], vals, context=context)
        return res_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
