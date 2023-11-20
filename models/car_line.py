from odoo import fields, models, api
from odoo.exceptions import ValidationError

class CarLine(models.Model):

    _name = "workshop.car.line"
    _description = "Car Line"
    _order = "name"

    brand_id = fields.Many2one(
        'workshop.car.brand', 
        'Marca'
    )

    name = fields.Char("Nombre", translate = True, index = True, required = True)
    description = fields.Text("Descripción", translate = True)

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(CarLine, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(CarLine, self).write(vals)

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name.upper())]) > 1:
                raise ValidationError("Línea debe ser única")