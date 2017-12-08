# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2016 FairCoop (<http://fair.coop>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Product Brand and Country filtering in Website',
    'category': 'Website',
    'author': 'FairCoop',
    'website':'http://fair.coop',
    'summary': '',
    'version': '1.0',
    'description': """
Allows to use product brands and countries as filtering for products in website.\n
This Module depends on product_brand module -https://github.com/OCA/product-attribute/tree/8.0/product_brand
        """,
    'depends': ['product_brand_custom','website_sale','web','product_custom'],
    'data': [
        "data/demands.xml",
        "security/ir.model.access.csv",
        "views/product_brand.xml",
        "views/brand_page.xml",
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
