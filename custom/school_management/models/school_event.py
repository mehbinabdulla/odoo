# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models


class SchoolEvent(models.Model):
    """Added club id to the event"""
    _inherit = 'event.event'

    club_id = fields.Many2one('school.club', string='Club')

    @api.autovacuum
    def _check_event_ended(self):
        """To check and archive the events that ended"""
        event_ids = self.search([('date_end', '<', fields.Date.today())])
        for event_id in event_ids:
            event_id.active = False

    def send_mail(self):
        """Action to execute when the scheduled action event_mail triggered"""
        employee_ids = self.env['res.partner'].search([('partner_type', 'in', ['teacher', 'staff'])])
        event_ids = self.search([])
        for event in event_ids:
            date_begin = event.date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
            if fields.Datetime.today() == (date_begin - timedelta(days=2)):
                for employee in employee_ids:
                    template = self.env.ref('school_management.employee_event_mail_template')
                    template.send_mail(
                        self.id,
                        email_values={
                            'email_to': employee.email,
                        },
                        force_send=True)
