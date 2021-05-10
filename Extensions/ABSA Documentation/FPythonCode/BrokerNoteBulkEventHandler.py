"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkEventHandler

DESCRIPTION
    This module is used to check for Valid Block Trades needed to trigger a XLS Broker Note.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-29      FAOPS-702       Joash Moodley                                   Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import EnvironmentFunctions

from at_logging import getLogger
from BrokerNoteBulkBusinessProcessCreator import BrokerNoteBulkBusinessProcessCreator
import DocumentGeneral
import smtplib, string


LOGGER = getLogger(__name__)


class BrokerNoteBulkEventHandler(object):
    """
    Definition of an event-handler for broker note processing.
    """

    def get_name(self):
        """
        Get the name of the Document Event Handler.
        """
        return 'Broker Note Event Handler'

    def handles(self, message, event_object):
        """
        Determine whether or not to trigger the event handler for an
        event on the specified object.
        """
        if not event_object.IsKindOf(acm.FTrade):
            return False
        
        trade = event_object
    
        if self._is_allocation_trade(trade):
            return False
    
        if not self._is_block_trade(trade):
            return False

        if self._is_full_allocated(trade):
            message = "Valid Block Trade: {trade_id}"
            LOGGER.info(message.format(
                trade_id=trade.Oid(),
            ))
            return True
    
        return False
    
    def handle_event(self, message, event_object):
        """
        Perform any event handling.
        """
        self._trigger_business_process_based_on_managing_party(event_object)
    
    def _is_full_allocated(self, trade):
        allocation_quantity = 0 
        for connected_trade in trade.TrxTrades():
            allocation_quantity = allocation_quantity + connected_trade.Quantity()

        if DocumentGeneral.is_almost_zero(trade.Quantity() - allocation_quantity):
            return True

        return False
    
    def _is_block_trade(self, trade):
        if trade.OptKey1() and trade.OptKey1().Name() == 'Block Trade':
            return True
        return False

    def _is_allocation_trade(self, trade):
        if trade.TrxTrade():
            return True
        return False

    def _send_alert_email(self, trade, non_production_email_addresses=None):
        mail_from = 'AbcapCMBonds@absa.africa'
        production_email_addresses = ['AbcapCMBonds@absa.africa']
        email_subject = 'Missing parent on Counterparty : {party_name} for Trade : {trade_id}'
        email_subject = email_subject.format(
            party_name=trade.Counterparty().Name(),
            trade_id=trade.Oid()
        )

        content = '''
        Good Day
 
        Please note that {counter_party} is missing static data and was not able generate an Excel Broker Note.
        If you still want to regenerate the Excel Broker Note please update the static data for the counterparty in question,
        Once Static Data has been loaded please ask Moreetsi to run the Excel Broker Note script by providing the Block trade number.
        '''

        content = content.format(counter_party=trade.Counterparty().Name())
        production_email_addresses = ['AbcapCMBonds@absa.africa']
        
        if EnvironmentFunctions.is_production_environment():
            mail_to = production_email_addresses

        else:
            non_production_email_addresses = DocumentGeneral.get_default_non_production_email_to_addresses()
            mail_to = non_production_email_addresses

            message = "Non-production environment detected - overriding 'Send To' email "
            message += "address with '{non_production_email_addresses}' (would have "
            message += "been sent to '{production_email_addresses}')."

            LOGGER.info(message.format(
                non_production_email_addresses=non_production_email_addresses,
                production_email_addresses=production_email_addresses
            ))
    
            self._send(mail_from, mail_to, email_subject, content)

    def _send(self, mail_from, mail_to, email_subject, message):
        host = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
        body = string.join((
            "From: %s" % mail_from,
            "To: %s" % mail_to,
            "Subject: %s" % email_subject,
            "", message), "\r\n")
            
        if not host:
            raise Exception("Could not initialise the smtp Host")
        
        server = smtplib.SMTP(host)
        server.sendmail(mail_from, mail_to.split(','), body)
        server.quit()

    def _trigger_business_process_based_on_managing_party(self, trade):
        """
        triggers the business process for bulk broker note
        """
        managing_party_list = []
        for connected_trade in trade.TrxTrades():
            managing_party = connected_trade.Counterparty().AdditionalInfo().BrokerNoteParty()
            if not managing_party:
                self._send_alert_email(connected_trade)
                message = "Missing Broker Note Party for {trade_id}".format(trade_id=connected_trade.Oid())
                raise ValueError(message)
            if managing_party not in managing_party_list:
                managing_party_list.append(managing_party)

        for managing_party in managing_party_list:
            message = "Creating Broker Note XLS for : {managing_party}"
            LOGGER.info(message.format(
                managing_party=managing_party.Name(),
            ))
            BrokerNoteBulkBusinessProcessCreator().create_broker_note_business_process(trade, managing_party)

