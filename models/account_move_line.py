from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    work_order_id = fields.Many2one(
        'workshop.work.order', 
        'Orden de trabajo'
    )

    unit_price_sale = fields.Float('Precio Venta', (10, 2))
    total_sale = fields.Float('Total Venta', (10, 2), compute = "_calculate_detail_total")

    # ----------------------------------------------------------------------------------------

    @api.onchange('quantity', 'unit_price_sale')
    def onchange_amount(self):
        self.__calculate_detail_total()

    @api.depends('quantity', 'unit_price_sale')
    def _calculate_detail_total(self):
        self.__calculate_detail_total()

    # ----------------------------------------------------------------------------------------

    def __calculate_detail_total(self):
        for record in self:
            record.total_sale = record.quantity * record.unit_price_sale
