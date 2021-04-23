
"""
Date                    : 2010-07-06
Purpose                 : Button to move trade from FO Confirmed to BO-BO Confirmed for Trade sheet in Trading Managerm, based on FChangeTradeStatusCode
Department and Desk     : OPS DERIVATIVES
Requester               : Sipho Ndlalane
Developer               : Rohan van der Walt
CR Number               : 363373
"""

import ael
import acm

global TradeStatusIn 
global ValidProfiles
global boolAuthorised

def checkUserProfile(aUser):
    if aUser.ActionAllowed(ael.enum_from_string('ActionType', 'BO Confirm')):
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
                check = func("Warning", "Are you sure you want to BO-BO Confirm this Trade? ", 1)
                if  check == 1:
                    tc = Trade.Clone()
                    tc.Status('BO-BO Confirmed')
                    Trade.Apply(tc)
                    try:
                        Trade.Commit()
                    except:
                        print 'Unable to Update the trade'
    else:
        print 'Not Authorised'    
