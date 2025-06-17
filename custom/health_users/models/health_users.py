# -*- coding: utf-8 -*-
import jwt
import secrets
from odoo import fields, models, api


class HealthUsers(models.Model):
    """Model to store the user credentials"""
    _name = 'health.users'
    _description = 'Health Users'

    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    secret_key = fields.Char(string='Secret Key', readonly=True)
    subscription_type = fields.Selection([
        ('free', 'Free'),
        ('premium', 'Premium')
    ], string='Subscription Type', default='free', required=True)
    expiry = fields.Date(string='Expiration')
    database_ids = fields.One2many('user.database', 'user_id')

    @api.model_create_multi
    def create(self, vals_list):
        """To override create() and generating JWT encoded secret key"""
        for vals in vals_list:
            secret = secrets.token_hex(32)
            payload = {
                'email': vals.get('email'),
                'subscription_type': vals.get('subscription_type'),
            }
            vals['secret_key'] = jwt.encode(payload, secret, algorithm="HS256")
        return super(HealthUsers, self).create(vals_list)

    def check_expiry(self):
        """To check the expiry of subscription plan"""
        today = fields.Date.today()
        for record in self.search([]):
            if today > record.expiry:
                record.subscription_type = 'free'

