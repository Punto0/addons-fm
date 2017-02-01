{
    'name': 'eCommerce FairMarket',
    'category': 'Website',
    'summary': 'Modification in website_sale for FairMarke',
    'website': 'https://www.odoo.com/page/e-commerce',
    'version': '1.0',
    'description': """
OpenERP E-Commerce modifications for FairMarket
==================

    """,
    'author': 'Punto0 - FairCoop',
    'depends': ['website_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        #'data/demo.xml',
    ],
    #'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': False,
}
