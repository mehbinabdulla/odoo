import logging
from odoo import _, fields, models


_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")], ondelete={'paytrail': 'set default'}
    )
    paytrail_merchant_id = fields.Char(
        string="Paytrail Merchant ID",
        help="The key solely used to identify the account with Razorpay.",
        required_if_provider='paytrail',
    )
    paytrail_key_secret = fields.Char(
        string="Paytrail Key Secret",
        required_if_provider='paytrail',
        groups='base.group_system',
    )
    paytrail_webhook_secret = fields.Char(
        string="Paytrail Webhook Secret",
        required_if_provider='paytrail',
        groups='base.group_system',
    )
