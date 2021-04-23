
  
"""
 FVerticalTrading ver 1.0.0 (compatible with PRIME 3.2.0)
 Implementation of vertical trading button action handler when adding or subtracting an order at a specific price
"""

import ael
import acm

global TradeStatusIn 
global ValidProfiles
global boolAuthorised

def checkUserProfile(aUser):
    '''print aUser.ActionAllowed(ael.enum_from_string('ActionType','BO Confirm'))'''
    if aUser.ActionAllowed(ael.enum_from_string('ActionType', 'BO Confirm')):
        '''print aUser.ActionAllowed(ael.enum_from_string('ActionType','BO Confirm'))'''
        return True
    return False


TradeStatusIn = 'FO Confirmed'

    

def ButtonCreate(invokationInfo):
    
    boolAuthorised = checkUserProfile(acm.User())
    if boolAuthorised:
        return True
    return False
    

def ButtonPush(invokationInfo):
    boolAuthorised = checkUserProfile(acm.User())
    if boolAuthorised:
        global TradeStatusIn
        sheet = invokationInfo.ExtensionObject().ActiveSheet()
        button = invokationInfo.Parameter("ClickedButton")
        if button:
            BusObject = button.BusinessObject()
            Trade = BusObject.Trade()
            if Trade.Status() ==  TradeStatusIn:
                func=acm.GetFunction('msgBox', 3)
                check = func("Warning", "Are you sure you want to BO Confirm this Trade? ", 1)
                if  check == 1:
                    tc = Trade.Clone()
                    tc.Status('BO Confirmed')
                    Trade.Apply(tc)
                    try:
                        Trade.Commit()
                    except:
                        print 'Unable to Update the trade'
     
    else:
        print 'Not Authorised'    
