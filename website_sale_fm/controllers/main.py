# -*- coding: utf-8 -*-
import werkzeug
import logging
from urlparse import urlparse, parse_qs
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
import openerp.addons.website_sale.controllers.main

class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    #------------------------------------------------------
    # Checkout
    #------------------------------------------------------

    # No acepta productos de distintas tiendas, retorna al carro 
    # La compañia con id 1 se añade para un envío genérico de FairMarket gratutito
    # Esto es necessario para no bloquear las ordenes a las tiendas que no hayan configurado metodo de envio
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        #logging.info("Start /shop/checkout in website_sale_fm")
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(force_create=1, context=context)
        companies = [1]

        for order_line in order.order_line:
            company = order_line.product_id.company_id.id
            if not company in companies:
                companies.append(company) 

        if len(companies) > 2:
            logging.info("Más de dos compañias detectada, redirigiendo") 
            # ToDo: mostrar ventana warning
            return request.redirect("/shop/cart")

        res = super(website_sale, self).checkout(**post)
        return res

    #------------------------------------------------------
    # Payment
    #------------------------------------------------------

    # Setea salesman y company de la orden
    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        #logging.info("Start /shop/payment in website_sale_fm")
        cr, uid, context = request.cr, request.uid, request.context
        #sale_order_obj = request.registry.get('sale.order')
        order = request.website.sale_get_order(context=context)
        for line in order.order_line:
            # puede que haya el metodo de envio generico de fm  
            if line.product_id.company_id.id is not 1:
                res = super(website_sale, self).payment(**post)
                order.company_id = line.product_id.company_id
                order.user_id = order.company_id.user_ids[0] # Cambia el salesman de la orden para que tenga acceso. User: All leads
                #logging.info("Returning : %s " %res)
                return res
        return request.redirect("/shop/cart")
