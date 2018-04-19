{
    'name' : 'Web pages for FairMarket',
    'version': '1.0',
    'author' : 'santi FairCoop',
    'summary': 'Web and static content of FairMarket',
    'category': 'Tools',
    'description':
        """
Web and static content of FairMarket

* Webpages
* Js and CSS modifications for backend and frontend
* Web menues
* Debrand page titles and backend footer
* Favicon
* Controller to request some stats
* No configurations, everything is harcoded
        """,
    'data': [
        'data/records.xml',
        'views/templates.xml',
    ],
    'depends' : ['website'],
    'application': True,
    #'qweb': ['static/src/xml/*.xml'],
    #'css': ['static/src/css/website.assets_backend.css']
}
