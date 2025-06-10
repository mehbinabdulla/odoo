# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """Adding a field for rating"""
    _inherit = 'product.template'

    rating = fields.Selection([
        ('0', 'No Rating'),
        ('1', 'One Star'),
        ('2', 'Two Star'),
        ('3', 'Tree Star'),
        ('4', 'Four Star'),
        ('5', 'Five Star'),
    ], 'Rating')