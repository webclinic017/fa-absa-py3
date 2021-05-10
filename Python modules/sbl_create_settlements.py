"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        Create adhoc settlement
DESK                 :  SBL PTS
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-16  CHG0105578     Libor Svoboda       Initial Implementation
"""
import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from FSettlementCreator import SettlementCreator
from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
from FSettlementEnums import SettlementType


LOGGER = getLogger(__name__)


ael_variables = AelVariableHandler()
ael_variables.add(
    'trade',
    label='Trade',
    cls='FTrade',
    multiple=True,
)
ael_variables.add(
    'settlement_status',
    label='New Settlement Status',
    cls='string',
    collection=acm.FEnumeration['enum(SettlementStatus)'].Enumerators(),
    multiple=False,
    default='Settled',
)


class SettlementCreatorCustom(SettlementCreator):
    
    def __init__(self, start_date, end_date):
        super(SettlementCreatorCustom, self).__init__()
        self._start_date = start_date
        self._end_date = end_date
    
    def _SettlementCreator__GetSettlements(self, trade):
        return trade.GenerateSettlements(self._start_date, self._end_date)
    
    def _SettlementCreator__IsPreventSettlement(self, settlement, isExDateApproved):
        isPreventSettlement = False
        addInfos = settlement.Trade().AdditionalInfo()
        
        if (settlement.Type() == SettlementType.NONE):
            isPreventSettlement = True
        elif 'MM_Ceded_Amount' in dir(addInfos) and 'MM_Account_Ceded' in dir(addInfos) and addInfos.MM_Account_Ceded() is True:
            # Check if the add infos exist on the trade
            if addInfos.MM_Ceded_Amount():
                # Check if account is ceded and if the ceded amount is set
                if (round(settlement.Amount(), 2)) == (settlement.Trade().AdditionalInfo().MM_Ceded_Amount()*-1):
                    # Block settlement if ceded amount is equal to the settle amount
                    isPreventSettlement = True
        elif self._SettlementCreator__depositHandler.PreventSettlementCreation(settlement) or \
           not isExDateApproved or (settlement.Amount() == 0.0):
            isPreventSettlement = True
        elif self._SettlementCreator__IsCreditDefaultLegTypeSettlement(settlement):
            isPreventSettlement = True
        return isPreventSettlement


def get_swift_flag(trade):
    if trade.AdditionalInfo().SL_SWIFT() == 'SWIFT':
        return True
    if trade.AdditionalInfo().SL_SWIFT() == 'DOM':
        return False
    return True


def create_settlement_for_trade(trade, settlement_status):
    if not trade:
        return
    LOGGER.info('Creating settlements for trade %s.' % trade.Oid())
    settlements = acm.FSettlement.Select('trade=%s and type in ("Security Nominal", "End Security")'
                                         % trade.Oid())
    if settlements:
        LOGGER.warning('Trade %s: "Security Nominal" or "End Security" settlement already exists.' 
                       % trade.Oid())
        return
    instrument = trade.Instrument()
    start_date = instrument.StartDate()
    end_date = instrument.ExpiryDateOnly()
    correct_trade_recaller = FSettlementCorrectTradeRecaller()
    settlement_creator = SettlementCreatorCustom(start_date, end_date)
    settlements = settlement_creator.CreateSettlements(trade, correct_trade_recaller)
    if not settlements:
        LOGGER.warning('Trade %s: No settlements generated.' % trade.Oid())
        return
    swift = get_swift_flag(trade)
    LOGGER.info('Trade %s: Swift flag %s.' % (trade.Oid(), swift))
    created_settlements = []
    security_settlements = [settlement for settlement in settlements 
                            if settlement.Type() in ("Security Nominal", "End Security")]
    LOGGER.info('Trade %s: Number of security settlements: %s.' 
                % (trade.Oid(), len(security_settlements)))
    trade_counterparty = trade.Counterparty()
    acm.BeginTransaction()
    try:
        for settlement in security_settlements:
            if len(security_settlements) > 1 and not swift:
                if trade_counterparty.Name() == 'SBL AGENCY I/DESK':
                    if settlement.Amount() >= 0 and settlement.Type() == "End Security":
                        continue
                    if settlement.Amount() <= 0 and settlement.Type() == "Security Nominal":
                        continue
                if trade_counterparty.Name() == 'ABSA SECURITIES LENDING':
                    if settlement.Amount() <= 0 and settlement.Type() == "End Security":
                        continue
                    if settlement.Amount() >= 0 and settlement.Type() == "Security Nominal":
                        continue
            settlement.Status(settlement_status)
            settlement.ValueDay(start_date)
            settlement.Commit()
            created_settlements.append(settlement)
            LOGGER.info('Trade %s: Committing settlement, type: %s, status: %s, value day: %s.' 
                        % (trade.Oid(), settlement.Type(), settlement.Status(), settlement.ValueDay()))
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception('Trade %s: Failed to create settlements.' % trade.Oid())
        return
    
    for settlement in created_settlements:
        counterparty = trade_counterparty
        modified_party_name = ''
        if settlement.Type() == 'Security Nominal':
            modified_party_name = trade.AdditionalInfo().SL_G1Counterparty1()
        if settlement.Type() == 'End Security':
            modified_party_name = trade.AdditionalInfo().SL_G1Counterparty2()
        if modified_party_name:
            counterparty = (acm.FParty[modified_party_name] 
                            if acm.FParty[modified_party_name] else counterparty)
        account = acm.Operations.AccountAllocator().CalculateCounterpartyAccountForSettlement(settlement, counterparty)
        settlement_image = settlement.StorageImage()
        settlement_image.Counterparty(counterparty)
        settlement_image.CounterpartyName(counterparty.Name())
        settlement_image.CounterpartyAccountRef(account)
        try:
            settlement_image.Commit()
            LOGGER.info('Trade %s: Modified SBL settlement %s.' 
                        % (trade.Oid(), settlement.Oid()))
        except:
            LOGGER.exception('Trade %s: Failed to modify SBL settlement %s.' 
                             % (trade.Oid(), settlement.Oid()))


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    trades = ael_params['trade']
    settlement_status = ael_params['settlement_status']
    for trade in trades:
        create_settlement_for_trade(trade, settlement_status)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')

