# -*- coding: utf-8 -*-
import json
from odoo import api, models, fields
from odoo.tools import json_default


class StudentReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    department_ids = fields.Many2many('school.department', store=True, readonly=False, compute='_compute_department_ids')
    class_ids = fields.Many2many('school.class', store=True, readonly=False, compute='_compute_class_ids')

    @api.depends('department_ids')
    def _compute_class_ids(self):
        """To set class id based None when the department id changed"""
        for record in self:
            record.class_ids = None

    @api.depends('class_ids')
    def _compute_department_ids(self):
        """To set department id based on class id"""
        for record in self:
            record.department_ids = record.class_ids.department_id

    def action_print_report(self):
        """To pass data to the template"""
        data = {
            'department_ids': [dept.id for dept in self.department_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'department_name': [dept.name for dept in self.department_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return self.env.ref('school_management.action_report_student_template').report_action(None, data)

    def action_print_xls(self):
        """To pass data to the XLSX sheet"""
        data = {
            'department_ids': [dept.id for dept in self.department_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'department_name': [dept.name for dept in self.department_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'report.school_management.report_student',
                 'options': json.dumps(data, default=json_default),
                 'output_format': 'xlsx',
                 'report_name': 'Student Report',
            },
            'report_type': 'xlsx',
        }

