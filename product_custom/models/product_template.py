# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# product_custom for Odoo                                                     #
# Copyright (C) 2017 Santi (<santi@þunto0.org>).                              #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as              #
# published by the Free Software Foundation, either version 3 of the          #
# License, or (at your option) any later version.                             #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
from openerp import models, fields, api
import logging

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(
         [('consu', 'Consumable'),('service','Service')],
         'Product Type',
         required=True,
         default='service',
         help="Consumable are product where you don't manage stock, a service is a non-material product provided by a company or an individual.",
	)
