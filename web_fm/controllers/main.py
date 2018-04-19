# -*- coding: utf-8 -*-
import openerp.http as http
from openerp.http import Response
from openerp.http import request
import json
import logging
_logger = logging.getLogger(__name__)

class StatsController(http.Controller):

    @http.route(['/stats'], type='json', auth='public', website=True)
    def stats(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        company_obj = pool['res.company']
        company_count = company_obj.search_count(cr, uid, [], context=context)
        product_obj = pool['product.template']
        product_count = product_obj.search_count(cr, uid, [('sale_ok','=',True),('website_published','=',True)])
        sale_order_obj = pool['sale.order']
        sale_count = sale_order_obj.search_count(cr, uid, [('state','in',['progress'] )])
        data = {
            "params": {
                "shops": company_count,
                "products": product_count,
                "purchases": sale_count
            }
        }
        return json.dumps(data)

    @http.route(['/how-it-works'], type='http', auth='public', website=True)
    def howitworks(self):
        return http.request.render('web_fm.howitworks', {})

    @http.route(['/aboutus'], type='http', auth='public', website=True)
    def aboutus(self):
        return http.request.render('web_fm.aboutus', {})

    @http.route(['/whatis'], type='http', auth='public', website=True)
    def whatisfairmarket(self):
        return http.request.render('web_fm.whatisfairmarket', {})
