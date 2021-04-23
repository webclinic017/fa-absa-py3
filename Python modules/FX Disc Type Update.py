'''
Purpose: script for a scheduled task to ensure that all fx cash and fx payments trades have the correct discount type  
Department : Trading
Desk : FX
Requester :  As a result of the upgrade to 2013.3
Developer : Anil Parbhoo
CR Number : N/A
Jira Reference Number : FAU-161

'''






import acm, ael

# predefine 'CCYBasis' as a DiscType in the choice list before running this script

def OtherFXSwapTrade(fx):

    if fx.IsFxSwapNearLeg():
        b = fx.FxSwapFarLeg().Oid()
        
    else:
        b = fx.FxSwapNearLeg().Oid()
    return b
        
def set_DiscType_non_FxSwap(trade):
    
    trade.DiscountingType('CCYBasis') 
    try:
        trade.Commit()
    except:
        acm.Log('could not commit the disc type for trade %s' %trade.Oid()) 
            
            
            
def set_DiscType_FxSwap(trade):
    
    otherTradeNumber = OtherFXSwapTrade(trade)
                
    t = ael.Trade[trade.Oid()] #t represents the ael trade
    ot = ael.Trade[otherTradeNumber] #ot represents the other ael trade
    disc_type_choice = ael.ChoiceList.read('list="DiscType" and entry="CCYBasis"')
    t = t.clone()
    t.disc_type_chlnbr = disc_type_choice
    try:
        t.commit_fx_swap(ot)
    except:
        acm.Log('could not commit the disc type for FX SWAP trade %s' %trade.Oid())
        



   
#-----------------------


List            = acm.FChoiceList['DiscType'].Choices()
TradeFilters    = acm.FTradeSelection.Select('').Sort()

ael_variables = \
[
['trades', 'Trade Filter', 'string', TradeFilters, 'fx cash trades not settled', 1, 0, '']
]




def ael_main(ael_dict):


    selection = acm.FTradeSelection[ael_dict['trades']]
    for trd in selection.Trades():

        
        if trd.Instrument().InsType()=='Curr':

            if trd.IsFxSwap():
                if not trd.MirrorTrade():
            
                    if trd.DiscountingType():
                        if trd.DiscountingType().Name() != 'CCYBasis':
                            set_DiscType_FxSwap(trd)
                    else:
                        set_DiscType_FxSwap(trd)
        
            else:
                if not trd.MirrorTrade():
                    if trd.DiscountingType():
                        if trd.DiscountingType().Name() != 'CCYBasis':
                            set_DiscType_non_FxSwap(trd)
                    else:
                        set_DiscType_non_FxSwap(trd)
            
        else:
            print 'trade %s is not a fx cash trade' % trd.Oid()
            
            
    print 'completed successfully'
        
        
