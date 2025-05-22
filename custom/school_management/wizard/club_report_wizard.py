
from odoo import models, fields, api


class ClubReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'club.report.wizard'
    _description = 'Club Report Wizard'

    club_ids = fields.Many2many('school.club', readonly=False, store=True, compute='_compute_club_ids')
    student_ids = fields.Many2many('student', readonly=False, store=True, compute='_compute_student_ids')
    
    @api.depends('student_ids')
    def _compute_club_ids(self):
        for record in self:
            record.club_ids = None

    @api.depends('club_ids')
    def _compute_student_ids(self):
        for record in self:
            record.student_ids = None

    def action_print_report(self):
        data = {
            'student_ids': [student.id for student in self.student_ids],
            'club_ids': [club.id for club in self.club_ids],
            'student_name': [student.name for student in self.student_ids],
            'club_name': [club.name for club in self.club_ids],
        }
        return self.env.ref('school_management.action_report_club_template').report_action(None, data)
