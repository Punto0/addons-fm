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
        if order:
            companies = [1]
            for order_line in order.order_line:
                company = order_line.product_id.company_id.id
                if not company in companies:
                    companies.append(company)
            if len(companies) > 2:
                logging.debug("Más de dos compañias detectadas, muestra el aviso") 
                valid = False
        else:
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
            context['send_email'] = False
            return super(website_sale, self).checkout(**post)
        else:
            return request.redirect("/shop/cart")

