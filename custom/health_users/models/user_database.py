
from odoo import fields, models


class UserDatabase(models.Model):
    _name = 'user.database'
    _description = 'User Database'

    name = fields.Char('Database Name')
    base_url = fields.Char('Base Url')
    user_id = fields.Many2one('health.users')