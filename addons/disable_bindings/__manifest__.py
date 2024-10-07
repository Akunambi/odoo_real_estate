# -*- coding: utf-8 -*-
{
    'name': "disable_bindings",
    'depends': ['base','web'],
    'application' : True,
    'data' : [],
     'assets': {
        'web.assets_backend': [
            'disable_bindings/static/src/js/menu.js',
            'disable_bindings/static/src/js/title.js',
        ],
    },
}
