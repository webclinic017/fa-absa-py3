"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanOpsCommitmentFeeCreator

DESCRIPTION
    This module contains objects used for triggering the regular or adhoc
    generation of Commitment Fee Invoice via the creation of confirmations 
    for the Commitment Fee Invoice event.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                      Initial Implementation.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import DocumentConfirmationGeneral


LOGGER = getLogger(__name__)
CONF_STATUS = ['Void', 'Exception']
PAYMENT_TYPE = ['Cash', 'Commitment Fee']


class LoanOpsCommitmentFeeCreator(object):
    """
    An object responsible for triggering the regular or adhoc
    generation of Commitment Fee Invoice via the creation of 
    confirmations for the Commitment Fee Invoice event.
    """

    def __init__(self, event_name, trade, date):
        """
        Constructor.
        """
        self.trade = trade
        self.event_name = event_name
        self.from_date = date
        self.to_date = date

    def create_commitment_fee_invoice(self):
        """
        Create daily Commitment Fee Invoice for the PRIMARY MARKETS acquirer.
        """
        if not self.invoice_exists():
            message = "Creating commitment fee for '{trade_id}' "
            message += "for date today '{date_today}'..."
            print(self.event_name)
            DocumentConfirmationGeneral.create_document_confirmation(
                self.event_name,
                self.trade,
                None,
                self.from_date,
                self.to_date,
                False
            )
        else:
            message = "Commitment Fee  for today '{date_today}' exists "
            message += "on trade '{trade_id}' ..."
            
        LOGGER.info(message.format(
            trade_id=self.trade.Oid(),
            date_today=acm.Time.DateToday())
        )

    def invoice_exists(self):
        confirmations = self.trade.Confirmations().AsArray()
        for confirmation in confirmations:
            if confirmation.CreateDay() == self.from_date:
                if confirmation.Status() not in CONF_STATUS:
                    if confirmation.EventChlItem().Name() == self.event_name:
                        for payment in confirmation.Trade().Payments():
                            if payment.PayDay() == self.from_date and confirmation.CreateDay() == self.from_date:
                                    if payment.Type() in PAYMENT_TYPE:
                                        return True
            
        return False

