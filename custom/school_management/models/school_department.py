# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolDepartment(models.Model):
    """Create Departments"""
    _name = 'school.department'
    _description = 'School Department'

    name = fields.Char(string='Department Name', required=True)
    hod_id = fields.Many2one('res.partner',string='Head OD')