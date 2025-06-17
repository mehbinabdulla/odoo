# -*- coding: utf-8 -*-
{
    'name': "Systray Weather",
    'version': '1.0',
    'category': 'Extras',
    'sequence': 5,
    'author': 'Mehbin Abdulla',
    'summary': "Weather in System Tray",
    'description': "Weather in System Tray",
    'depends': ['base', 'base_setup', 'base_address_extended', 'web'],
    'images': [
            'static/description/icon.png'
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'systray_weather/static/src/xml/systray_weather.xml',
            'systray_weather/static/src/js/systray_weather.js',
        ]
    },
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
