# -*- coding: utf-8 -*-

from openerp import models, fields, api

class product_template(models.Model):
    _inherit = "product.template"

    def create(self, vals, context=None):
        ''' save the product brand automatically '''
        product_template_id = super(product_template, self).create(vals, context=context)
        brand_id = self.env['product.brand'].search([('company_id', '=', vals['company_id'])], context=context)
        if brand_id:
            related_vals = {}
            related_vals['product_brand_id'] = brand_id[0]
            self.write(product_template_id, related_vals, context=context)

        return product_template_id

