{
    'name': 'Custom Backend Theme',
    'version': '1.1',
    'summary': 'Change Odoo Backend UI Colors',
    'category': 'Themes/Backend',
    'author': 'Mehbin Abdulla',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'custom_theme/static/src/scss/custom.scss',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
