# -*- coding: utf-8 -*-
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
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend':[
        ],
        'point_of_sale._assets_pos': [
            'pos_product/static/src/xml/pos_product_card.xml',
            'pos_product/static/src/xml/orderline.xml',
            'pos_product/static/src/xml/modal.xml',
            'pos_product/static/src/js/modal.js',
            'pos_product/static/src/js/orderline.js',
        ]
    },
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
