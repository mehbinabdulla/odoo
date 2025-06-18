# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import api, fields, models
from odoo.api import ondelete


class ResConfigSettings(models.TransientModel):
    """Integration of OpenWeatherMap API"""
    _inherit = 'res.config.settings'

    open_weather_is_active = fields.Boolean()
    open_weather_api = fields.Char('API Key')
    open_weather_location = fields.Many2one('res.city', 'Location')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        open_weather_is_active = icp_sudo.get_param('res.config.settings.open_weather_is_active')
        open_weather_api = icp_sudo.get_param('res.config.settings.open_weather_api')
        open_weather_location = icp_sudo.get_param('res.config.settings.open_weather_location')
        res.update(
            open_weather_api = open_weather_api,
            open_weather_is_active = open_weather_is_active,
            open_weather_location = self.env['res.city'].browse(int(open_weather_location)),
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.open_weather_is_active', self.open_weather_is_active)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.open_weather_api', self.open_weather_api)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.open_weather_location', self.open_weather_location.id)
        return res