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
- banner across the site
- Record rules and ACL
- js and css modifications
        """,
    'data': [
        'data/new_shop_form.xml',
        #'views/dev_site_banner.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
    ],
    'depends' : ['base','web','sale','website_sale','crm','portal'],
    'application': True,
    'qweb': ['static/src/xml/*.xml'],
    'css': ['static/src/css/website.assets_backend.css']
}
