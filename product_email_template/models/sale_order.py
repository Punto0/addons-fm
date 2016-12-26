# -*- coding: utf-8 -*-

import logging
from openerp.osv import osv

class sale_order(osv.Model):
    _inherit = 'sale.order'

    def sale_order_confirm_send_email(self, cr, uid, ids, context=None):
        Composer = self.pool['mail.compose.message']
        for order in self.browse(cr, uid, ids, context=context):
            # send template only on customer invoice
            #if invoice.type != 'out_invoice':
            #    continue
            # subscribe the partner to the sale oder if not
            if order.partner_id not in order.message_follower_ids:
                self.message_subscribe(cr, uid, [order.id], [order.partner_id.id], context=context)
            for line in order.order_line:
                if line.product_id.email_template_id:
                # CLEANME: should define and use a clean API: message_post with a template
                    composer_id = Composer.create(cr, uid, {
                        'model': 'sale.order',
                        'res_id': order.id,
                        'template_id': line.product_id.email_template_id.id,
                        'composition_mode': 'comment',
                        }, context=context)
                    template_values = Composer.onchange_template_id(
                          cr, uid, composer_id, line.product_id.email_template_id.id, 'comment', 'sale.order', order.id)['value']
                    template_values['attachment_ids'] = [(4, id) for id in template_values.get('attachment_ids', [])]
                    Composer.write(cr, uid, [composer_id], template_values, context=context)
                    Composer.send_mail(cr, uid, [composer_id], context=context)
        return True

    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
        self.sale_order_confirm_send_email(cr, uid, ids, context=context)
        return res
