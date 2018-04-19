# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# product_custom for Odoo                                                     #
# Copyright (C) 2017 - 2018 Santi (<santi@punto0.org>).                              #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as              #
# published by the Free Software Foundation, either version 3 of the          #
# License, or (at your option) any later version.                             #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
from openerp import models, fields, api
import logging

class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(
         [('consu', 'Consumable'),('service','Service')],
         'Product Type',
         required=True,
         default='consu',
         help="Consumable: Apply delivery methods but not stock.\nService: Non-material product, does not apply delivery methods nor stock.",
	)
    discount = fields.Boolean('Campaign discount',help="This product apply the 1:1 campaign and it will have a 20% discount on the price.")

    # onchange no permite la actualizacion de campos many2many, lo hacemos aqui
    @api.one
    def write(self, vals):
        if 'discount' in vals:
            new_vals = self.set_style(vals)
            self.set_discount_company(vals.get('discount'),vals.get('company_id', False))
        else:
            new_vals = vals
        return super(ProductTemplateCustom, self).write(new_vals)

    @api.model
    def create(self, vals):
        ''' Set the style and category'''
        if vals.get('discount', False):
            new_vals = self.set_style(vals)
        else:
            new_vals = vals
            new_vals['categ_id'] = self.env.ref('product_custom.product_category_normal').id # Default cat
        ''' save the product brand automatically '''
        company_id = False
        if not vals.get('company_id'):
            company_id = self.env['res.company'].search([('id', '=', vals['company_id'])])
            if company_id:
                vals['company_id'] = company_id.id
        else:
            company_id = self.env['res.company'].browse(vals.get('company_id'))
        p = super(ProductTemplateCustom, self).create(new_vals)
        ''' check for discount on  the shop'''
        company_id.check_discount()
        return p

    def set_style(self, vals):
        style = self.env.ref("website_sale.image_promo")
        if vals.get('discount', False):
            vals['website_style_ids'] = [[4, style.id, []]]
            vals['categ_id'] = self.env.ref('product_custom.product_category_discount_campaign').id
        else:
            vals['website_style_ids'] = [[3, style.id, []]]
            vals['categ_id'] = self.env.ref('product_custom.product_category_normal').id
        return vals

    def set_discount_company(self, discount, company_id = None):
        logging.debug("set_discount_company : %s -- %s" %(discount, company_id))
        if company_id:
            company_obj = self.env['res.company'].browse(brand_id)
        else:
            company_obj = self.company_id
        res = company_obj.check_discount()
        # logging.info("res\n%s" %res)
        return True
