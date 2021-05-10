"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NetMaturitySettlementsSTPAutoReleaseHook

DESCRIPTION
    This module contains a hook for netting of maturities (FRN / Deposit) base on setting the mm settle instruct

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date         Change no              Developer               Requester            Description
-----------------------------------------------------------------------------------------------------------------------------------------
13/05/2019   FAOPS-308/FAOPS-454    Joash Moodley           Kgomotso Gumbo       Net based of settle instruct
05/12/2019   FAOPS-635              Tawanda Mukhalela       Wandile Sithole      Added check to only release Outgoing

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

SETTLE_INSTUCT_LIST = [
    "Pay Out : Capital", 
    "Pay Out : Interest", 
    "Pay Out : Capital and Interest"
]


def check_for_valid_confo_details(trade, status, event_types):
    """
    Check for matched confo based on status or event type.
    """
    LOGGER.info(
        'Checking Confirmations for trade {trade} :'.format(
            trade=trade.Oid())
    )
    for confo in trade.Confirmations():
        event_type = confo.EventChlItem().Name()
        LOGGER.info('checking status for {confo_id}'.format(confo_id=confo.Oid()))
        if confo.Status() == status:
            LOGGER.info('status matched for {confo_id}'.format(confo_id=confo.Oid()))
            if check_for_valid_confo_doc_type(confo, '320'):
                return True
            elif event_type in event_types:
                LOGGER.debug(
                    'confo {confo_id} event : {event_type}'.format(
                    confo_id=confo.Oid(),
                    event_type=event_type
                    )
                )
                return True
    LOGGER.info('No Valid Confirmations Found')
    return False


def check_for_valid_confo_doc_type(confo, msg_type):
    """
    Check for for specified confo doc type.
    """
    LOGGER.info(
        'checking Doc type confirmation for {confo_id}'.format(
        confo_id=confo.Oid())
    )
    for doc in confo.Documents():
        if str(doc.SwiftMessageType()) == msg_type:
            LOGGER.debug(
                'SwiftMessageType matched for  confirmation {confo_id}'.format(
                confo_id=confo.Oid())
            )
            return True
    return False


class NetMaturitySettlementsSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform Netting for triggered by setting
    the MM Settle Instruct 
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Net Maturity Settlements Hook MM Settle Instruct'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if eventObject.IsKindOf(acm.FSettlement):

            settlement = eventObject
            if not settlement.Trade():
                return False
            if settlement.Currency().Name() != 'ZAR':
                return False
            if settlement.Instrument().InsType() in ["Deposit", "FRN"]:
                LOGGER.debug('InsType : {ins_type}'.format(ins_type=settlement.Instrument().InsType()))
                if settlement.Status() == 'Authorised':
                    settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
                    if settle_instruct in  SETTLE_INSTUCT_LIST:
                        trade = settlement.Trade()
                        LOGGER.debug('settle_instruct : {settle_instruct}'.format(settle_instruct=settle_instruct))
                        if trade.Acquirer().Name() == 'Funding Desk':
                            LOGGER.debug('Acquirer : Funding Desk')
                            if check_for_valid_confo_details(trade, 'Matched', ["Maturity Notice"]):
                                LOGGER.info('Valid Settlement for Net')
                                return True

        elif eventObject.IsKindOf(acm.FConfirmation):
    
            confo = eventObject
            if confo.Status() == "Matched":
                if check_for_valid_confo_doc_type(confo, '320'):
                    return True
                
                elif confo.EventChlItem().Name() == 'Maturity Notice':
                    return True


    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        settlement = None
        
        if eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject
        elif eventObject.IsKindOf(acm.FConfirmation):
            confirmation = eventObject
            settlements = confirmation.Trade().Settlements()
            for settlement in settlements:
                if settlement.Currency().Name() != 'ZAR':
                    continue
                settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
                if settle_instruct in SETTLE_INSTUCT_LIST and settlement.Status() == 'Authorised':
                    break 

        if self.netCapitalInterestSettlements(settlement):
            LOGGER.info('Netting For Capital and Interest Payment')
        elif self.payCapital(settlement):
            LOGGER.info('Netting For Capital Payment')
        elif self.payInterest(settlement):
            LOGGER.info('Netting For Interest Payment')

    def _get_valid_settlements_to_net(self, settlements, allow_types):
        settlements_to_net = []
        for settlement in settlements:
            if settlement.Status() == 'Authorised' and settlement.Type() in allow_types:
                LOGGER.debug('settlement type : {type}'.format(type=settlement.Type()))
                settlements_to_net.append(settlement)
        return settlements_to_net       
   
    def netCapitalInterestSettlements(self, settlement):
        if not settlement or not settlement.Trade():
            return False
        allow_types = ["Fixed Rate",   "Fixed Amount", "Payment Cash"]
        settle_instruct = settlement.AdditionalInfo().Settle_Instruct()

        if settle_instruct == "Pay Out : Capital and Interest":
            LOGGER.debug('settle_instruct : Pay Out : Capital and Interest')
            settlements = settlement.Trade().Settlements().AsArray()
            settlements_to_net = self._get_valid_settlements_to_net(
                settlements,
                allow_types
            )
            OperationsSTPFunctions.net_settlements(settlements_to_net)
            return True
        LOGGER.info('Not Valid Capital and Interest Net')                    
        return False

        
    def payCapital(self, settlement):
        if not settlement or not settlement.Trade():
            return False
        LOGGER.info('checking for valid Capital Pay Out for settlement %s' % settlement.Oid())
        settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
        allow_types = ["Fixed Amount", "Payment Cash"]

        if settle_instruct == "Pay Out : Capital":
            LOGGER.debug('settle_instruct matched: Pay Out : Capital')
            settlements = settlement.Trade().Settlements().AsArray()
            settlements_to_net = self._get_valid_settlements_to_net(
                settlements,
                allow_types
            )

            if len(settlements_to_net) > 1:
                OperationsSTPFunctions.net_settlements(settlements_to_net)
                return True
    
        LOGGER.info('Not Valid Capital net payment')                          
        return False

    def payInterest(self, settlement):
        if not settlement or not settlement.Trade():
            return False
        LOGGER.info('checking for valid Interest Pay Out for settlement %s' % settlement.Oid())
        settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
        allow_types = ["Fixed Rate", "Payment Cash"]

        if settle_instruct == "Pay Out : Interest":
            LOGGER.debug('settle_instruct matched: Pay Out : Interest')
            settlements = settlement.Trade().Settlements().AsArray()
            settlements_to_net = self._get_valid_settlements_to_net(
                settlements,
                allow_types
            )

            if len(settlements_to_net) > 1:
                OperationsSTPFunctions.net_settlements(settlements_to_net)
                return True

        LOGGER.info('Not Valid Interest  net Payment')
        return False


class NetMaturitySettlementsSTPAutoReleaseHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP for triggered by setting
    the MM Settle Instruct 
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Net Maturity Settlements Based on MM Settle Insturct Auto Release Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject
            if not settlement.Trade():
                return False
        
            if settlement.Instrument().InsType() in ["Deposit", "FRN"]:
                if settlement.Status() == 'Authorised':
                    settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
                    trade = settlement.Trade()
                    if trade.Acquirer().Name() == 'Funding Desk':
                        if settle_instruct in SETTLE_INSTUCT_LIST:
                            if check_for_valid_confo_details(trade, 'Matched', ["Maturity Notice"]):
                                return True
                        elif settlement.RelationType() == 'Ad Hoc Net':
                            if settlement.Currency().Name() == 'ZAR':
                                if check_for_valid_confo_details(trade, 'Matched', ["Maturity Notice"]):
                                    return True
        elif eventObject.IsKindOf(acm.FConfirmation):
            confo = eventObject
            if confo.Status() == "Matched":
                if check_for_valid_confo_doc_type(confo, '320'):
                    return True
                
                elif confo.EventChlItem().Name() == 'Maturity Notice':
                    return True

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        settlement = None
        if eventObject.IsKindOf(acm.FSettlement):
            settlement = eventObject
        elif eventObject.IsKindOf(acm.FConfirmation):
            confirmation = eventObject
            trade = confirmation.Trade()
            settlements = trade.Settlements().AsArray()
            for settlement in settlements:
                if settlement.Currency().Name() != 'ZAR':
                    continue
                if settlement.ValueDay() != acm.Time().DateToday():
                    continue
    
                settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
                if settlement.RelationType() ==  'Ad Hoc Net':
                    if settlement.Status() == 'Authorised':
                        LOGGER.debug('Matched Ad Hoc Net Setttlement : {set_id}'.format(set_id=settlement.Oid()))
                        break
                elif settle_instruct == "Pay Out : Interest":
                    if settlement.Type() == "Fixed Rate" and settlement.Status() == 'Authorised':
                        LOGGER.debug('Matched Fixed Rate Setttlement : {set_id}'.format(set_id=settlement.Oid()))
                        break
                elif settle_instruct == "Pay Out : Capital":
                    if settlement.Type() == "Fixed Amount" and settlement.Status() == 'Authorised':
                        LOGGER.debug('Matched Fixed Amount Setttlement : {set_id}'.format(set_id=settlement.Oid()))
                        break
    
        if settlement and settlement.Currency().Name() == 'ZAR':
            if settlement.Trade() and OperationsSTPFunctions.is_outgoing_settlement(settlement):
                if settlement.ValueDay() == acm.Time().DateToday():
                    settle_instruct = settlement.AdditionalInfo().Settle_Instruct()
                    if self.payNettedSettlements(settlement):
                        LOGGER.info('Performing STP for Netted Settlements')
                        OperationsSTPFunctions.release_settlement(settlement)
                
                    elif settlement.Type() == "Fixed Rate":
                        if settle_instruct == "Pay Out : Interest":
                            LOGGER.info('Performing STP for Interest payment')
                            OperationsSTPFunctions.release_settlement(settlement)

                    elif settlement.Type() == "Fixed Amount":
                        if settle_instruct == "Pay Out : Capital":
                            LOGGER.info('Performing STP for Capital payment')
                            OperationsSTPFunctions.release_settlement(settlement)

    def payNettedSettlements(self, settlement):
        LOGGER.info('payNettedSettlements : checking for netted settlements')

        if settlement.RelationType() == 'Ad Hoc Net':
            LOGGER.info('RelationType : Ad Hoc Net')
            for child in settlement.Children():
                if child.Type() not in ["Fixed Amount", "Fixed Rate", "Payment Cash"]:
                    LOGGER.debug('type : {type} not valid'.format(type=child.Type()))
                    return False
            if settlement.Parent():
                LOGGER.info('' % settlement.Oid())
                LOGGER.info(
                    'settlement : is not the parent settlement {set_id}'.format(
                    set_id=settlement.Oid())
                )
                return False
            LOGGER.info('Valid Netted Settlement')
            return True
        return False
