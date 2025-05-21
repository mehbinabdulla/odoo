
from odoo import models, fields


class ClubReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'club.report.wizard'
    _description = 'Club Report Wizard'

    club_ids = fields.Many2many('school.club')
    student_ids = fields.Many2many('student')

    def action_print_report(self):
        data = {
            'student_ids': [student.id for student in self.student_ids],
            'club_ids': [club.id for club in self.club_ids],
            'student_name': [student.name for student in self.student_ids],
            'club_id': [club.name for club in self.club_ids],
        }
        #return self.env.ref('school_management.action_report_club_template').report_action(None, data)
