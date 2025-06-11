# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    discount_limit = fields.Float(compute='_compute_discount_limit', store=True, default=1)

    @api.depends('pos_categ_ids.discount_limit')
    def _compute_discount_limit(self):
        for rec in self:
            min_discount = min([categ.discount_limit for categ in rec.pos_categ_ids]) if rec.pos_categ_ids else 1
            rec.discount_limit = min_discount