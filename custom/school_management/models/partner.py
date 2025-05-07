# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Partner(models.Model):
    """Added partner type and student id fields"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[('student','Student'), ('teacher','Teacher'), ('staff','Office Staff')], string='User Type')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)',
         "You entered Email is already exists. Please check the data is correct!"),
        ('unique_mobile', 'UNIQUE(mobile)',
         "You entered Mobile is already exists. Please check the data is correct!")
    ]
