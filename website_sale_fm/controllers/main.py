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
    # No filtra los acquirers por cia --> No se puede cambiar eso, lo modifico directamente en website_sale
    # ¡Atentos a actualizaciones!!!
    #------------------------------------------------------
    
    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(context=context)
        for line in order.order_line:
            # puede que haya el metodo de envio generico de fm  
            if line.product_id.company_id.id is not 1:
                res = super(website_sale, self).payment(**post)
                order.company_id = line.product_id.company_id
                order.user_id = order.company_id.user_ids[0] # Cambia el salesman de la orden para que tenga acceso. User: All leads
                return res
        return request.redirect("/shop/cart")

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

 # vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:

