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
        'base'
    ],
    'data': [
        'views/workshop_menu.xml',
        'views/brand_view.xml',
        'views/brand_line_view.xml',
        'views/work_order_view.xml',
        'views/work_order_kanban_view.xml',
        'views/provider_invoice_view.xml',
        'views/bank_view.xml',
        'reports/work_order_shipping.xml',
        'reports/work_order_shipping_view.xml'
    ]
}
