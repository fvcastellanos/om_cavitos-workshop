from odoo import fields, models, api
from odoo.exceptions import ValidationError
from pydispatch import dispatcher

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    order_number = fields.Char("Número de orden", index = True, translate = True)

    @api.model
    def create(self, vals):

        record = super(AccountMoveLine, self).create(vals)

        if 'order_number' in vals and vals['order_number']:
            dispatcher.send(signal="account_move_line_created", sender="account_move_line", invoice_id=record.id)

        return record

    def write(self, vals):

        result = super(AccountMoveLine, self).write(vals)
        # self._update_work_order_detail(self)

        # self._update_related_work_order(vals)

        # if 'order_number' in vals and vals['order_number'] != self.order_number:

        #     self._delete_work_order_detail(self.id)

        #     if vals['order_number']:
        #         self._update_work_order_detail(self)

        return result

    # --------------------------------------------------------------------

    def _update_related_work_order(self, vals):

        if 'order_number' in vals and vals['order_number'] != self.order_number:

            self._delete_work_order_detail(self.id)

            if vals['order_number']:
                self._update_work_order_detail(self)


    def _update_work_order_detail(self, record):

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


    def _delete_work_order_detail(self, account_move_line_id):

        work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', account_move_line_id)])

        if work_order_detail:

            work_order_detail.unlink()

        return
