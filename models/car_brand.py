from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarBrand(models.Model):
    _name = "workshop.car.brand"
    _description = "Car Brand"
    _order = "name"

    lines = fields.One2many(
        'workshop.car.line',
        'brand_id',
        'Líneas asociadas a la marca'
    )

    name = fields.Char("Nombre", translate = True, index = True, required = True)
    description = fields.Text("Descripción", translate = True)

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(CarBrand, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(CarBrand, self).write(vals)

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name.upper())]) > 1:
                raise ValidationError("Marca debe ser única")

