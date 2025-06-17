import requests

from odoo import http
from odoo.http import request


class SystrayWeatherController(http.Controller):
    @http.route(['/api/openweather/credentials'], type='json', auth='user')
    def open_weather(self):
        active = request.env['ir.config_parameter'].sudo().get_param('res.config.settings.open_weather_is_active')
        if not active:
            return None
        api_key = request.env['ir.config_parameter'].sudo().get_param('res.config.settings.open_weather_api')
        location_id = request.env['ir.config_parameter'].sudo().get_param('res.config.settings.open_weather_location')
        location = request.env['res.city'].sudo().browse(location_id)
        print(location)

        response = {
            'api_key': api_key,
            'location': {
                'name': location.name,
                'state': location.state_id.name if location.state_id else None,
                'country': location.country_id.name if location.country_id else None,
            } if location else None
        }
        return response
