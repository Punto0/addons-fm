{
    'name' : 'FairMarket tunning module',
    'version': '1.0',
    'author' : 'santi FairCoop',
    'summary': 'Modifications for FairMarket',
    'category': 'Tools',
    'description':
        """
FairMarket tunning module
=================
Modifications of Odoo for FairMarket.
- webpages
- some debrand
- new shop request form
- banner acrros the site
- Security
        """,
    'data': [
        'data/new_shop_form.xml',
        'data/records.xml',
        'views/product_custom_web.xml',
        #'views/dev_site_banner.xml',
        'views/brand_custom_web.xml',
        'views/products_page.xml',
        'views/templates.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
    ],
    'depends' : ['base', 'web','website_sale','website_product_brand'],
    'application': True,
    #'qweb': ['static/src/xml/*.xml'],
}
