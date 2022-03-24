from odoo import fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection([
        ('savings', 'Ahorro'),
        ('checking', 'Monetaria'),
        ('credit', 'Tarjeta de Credito'),
    ], "Tipo de Cuenta", index = True, default='savings')
