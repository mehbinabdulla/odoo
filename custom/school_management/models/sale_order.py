from odoo import models, fields


class SaleOrder(models.Model):
    """Added new state"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])