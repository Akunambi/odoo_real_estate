# -*- coding: utf-8 -*-
{
    'name': "estate",
    'depends': ['base', 'web'],
    'application' : True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
}
