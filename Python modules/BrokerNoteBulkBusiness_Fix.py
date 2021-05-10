from BrokerNoteBulkBusinessProcessCreator import BrokerNoteBulkBusinessProcessCreator
from at_logging import getLogger
import acm

 


LOGGER = getLogger(__name__)

 


    
def _trigger_business_process_based_on_managing_party(trade):
    """
    triggers the business process for bulk broker note
    """
    managing_party_list = []
    for connected_trade in trade.TrxTrades():
        managing_party = connected_trade.Counterparty().AdditionalInfo().BrokerNoteParty()
        if not managing_party:
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

 

#trade_ids = [,,,]
trade_ids = [127036415]

 

for id in trade_ids:
    trade = acm.FTrade[id]
    _trigger_business_process_based_on_managing_party(trade)
