from odoo import models, fields


class ProductTemplate(models.Model):
    """Added new state"""
    _inherit = 'product.template'

    rating = fields.Selection([
        ('1', 'One Star'),
        ('2', 'Two Star'),
        ('3', 'Tree Star'),
        ('4', 'Four Star'),
        ('5', 'Five Star'),
    ], 'Rating')




