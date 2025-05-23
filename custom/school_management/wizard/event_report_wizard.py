
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EventReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'event.report.wizard'
    _description = 'Event Report Wizard'

    duration = fields.Selection([
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('custom', 'Custom Date'),
        ('all', 'All')
    ], default='today', required=True)
    start_date = fields.Date(required=True if duration == 'custom' else False)
    end_date = fields.Date(required=True if duration == 'custom' else False)
    club_ids = fields.Many2many('school.club')

    @api.constrains('start_date', 'end_date')
    def _check_date_difference(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date must be greater than or equal to end date!')

    def action_print_report(self):
        data = {
            'duration': self.duration,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'club_ids': [club.id for club in self.club_ids],
            'club_name': [club.name for club in self.club_ids],
        }
        print(data)
        return self.env.ref('school_management.action_report_event_template').report_action(None, data)


