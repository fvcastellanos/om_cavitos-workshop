import logging
from pydispatch import dispatcher

_logger = logging.getLogger(__name__)

class ProviderInvoiceEventListener(object):

    # def __init__(self, pool):
    def __init__(self):
        
        # self.pool = pool

        dispatcher.connect(self.__on_provider_invoice_paid, signal="account_move_line_created", sender=dispatcher.Any)

    def __on_provider_invoice_paid(self, invoice_id):

        # invoice = self.pool.get('provider_invoice').browse(invoice_id)
        # for line in invoice.lines:
        #     line.product_id.qty_available += line.quantity

        _logger.info("Provider Invoice %s paid" % invoice_id)
