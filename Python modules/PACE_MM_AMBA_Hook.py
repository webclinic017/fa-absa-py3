'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_AMBA_Hook
PROJECT                 :       PACE MM
PURPOSE                 :       AMBA Hook that will do additional filtering before the AMBA message gets placed
                                onto the AMB. It will also do message modification, i.e. remove unwanted cashflow
                                nodes to make the messages smaller.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

2012-11-22      603220          Heinrich Cronje                 PACE MM EOY Deployment - Added section
                                                                Notice Call Deposit Check

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Parameter settings inside the AMBA ini:
        ael_module_name = PACE_MM_AMBA_Hook             :       The name of the hook module.
        ael_sender_modify = PACE_AMBA_ini_Initialize    :       The name of the entry function for the Hook.
    
    When a message is picked up from the ADS via the AMBA, it hasses through this hook.
    The following filtering/checking gets performed in the hook:
    
        If message is a Trade message:
        
            Trade Status        :       The status of the trade should be valid according to the trade status parameters.
            Instrument Type     :       The instrument type should be valid according to the instrument type parameters.
            Counterparty Check  :       The counterparty should be a PACE client.
            Deposit Check       :       No Fixed Term Loans are allowed or Call Deposits with a quantity other than 1.
            
            If all three checks are passed, the message is placed onto the AMB.
        
        If message is an Instrument message:
        
            Check the following items on all trades on the specific instrument:
            
            Trade Status        :       The status of the trade should be valid according to the trade status parameters.
            Acquirer            :       The Acquirer of the trade should be valid according to the acquirer parameter.
            Counterparty Check  :       The counterparty should be a PACE client.
            Deposit Check       :       No Fixed Term Loans are allowed or Call Deposits with a quantity other than 1.
            
            If one trade on the specific instrument passes all the checks, the message is placed onto the AMB.
            
        Remove relevant cashflow nodes from the message:
            
            If instrument is a Call Account: Remove all cashflows that are not touched.
            If instrument is a Term Deposit: Remove all cashflows.
'''

import PACE_MM_Parameters as Parameters
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils

class Modify_PACE_MM_AMBA_Sender():
    
    def __init__(self, message):
        self.AMBA_MESSAGE = message
        
    def __remove_Relevant_CashFlows(self, leg_obj, prefix):
        for cashFlow_obj in AMBA_Utils.objects_by_name(leg_obj, prefix, 'CASHFLOW'):
            leg_obj.mbf_remove_object()
            
    def __validate_message(self):
        msgType = AMBA_Utils.get_object_type(self.AMBA_MESSAGE)
        if not msgType in ('TRADE', 'INSTRUMENT'):
            return False
            
        object = AMBA_Utils.object_by_name(self.AMBA_MESSAGE, ['+', '!'], msgType)
        if not object:
            return False
            
        if msgType == 'TRADE':
            '''--------------------------------------------------------------------------
                                            Trade Status Check
            --------------------------------------------------------------------------'''
            trade_status = AMBA_Utils.get_AMBA_Object_Value(object, 'STATUS')
            if not (trade_status in Parameters.VALID_TRADE_STATUS):
                return False
            
            '''--------------------------------------------------------------------------
                                            Instrument Type Check
            --------------------------------------------------------------------------'''
            insType = AMBA_Utils.get_AMBA_Object_Value(object, 'INSADDR.INSTYPE')
            if not (insType in Parameters.VALID_INSTRUMENT_TYPE):
                return False
            
            '''--------------------------------------------------------------------------
                                            PACE Counterparty Check
            --------------------------------------------------------------------------'''
            ptynbr = AMBA_Utils.get_AMBA_Object_Value(object, 'COUNTERPARTY_PTYNBR')
            if ptynbr and not (Utils.is_PACE_Party(ptynbr)):
                return False

            '''--------------------------------------------------------------------------
                                            Deposit (Not Loan) Check
            --------------------------------------------------------------------------'''
            trdnbr = AMBA_Utils.get_AMBA_Object_Value(object, 'TRDNBR')
            if trdnbr and Utils.is_Loan(trdnbr, 'string'):
                return False
            
            '''--------------------------------------------------------------------------
                                            Notice Call Deposit Check
            --------------------------------------------------------------------------'''
            for addInfoObj in AMBA_Utils.objects_by_name(object, ['+', '!', ''], 'ADDITIONALINFO'):
                addInfoSpec = AMBA_Utils.get_AMBA_Object_Value(addInfoObj, 'ADDINF_SPECNBR.FIELD_NAME')
                if addInfoSpec and addInfoSpec == 'Funding Instype':
                    addInfoValue = AMBA_Utils.get_AMBA_Object_Value(addInfoObj, 'VALUE')
                    if addInfoValue in Parameters.NOTICE_CALL_DEPOSIT:
                        return False
            
        elif msgType == 'INSTRUMENT':
            '''--------------------------------------------------------------------------
                        Trade Status, Accquirer and PACE Counterparty Check
            --------------------------------------------------------------------------'''
            insaddr = AMBA_Utils.get_AMBA_Object_Value(object, 'INSADDR')
            if insaddr:
                trades = Utils.get_Trades(insaddr)
                if not trades:
                    return False
            else:
                return False

            '''--------------------------------------------------------------------------
                        Remove non adjusted cashflows from a Call Account and all
                                    cashflow from Fixed Term Deposits.
            --------------------------------------------------------------------------'''
            for leg_obj in AMBA_Utils.objects_by_name(object, ['', '+', '!'], 'LEG'):
                leg_type = AMBA_Utils.get_AMBA_Object_Value(leg_obj, 'TYPE')
                if leg_type in Parameters.VALID_CALL_LEG_TYPE:
                    self.__remove_Relevant_CashFlows(leg_obj, [''])
                else:
                    self.__remove_Relevant_CashFlows(leg_obj, ['', '+', '!', '-'])
                
        return True

    def modify_PACE_MM_AMBA_Sender(self):
        if self.__validate_message():
            return self.AMBA_MESSAGE
        return None

def PACE_AMBA_ini_Initialize(m, s): 
    c = Modify_PACE_MM_AMBA_Sender(m)
    AMBA_Message = c.modify_PACE_MM_AMBA_Sender()
    if AMBA_Message:
        return (AMBA_Message, s)
    return None
