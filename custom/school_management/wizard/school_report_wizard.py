import base64
from io import BytesIO
import openpyxl
from odoo import models, fields
from odoo.exceptions import UserError


class SchoolReportFilterWizard(models.TransientModel):
    """Upload sale order lines from wizard"""
    _name = 'school.report.wizard'
    _description = 'School Report Wizard'

    model = fields.Many2one('ir.model', domain=[('modules', '=', 'school_management')])
    domain = fields.Char(string='Filter')

    def action_print_report(self):
        print('d')

