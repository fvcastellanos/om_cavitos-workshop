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
        is_vendor_invoice = self._belongs_to_vendor_invoice(record)

        if 'order_number' in vals and vals['order_number'] and is_vendor_invoice:

            self._create_work_order_detail(record, vals['order_number'])

        if is_vendor_invoice:

            _logger.info(f"Let's do some magic with Inventory")

            self._create_stock_move(record)

        return record

    def write(self, vals):

        result = super(AccountMoveLine, self).write(vals)

        belongs_to_vendor_invoice = self._belongs_to_vendor_invoice(self)

        if belongs_to_vendor_invoice:

            self._update_work_order_detail(self, vals)
        
        return result

    def unlink(self):

        belongs_to_vendor_invoice = self._belongs_to_vendor_invoice(self)

        result = super(AccountMoveLine, self).unlink()

        if belongs_to_vendor_invoice:

            self._delete_work_order_detail(self)

        return result

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

                    work_order_detail.with_context({'from_account_move_line': True}).write({
                        'amount': record.quantity,
                        'unit_price': record.price_unit,
                        'detail_total': record.price_subtotal,
                        'product_id': record.product_id.id,
                    })
                
                return

            # search for account move line in work order detail, if found, delete it
            self._delete_work_order_detail(record)

            if vals['order_number']:

                self._create_work_order_detail(record, vals['order_number'])

    def _delete_work_order_detail(self, records): 
            
            for record in records:
    
                work_order_detail = self.env['workshop.work.order.detail'].search([('account_move_line_id', '=', record.id)], limit=1)
    
                if work_order_detail:
    
                    work_order_detail.unlink()


    def _belongs_to_vendor_invoice(self, record):

        if record.move_id.move_type == 'in_invoice':

            return True

        return False

    def _belongs_to_vendor_invoice(self, records):

        for record in records:

            if record.move_id.move_type == 'in_invoice':

                return True

        return False


    def _create_stock_move(self, invoice_line):

        if invoice_line.product_id and invoice_line.product_id.type == 'product':

            invoice = invoice_line.move_id

        # Create a stock move for the invoice line
            self.env['stock.move'].create({
                'name': invoice_line.name,
                'partner_id': invoice.partner_id.id,
                'product_id': invoice_line.product_id.id,
                'product_uom': invoice_line.product_id.uom_id.id,
                'product_uom_qty': invoice_line.quantity,
                'price_unit': invoice_line.price_unit,
                'quantity': invoice_line.quantity,
                'location_id': self.env.ref('stock.stock_location_suppliers').id,
                'location_dest_id': self.env.ref('stock.stock_location_stock').id,
                'state': 'draft',
                'account_move_line_id': invoice_line.id
            })
