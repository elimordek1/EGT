{
    'name': 'Test PDF Reports',
    'version': '1.0',
    'summary': 'Custom PDF Report Templates',
    'description': 'Module for custom quotation templates for EGT Georgia',
    'category': 'Sales',
    'author': 'Ramaziko',
    'depends': ['base', 'web', 'sale'],
    'data': [
        'report/report.xml',
        'report/report_quotation_rent.xml',
        'report/report_quotation_sale.xml',
    ],
    'assets': {
        'web.assets_common': [
            '/test_pdf/static/src/img/egt_logo.png',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}