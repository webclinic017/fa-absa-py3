"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SBLSettlementsSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the creation of SBL MT5xx settlements

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-02-06                      Tawanda Mukhalela       Gasant Thulsie          Auto Hold and Release Settlements
2020-11-30                      Buhlebezwe Ngubane      Gasant Thulsie          Auto Release New Security Loan Settlements
-----------------------------------------------------------------------------------------------------------------------------------------
"""
import acm
from at_logging import getLogger
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook

LOGGER = getLogger(__name__)


class AutoHoldSBLSettlementSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the SBL
    Settlements. Move settlment to hold if conditions are met.
    """

    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Auto Hold SBL Security Settlement STP Hook'

    # noinspection PyPep8Naming,PyPep8Naming
    def IsTriggeredBy(self, settlement):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not _is_valid_sbl_settlement(settlement):
            return False
            
        partial_return_identifier = settlement.Trade().Text1()
        if settlement.Status() != 'Authorised':
            return False
        if partial_return_identifier != 'PARTIAL_RETURN':
            return False
        loan_trade = settlement.Trade().ContractTrdnbr()
        if _is_settled_loan_settlements(loan_trade):
            return False

        return True

    # noinspection PyPep8Naming
    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.
        """
        LOGGER.info("Loan Settlements are not yet Settled, Auto Holding Return Settlement")
        LOGGER.info("Auto Holding Settlement with id {settlement}".format(settlement=settlement))
        OperationsSTPFunctions.hold_settlement(settlement)


class AutoAuthoriseSBLSettlementSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the SBL
    Settlements. Move settlement to Authourised status if conditions are met.
    """

    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Authorise Held SBL Security Settlement STP Hook'

    # noinspection PyPep8Naming,PyPep8Naming
    def IsTriggeredBy(self, settlement):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not _is_valid_sbl_settlement(settlement):
            return False
            
        partial_return_identifier = settlement.Trade().Text1()
        if settlement.Status() != 'Settled':
            return False
        if partial_return_identifier not in ['', None]:
            return False
        loan_trade = settlement.Trade().ContractTrdnbr()
        if not _is_settled_loan_settlements(loan_trade):
            return False

        return True

    # noinspection PyPep8Naming
    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        partial_return_trades = list()
        next_trade = settlement.Trade().ConnectedTrade()
        partial_return_trades.append(next_trade)

        while next_trade.ConnectedTrade() != settlement.Trade():
            partial_return_trades.append(next_trade.ConnectedTrade())
            next_trade = next_trade.ConnectedTrade()
        settlements = _get_valid_return_settlements(partial_return_trades)
        for settlement in settlements:
            if settlement.Status() == 'Hold':
                LOGGER.info("Loan Settlements have been Settled")
                LOGGER.info("Authorising Settlement with id {settlement}".format(settlement=settlement.Oid()))
                OperationsSTPFunctions.authorise_settlement(settlement)

                
class AutoReleaseSBLSettlementSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the SBL
    Settlements. Move settlement to Released status if conditions are met.
    """
    
    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Release Authorised SBL Security Settlement STP Hook'

    # noinspection PyPep8Naming,PyPep8Naming
    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False

        settlement = eventObject
        
        if not _is_valid_sbl_security_loan(settlement):
            return False
            
        partial_return_identifier = settlement.Trade().Text1()
        if settlement.Status() != 'Authorised':
            return False
        
        if partial_return_identifier not in ['', None]:
            return False

        return True

    # noinspection PyPep8Naming
    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        
        OperationsSTPFunctions.release_settlement(settlement)


class AutoSetCallConfirmationSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the SBL
    Settlements. Set flag on SBL confirmation
    """

    # noinspection PyPep8Naming
    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'SBL Auto Set Call Confirmation for Manual Release'

    # noinspection PyPep8Naming,PyPep8Naming
    def IsTriggeredBy(self, settlement):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if not _is_valid_sbl_fee_settlement(settlement):
            return False

        return True

    # noinspection PyPep8Naming
    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        additional_info_field = 'Call_Confirmation'
        additional_info_value = 'SBLManualRelease'
        settlement.AddInfoValue(additional_info_field, additional_info_value)
        LOGGER.info("Auto-setting Call_Confirmation for Settlement with id {settlement}".format(settlement=settlement.Oid()))
        settlement.Commit()


def _is_settled_loan_settlements(loan_trade):
    """
    returns True if any of the loan Security Settlements are Settled
    """
    trade = acm.FTrade[loan_trade]
    settlements = trade.Settlements().AsArray()
    if settlements:
        for settlement in settlements:
            if settlement.Status() == 'Settled':
                return True

    return False


def _is_valid_sbl_settlement(settlement):
    """
    Checks if given settlement is a valid settlement
    for the SBL Business
    """
    if not settlement.IsKindOf(acm.FSettlement):
        return False

    if not settlement.Trade():
        return False
        
    trade = settlement.Trade()
    acquirer = trade.Acquirer().Name()
    instrument = trade.Instrument().InsType()
    delivery_type = trade.AddInfoValue("SL_SWIFT")
    if instrument != 'SecurityLoan':
        return False
    if acquirer != 'SECURITY LENDINGS DESK':
        return False
    if delivery_type != 'SWIFT':
        return False
    if settlement.Type() not in ['Security Nominal', 'End Security']:
        return False

    return True


def _is_valid_sbl_fee_settlement(settlement):
    """
    Checks if given settlement is a valid settlement
    for the SBL Business
    """
    if not settlement.IsKindOf(acm.FSettlement):
        return False

    if not settlement.Trade():
        return False

    if settlement.AdditionalInfo().Call_Confirmation():
        return False
        
    if settlement.Status() != 'Authorised':
        return False
    acquirer = settlement.Trade().Acquirer().Name()
    instrument = settlement.Trade().Instrument().InsType()
    if acquirer not in ('SECURITY LENDINGS DESK', 'PRIME SERVICES DESK'):
        return False

    if acquirer == 'SECURITY LENDINGS DESK':
        if instrument != 'SecurityLoan':
            return False

    if acquirer == 'PRIME SERVICES DESK':
        if instrument != 'Deposit':
            return False
        if settlement.Trade().Portfolio().Name() != 'Call_SBL_Agency_Collateral':
            return False

    if settlement.Type() not in ['Cash', 'Loan Fee', 'Finder Fee', 'Call Fixed Rate Adjustable']:
        return False

    return True
    

def _is_valid_sbl_security_loan(settlement):
    instrument = settlement.Trade().Instrument()
    trade = settlement.Trade()
    
    if instrument.InsType() != 'SecurityLoan':
        return False
    
    if instrument.OpenEnd() != 'Open End':
        return False
    
    if trade.Type() != 'None':
        return False
    
    if trade.Status() != 'BO Confirmed':
        return False
    
    if trade.ContractTrdnbr() != trade.Oid():
        return False
        
    if trade.SettleCategoryChlItem().Name() != 'SL_STRATE':
        return False
    
    if settlement.Type() not in ['Security Nominal', 'End Security']:
        return False
    
    return True


def _get_valid_return_settlements(trades):
    """
    Gets all valid settlements for authorising
    """
    settlements = list()
    for trade in trades:
        if not trade.Settlements():
            continue
        for settlement in trade.Settlements():
            if settlement.Status() != 'Hold':
                continue
            if settlement.Type() in ['Security Nominal', 'End Security']:
                settlements.append(settlement)

    return settlements
