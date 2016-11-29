# -*- coding: utf-8 -*-
import werkzeug
import openerp
from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect

class website_sale_brand(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/shop/brands'], type='http', auth='public', website=True)
    def shop(self, page = 0, category = None, search = '', **post):
        return "<h1>This is a test</h1>"
