# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models


class SchoolEvent(models.Model):
    """Added club id to the event"""
    _inherit = 'event.event'

    club_id = fields.Many2one('school.club', string='Club')

    def action_send_mail(self):
        employee_ids = self.env['res.partner'].search([('partner_type', 'in', ['teacher', 'staff'])])
        event_ids = self.search([])
        print(employee_ids)
        for event in event_ids:
            print(event.name)
            date_begin = event.date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
            print(date_begin - timedelta(days=2))
            if fields.Datetime.today() == (date_begin - timedelta(days=2)):
                for employee in employee_ids:
                    print(employee)
                    template = self.env.ref('school_management.employee_event_mail_template')
                    template.send_mail(
                        self.id,
                        email_values={
                            'email_to': employee.email,
                        },
                        force_send=True)

    @api.autovacuum
    def _check_event_ended(self):
        event_ids = self.search([('date_end', '<',  fields.Date.today())])
        for event_id in event_ids:
            print(event_id.name)
            event_id.active = False
