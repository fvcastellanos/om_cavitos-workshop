from odoo import fields, models, api

class WorkOrderShipping(models.Model):
    _name = "workshop.work.order.shipping"
    _description = "Order Shipping"

    work_order_id = fields.Many2one(
        'workshop.work.order',
        'Orden de trabajo'
    )

    shipping_date = fields.Date('Fecha', default = lambda self: fields.Date.today(), required = True)

    name = fields.Char("Nombre")
    personal_id = fields.Char("DPI")
    phone = fields.Char("Teléfono")    
    sign = fields.Char("Firma")    
