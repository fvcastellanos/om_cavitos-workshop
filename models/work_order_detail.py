from odoo import fields, api, models

class WorkOrderDetail(models.Model):
    _name = "workshop.work.order.detail"
    _description = "Order Detail"
    # _order = "order_number desc"

    work_order_id = fields.Many2one(
        'workshop.work.order',
        'Orden de trabajo'
    )

    product_id = fields.Many2one(
        'product.product',
        'Producto'
    )

    amount = fields.Float('Cantidad', (4, 2), required = True)

    # Add currency field
    unit_price = fields.Float('Precio Unitario', (10, 2), required = True)

    detail_total = fields.Float('Total', (10, 2), compute = "_calculate_detail_total")

    # ----------------------------------------------------------------------------------------

    @api.onchange('amount', 'unit_price')
    def onchange_amount(self):
        self.__calculate_detail_total()

    @api.depends('amount', 'unit_price')
    def _calculate_detail_total(self):
        self.__calculate_detail_total()

    # ----------------------------------------------------------------------------------------

    def __calculate_detail_total(self):
        for record in self:
            record.detail_total = record.amount * record.unit_price
