import acm

"""----------------------------------------------------------------------------

MODULE

    AutoStartAlgos: Methods for an ATS to Automatically start Execution Agents.
    Start the ATS with -module_name AutoStartAlgos
    
    (C) Copyright 2013 Front Capital Systems AB. All rights reserved.

DESCRIPTION


NOTES:
    
     
    
------------------------------------------------------------------------------"""


def start():
    marketPlaces = acm.Trading.GetConnectableMarketPlaces()
    
    for m in marketPlaces :
        m.Connect()
    
    """
    
    # Example of how a real OrderSheetTemplate can be used as input for automatic 
    # dispatching of Agents. Needed if user want a specific Order Filter that e.g 
    # filters out some specific Trading Strategies, OrderBook etc.
    
    workbooks  = acm.FWorkbook.Select('createUser = ' + str(acm.FUser[acm.UserName()].Oid()))
    templates  = acm.FTradingSheetTemplate.Select('name = sheetTemplateName')
    template   = templates.At(0)

    dispatcher = acm.Trading.CreateOrderDispatcher(template)
    
    """
    
    dispatcher = acm.Trading.CreateOrderDispatcher(None)
    dispatcher.Enable(True)
    
    return

def stop():
    marketPlaces = acm.Trading.GetConnectableMarketPlaces()
    
    for m in marketPlaces :
        m.Disconnect()

    
def work():
    return 1
