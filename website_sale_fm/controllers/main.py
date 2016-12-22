# -*- coding: utf-8 -*-
import werkzeug
import logging
import pprint
from urlparse import urlparse, parse_qs
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
import openerp.addons.web.controllers.main
import openerp.addons.website_sale.controllers.main

_logger = logging.getLogger(__name__)

class website_sale(openerp.addons.website_sale.controllers.main.website_sale):
    """
    # Update the total amount in the parent cp and subscribe the user to the wall
    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.registry['sale.order'].browse(cr, SUPERUSER_ID, sale_order_id, context=context)
        else:
            return request.redirect('/shop')
        #order.action_button_confirm()
        res = super(website_sale, self).payment_confirmation(**post)
        return res
    """
    #------------------------------------------------------
    # Checkout
    # No acepta productos de distintas tiendas, retorna al carro 
    # La compañia con id 1 se añade para un envío genérico de FairMarket gratutito
    # Esto es necessario para no bloquear las ordenes a las tiendas que no hayan configurado metodo de envio
    #------------------------------------------------------
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        _logger.info("Start /shop/checkout in website_sale_fm")
        order = request.website.sale_get_order(force_create=1, context=context)
        companies = [1]

        for order_line in order.order_line:
            if not order_line.product_id.sale_ok:
                logging.info("Este producto no se puede vender en la tienda") 
                # ToDo: mostrar ventana warning
                return request.redirect("/purchase/open")

        for order_line in order.order_line:
            company = order_line.product_id.company_id.id
            if not company in companies:
                companies.append(company) 

        if len(companies) > 2:
            logging.info("Más de dos compañias detectadas, redirigiendo al carro") 
            # ToDo: mostrar ventana warning
            return request.redirect("/shop/cart")

        res = super(website_sale, self).checkout(**post)
        return res

    #------------------------------------------------------
    # Payment
    # Setea salesman y company de la orden.
    # No filtra los acquirers por cia
    #------------------------------------------------------

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        _logger.info("/shop/payment :: Init payment inherited %s" %post)
        """      
        payment_obj = request.registry.get('payment.acquirer')
        sale_order_obj = request.registry.get('sale.order')

        order = request.website.purchase_get_order(context=context)
        logging.info("order : %s" %order)
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        shipping_partner_id = False
        if order:
            if order.partner_shipping_id.id:
                shipping_partner_id = order.partner_shipping_id.id
            else:
                shipping_partner_id = order.partner_invoice_id.id

        values = {
            'order': request.registry['sale.order'].browse(cr, SUPERUSER_ID, order.id, context=context)
        }
        values['errors'] = sale_order_obj._get_errors(cr, uid, order, context=context) # casca en website_sale_delivery

        values.update(sale_order_obj._get_website_data(cr, uid, order, context))

        if not values['errors']:
            acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True)], context=context)
            values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
            render_ctx = dict(context, submit_class='btn btn-primary', submit_txt=_('Pay Now'))
            for acquirer in values['acquirers']:
                acquirer.button = payment_obj.render(
                    cr, SUPERUSER_ID, acquirer.id,
                    order.name,
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    partner_id=shipping_partner_id,
                    tx_values={
                        'return_url': '/shop/payment/validate',
                    },
                    context=render_ctx)
            for line in order.order_line:
            # puede que haya el metodo de envio generico de fm  
            if line.product_id.company_id.id is not 1:
                #res = super(website_sale, self).payment(**post)
                order.company_id = line.product_id.company_id
                order.user_id = order.company_id.user_ids[0] # Cambia el salesman de la orden para que tenga acceso. User: All leads
        """ 
        res = super(website_sale, self).payment(**post) # No usamos res, pero no quiere ejecutarse si en el super
        _logger.info("res : %s ", pprint.pformat(res))
        return res
        #return request.website.render("website_sale", values)

 # vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:

