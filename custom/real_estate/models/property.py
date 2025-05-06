from odoo import models, fields, api


class Property(models.Model):
    _inherit = 'product.template'

    is_property = fields.Boolean(string="Is a Property")
    property_type_id = fields.Many2one('real.estate.property.type', string='Property Type')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                                             domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    