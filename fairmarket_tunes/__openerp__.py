{
    'name' : 'FairMarket tunning module',
    'version': '1.0',
    'author' : 'Bumbum ',
    'summary': 'Modifications for FairMarket',
    'category': 'Tools',
    'description':
        """
FairMarket tunning module
=================
Modifications of Odoo for FairMarket
        """,
    'data': [
        'data/new_shop_form.xml',
        'data/menues.xml',
        'views/product_custom_web.xml',
        'views/dev_site_banner.xml',
        'views/brand_custom_web.xml',
        'views/products_page.xml',
        'views/templates.xml', 
        'security/record_rules.xml',
        'security/ir.model.access.csv',
    ],
    'depends' : ['base', 'web','website_sale','website_product_brand'],
    #'qweb': ['static/src/xml/*.xml'],
    'application': True,
}
