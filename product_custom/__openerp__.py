# -*- coding: utf-8 -*-

{
    'name': 'Product Custom',
    'depends': ['product','website_sale'],
    'author': 'Santi Punto0 - FairCooop',
    'category': 'Product',
    'description': """
Customization on the product model for FairMarket
    """,
    'website': 'https://punto0.org',
    'data': [
        'views/product_view.xml',
        'views/templates.xml',
        'data/records.xml',
    ],
    'installable': True,
    'auto_install': False,
}
