# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolClass(models.Model):
    """Create Classes"""
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string='Class', required=True)
    department_id = fields.Many2one('school.department',string='Department', required=True)
    hod_id = fields.Many2one('res.partner', string='Head OD', related='department_id.hod_id')