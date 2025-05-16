from odoo import models, fields


class SaleOrder(models.Model):
    """Added new state"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])
    file = fields.Binary(string='Upload TC')
    file_name = fields.Char()

    def action_import_order_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Order Lines',
            'res_model': 'upload.sale.order.line.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'active_id': self.id},
        }

