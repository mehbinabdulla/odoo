# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolSubject(models.Model):
    """Create subjects"""
    _name = 'school.subject'
    _description = 'School Subject'

    name = fields.Char(string='Subject', required=True)
    department_id = fields.Many2one('school.department', string='Department', required=True)