{
    'name': 'eCommerce FairMarket',
    'category': 'Website',
    'summary': 'Modification in website_sale for FairMarket',
    'website': 'https://www.odoo.com/page/e-commerce',
    'version': '1.0',
    'description': """
OpenERP E-Commerce modifications for FairMarket
==================
* Demands category
* Does not allow multishop orders
* Set company on sale order before payment
* Better confirmation page
* Geograhical filter
* Shops pages
* Webs menues
    """,
    'author': 'Santi - FairCoop',
    'depends': ['website_sale','sale','website_partner'],
    'data': [
        'data/records.xml',
        'views/templates.xml',
    ],
    'demo': [
        #'data/demo.xml',
    ],
    #'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': False,
}
