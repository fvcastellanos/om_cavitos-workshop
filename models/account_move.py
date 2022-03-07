import logging
from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    work_order_id = fields.Many2one(
        'workshop.work.order', 
        'Orden de trabajo'
    )

    work_order_number = fields.Char("Número de orden", index = True, translate = True, required = True)

    # ------------------------------------------------------------------------------------------

    @api.onchange('work_order_number')
    def onchange_work_order_number(self):

        _logger.info(f"Searching for Work Order Number: {self.work_order_number}")
        _work_order_id = self.env['workshop.work.order'].search([('order_number', '=', self.work_order_number)])

        if _work_order_id.order_number != False:

            for record in _work_order_id:

                _logger.info(f"Work Order Id: {record.id} was found for Order number: {self.work_order_number}")
                self.work_order_id = record.id
        else:

            _logger.error(f'No work order found for Order Number: {self.work_order_number}')            
            raise ValidationError('Orden de trabajo no encontrada')
