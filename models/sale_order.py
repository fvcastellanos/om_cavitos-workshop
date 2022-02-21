from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    work_order_id = fields.One2many(
        'workshop.work.order',
        'order_id'
        'Orden de trabajo relacionada al presupuesto'
    )