# -*- coding: utf-8 -*-
import logging

from openerp import api, models, fields, osv, _

class res_company(models.Model):
  _name = "res.company"
  _inherit = ['res.company']
  discount = fields.Boolean(string="Discount campaign.", 
                   help="This shop participates in the discount campaign.", 
                   default=False)
  description = fields.Text('Description', 
                      help="A text about your project or your products. It will be showed in your shop page and at the side of your products pages.", 
                      translate=True)
  logo2 = fields.Binary('Second Logo File')
  product_ids = fields.One2many(
    'product.template',
    'company_id',
    string='Shop Products',
  )
  products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
  )
  company_supplier = fields.Boolean(string="Sell in Collective Orders", related='partner_id.supplier',
                                    help="This brand apply for collective orders. Please, contact the admin team before planning a collective purchase.")

  @api.one
  @api.depends('product_ids')
  def _get_products_count(self):
    self.products_count = len(self.product_ids)

  def check_discount(self):
    for p in self.product_ids:
      if p.discount:
        self.discount = True
        return True
    self.discount = False
    return False
