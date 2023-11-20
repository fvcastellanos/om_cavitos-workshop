from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_category_id = fields.Many2one(
        'workshop.product.category',
        'Familia de Producto',
        required=True
    )

    @api.model
    def create(self, vals):

        seq = self.env['ir.sequence'].next_by_code('workshop.product.template') or '/'
        vals['default_code'] = seq

        return super(ProductTemplate, self).create(vals)
