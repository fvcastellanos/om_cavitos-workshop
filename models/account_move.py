from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    work_order_id = fields.Many2one(
        'workshop.work.order', 
        'Orden de trabajo'
    )

