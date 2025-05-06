# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolAcademicYear(models.Model):
    _name = 'school.academic.year'
    _description = 'School Academic Year'

    name = fields.Char(string='Academic Year', required=True)
    start_date = fields.Date(string='Period', required=True)
    end_date = fields.Date(required=True)