# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# product_image_from_url for Odoo                                             #
# Copyright (C) 2017 Santiky (<santi@punto0.org>).                            #
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
from PIL import Image
import requests
from StringIO import StringIO
import base64#file encode
import cStringIO
import logging
from openerp import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_url = fields.Char(
        string='Image URL',
        help='Import an image in this product from a external website'
	)

    @api.onchange('image_url')
    def import_image(self):
       if self.image_url:
         logging.info('start import image %s' %self.image_url)
         try:
           response = requests.get(self.image_url)
           response.raise_for_status()
           img = Image.open(StringIO(response.content))
           output = cStringIO.StringIO()
           img.save(output, 'PNG')
           output.seek(0)
           output_s = output.read()
           b64 = base64.b64encode(output_s).decode()
           self.image_medium = b64
           self.image = b64
         except requests.exceptions.HTTPError as err:
           mess = "Please, check the provided URL.\nHTTPError : %s" %err
           logging.error(mess)
           return {
                    'warning': {'title': "Error", 'message': mess},
           }
         except requests.exceptions.Timeout:
           return {
                    'warning': {'title': "Error", 'message': 'Connection timeout'},
           }
         except requests.exceptions.TooManyRedirects:
           return {
                    'warning': {'title': "Error", 'message': 'Too many redirect'},
           }
         except requests.exceptions.RequestException as e:
           return {
                    'warning': {'title': "Error", 'message': e},
           }
       return self

                  
