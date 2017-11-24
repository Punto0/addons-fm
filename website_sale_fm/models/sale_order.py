# -*- coding: utf-8 -*-

from openerp.osv import orm, fields

class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    _columns = {
        'user_id': fields.many2one('res.users', 'Salesperson', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True, track_visibility='never'),
    }
