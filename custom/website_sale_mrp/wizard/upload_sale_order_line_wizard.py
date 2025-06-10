# -*- coding: utf-8 -*-
import base64
from io import BytesIO
import openpyxl
from odoo import models, fields
from odoo.exceptions import UserError


class UploadSaleOrderLineWiard(models.TransientModel):
    """Upload sale order lines from wizard"""
    _name = 'upload.sale.order.line.wizard'
    _description = 'Upload Sale Order Line Wizard'

    file = fields.Binary(string='Upload', required=True)
    file_name = fields.Char()

    def action_upload_file(self):
        active_id = self.env.context.get('active_id')
        record = self.env['sale.order'].browse(active_id)
        record.write({
            'order_line': self._create_order_line(record)
        })
        return {'type': 'ir.actions.act_window_close'}

    def _create_order_line(self, order):
        line_ids = []
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)), read_only=True
            )
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,max_col=None, values_only=True):
                line_id = self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': self._get_product(record).id,
                    'product_uom_qty': record[1] if record[1] else 1,
                    'price_unit': record[3] if record[3] else self._get_product(record).list_price,
                    'name': record[4] if record[4] else self._get_product(record).name,
                }).id
                line_ids = [(4, line_id)]
            return line_ids
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except Exception as e:
            raise UserError(f'{e}')

    def _get_product(self, record):
        product = self.env['product.product'].search([('name', '=', record[0])], limit=1)
        if product:
            return product
        return self.env['product.product'].create({
            'name': record[0],
            'uom_id': self._get_uom(record),
            'list_price': record[3],
        })

    def _get_uom(self, record):
        uom_name = record[2] if record[2] else 'Units'
        uom = self.env['uom.uom'].search([('name', '=', uom_name)], limit=1)
        if uom:
            return uom.id
        return self.env['uom.uom'].create({
            'name': uom_name,
            'category_id': self.env['uom.category'].create({'name': uom_name}).id
        }).id