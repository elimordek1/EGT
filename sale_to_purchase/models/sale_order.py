from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #saleorderze dalinkva
    purchase_order_ids = fields.One2many(
        comodel_name='purchase.order', 
        inverse_name='sale_order_id', 
        string='Purchase Orders'
    )
    
    def action_create_po(self):
        """Create a purchase order from the sale order."""
        self.ensure_one()
        
        if not self.order_line:
            raise UserError(_("You cannot create a PO without any products."))
            
        partner = self.partner_id
        
        if not partner.supplier_rank:
            partner.write({'supplier_rank': 1})
            
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']
        
        # Create Purchase Order
        purchase_order = PurchaseOrder.create({
            'partner_id': partner.id,
            'date_order': fields.Datetime.now(),
            'origin': self.name,
            'company_id': self.company_id.id,
            'currency_id': partner.property_purchase_currency_id.id or self.company_id.currency_id.id,
            'sale_order_id': self.id,  # Link back to sale order
        })
        
        # Create purchase order lines
        for line in self.order_line:
            if not line.product_id or line.product_id.type == 'service':
                continue
                
            seller = line.product_id._select_seller(
                partner_id=partner,
                quantity=line.product_uom_qty,
                date=purchase_order.date_order,
                uom_id=line.product_uom
            )
            
            PurchaseOrderLine.create({
                'order_id': purchase_order.id,
                'name': line.name,
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': seller.price if seller else line.price_unit,
                'date_planned': fields.Datetime.now(),
                'taxes_id': [(6, 0, line.product_id.supplier_taxes_id.ids)],
            })
        
        self.env['bus.bus']._sendone(
            self.env.user.partner_id, 
            'simple_notification', 
            {
                'title': _('Success'),
                'message': _('Purchase Order created successfully for %s') % self.name,
                'type': 'success'
            }
        )
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }
    
    def action_view_purchase_orders(self):
        """Open purchase orders linked to this sale order"""
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {}
        return action

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    sale_order_id = fields.Many2one(
        comodel_name='sale.order', 
        string='Source Sales Order', 
        copy=False, 
        readonly=True
    )
    
    def action_view_sale_order(self):
        """Open the source Sales Order"""
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("No source Sales Order found for this Purchase Order."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'context': {
                'form_view_initial_mode': 'edit',  
                'create': False,  
                'edit': True  
            }
        }