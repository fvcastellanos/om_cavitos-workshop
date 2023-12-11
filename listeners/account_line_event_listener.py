import logging
from pydispatch import dispatcher

_logger = logging.getLogger(__name__)

# Event Handlers
def _on_create(model):

    _logger.info(f"Account Line: {model.id} created")

    if model and model.order_number:
        __create_work_order_detail(model)


def _on_write(model):

    _logger.info(f"Account Line: {model.id} written")

    if model and model.order_number:
        __delete_work_order_detail(model, model.id)
        __create_work_order_detail(model)

def _on_delete(model):

    _logger.info(f"Account Line: {model.id} deleted")


# Create a listener for the signal
dispatcher.connect(_on_create, signal="account_move_line_created", sender=dispatcher.Any)
dispatcher.connect(_on_write, signal="account_move_line_updated", sender=dispatcher.Any)
dispatcher.connect(_on_delete, signal="account_move_line_deleted", sender=dispatcher.Any)


# DB Operations
def __delete_work_order_detail(model, account_move_line_id):

    work_order_detail = model.env['workshop.work.order.detail'].search([('account_move_line_id', '=', account_move_line_id)])

    if work_order_detail:

        work_order_detail.unlink()

def __create_work_order_detail(model):

    if model and model.order_number:

        work_order = model.env['workshop.work.order'].search([('order_number', '=', model.order_number)], limit=1)
        
        if work_order:

            work_order_detail = model.env['workshop.work.order.detail']

            work_order_detail.create({
                'work_order_id': work_order.id,
                'product_id': model.product_id.id,
                'amount': model.quantity,
                'unit_price': model.price_unit,
                'detail_total': model.price_subtotal,
                'account_move_line_id': model.id
            })
