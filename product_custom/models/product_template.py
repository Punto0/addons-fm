# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# product_custom for Odoo                                                     #
# Copyright (C) 2017 Santi (<santi@þunto0.org>).                              #
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
        else:
            new_vals = vals
        return super(ProductTemplateCustom, self).write(new_vals)

    @api.model
    def create(self, vals):
        if not vals.get('categ_id'):
	    vals['categ_id'] = self.env['product.category'].search([('name','=','Normal')])[0]
        if 'discount' in vals:
            new_vals = self.set_style(vals)
        else:
            new_vals = vals
        return super(ProductTemplateCustom, self).create(new_vals)

    def set_style(self, vals):
        style = self.env.ref("website_sale.image_promo")
        if vals.get('discount',False):
            vals['website_style_ids'] = [[4, style.id, []]]
            vals['categ_id'] = self.env.ref('product_custom.product_category_discount_campaign').id
        else:
            vals['website_style_ids'] = [[3, style.id, []]]
            vals['categ_id'] = self.env.ref('product_custom.product_category_normal').id
        return vals
