# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolEvent(models.Model):
    """Added club id to the event"""
    _inherit = 'event.event'

    club_id = fields.Many2one('school.club', string='Club')

    @api.model_create_multi
    def create(self, vals_list):
        template = self.env.ref('school_management.employee_event_mail_template')
        template.send_mail(self.id, force_send=True)
        return super(SchoolEvent, self).create(vals_list)

    @api.autovacuum
    def _check_event_ended(self):
        event_ids = self.search([('date_end', '<',  fields.Date.today())])
        for event_id in event_ids:
            print(event_id.name)
            event_id.active = False
