from ast import literal_eval
from odoo import api, fields, models


class WebsiteBomProduct(models.TransientModel):
    _inherit = 'res.config.settings'

    product_ids = fields.Many2many('product.product', string='Products')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(WebsiteBomProduct, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        product_ids = icp_sudo.get_param('res.config.settings.product_ids')
        res.update(
            product_ids=[(6, 0, literal_eval(product_ids))] if product_ids else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(WebsiteBomProduct, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.product_ids', self.product_ids.ids)
        return res