# -*- coding: utf-8 -*-
import logging

from openerp import models, fields, osv, _

class ProductBrand(models.Model):
  _inherit = 'product.brand'
  user_id = fields.Many2one('res.users','User',help="User authorized for this Brand")
  company_id = fields.Many2one(
        'res.company',
        string='Project',
        help='Select a project for this brand',
        ondelete='restrict')
  company_name = fields.Char(string='Name of the Company', related='company_id.name')
  company_logo = fields.Binary(string="Another Logo",related="company_id.logo")
  company_parent_id = fields.Many2one(string="Parent company",related='company_id.parent_id')
  company_partner_id = fields.Many2one(string="Partner asociated", related='company_id.partner_id')
  company_street = fields.Char(string="Street", related='company_id.street')
  company_city = fields.Char(string="City", related='company_id.city')
  company_state_id = fields.Many2one(string="State",related='company_id.state_id')
  company_zip = fields.Char(string="ZIP", related='company_id.zip')
  company_country_id = fields.Many2one(string="Country", related='company_id.country_id')
  company_rml_header1 = fields.Char(string="Short description", related='company_id.rml_header1')
  company_website = fields.Char(string="Website",related='company_id.website') 
  company_phone = fields.Char(string="phone", related='company_id.phone')
  company_email = fields.Char(string="email", related='company_id.email')
  company_faircoin_account = fields.Char(string="FairCoin address", related='company_id.faircoin_account')
  company_sale_note = fields.Text(string="Terms and Conditions",related='company_id.sale_note')
  company_supplier = fields.Boolean(string="Sell in Collective Orders", related='company_id.partner_id.supplier')

  def button_save(self, cr, uid, vals, context=None):
        return {'type': 'ir.actions.act_window_close'}

  def search_brand(self, cr, uid, vals, context=None):
    logging.info("search_brand")
    # Devuelve la ficha en edición de la marca del usuario
    brand_ids = self.pool.get('product.brand').search(cr, uid, [('user_id','=',uid)], context=context)
    logging.info("Brand ids %s" %brand_ids)
    view_list = self.pool.get('ir.ui.view').search_read(cr, uid, [('name','=','product.brand.form')],context=context )
    for view in view_list:
      if view['xml_id'] == 'product_brand.view_product_brand_form':
        view_id = view['id']
        break 
    logging.info("view id : %s" %view_id)
    # Fin de la chapuza
    context['view_buttons'] = True
    view = {
      'name': _('Project Configuration'),
      'view_type': 'form',
      'view_mode': 'form',
      'res_model': 'product.brand',
      'view_id': view_id,
      'type': 'ir.actions.act_window',
      'target': 'inline',
      'readonly': False,
      'context': context,
      'res_id': brand_ids[0],
    }
    return view  
