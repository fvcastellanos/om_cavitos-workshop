import logging
from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    order_number = fields.Char(
        "Número de orden", 
        index = True, 
        translate = True, 
    )
    
    @api.model
    def create(self, vals):

        record = super(AccountMoveLine, self).create(vals)

        if 'order_number' in vals and vals['order_number']:

            self._create_work_order_detail(record, vals['order_number'])

        return record

    def write(self, vals):

        result = super(AccountMoveLine, self).write(vals)

        self._update_work_order_detail(self, vals)
        
        # for record in self:

        #     if not 'order_number' in vals:

        #         # search for account move line in work order detail
        #         work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', record.id)], limit=1)

        #         if work_order_detail:

        #             work_order_detail.write({
        #                 'amount': record.quantity,
        #                 'unit_price': record.price_unit,
        #                 'detail_total': record.price_subtotal,
        #                 'product_id': record.product_id.id,
        #             })
                
        #         return

        #     # search for account move line in work order detail
        #     work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', record.id)], limit=1)

        #     if work_order_detail:

        #         work_order_detail.unlink()


        #     if vals['order_number']:

        #         self._create_work_order_detail(record, vals['order_number'])

        return result

    def unlink(self):
        
        # if self.order_number:
        #     dispatcher.send(signal="account_move_line_deleted", sender="account_move_line", model=self)

        return super(AccountMoveLine, self).unlink()

    # --------------------------------------------------------------------

    @api.constrains('order_number')
    def _check_order_number(self):
        for record in self:
            
            if record.order_number:

                work_order = self.env['workshop.work.order'].search([('order_number', '=', record.order_number)], limit=1)
                if not work_order:
                    raise ValidationError("Orden de trabajo no encontrada")

    # --------------------------------------------------------------------

    def _create_work_order_detail(self, record, order_number):

        if order_number:

            work_order = self.env['workshop.work.order'].search([('order_number', '=', order_number)], limit=1)
            
            if work_order:

                _logger.info(f"Create work order detail for invoice detail: {record.id}")

                work_order.order_details = [(0, 0, {
                    'work_order': work_order.id,
                    'product_id': record.product_id.id,
                    'amount': record.quantity,
                    'unit_price': record.price_unit,
                    'detail_total': record.price_subtotal,
                    'account_move_line_id': record.id,
                })]

                return

            raise ValidationError("Orden de trabajo no encontrada")

    def _update_work_order_detail(self, records, vals):

        for record in records:

            if not 'order_number' in vals:

                # search for account move line in work order detail
                work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', record.id)], limit=1)

                if work_order_detail:

                    work_order_detail.write({
                        'amount': record.quantity,
                        'unit_price': record.price_unit,
                        'detail_total': record.price_subtotal,
                        'product_id': record.product_id.id,
                    })
                
                return

            # search for account move line in work order detail
            work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', record.id)], limit=1)

            if work_order_detail:

                work_order_detail.unlink()


            if vals['order_number']:

                self._create_work_order_detail(record, vals['order_number'])


    # def _delete_work_order_detail(self, account_move_line_id):

    #     work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', account_move_line_id)])

    #     if work_order_detail:

    #         work_order_detail.unlink()

    #     return
