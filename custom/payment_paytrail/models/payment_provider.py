import logging
import hmac, hashlib, base64, json, requests
import uuid
from datetime import datetime, timezone
from odoo import fields, models


_logger = logging.getLogger(__name__)


class Crypto:

  @staticmethod
  def compute_sha256_hash(message: str, secret: str) -> str:
    hash_key = hmac.new(secret.encode(), message.encode() ,digestmod=hashlib.sha256)
    return hash_key.hexdigest()

  @staticmethod
  def calculate_hmac(self, secret: str, header_params: dict, body: str='') -> str:
    data = []
    for key,value in header_params.items():
      if key.startswith('checkout-'):
        data.append('{key}:{value}'.format(key = key, value = value))
    data.append(body)
    return self.compute_sha256_hash('\n'.join(data), secret)

# class Crypto:
#
#     @staticmethod
#     def compute_sha256_hash(message: str, secret: str) -> str:
#         hash_key = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
#         return hash_key.hexdigest()
#
#     @staticmethod
#     def calculate_hmac(self, secret: str, header_params: dict, body: str = '') -> str:
#         # Only take headers starting with "checkout-"
#         filtered_headers = {
#             k.lower(): v for k, v in header_params.items() if k.lower().startswith('checkout-')
#         }
#
#         # Sort keys alphabetically
#         sorted_keys = sorted(filtered_headers.keys())
#
#         # Build the signed string
#         data_lines = [f"{key}:{filtered_headers[key]}" for key in sorted_keys]
#         if body:
#             data_lines.append(body)
#
#         signed_string = '\n'.join(data_lines)
#         return self.compute_sha256_hash(signed_string, secret)



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
    paytrail_secret_key = fields.Char(
        string="Paytrail Key Secret",
        required_if_provider='paytrail',
        groups='base.group_system',
    )

    # def _get_item(self, unit_price, units, vat_percentage, product_code, delivery_date):
    #     return {
    #         "unitPrice": unit_price,
    #         "units": units,
    #         "vatPercentage": vat_percentage,
    #         "productCode": product_code,
    #         "stamp": delivery_date
    #     }

    def paytrail_create_payment(self, transaction):
        payload = {
            "stamp": str(uuid.uuid4()),
            "reference": transaction.reference,
            "amount": int(transaction.amount * 100),
            "currency": "EUR",
            "language": "EN",
            "items": [{
                "unitPrice": int(transaction.amount * 100),
                "units": 1,
                "vatPercentage": 15,
                "productCode": transaction.reference,
                "stamp": str(uuid.uuid4())
            }],
            "customer": {"email": transaction.partner_email},
            "redirectUrls": {
                "success": transaction.provider_id.get_base_url() + "/payment/paytrail/return",
                "cancel": transaction.provider_id.get_base_url() + "/payment/paytrail/cancel",
            },
        }

        headers = {
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z",
            "content-type": "application/json"
        }

        body = json.dumps(payload, separators=(',', ':'))
        enc_data = Crypto.calculate_hmac(Crypto, self.paytrail_secret_key, headers, body)
        headers["signature"] = enc_data
        print(headers)
        response = requests.post("https://services.paytrail.com/payments", headers=headers, data=body)

        if response.status_code == 201:
            print(response.json()['href'])
            return response.json()["href"]
        else:
            raise Exception(f"Paytrail Error: {response.text}")

