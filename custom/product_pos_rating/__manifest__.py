{
    'name': 'POS Product Rating',
    'version': '18.0.1.1.0',
    'summary': 'Custom Features for Odoo POS Module',
    'description': 'Custom Features for Odoo POS Module',
    'category': 'Sales',
    'author': 'Mehbin Abdulla',
    'depends': ['base','sale', 'point_of_sale', 'product'],
    'sequence':2,
    'images': [
        'static/description/icon.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_frontend':[
        ],
    },
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
