{
    'name': 'Sale to Purchase Integration',
    'version': '1.0',
    'category': 'Sales/Purchase',
    'summary': 'Create purchase orders from sales orders with one click',
    'description': """
        This module adds a PO button in sales orders to create purchase requests automatically.
    """,
    'depends': ['sale_management', 'purchase', 'sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}