from odoo import models, fields


class ResPartnerFieldHelper(models.Model):
    _name = 'res.partner.field.helper'
    _description = 'Partner Field Helper'

    name = fields.Char()
    key = fields.Char()

    def create_records(self):
        partner_fields = self.env['res.partner'].fields_get()
        for key, value in partner_fields.items():
            self.create({
                'name': value['string'],
                'key': key,
            })
