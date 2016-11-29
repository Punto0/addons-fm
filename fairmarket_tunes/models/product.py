# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv, fields
import logging

_logger = logging.getLogger(__name__)

class product_template(osv.Model):
    _inherit = "product.template"
    #_column = {'my_field': fields.char('My new field')}

    def create(self, cr, uid, vals, context=None):
        ''' save the product brand automatically '''
        product_template_id = super(product_template, self).create(cr, uid, vals, context=context)
        brand_id = self.pool['product.brand'].search(cr, uid, [('company_id', '=', vals['company_id'])], context=context)
        if brand_id:
            related_vals = {}
            related_vals['product_brand_id'] = brand_id[0]
            self.write(cr, uid, product_template_id, related_vals, context=context)

        return product_template_id

