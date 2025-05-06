# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolClub(models.Model):
    _name = 'school.club'
    _description = 'School Club'

    name = fields.Char(string='Club Title', required=True)
    student_ids = fields.Many2many('student', string='Students', domain=[('stage', '=', 'registered')])
    event_count = fields.Integer(compute='_compute_event_count')

    def action_event_smart_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'kanban,calendar,pivot,graph,activity,list,form',
            'res_model': 'event.event',
            'context': {'default_club_id': self.id},
            'domain': [('club_id', '=', self.name)],
        }

    def _compute_event_count(self):
        for record in self:
            record.event_count = self.env['event.event'].search_count(
                [('club_id', '=', self.name)])