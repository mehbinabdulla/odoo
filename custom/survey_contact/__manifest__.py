# -*- coding: utf-8 -*-
{
    'name': 'Survey Contacts',
    'version': '18.0.1.1.0',
    'summary': 'Contact Creation from Survey',
    'category': 'Marketing',
    'author': 'Mehbin Abdulla',
    'depends': ['base','survey'],
    'sequence':'1',
    'images': [
        'static/description/icon.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_survey_views.xml',
    ],
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
