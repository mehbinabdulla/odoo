# -*- coding: utf-8 -*-
from odoo import models, fields


class PosCategory(models.Model):
    """pos.category is inherited to add discount limit"""
    _inherit = 'pos.category'

    discount_limit = fields.Float('Discount Limit', default=1)

    _sql_constraints = [('check_limit', 'CHECK(discount_limit BETWEEN 0 AND 1)', 'Discount limit must be between 0 and 100')]