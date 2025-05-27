# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ExamReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'exam.report.wizard'
    _description = 'Exam Report Wizard'

    student_ids = fields.Many2many('student', store=True, readonly=False, compute='_compute_student_ids')
    class_ids = fields.Many2many('school.class', store=True, readonly=False, compute='_compute_class_ids')

    @api.depends('student_ids')
    def _compute_class_ids(self):
        """To set the class based on the student"""
        for record in self:
            record.class_ids = record.student_ids.class_id

    @api.depends('class_ids')
    def _compute_student_ids(self):
        """To set the student id None when the class id is changed"""
        for record in self:
            record.student_ids = None

    def action_print_report(self):
        """To pass data to the template"""
        data = {
            'student_ids': [student.id for student in self.student_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'student_name': [student.name for student in self.student_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return self.env.ref('school_management.action_report_exam_template').report_action(None, data)
