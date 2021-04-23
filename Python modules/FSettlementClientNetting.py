'''
Created on 29 jun 2009

@author: fregus01

Purpose : Module to define netting hooks used by settlement manager to determine if cashflows can be netted
Developer : Anwar Banoo, Willie van der Bank
Requestor : FATLM, Ops
Date : 2010-09-16, 852496 08/12/2011
Change : Add IRD desk netting rule for fix rate and floating rate cashflows to be netted, Bringing online of new desks
'''


import FOperationsUtils as Utils

def client_netting_1(settlement):
    """
    Input-parameter settlement is of type acm.FSettlement
    The client netting function shall return either True or False.
    Treat entity as read-only.
    """
    Utils.LogTrace()
    
    doNetting = False
    trade = settlement.Trade()
    legs = trade.Instrument().Legs()
    if legs:
        try:
            additionalInfo = trade.add_info('Funding Instype')
            firstLeg = legs.First()
            if firstLeg.AmortType() == 'Annuity' and additionalInfo == 'FDI':
                doNetting = True
        except RuntimeError:
            Utils.Log(True, "Additional info 'Funding Instype' not found")
    
    return doNetting

def Swap_netting(settlement):
    """
    Input-parameter settlement is of type acm.FSettlement
    The client netting function shall return either True or False.
    Treat entity as read-only.
    """
    Utils.LogTrace()
    
    insType = settlement.Trade().Instrument().InsType()
    try:
        #Money Market Desk, IRD DESK, FOREX DESK, LIQUID ASSET DESK, REPO DESK, FORWARDS DESK, Non Linear Deriv, Swaps Desk, ZZZ DO NOT USE IRP_FX Desk, NLD DESK, BONDS DESK
        return (settlement.Acquirer().Oid() in (2246, 30300, 16219, 17657, 30327, 215, 102, 17, 9693, 30311, 30326)) and (insType in ('Swap', 'CurrSwap', 'IndexLinkedSwap')) and (settlement.Type() in ('Fixed Rate', 'Float Rate'))
    except Exception, e:
        Utils.Log(True, e)
        return False

def is_valid_DIS_settlement(settlement):
    dis_acquirers = ['BAGL ACQUIRER', 'GROUP TREASURY']
    if settlement.SecurityInstrument():
        if settlement.SecurityInstrument().IssuingPayingAgent().Name() == 'ABSA BANK LIMITED':
            pass
        if settlement.SecurityInstrument().AddInfoValue('DIS_Instrument'):
            pass
        if settlement.Trade().SettleCategoryChlItem():
            if settlement.Trade().settleCategoryChlItem().Name() == 'DIS':
                pass
        if settlement.Acquirer() == settlement.SecurityInstrument().Issuer():
            if settlement.Acquirer().Name() in dis_acquirers:
                return True
                
        return False
        
    else:
        return False
        
            
def DIS_Coupon_Netting(settlement):

    if settlement.Type() == 'Coupon':
        return is_valid_DIS_settlement(settlement)
        
    return False
    
        
def DIS_Redemption_Netting(settlement):

    if settlement.Type() == 'Redemption':
        return is_valid_DIS_settlement(settlement)
    
    return False
