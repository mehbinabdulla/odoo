from odoo import models, fields


class PosCategory(models.Model):
    _inherit = 'pos.category'

    discount_limit = fields.Float('Discount Limit')
    discount = fields.Char('Discount Limit')