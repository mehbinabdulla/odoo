# -*- coding: utf-8 -*-
from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config_id):
        """To load the field rating to POS"""
        result = super()._load_pos_data_fields(config_id)
        result.append('rating')
        return result