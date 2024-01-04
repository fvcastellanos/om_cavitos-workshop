from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    account_move_line_id = fields.Integer('Detalle de Factura', index = True)

    def action_done(self):

        self._action_confirm()
        self._action_assign()
        self._action_done()

