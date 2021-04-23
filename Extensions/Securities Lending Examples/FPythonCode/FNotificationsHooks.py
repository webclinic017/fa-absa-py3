""" Compiled: 2018-09-19 12:03:25 """

#__src_file__ = "extensions/SecuritiesLending/etc/FNotificationsHooks.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FNotificationsHooks

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Hooks for customising the behaviour of the Notification Viewer.

------------------------------------------------------------------------------------------------"""


import acm
import FSheetUtils
from FSecLendUtils import logger
from ACMPyUtils import Transaction

try:
    import FNotificationsCustomHooks
except StandardError:
    FNotificationsCustomHooks = None

def GetCustomHook(ObjName):
    if FNotificationsCustomHooks is not None:
        if hasattr(FNotificationsCustomHooks, ObjName):
            return getattr(FNotificationsCustomHooks, ObjName)



def OnHandleRerateAlerts(alert, *args):

    hook = GetCustomHook("OnHandleRerateAlerts")
    if hook is not None:
        return hook()
    from FSecLendReratePanel import RerateProcessing   
    Theor_Fee_Col = 'Security Loan Suggested Fee'    
    cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FAlertSheet')
    rerateDict = acm.FDictionary()
    if alert is not None:
        values = []
        ruleSelected = alert.AppliedRule()
        if alert.Subject().IsKindOf(acm.FSecurityLoan):
            ins = alert.Subject()
            fee = cs.CreateCalculation(alert, Theor_Fee_Col).Value()
            date = acm.Time.DateToday()
            calInfo = ins.PayLeg().Currency().Calendar().CalendarInformation()
            if calInfo and calInfo.IsNonBankingDay(date):
                date = calInfo.AdjustBankingDays(date, 1)
            values = [fee, date, ins]
        if values:
            rerateDict.AtPut(ins.Name(), values)
    RerateProcessing(rerateDict)
    return



def OnDetailsRerateAlerts(alerts, *args):

    hook = GetCustomHook("OnDetailsRerateAlerts")
    if hook is not None:
        return hook()
        
    if alerts:
        import ViewLauncher
        trdMgr = ViewLauncher.Launch('SecLendPortfolioView')
        sheet = trdMgr.ActiveWorkbook().ActiveSheet()
        ins = alerts.Transform('Subject', acm.FSet, None)
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        opNode = None
        opNode = query.AddOpNode('OR')
        for i in ins:
            opNode.AddAttrNode('Instrument.Name', 'EQUAL', i.Name())
        sheet.InsertObject(acm.FASQLQueryFolder(name = 'Rerate Warning Instruments', asqlQuery=query), 1)
        FSheetUtils.ApplyGrouperToSheet(sheet, 'Underlying/Counterparty')
        FSheetUtils.ExpandTree(sheet, level=3)
        trdMgr.ShowDockWindow('SecLendReratePanel')
    else:
        return

def OnHandleRecallAlerts(alert,*args):
    hook = GetCustomHook("OnHandleRecallAlerts")
    if hook is not None:
        return hook()
    
    import FSecLendHooks
    import FSecLendReturns
    
    target = alert.TargetObject()
    targetKey = target.TargetId()
    threshold = alert.Threshold().ThresholdValue()
    try:
        nominal = float(alert.Information())
        recallNom = nominal - threshold
    except:
        recallNom = 0.0
        logger.error("Can't convert '%s' to float. {}".format(alert.Information()))
    
    positionDesc = acm.FCustomArchive[targetKey]
    positionParams = positionDesc.FromArchive('attributes')
    
    # Return API requires Counterparty and Underlying for return candidates.
    underlying = positionParams['Underlying'] if positionParams['Underlying'] else None
    counterparty = positionParams['Counterparty'] if positionParams['Counterparty'] else None   
    
    if not (counterparty or underlying):
        logger.error('Counterparty grouper is needed. No trades to return')
        return
        
    # Retrieve quantity from recall nominal based on the current underlying price
    quantity = 0
    space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    marketPrice = underlying.Calculation().MarketPrice(space).Value().Number()
    if marketPrice and marketPrice != 0:
        quantity = int(recallNom/marketPrice)
    
    # For returning trades, reverse sign of quantity
    quantity = -1*quantity
    
    trades = []
    try:
        query = FSecLendHooks.ActiveLoansQuery(counterparty, [underlying])
        query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.DefaultTradeStatus())
        query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.OnHoldTradeStatus())
        activeLoans = query.Select()
        trades = FSecLendReturns.CreateReturnTrades(activeLoans, 
                                                    quantity, 
                                                    clientReturns=False if quantity < 0 else True, 
                                                    returnPartial=False,
                                                    returntype='recall')
    except FSecLendReturns.NoQuantityFoundError:
        logger.error('Quantity to return must be a number.')
    except FSecLendReturns.NoReturnLoansFoundError:
        logger.error('No loans found to return from.')
    except Exception as e:
        logger.error('CreateReturnTrades Error:{}'.format(e))    

    with Transaction():
        for trade in trades:
            trade.Simulate()
            if trade.Instrument().IsInfant():
                trade.Instrument().Commit()
            trade.Commit()



def OnDetailsRecallAlerts(alerts, *args):

    hook = GetCustomHook("OnDetailsRecallAlerts")
    if hook is not None:
        return hook()
        
    if alerts:
        import FSecLendOrdersView
        eii = acm.UX().SessionManager()
        FSecLendOrdersView.OrderManagerMenuItem(eii).Invoke(eii)
    else:
        return
