{
    'name': 'EGT Quotation Rent Report',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom Quotation Rent Report for EGT',
    'description': 'Custom report template for EGT quotation rentals',
    'depends': ['sale'],
    'data': [
        'report/quotation_rent_report.xml',
        'report/quotation_sale_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}