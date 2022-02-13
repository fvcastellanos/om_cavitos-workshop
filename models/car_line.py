from odoo import fields, models

class CarLine(models.Model):

    _name = "workshop.car.line"
    _description = "Car Line"
    _order = "name"

    brand_id = fields.Many2one(
        'workshop.car.brand', 
        'Marca'
    )

    name = fields.Char("Nombre", translate = True, index = True, required = True)
    description = fields.Text("Descripcion", translate = True)
    active = fields.Boolean('Activo', default = True, readonly = True)
