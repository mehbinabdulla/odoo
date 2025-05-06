from odoo import models, fields


class PropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Property Type'

    property_type = fields.Char(string='Property Type')