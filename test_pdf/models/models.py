from odoo import models, fields, api
import base64
import os

class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string="Name")
    
    def get_logo_base64(self):
        path = os.path.join(os.path.dirname(__file__), '../static/src/img/egt_logo.png')
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            return ""



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    quotation_type = fields.Selection([
        ('rent', 'Quotation Rent'),
        ('sale', 'Quotation Sale')
    ], string="Quotation Type", default="sale")
    
    def format_amount(self, amount):
        return "{:,.2f}".format(amount) if amount else "0.00"