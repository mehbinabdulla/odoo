from odoo import models


class SchoolManagementReport(models.TransientModel):
    _name = 'school.management.report'
    _description = 'School Management Report'

    def action_import_order_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Print',
            'res_model': 'school.report.wizard',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'model': self.env['ir.model']},
        }