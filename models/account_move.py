from odoo import api, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):

        # Call the original action_post method
        result = super().action_post()

        # If it's a vendor invoice, update the related stock moves
        if self.move_type == 'in_invoice':
            for line in self.invoice_line_ids:
                if line.product_id and line.product_id.type == 'product':
                    # Find the related stock move
                    stock_move = self.env['stock.move'].search([
                        ('account_move_line_id', '=', line.id),
                        ('state', '=', 'draft'),
                    ], limit=1)

                    if stock_move:
                        # Update the state of the stock move to 'done'
                        # Note: In a real-world scenario, you would need to properly handle the stock move validation
                        # This might involve calling the _action_done method, or manually setting the 'done' state
                        # and updating the product's quantity, depending on your specific requirements
                        stock_move.write({'state': 'done'})
                        # stock_move.action_done()

        return result