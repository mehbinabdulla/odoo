{
    'name': 'Sales Custom Features',
    'version': '18.0.1.1.0',
    'summary': 'Custom Features for Odoo Sales Module',
    'description': 'Custom Features for Odoo Sales Module',
    'category': 'Sales',
    'author': 'Mehbin Abdulla',
    'depends': ['base','sale', 'website_sale', 'mrp'],
    'sequence':2,
    'images': [
        'static/description/icon.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/website_sale_templates.xml',
        'views/res_config_settings_views.xml',
        'views/website_bom_product_views.xml',
        'wizard/upload_sale_order_line_wizard_views.xml',
    ],
    'assets': {
        'web.assets_frontend':[
            'website_sale_mrp/static/src/js/website_sale_mrp.js',
        ],
    },
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
