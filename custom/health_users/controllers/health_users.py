from odoo import http
from odoo.http import request


class HealthUsersController(http.Controller):
    @http.route(['/payment'], type='http', auth='public')
    def payment(self):
        pass

    @http.route(['/subscription'], type='http', auth='user')
    def subscription(self, **kwargs):
        token = request.httprequest.headers.get('key')
        user_id = request.env['health.users'].sudo().search([('secret_key', '=', token)], limit=1)
        if user_id:
            if user_id.subscription_type == 'premium':
                return #premium response
            elif user_id.subscription_type == 'free':
                return #free response
        else:
            return