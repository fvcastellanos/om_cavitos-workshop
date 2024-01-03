from odoo import fields, api, models
from odoo.exceptions import ValidationError

class WorkOrderDetail(models.Model):
    _name = "workshop.work.order.detail"
    _description = "Order Detail"

    # _order = "order_number desc"

    work_order = fields.Many2one(
        'workshop.work.order',
        'Orden de trabajo'
    )

    # currency_id = fields.Many2one(
    #     'pricelist_id.currency_id', 
    #     'Moneda')    

    product_id = fields.Many2one(
        'product.product',
        'Producto'
    )

    account_move_line_id = fields.Integer('Linea de cuenta', index = True)

    amount = fields.Float('Cantidad', (4, 2), required = True)

    unit_price = fields.Float('Precio Unitario', (10, 2), required = True)

    detail_total = fields.Float('Total', (10, 2), compute = "_calculate_detail_total")

    provider_invoice = fields.Char('Factura de proveedor', size = 50, compute = "_get_provider_invoice")

    # ----------------------------------------------------------------------------------------

    @api.onchange('amount', 'unit_price')
    def onchange_amount(self):
        self._calculate_detail_total()

    @api.depends('amount', 'unit_price')
    def _calculate_detail_total(self):
        self._calculate_detail_total()

    def write(self, vals):

        self._validate_detail_modification(self)

        return super().write(vals)

    def unlink(self):

        self._update_account_move_line(self)

        return super(WorkOrderDetail, self).unlink()

    # ----------------------------------------------------------------------------------------

    def _calculate_detail_total(self):
        for record in self:
            record.detail_total = record.amount * record.unit_price

    def _get_provider_invoice(self):

        for record in self:
            if record.account_move_line_id:

                detail = self.env['account.move.line'].search([('id', '=', record.account_move_line_id)], limit=1)

                if detail:
                    record.provider_invoice = detail.move_id.name

            else:
                record.provider_invoice = None


    def _update_account_move_line(self, records):

        for record in records:

            if record.account_move_line_id:

                accountMoveLine = self.env['account.move.line'].search([('id', '=', record.account_move_line_id)])

                if accountMoveLine and accountMoveLine.order_number:
                    accountMoveLine.write({'order_number': None})

    def _validate_detail_modification(self, records): 

        for record in records:

            from_account_move_line = record._context.get('from_account_move_line')

            if record.account_move_line_id and not from_account_move_line:

                raise ValidationError("No es posible modificar el detalle de la orden de trabajo, se debe modificar la factura de proveedor")
