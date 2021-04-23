import acm, ael
'''================================================================================================
================================================================================================'''
def trade_system(trade,*rest):
    if trade.trdnbr != None:
        trade = acm.FTrade[trade.trdnbr]
        if trade.IsFxSwapFarLeg(): trade = trade.FxSwapNearLeg()
        if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
        if trade.Trader().Name() == 'STRAUSD': return 'MIDAS CFR'
        Key = trade.OptionalKey()
        if len(Key.split('|')) > 1: return Key.split('|')[1]
    return ''    
'''================================================================================================
================================================================================================'''
def reuters_feed(trade,*rest):
    if trade.group_trdnbr!= None: trade = trade.group_trdnbr
    key = trade.optional_key if trade.insaddr.instype in ['Curr', 'FXOptionDatedFwd'] else trade.insaddr.extern_id1
    if len(key.split('#')) > 1: return key.split('#')[0]
'''================================================================================================
================================================================================================'''
def midas_dealno(trade,*rest):
    trade = acm.FTrade[trade.trdnbr]
    if trade.IsFxSwapFarLeg(): trade = trade.FxSwapNearLeg()
    if trade.GroupTrdnbr()!= None: trade = trade.GroupTrdnbr()
    if trade.Trader().Name() == 'STRAUSD':
        if trade.OptionalKey() == '':
            MidasNo = trade.add_info('Source Trade Id')
        else:    
            MidasNo = trade.OptionalKey()
        if len(MidasNo.split('_')) > 1:
            return MidasNo.split('_')[1]    
    else:
        if trade.YourRef() == '':
            if len(trade.OptionalKey().split('|')) > 1:
                optkey = trade.OptionalKey().split('|')[0]
                return optkey[4:10]
        else:
            return trade.YourRef()
    return ''        
'''================================================================================================
print trade_system(ael.Trade[68617355])
================================================================================================'''
#print midas_dealno(ael.Trade[68617354])
#print trade_system(ael.Trade[68617354])
