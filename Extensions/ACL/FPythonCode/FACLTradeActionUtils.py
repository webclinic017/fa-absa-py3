""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLTradeActionUtils.py"
import acm
import FBDPCommon

def is_trade_action_close( trade ):
    answer = False
    if trade.Type() == "Closing" and trade.Contract():
        answer = True        
    return answer

def is_trade_action_novate( trade ):
    answer = False
    if trade.Type() in ( "Novated", "Novated Assigned" ):
        answer = True        
    return answer

def is_trade_action_mirror( trade ):
    answer = False
    if trade.TrxTrade():
        originalTrade = trade.TrxTrade()
        if originalTrade.Acquirer().Oid() == trade.Counterparty().Oid():
            answer = True        
    return answer

def is_trade_action_exercise( trade ):
    answer = False
    if trade.Type() in ("Exercise",  "Assign",  "Abandon") and trade.Contract():
        answer = True        
    return answer

def is_trade_action_prolong( trade ):
    insType = trade.Instrument().InsType()

    if trade.IsFxSwap():
        # the 8th bit is TRADE_PROCESS_PROLONG_CHILD
        return trade.TradeProcess() & (1<<8) != 0
    elif (trade.Instrument().IsRepoInstrument() or insType == 'Deposit') and trade.Type() == 'Normal':
        contract = trade.Contract()
        return contract and contract.OriginalOrSelf().Oid() != trade.OriginalOrSelf().Oid() and\
            contract.OriginalOrSelf().Instrument().Oid() != trade.OriginalOrSelf().Instrument().Oid()
    
    return False

def is_trade_action_odf_merge( trade ):
    answer = False
    instrument = trade.Instrument()
    if instrument.IsKindOf( acm.FOdf ):
        for exerciseEvent in instrument.ExerciseEvents():
            if exerciseEvent.Type() == "DrawdownPeriod" and exerciseEvent.Strike() == 0.0 and exerciseEvent.Strike2() == 0.0:
                answer = True
                break
    return answer

def is_trade_part_of_trade_action( insDefApp ):
    returnValue = False

    trade = insDefApp.EditTrade()

    if not trade.Original():
        # it must be an unsaved clone
        if is_trade_action_close( trade ):
            returnValue = True
        elif is_trade_action_novate( trade ):
            returnValue = True
        elif is_trade_action_mirror( trade ):
            returnValue = True
        elif is_trade_action_exercise( trade ):
            returnValue = True
        elif is_trade_action_prolong( trade ):
            returnValue = True
        elif is_trade_action_odf_merge( trade ):
            returnValue = True
    
    return returnValue

def trade_is_repricing_close(trade):
    returnValue = False
    if trade.Type() == 'Closing':
        st = "contractTrdnbr = %s" % (trade.ContractTrdnbr())
        for t in acm.FTrade.Select(st):
            if t.Type() == 'Reprice':
                returnValue = True
        
    return returnValue

def is_reprice_type_trade( trade ):
    returnValue = False
    if trade.Type() == 'Reprice':
        returnValue = True
    elif trade_is_repricing_close(trade):
        returnValue = True

    return returnValue

def trade_is_corrected(trade):
    for be in trade.BusinessEvents('Correct Trade'):
        for tl in be.TradeLinks():
            if tl.Trade() == trade and tl.TradeEventType() == 'Cancel':                
                return True
    return False

def is_closing_type_trade(trade):
    if trade:
        return trade.Type() == 'Closing' or \
               trade.Type() == 'Novated' or \
               trade.IsDrawdownOffset()
    else:
        return False

def is_option_settlement_trade(trade):
    return trade and \
           trade.Type() in ('Exercise', 'Assign', 'Abandon') and \
           trade.Contract() and \
           trade.Contract().Instrument().Underlying() == trade.Instrument()

def calculate_remaining_nominal(trade):
    if trade.IsDrawdownOriginal():
        from math import copysign
        # RemainingDrawdownAmount returns absolute value, we need to preserve it
        raw = copysign(trade.RemainingDrawdownAmount(), trade.Nominal())
    else:
        raw = acm.TradeActionUtil().RemainingNominal(trade, trade.ValueDay(), trade.AcquireDay())
    # When doing a full close, this value is sometimes slightly different from zero due to rounding issues.
    return round(raw, 4)

def isFXNDF_trade(trade):
    insaddr = FBDPCommon.acm_to_ael(trade.Instrument())
    ins_is_fx_ndf = (insaddr.instype == 'Future/Forward' and
            insaddr.und_instype == 'Curr' and
            insaddr.paytype == 'Forward' and
            insaddr.settlement == 'Cash')
    return ins_is_fx_ndf
