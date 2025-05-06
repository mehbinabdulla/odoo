{
    'name': 'Real Estate',
    'version': '1.1',
    'summary': 'Odoo Real Estate management',
    'category': 'Real Estate',
    'author': 'Mehbin Abdulla',
    'depends': ['base','product'],
    'sequence':'1',
    'images': [
        'static/description/icon.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/real_estate_order_sequence.xml',
        'views/property_views.xml',
        'views/real_estate_orders_views.xml',
        'views/real_estate_menu_views.xml',
        'views/property_type_views.xml'
    ],
    'web_icon': 'static/description/icon.png',

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
