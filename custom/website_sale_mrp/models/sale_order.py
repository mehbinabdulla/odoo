# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    """Adding fields for imported file"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])
    file = fields.Binary()
    file_name = fields.Char()

    def action_import_order_lines(self):
        """To return the model and active id to the wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Order Lines',
            'res_model': 'upload.sale.order.line.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'active_id': self.id},
        }


