from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


class PaymentPaytrailController(http.Controller):
    @http.route('/payment/paytrail/redirect/<int:transaction_id>', type='http', auth='public')
    def paytrail_redirect(self, transaction_id):
        transaction = request.env['payment.transaction'].sudo().browse(transaction_id)
        redirect_url = transaction.provider_id.paytrail_create_payment(transaction)
        return redirect(redirect_url, code=302)

    @http.route('/payment/paytrail/return', type='http', auth='public')
    def paytrail_return(self, **kwargs):
        reference = kwargs.get('checkout-reference')
        print('\nResponse: ', kwargs, '\n------------------end---------------------')
        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if transaction:
            transaction._set_done()
        return request.redirect('/payment/status')

    @http.route('/payment/paytrail/cancel', type='http', auth='public')
    def paytrail_cancel(self, **kwargs):
        return request.redirect('/payment/status?cancel=true')
