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

    def check_cart(self):
        order = request.website.sale_get_order()
        valid = True
        companies = [1]
        for order_line in order.order_line:
            company = order_line.product_id.company_id.id
            if not company in companies:
                companies.append(company)
        if len(companies) > 2:
            logging.debug("Más de dos compañias detectadas, muestra el aviso") 
            valid = False
        return valid

    # Set Valid/invalid flag to show/hide warning
    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        valid = self.check_cart()
        order = request.website.sale_get_order()
        values = {
          'website_sale_order': order,
          'valid':valid,
        }
        return request.render("website_sale.cart", values)

    #------------------------------------------------------
    # Checkout
    # No acepta productos de distintas tiendas, retorna al carro 
    # Esto es necessario para no bloquear las ordenes a las tiendas que no hayan configurado metodo de envio
    #------------------------------------------------------
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        if self.check_cart():
            cr, uid, context = request.cr, request.uid, request.context
            order = request.website.sale_get_order(force_create=1, context=context)
            return super(website_sale, self).checkout(**post)
        else:
            return request.redirect("/shop/cart")

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
     
 # vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:

