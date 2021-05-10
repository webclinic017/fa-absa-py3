""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLUtils.py"
import acm
from FACLTradeActionUtils import is_trade_action_prolong

# ************************************************
# Create an FX Swap Far Leg Trade from InsDefApp
# ************************************************
def fxSwapFarLegTradeFromNearLegTrade(nearLegTrade, fxSwapDictionary):
    trade = nearLegTrade
    if nearLegTrade and nearLegTrade.IsFxSwap():
        farTrade = acm.FX.GetSwapFarTrade(nearLegTrade)
        
        if not farTrade:
            # Copy editTrade and create a new near leg
            nearTrade = acm.FTrade()
            nearTrade.Apply(nearLegTrade)
            nearTrade.RegisterInStorage()
            nearTrade.ConnectedTrade(nearTrade)
            
            # To allow Reference attribute to be properly evaluated for this swap
            nearTrade.AdditionalInfo().ACR_REF(nearLegTrade.OriginalOrSelf().Oid())
            
            # Copy editTrade, fill from dictionary and create a new far leg
            farTrade = acm.FTrade()
            farTrade.Apply(nearLegTrade)
            farTrade.RegisterInStorage()
            farTrade.Currency(fxSwapDictionary.At('currencyName'))
            farTrade.Instrument(fxSwapDictionary.At('instrumentName'))
            farTrade.ValueDay(fxSwapDictionary.At('valueDay'))
            farTrade.AcquireDay(fxSwapDictionary.At('acquireDay'))
            farTrade.Quantity(fxSwapDictionary.At('quantity'))
            farTrade.Premium(fxSwapDictionary.At('premium'))
            farTrade.Price(fxSwapDictionary.At('price'))
            farTrade.ClsStatus(fxSwapDictionary.At('clsStatus'))
            farTrade.TradeProcess(32768)
            farTrade.ConnectedTrade(nearTrade)
    
        trade = farTrade
        
    return trade
    
def fxOptionDatedFwdTrade(odfTrade, exerciseEventDicts):
    def populateExerciseEvents(ins, exerciseEventDicts):
        for eventDict in exerciseEventDicts:
            event = acm.FExerciseEvent()
            event.RegisterInStorage()
            event.Strike(eventDict.At('strike'))
            event.Strike2(eventDict.At('strike2'))
            event.StartDate(eventDict.At('startDate'))
            event.EndDate(eventDict.At('endDate'))
            event.Type('DrawdownPeriod')
            ins.ExerciseEvents().Add(event)
            
        
    trade = odfTrade
    if odfTrade and odfTrade.Instrument().InsType() == 'FXOptionDatedFwd':
        trade = acm.FTrade()
        trade.RegisterInStorage()
        trade.Apply(odfTrade)
        trade.AdditionalInfo().ACR_REF(odfTrade.OriginalOrSelf().Oid())
        
        ins = acm.FOdf()
        ins.Apply(trade.Instrument().Clone())
        ins.RegisterInStorage()
            
        if exerciseEventDicts:
            ins.DeleteExerciseEvents()
            populateExerciseEvents(ins, exerciseEventDicts)
            
        trade.Instrument(ins)

    return trade

def ensureConnectedToAMB(username, password, address, ambModule = None):
    ambModule = __import__('amb') if ambModule is None else ambModule
    ambModule.mb_close()
    loginStr = address
    if username != None and password != None:
        loginStr = '%s/%s/%s' % (loginStr, username, password)
    try:
        ambModule.mb_init(loginStr)
    except Exception as e:
        raise Exception('Could not connect to AMB at "%s": %s' % (loginStr, str(e)))
    try:
        ambModule.mb_get_socket()
    except Exception as e:
        raise Exception('No connection to AMB ...')

# ************************************************
# Trade to read the (updated) attributes from 
# ************************************************
def faclObjectFromInsDef(insDefApp):
    trade = insDefApp.EditTrade()
    if trade.IsFxSwap() and trade.IsFxSwapNearLeg():
        fxSwapDictionary = insDefApp.FxSwapFarTradeDictionary().At('fxSwapFarLeg')
        trade = fxSwapFarLegTradeFromNearLegTrade(trade, fxSwapDictionary)
    elif trade.Instrument().InsType() == 'FXOptionDatedFwd':
        exerciseEventDicts = insDefApp.FOdfDictionary().At('odf').At('drawDownPeriod')
        trade = fxOptionDatedFwdTrade(trade, exerciseEventDicts)
    return trade
    

# is prolong child (includes early delivery)
def IsProlongChild(trade):
    return trade.TradeProcess() & 256 != 0

def IsDepositProlongChild(trade):
    return trade.Instrument().InsType() == 'Deposit' and is_trade_action_prolong(trade)
    
def IsRepoProlongChild(trade):
    return trade.Instrument().IsRepoInstrument() and is_trade_action_prolong(trade)
    
def IsSecurityLoanProlongChild(trade):
    return trade.Instrument().InsType() == 'SecurityLoan' and is_trade_action_prolong(trade)
