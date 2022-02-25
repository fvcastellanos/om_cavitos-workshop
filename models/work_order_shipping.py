from odoo import fields, models, api

class WorkOrderShipping(models.Model):
    _name = "workshop.work.order.shipping"
    _description = "Order Shipping"
    _order = "shipping_date desc"

    work_order_id = fields.Many2one(
        'workshop.work.order',
        'Orden de trabajo'
    )

    shipping_date = fields.Date('Fecha', default = lambda self: fields.Date.today(), required = True, index = True)

    name = fields.Char("Nombre", required = True)
    personal_id = fields.Char("DPI", required = True)
    phone = fields.Char("Teléfono", required = True)    
    sign = fields.Char("Firma")    
