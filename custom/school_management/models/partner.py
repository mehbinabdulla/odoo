# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[('student','Student'), ('teacher','Teacher'), ('staff','Office Staff')], string='User Type')
    student_id = fields.Many2one('student')