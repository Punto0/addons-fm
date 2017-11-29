# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ProductTemplateBrand(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals, context=None):
        ''' save the product brand automatically '''
        if not vals.get('product_brand_id'):
            brand_id = self.env['product.brand'].search([('company_id', '=', vals['company_id'])])
            if brand_id:
                vals['product_brand_id'] = brand_id.id
        return super(ProductTemplateBrand, self).create(vals)

