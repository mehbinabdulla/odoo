{
    'name': 'Sales Custom Features',
    'version': '18.0.1.1.0',
    'summary': 'Custom Features for Odoo Sales Module',
    'description': 'Custom Features for Odoo Sales Module',
    'category': 'Sales',
    'author': 'Mehbin Abdulla',
    'depends': ['base','sale',],
    'sequence':2,
    'images': [
        'static/description/icon.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/upload_sale_order_line_wizard_views.xml',
    ],
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
