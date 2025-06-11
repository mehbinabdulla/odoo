# -*- coding: utf-8 -*-
from odoo import models, fields


class PosCategory(models.Model):
    """pos.category is inherited to add discount limit"""
    _inherit = 'pos.category'

    discount_limit = fields.Float('Discount Limit', default=100)