from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])