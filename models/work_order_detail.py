from odoo import fields, api, models

class WorkOrderDetail(models.Model):
    _name = "workshop.work.order.detail"
    _description = "Order Detail"

    # _sql_constraints = [
    #         ('uq_account_move_line_id', 'UNIQUE(account_move_line_id)', 'The account move line must be unique.'),
    #     ]

    # _order = "order_number desc"

    work_order_id = fields.Many2one(
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

    def unlink(self):

        result = super(WorkOrderDetail, self).unlink()

        self._update_account_move_line(self.account_move_line_id)

        # accountMoveLine = self.env['account.move.line'].search([('id', '=', self.account_move_line_id)])

        # if accountMoveLine:
        #     accountMoveLine.write({'order_number': None})

        return result

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

    def _update_account_move_line(self, account_move_line_id):

        accountMoveLine = self.env['account.move.line'].search([('id', '=', account_move_line_id)])

        if accountMoveLine:
            accountMoveLine.write({'order_number': None})
