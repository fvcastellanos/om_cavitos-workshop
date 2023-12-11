from odoo import fields, models, api

class WorkOrder(models.Model):
    _name = "workshop.work.order"
    _description = "Work Order"
    _order = "order_number desc"

    partner_id = fields.Many2one(
        'res.partner',
        'Cliente'
    )

    car_line_id = fields.Many2one(
        'workshop.car.line',
        'Línea'
    )

    # order_id = fields.Many2one(
    #     'sale.order',
    #     'Presupuesto'
    # )

    order_details = fields.One2many(
        'workshop.work.order.detail',
        'work_order',
        'Detalle de la orden'
    )

    # order_shippings = fields.One2many(
    #     'workshop.work.order.shipping',
    #     'work_order_id',
    #     'Nota de envío'
    # )

    order_number = fields.Char("Número de orden", index = True, translate = True, required = True)
    date_received = fields.Date('Fecha de ingreso', default = lambda self: fields.Date.today(), required = True)

    # order_type = fields.Selection([
    #     ('product', 'Producto'),
    #     ('service', 'Reparación')
    # ], index = True, default = 'service')

    order_status = fields.Selection([
        ('process', 'En Proceso'),
        ('closed', 'Facurada'),
        ('invoice_pending', 'Pendiente facturar'),
        ('cancelled', 'Anulada'),
        ('guarantee', 'Garantia')
    ], "Estado", index = True, default='process')

    order_notes = fields.Text('Notas', translate = True)

    car_brand = fields.Char("Marca", compute = "_get_car_brand", readonly = True)
    car_plate = fields.Char("Placas", index = True, translate = True)
    car_color = fields.Char("Color", translate = True)
    car_year = fields.Integer("Modelo")
    car_odometer_value = fields.Integer('Valor odometro')
    car_odometer_measurement = fields.Selection([
        ('kms', 'Kilómetros'),
        ('mls', 'Millas')
    ], 'Tipo medida odometro')

    # ------------------------------------------------------------------------------------------

    @api.onchange('car_line_id')
    def onchange_car_line_id(self):
        self.car_brand = self.car_line_id.brand_id.name

    @api.depends('car_line_id.brand_id.name')
    def _get_car_brand(self):
        self.car_brand = self.car_line_id.brand_id.name
        