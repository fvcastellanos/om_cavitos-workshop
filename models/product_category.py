
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductCategory(models.Model):
    _name = 'workshop.product.category'
    _description = 'Product Category'

    products = fields.One2many(
        'product.template',
        'product_category_id',
        'Productos asociados a la categoría'
    )

    code = fields.Char("Código", translate = True, index = True, readonly=True)
    name = fields.Char("Nombre", translate = True, index = True, required = True)
    description = fields.Text("Descripción", translate = True)

    @api.model
    def create(self, vals):

        seq = self.env['ir.sequence'].next_by_code('workshop.product.category.template') or '/'
        name = vals['name'].upper()

        vals['code'] = seq
        vals['name'] = name

        return super(ProductCategory, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(ProductCategory, self).write(vals)

    # ----------------------------------------------------------------------------

    @api.constrains('name')
    def _check_name(self):

        for record in self:
            if self.search_count([('name', '=', record.name.upper())]) > 1:
                raise ValidationError("Categoría debe ser única")
