
from odoo import models, fields


class EventReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'event.report.wizard'
    _description = 'Event Report Wizard'

    duration = fields.Selection([
        ('day', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('custom', 'Custom Date')
    ], default='day', required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    club_ids = fields.Many2one('school.club')

    def action_print_report(self):
        data = {
            'duration': self.duration,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'club_ids': [club.id for club in self.club_ids],
            'club_name': [club.name for club in self.club_ids],
        }
        return self.env.ref('school_management.action_report_event_template').report_action(None, data)


