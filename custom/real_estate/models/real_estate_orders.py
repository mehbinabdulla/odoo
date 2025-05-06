from odoo import models, fields, api


class RealEstateOrders(models.Model):
    _name = 'real.estate.orders'
    _description = 'Real Estate'

    order_id = fields.Char(string='Order ID', required=True, default='New', readonly=True)
    partner_id = fields.Many2one('res.partner',string='Customer')
    email = fields.Char(string='Email', related="partner_id.email", store=True, readonly=False)
    property_id = fields.Many2one('product.product')
    

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('order_id', 'New') == 'New':
                val['order_id'] = self.env['ir.sequence'].next_by_code('real_estate_orders') or 'New'
        return super(RealEstateOrders, self).create(vals)

    @api.depends('partner_id')
    def _compute_partner_email(self):
        for order in self:
            order.email = order.partner_id.email if order.partner_id else False
