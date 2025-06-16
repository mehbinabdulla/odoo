# -*- coding: utf-8 -*-
{
    'name': "Health Users",
    'version': '1.0',
    'category': 'Others',
    'sequence': 5,
    'author': 'Mehbin Abdulla',
    'summary': "Health Users",
    'description': "Health Users",
    'depends': ['base', 'base_automation'],
    'data': [
        'security/ir.model.access.csv',
        'views/health_users_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
