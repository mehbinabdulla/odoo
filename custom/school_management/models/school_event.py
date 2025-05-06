# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolEvent(models.Model):
    _inherit = 'event.event'

    club_id = fields.Many2one('school.club', string='Club')

    # @api.model
    # def unlink(self):
    #     return super(SchoolEvent, self).unlink()
    #
    # def create_attendee(self):
    #     attendee_obj = self.env['event.registration']
    #     print(self.id)
    #     self.ensure_one()
    #     attendee_obj.search(['event_id.name', '=', self.name]).unlink()
    #     for attendee in self.club_id.student_ids:
    #         attendee_obj.create([{
    #             'name': f"{attendee.first_name} {attendee.last_name}",
    #             'event_id': self.id,
    #         }])
    #
    # def write(self, vals):
    #     res = super(SchoolEvent, self).write(vals)
    #     self.create_attendee()
    #     return res