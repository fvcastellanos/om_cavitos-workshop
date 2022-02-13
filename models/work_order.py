from operator import index
from odoo import fields, models

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
        'Linea'
    )

    order_number = fields.Char("Numero de orden", index = True, translate = True, required = True)
    date_received = fields.Date('Fecha de ingreso', default = lambda self: fields.Date.today(), required = True)
    order_status = fields.Selection([
        ('process', 'En Proceso'),
        ('closed', 'Facurada'),
        ('invoice_pending', 'Pendiente facturar'),
        ('cancelled', 'Anulada'),
        ('guarantee', 'Garantia')
    ], "Estado", index = True)
    order_notes = fields.Text('Notas', translate = True)
    car_plate = fields.Char("Placas", index = True, translate = True, required = True)
    car_color = fields.Char("Color", translate = True)
    car_year = fields.Integer("Modelo")
    car_odometer_value = fields.Integer('Valor odometro', required = True)
    car_odometer_measurement = fields.Selection([
        ('kms', 'Kilometros'),
        ('mls', 'Millas')
    ], 'Tipo medida')
