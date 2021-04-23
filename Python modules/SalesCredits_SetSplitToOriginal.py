'''-----------------------------------------------------------------------
MODULE
    SalesCredits_SetSplitToOriginal

DESCRIPTION
        
    Date                : 2011-02-28
    Purpose             : Sets sales credits of connected trades created by splitting to zero
    Department and Desk : PCG
    Requester           : Thalia Petousis
    Developer           : Ickin Vural
    CR Number           : C000000591609

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import acm


def ASQL(*rest):
    acm.RunModuleWithParameters('SalesCredits_SetSplitToOriginal', 'Standard' )
    return 'SUCCESS'  

ael_variables = [['Trdnbr', 'Trade Number', 'int', None, '13698931', 1]]

def ael_main(parameter, *rest):

    Trdnbr = parameter['Trdnbr']
   
    list = []
    
    filteredTrades = acm.FTrade.Select("connectedTrdnbr = %i" %(Trdnbr))
       
    for trade in filteredTrades:
            if trade.Status() not in ('Void'):
                list.append(trade)
                
                
    try:
        list.pop()
    except:
        print('Empty List')
    
    
    for trade in list:
        
        # Set Sales Credits to Zero
        if trade.SalesCredit() != '':
        
            trade_clone = trade.Clone()
            trade_clone.SalesCredit(0.0)
            trade_clone.RegisterInStorage()
            trade.Apply(trade_clone)
            trade.Commit()
        
        if trade.IsClone():
            trade.RegisterInStorage()
    
        if trade.AdditionalInfo().Sales_Credit2() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().Sales_Credit2(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
        
        if trade.AdditionalInfo().Sales_Credit3() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().Sales_Credit3(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
            
        if trade.AdditionalInfo().Sales_Credit4() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().Sales_Credit4(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
            
        if trade.AdditionalInfo().Sales_Credit5() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().Sales_Credit5(0.0)
            trade.Apply(trade_clone)
            trade.Commit()



        # Set Value Add to Zero
        
        if trade.AdditionalInfo().ValueAddCredits() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().ValueAddCredits(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
        
        if trade.AdditionalInfo().ValueAddCredits2() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().ValueAddCredits2(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
        
        if trade.AdditionalInfo().ValueAddCredits3() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().ValueAddCredits3(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
            
        if trade.AdditionalInfo().ValueAddCredits4() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().ValueAddCredits4(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
            
        if trade.AdditionalInfo().ValueAddCredits5() != '':
        
            trade_clone = trade.Clone()
            trade_clone.AdditionalInfo().ValueAddCredits5(0.0)
            trade.Apply(trade_clone)
            trade.Commit()
