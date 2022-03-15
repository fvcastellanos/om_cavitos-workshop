from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    work_order_id = fields.Many2one(
        'workshop.work.order', 
        'Orden de trabajo'
    )
