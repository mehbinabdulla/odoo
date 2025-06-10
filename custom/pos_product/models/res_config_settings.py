# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Transient model for the field product id in settings"""
    _inherit = 'res.config.settings'

    category_ids = fields.Many2many('pos.category', string='Category', relation='pos_category_discount_limit_rel')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        category_ids = icp_sudo.get_param('res.config.settings.category_ids')
        res.update(
            category_ids=[(6, 0, literal_eval(category_ids))] if category_ids else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.category_ids', self.category_ids.ids)
        return res