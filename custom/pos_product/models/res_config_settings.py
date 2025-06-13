# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import api, fields, models
from odoo.api import ondelete


class ResConfigSettings(models.TransientModel):
    """Transient model for the field category ids in settings"""
    _inherit = 'res.config.settings'

    is_discount_limit = fields.Boolean()
    category_ids = fields.Many2many('pos.category', string='Category', relation='pos_category_discount_limit_rel', ondelete='cascade')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        category_ids = icp_sudo.get_param('res.config.settings.category_ids')
        is_discount_limit = icp_sudo.get_param('res.config.settings.is_discount_limit')
        res.update(
            is_discount_limit = is_discount_limit,
            category_ids = [(6, 0, literal_eval(category_ids))] if category_ids else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        categories = self.env['pos.category'].sudo().search([('discount_limit','!=',1)])
        print(categories)
        for category in categories:
            if not self.is_discount_limit:
                category.discount_limit = 1
            if category.id not in self.category_ids.ids:
                category.discount_limit = 1
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.category_ids', self.category_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.is_discount_limit', self.is_discount_limit)
        return res