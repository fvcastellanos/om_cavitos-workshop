from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    order_number = fields.Char("Número de orden", index = True, translate = True)

    @api.model
    def create(self, vals):

        record = super(AccountMoveLine, self).create(vals)
        self.update_work_order(record)

        return record

    def write(self, vals):

        result = super(AccountMoveLine, self).write(vals)
        # self.update_work_order(self)
        
        return result

    def update_work_order(self, record):

        if record.order_number:

            work_order = self.env['workshop.work.order'].search([('order_number', '=', record.order_number)], limit=1)
            
            if work_order:

                work_order_detail = self.env['workshop.work.order.detail']

                work_order_detail.create({
                    'work_order_id': work_order.id,
                    'product_id': record.product_id.id,
                    'amount': record.quantity,
                    'unit_price': record.price_unit,
                    'detail_total': record.price_subtotal,
                    'account_move_line_id': record.id
                })

                return

            raise ValidationError("Orden de trabajo no encontrada")
