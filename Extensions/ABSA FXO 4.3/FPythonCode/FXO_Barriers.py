'''
MODULE
    FXO_Barriers
    
DESCRIPTION
    Date                :2011-01-01
    Purpose             :Create Vanilla trades for crossed barriers
    Department and Desk : IT Pricing & Risk, FX Options
    Requester           : Matt Berry
    Developer           : Zaakirah Kajee
    CR Number           : 
    
UPDATES
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-05-25    667266          Zaakirah Kajee     Include Trade on new trade


'''
import acm
def createTrade(trade,Ins=0, qFac=1,type='Normal'):

    today = acm.Time().DateNow()
    newTrade = acm.FTrade()
    if Ins:
        newTrade.Instrument(Ins)
    else:
        newTrade.Instrument(trade.Instrument())
    newTrade.Currency(trade.Currency())
    newTrade.TradeTime(today)
    newTrade.AcquireDay(today)
    newTrade.ValueDay(today)
    newTrade.Acquirer(trade.Acquirer())
    newTrade.Portfolio(trade.Portfolio())
    newTrade.Counterparty(trade.Counterparty())
    newTrade.Quantity(trade.Quantity()*qFac)
    newTrade.TrxTrade(trade.Oid())
    newTrade.Trader(trade.Trader())
    newTrade.Type(type)
    newTrade.Status('FO Confirmed')
    
    return newTrade

def createInstrument(trade):
    ins = trade.Instrument()
    newi = ins.Clone()
    newi.Barrier(0)
    newi.MtmFromFeed('No')
    newi.Name(newi.SuggestName())
    newi.ExoticType(0)
    newi.Commit()
    newi.ExoticEvents().Delete()
    newi.Exotics().Delete()
    newi.Commit()
    return newi

def IsClosed(trade):
    
    if trade.Type() != 'Normal':
        print 'Trade : ', trade.Oid(), 'Is of Type ', trade.Type()
        return True
    ins = trade.Instrument()
    trades = ins.Trades()
    for t in trades:
        if t.Type() == 'Closing' and t.TrxTrade() and t.TrxTrade().Oid() == trade.Oid() and t.Oid != trade.Oid() \
         and t.Status() not in ('Void', 'Simulated') and t.Oid() > 0:
            print 'Trade : ', trade.Oid(), 'has been closed. ', t.Oid()
            return True
    return False

def IsValidInstrument(trade):
    ins = trade.Instrument()
    if ins.IsBarrier() and not ins.Digital() and ins.Exotic().BarrierOptionType() in ('Up & In', 'Down & In', 'Double In'):
        return True
    print 'Trade : ', trade.Oid(), 'is not a Valid Instrument. '
    return False
    
def IsConfirmed(trade):
    ins = trade.Instrument()
    if ins.IsBarrier() and ins.Exotic().BarrierCrossedStatus() == 'Confirmed':
        return True
    print 'Trade : ', trade.Oid(), 'Barrier Crossed Status has not been confirmed.'
    return False

def ProcessKnockInBarriers(trades):
    
    print '\n', '*' * 70, '\n'
    for t in trades:
        if not IsClosed(t) and IsValidInstrument(t) and IsConfirmed(t) :
            vanillaIns = createInstrument(t)
            try:
                acm.BeginTransaction()
                
                closeTrade = createTrade(t, qFac=-1, type='Closing')
                vanillaTrade = createTrade(t, Ins = vanillaIns)

                closeTrade.Commit()
                vanillaTrade.Commit()
                acm.CommitTransaction()
                print 'Trade Process: ', t.Oid(), ' Close Out Trade: ', closeTrade.Oid(), ' New Vanilla Trade: ', vanillaTrade.Oid()
            except Exception, e:
                print 'Trade Process: ', t.Oid(), ' ERROR processing Trade', str(e)
                acm.AbortTransaction()
        else:
            print 'Trade Process: ', t.Oid(), ' has been ignored.'
    print '\n', '*' * 70


def FXO_GUI_CALL(object):
    trade = object.ExtensionObject().OriginalTrade()
    if trade:
        ProcessKnockInBarriers([trade])
        
