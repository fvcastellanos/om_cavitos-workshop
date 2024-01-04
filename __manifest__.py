{
    'name' : 'Workshop Center Management',
    'version' : '1.0',
    'summary': 'Automobile Workshop Management',
    'description': """
        Automobile Workshop Management
    """,
    'category': 'Services',
    'author': 'Cavitos.NET',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': [
        'account',
        'base',
        'stock'
    ],
    'data': [
        'data/actions.xml',
        'data/sequences.xml',
        'data/workshop_product_category.xml',
        'views/car_brand_view.xml',
        # 'views/car_line_view.xml',
        'views/product_view.xml',
        'views/product_category_view.xml',
        'views/workshop_menu.xml',
        'views/work_order_view.xml',
        'views/account_move_line.xml'
    ]
}
