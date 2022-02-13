from email.policy import default
from fnmatch import translate
from odoo import fields, models

class CarBrand(models.Model):

    _name = "workshop.car.brand"
    _description = "Car Brand"
    _order = "name"

    car_lines_ids = fields.One2many(
        'workshop.car.line',
        'brand_id',
        'Lineas asociadas a la marca'
    )

    name = fields.Char("Nombre", translate = True, index = True, required = True)
    description = fields.Text("Descripcion", translate = True)
    active = fields.Boolean('Activo', default = True, readonly=True)
