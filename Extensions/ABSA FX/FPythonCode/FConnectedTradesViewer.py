'''================================================================================================
Decscription:
        This module loads the graphical trades viewer , which shows a picture of trades that
        are connected via the trade groupnbr
================================================================================================'''
import acm
'''================================================================================================
================================================================================================'''
def insdefStartApplication(eii):
    insdef = eii.ExtensionObject()
    trade = insdef.OriginalTrade()
    acm.StartApplication("Connected Trades VIewer", trade)
'''================================================================================================
================================================================================================'''
def contextStartApplication(eii):
    shell = eii.Parameter('shell')    
    'ExtensionObject returns a FArray containing the real object'
    ob = eii.ExtensionObject()[0]
    if ob.IsKindOf(acm.FTrade):  
        acm.StartApplication("Connected Trades VIewer", ob)
'''================================================================================================
================================================================================================'''
