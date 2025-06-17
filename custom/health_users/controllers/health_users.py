# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HealthUsersController(http.Controller):
    """Controllers for health users"""

    @http.route(['/signin'], type='http', auth='public')
    def signup(self, **kwargs):
        """To manage user signup process"""
        email = kwargs.get('email')
        password = kwargs.get('password')
        user_id = request.env['health.users'].sudo().search([('email', '=', email)], limit=1)
        if not user_id:
            user_id = request.env['health.users'].sudo().create({
                'email': email,
                'password': password,
            })
        response = {
            'status_code': 200,
            'data': {
                'email': user_id.email,
                'secret_key': user_id.secret_key,
            },
        }
        return response


    @http.route(['/payment'], type='http', auth='user')
    def payment(self):
        """To manage payments"""
        pass

    @http.route(['/subscription'], type='http', auth='user')
    def subscription(self, **kwargs):
        """To manage subscription plans"""
        token = request.httprequest.headers.get('key')
        user_id = request.env['health.users'].sudo().search([('secret_key', '=', token)], limit=1)
        if user_id:
            if user_id.subscription_type == 'premium':
                return #premium response
            elif user_id.subscription_type == 'free':
                return #free response
        else:
            return #No user found!