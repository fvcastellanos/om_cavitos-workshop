# -*- coding: utf-8 -*-
{
    'name' : 'Workshop Center',
    'version' : '0.1',
    'summary': 'Automobile Workshop Management',
    'description': """
        Automobile Workshop Management
    """,
    'category': 'Services',
    'author': 'Cavitos.NET',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': [
        'account',
        'base',
        'sale_management',
        'stock'
    ],
    'data': [
        'views/workshop_menu.xml',
        'views/brand_view.xml',
        'views/brand_line_view.xml',
    ]
}
