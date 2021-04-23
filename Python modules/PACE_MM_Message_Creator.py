'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Message_Creator
PROJECT                 :       PACE MM
PURPOSE                 :       This module will use the properties set from the PACE_MM_Processing module
                                and construct an AMBA message that will be sent to the AMB via the PACE_MM_ATS.
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
2012-10-22      549725          Heinrich Cronje                 Added PACE_MESSAGE_TYPE Instrument Amendment Rate Change
                                                                to cater for the scenarios where the leg and cashflow
                                                                changes are in one message.
2012-11-08      603220          Heinrich Cronje                 Added Cash Flow Start Day check for 0000-01-01.
2013-03-09      851429          Heinrich Cronje                 Set the underlying type from None to blank.
2014-10-14                      Matthias Riedel                 Replace Pace IDs by Barx IDs in the Non ZAR project
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    When this module is called, properties are already set that this module will use to construct an AMBA
    message.
    An addition to these pre set properties, logic is applied to determine further detail needed for the
    outgoing message.
    Once all the detail is determined the body is constructed by setting properties of the trade, 
    counterparty, instrument, leg and cashflow to dictionaries that are being used to construct the message.
    
    NOTE: When a ADS Message is processed all information from the AMBA message will be used before ADS
          called are made. This will minimise the changes for the Message data and the ADS data to be out
          of sync when AMBA or ATS is experiencing Backlogs.
'''

import amb, acm
import PACE_MM_Parameters as Params
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils

class PACE_MM_Message_Creator():

    def __init__(self, data_Struct):
        self.data_Struct = data_Struct

    def __get_TRDNBR(self):
        trdnbrs = acm.FSortedCollection()
        if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
            trdnbr = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'TRDNBR')
            trdnbrs.Add(acm.FTrade[trdnbr])
        elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
            insaddr = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'INSADDR')
            trdnbrs = Utils.get_Trades(insaddr)

        return trdnbrs
    
    def __get_Trade_Detail(self, trade):
        trade_Detail = {}
        trade_Detail['OID'] = ''
        trade_Detail['TIME'] = ''
        trade_Detail['OPTIONAL_KEY'] = ''
        trade_Detail['QUANTITY'] = ''
        
        if trade != None:
            if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
                trade_Detail['OID'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'TRDNBR')
                trade_Detail['TIME'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'TIME')
                trade_Detail['QUANTITY'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'QUANTITY')
                trade_Detail['OPTIONAL_KEY'] = self.data_Struct.OPTIONAL_KEY
            elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
                trade_Detail['OID'] = trade.Oid()
                trade_Detail['TIME'] = trade.TradeTime()
                trade_Detail['QUANTITY'] = trade.Quantity()
                optional_key = trade.OptionalKey()
                if Utils.is_Valid_Optional_Key(optional_key):
                    trade_Detail['OPTIONAL_KEY'] = optional_key
            
            if self.data_Struct.PACE_Message_Type == 'New Trade From Void':
                trade_Detail['OPTIONAL_KEY'] = ''
            
        return trade_Detail
    
    def __get_Party_Detail(self, trade):
        party_Detail = {}
        party_Detail['COUNTERPARTY_SDS'] = ''
        
        if trade != None:
            if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
                counterparty = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'COUNTERPARTY_PTYNBR.PTYID')
                if counterparty:
                    try:
                        party_Detail['COUNTERPARTY_SDS'] = acm.FParty[counterparty].add_info('BarCap_SMS_CP_SDSID')
                    except:
                        party_Detail['COUNTERPARTY_SDS'] = ''
            elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
                try:
                    party_Detail['COUNTERPARTY_SDS'] = trade.Counterparty().add_info('BarCap_SMS_CP_SDSID')
                except:
                    party_Detail['COUNTERPARTY_SDS'] = ''

        return party_Detail
    
    def __get_Instrument_Detail(self, trade):
        instrument_Detail = {}
        instrument_Detail['NAME'] = ''
        instrument_Detail['CURRENCY'] = ''
        instrument_Detail['CONTRACT_SIZE'] = ''
        instrument_Detail['EXPIRY_DATE'] = ''
        
        if trade != None:
            if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
                instr = trade.Instrument()
                instrument_Detail['NAME'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'INSADDR.INSID')
                instrument_Detail['CURRENCY'] = instr.Currency().Name()
                instrument_Detail['CONTRACT_SIZE'] = instr.ContractSize()
                instrument_Detail['EXPIRY_DATE'] = instr.ExpiryDate()
            elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
                instrument_Detail['NAME'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'INSID')
                instrument_Detail['CURRENCY'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'CURR.INSID')
                instrument_Detail['CONTRACT_SIZE'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'CONTR_SIZE')
                instrument_Detail['EXPIRY_DATE'] = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.AMB_TRD_INSTR_Obj, 'EXP_DAY')
                
        return instrument_Detail
    
    def __get_Leg_Detail(self, trade):
        leg_Detail = {}
        leg_Detail['START_DAY'] = ''
        leg_Detail['REINVEST'] = ''
        leg_Detail['RATE'] = ''
        
        if trade != None:
            if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
                leg_Detail['START_DAY'] = trade.Instrument().Legs()[0].StartDate()
                leg_Detail['REINVEST'] = trade.Instrument().Legs()[0].Reinvest()
                leg_Detail['RATE'] = trade.Instrument().Legs()[0].FixedRate()
            elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
                leg_obj = AMBA_Utils.object_by_name(self.data_Struct.AMB_TRD_INSTR_Obj, ['', '+', '!'], 'LEG')
                leg_Detail['START_DAY'] = AMBA_Utils.get_AMBA_Object_Value(leg_obj, 'START_DAY')
                leg_Detail['REINVEST'] = AMBA_Utils.get_AMBA_Object_Value(leg_obj, 'REINVEST')
                leg_Detail['RATE'] = AMBA_Utils.get_AMBA_Object_Value(leg_obj, 'FIXED_RATE')
            
        return leg_Detail
    
    def __get_CashFlow_Detail(self, trade, cashflow, event_type = ''):
        cashFlow_Detail = {}
        cashFlow_Detail['OID'] = ''
        cashFlow_Detail['PAY_DAY'] = ''
        cashFlow_Detail['FIXED_AMOUNT'] = ''
        cashFlow_Detail['NOMINAL_FACTOR'] = ''
        cashFlow_Detail['PACE_MM_EVENT_ID'] = ''

        if cashflow != None:
            try:
                cashflow_oid = cashflow.Oid()
            except:
                cashflow_oid = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'CFWNBR')
                
            if self.data_Struct.AMBA_Message_Type.__contains__('TRADE'):
                cashFlow_Detail['OID'] = cashflow_oid
                cashFlow_Detail['PAY_DAY'] = cashflow.PayDate()
                if cashflow.StartDate():
                    cashFlow_Detail['PAY_DAY'] = cashflow.StartDate()
                cashFlow_Detail['FIXED_AMOUNT'] = cashflow.FixedAmount()
                cashFlow_Detail['NOMINAL_FACTOR'] = cashflow.NominalFactor()
                cashFlow_Detail['PACE_MM_EVENT_ID'] = cashflow.ExternalId()
            elif self.data_Struct.AMBA_Message_Type.__contains__('INSTRUMENT'):
                try:
                    cashFlow_Detail['OID'] = cashflow_oid
                    cashFlow_Detail['PAY_DAY'] = cashflow.PayDate()
                    if cashflow.StartDate():
                        cashFlow_Detail['PAY_DAY'] = cashflow.StartDate()
                    cashFlow_Detail['FIXED_AMOUNT'] = cashflow.FixedAmount()
                    cashFlow_Detail['NOMINAL_FACTOR'] = cashflow.NominalFactor()
                    cashFlow_Detail['PACE_MM_EVENT_ID'] = cashflow.ExternalId()
                except:
                    cashFlow_Detail['OID'] = cashflow_oid
                    cashFlow_Detail['PAY_DAY'] = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'PAY_DAY')
                    if AMBA_Utils.get_AMBA_Object_Value(cashflow, 'START_DAY') != '0000-01-01':
                        cashFlow_Detail['PAY_DAY'] = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'START_DAY')
                    cashFlow_Detail['FIXED_AMOUNT'] = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'FIXED_AMOUNT')
                    cashFlow_Detail['NOMINAL_FACTOR'] = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'NOMINAL_FACTOR')
                    cashFlow_Detail['PACE_MM_EVENT_ID'] = AMBA_Utils.get_AMBA_Object_Value(cashflow, 'EXTERN_ID')
                    
            if event_type == 'ACKNOWLEDGE':
                externalId = Params.PACE_MM_EVENT_ID[str(cashflow_oid)]
                if externalId:
                    cashFlow_Detail['PACE_MM_EVENT_ID'] = externalId
                    Params.PACE_MM_EVENT_ID.RemoveKey(str(cashflow_oid))
            
        return cashFlow_Detail
    
    def __get_cashflows(self, trade):
        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', trade.Instrument().Oid())
        cashFlowType = cashFlowQuery.AddOpNode('OR')
        cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Amount'))
        cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Interest Reinvestment'))
        cashFlows = cashFlowQuery.Select()
        return cashFlows
    
    def __set_Exception_Msg_Keys(self, trade_Detail, instrument_Detail, cashFlow_Detail):
        mmg_msg_id                      = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'MMG_MSG_ID').strip()
        data                            = AMBA_Utils.object_by_name(self.data_Struct.message, [''], 'DATA')
        pace_mm_original_deal_id        = AMBA_Utils.get_AMBA_Object_Value(data, 'PACE_MM_ORIGINAL_DEAL_ID').strip()
        pace_mm_event_id                = AMBA_Utils.get_AMBA_Object_Value(data, 'PACE_MM_EVENT_ID').strip()
        fa_trade_id                     = AMBA_Utils.get_AMBA_Object_Value(data, 'FA_TRADE_ID').strip()
        fa_event_id                     = AMBA_Utils.get_AMBA_Object_Value(data, 'FA_EVENT_ID').strip()
        
        if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
            trade_Detail['OID'] = str(fa_trade_id)
        elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
            instrument_Detail['NAME'] = str(fa_trade_id)

        trade_Detail['OPTIONAL_KEY'] = 'BARXMM-%s-MMG-%s' %(str(pace_mm_original_deal_id), str(mmg_msg_id))
        cashFlow_Detail['PACE_MM_EVENT_ID'] = 'BARXMM-%s-MMG-%s' %(str(str(pace_mm_event_id)), str(mmg_msg_id))
        cashFlow_Detail['OID'] = str(fa_event_id)
        
        return (trade_Detail, instrument_Detail, cashFlow_Detail)
        
    def __construct_message(self, trade, event_type, cashflow = None, underlyingEvent = '', message_type = 'SYSTEM_GENERATED'):
        '''--------------------------------------------------------------------------
                                Setting Message Attributes
        --------------------------------------------------------------------------'''
        if event_type == 'NOT_ACKNOWLEDGE':
            trade_Detail = self.__get_Trade_Detail(None)
            party_Detail = self.__get_Party_Detail(None)
            instrument_Detail = self.__get_Instrument_Detail(None)
            leg_Detail = self.__get_Leg_Detail(None)
            cashFlow_Detail = self.__get_CashFlow_Detail(None, None)
            
            trade_Detail, instrument_Detail, cashFlow_Detail = self.__set_Exception_Msg_Keys(trade_Detail, instrument_Detail, cashFlow_Detail)
        else:
            trade_Detail = self.__get_Trade_Detail(trade)
            party_Detail = self.__get_Party_Detail(trade)
            instrument_Detail = self.__get_Instrument_Detail(trade)
            leg_Detail = self.__get_Leg_Detail(trade)
            cashFlow_Detail = self.__get_CashFlow_Detail(trade, cashflow, event_type)
        
        trade_section = [('TRADE', trade_Detail), ('PARTY', party_Detail)]
        instrument_section = [('INSTRUMENT', instrument_Detail), ('LEG', leg_Detail), ('CASHFLOW', cashFlow_Detail)]
        
        complete_section = [trade_section, instrument_section]

        '''--------------------------------------------------------------------------
                                Constructing the AMBA Message
        --------------------------------------------------------------------------'''
        message = amb.mbf_start_message(None, message_type, '1.0', None, Params.senderExternalSource)
        message.mbf_add_string('EVENT_TYPE', event_type)
        message.mbf_add_string('INSTRUMENT_TYPE', self.data_Struct.Instrument_Type)
        message.mbf_add_string('ERROR_NUMBER', str(self.data_Struct.ERROR_NUMBER))
        message.mbf_add_string('FREE_TEXT', self.data_Struct.Free_Text)
        message.mbf_add_string('UNDERLYING_EVENT', underlyingEvent)
        
        message.mbf_add_string('MESSAGE_CODE', Utils.get_Message_Event_Code(self.data_Struct.Instrument_Type, event_type, underlyingEvent))
        
        msgList = message.mbf_start_list('DATA')
        
        for section in complete_section:
            tag_list = [msgList]
            
            for tuple in section:
                mb_msg = tag_list[len(tag_list) - 1].mbf_start_list(tuple[0])
                for item in tuple[1]:
                    mb_msg.mbf_add_string(item, str(tuple[1][item]))
                tag_list.append(mb_msg)
            
            item = len(tag_list) - 1
            for i in range(item, 0):
                tag_list[i].mbf_end_list()
        
        msgList.mbf_end_list()
        message.mbf_end_message()
        
        return message
    
    def __get_CashFlow_Type(self, trade, cashflow_obj, original_type = 0):
        message_type = 'INVALID_CASH_FLOW'
        cf_type = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'TYPE')
        
        if original_type:
            cf_type = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, '!TYPE')
            
        if cf_type == 'Interest Reinvestment':
            message_type = 'INTEREST_REINVESTMENT'
        elif cf_type == 'Fixed Amount':
            projected = 0
            fixed_amount = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'FIXED_AMOUNT')
            nominal_factor = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'NOMINAL_FACTOR')
            quantity = trade.Quantity()
            contractSize = trade.Instrument().ContractSize()
            if fixed_amount and nominal_factor:
                projected = float(fixed_amount) * float(nominal_factor) * quantity * contractSize
                
            if projected < 0:
                message_type = 'WITHDRAWAL'
            else:
                message_type = 'DEPOSIT'
        
        return message_type

    
    def __get_CashFlow_Message_Type(self, trade, cashflow_obj):
        message_type = 'INVALID_CASH_FLOW'
        cf_object_Name = cashflow_obj.mbf_get_name()
        
        if not cf_object_Name:
            return message_type
            
        VALID_CF_TYPES = ['Fixed Amount', 'Interest Reinvestment']
        type = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'TYPE')
        
        '''--------------------------------------------------------------------------
                                Insert CashFlow Logic
        --------------------------------------------------------------------------'''
        if cf_object_Name.__contains__('+'):
            if type not in VALID_CF_TYPES:
                return message_type
                
            cf_nbr = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'CFWNBR')
            pace_mm_cf_id = None
            
            if cf_nbr:
                try:
                    pace_mm_cf_id = Params.PACE_MM_EVENT_ID[str(cf_nbr)]
                except:
                    pace_mm_cf_id = None
                
            if pace_mm_cf_id:
                message_type = 'ACKNOWLEDGE'
            else:
                message_type = self.__get_CashFlow_Type(trade, cashflow_obj)
                        
        elif cf_object_Name.__contains__('!'):
            '''--------------------------------------------------------------------------
                                    Update CashFlow Logic
            --------------------------------------------------------------------------'''
            original_Type = AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, '!TYPE')
            
            is_Valid_Original_Type = False
            is_Valid_Type = False
            if original_Type in VALID_CF_TYPES:
                is_Valid_Original_Type = True
            if type in VALID_CF_TYPES:
                is_Valid_Type = True

            if is_Valid_Original_Type and not is_Valid_Type:
                message_type = 'CANCEL'
                return message_type
            if original_Type and (not is_Valid_Original_Type) and is_Valid_Type:
                message_type = self.__get_CashFlow_Type(trade, cashflow_obj)
                return message_type
                
            '''--------------------------------------------------------------------------
                                    AMENDMENT Identification
            --------------------------------------------------------------------------'''
            AMENDMENT_LIST = ['FIXED_AMOUNT', 'NOMINAL_FACTOR', 'PAY_DAY']
            isAmendment = False
            for item in AMENDMENT_LIST:
                if AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, '!' + item):
                    '''--------------------------------------------------------------------------
                                Check if FIXED_AMOUNT differs less than 2 decimals
                    --------------------------------------------------------------------------'''
                    if item == 'FIXED_AMOUNT':
                        new_fixed_amount = round(float(AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, 'FIXED_AMOUNT')), 2)
                        original_fixed_amount = round(float(AMBA_Utils.get_AMBA_Object_Value(cashflow_obj, '!FIXED_AMOUNT')), 2)
                        if new_fixed_amount != original_fixed_amount:
                            isAmendment = True
                    else:
                        isAmendment = True
            
            if not isAmendment:
                '''--------------------------------------------------------------------------
                                    CashFlow type moves from Valid to Valid
                --------------------------------------------------------------------------'''
                if is_Valid_Original_Type and is_Valid_Type and original_Type != type:
                    isAmendment = True
                    
            if isAmendment:
                message_type = 'AMENDMENT'
        elif cf_object_Name.__contains__('-'):
            '''--------------------------------------------------------------------------
                                    Delete CashFlow Logic
            --------------------------------------------------------------------------'''
            if type in VALID_CF_TYPES:
                message_type = 'CANCEL'
                
        return message_type
    
    def __get_CashFlow_Message_Type_ACM(self, trade, acm_cf_object):
        message_type = 'INVALID_CASH_FLOW'
        if acm_cf_object.CashFlowType() == 'Interest Reinvestment':
            message_type = 'INTEREST_REINVESTMENT'
        elif acm_cf_object.CashFlowType() == 'Fixed Amount':
            projected = trade.Quantity() * trade.Instrument().ContractSize() * acm_cf_object.FixedAmount() * acm_cf_object.NominalFactor()
            if projected < 0:
                message_type = 'WITHDRAWAL'
            else:
                message_type = 'DEPOSIT'
        return message_type

    def create_PACE_MM_Message(self):
        paceMessageList = []
        trades = self.__get_TRDNBR()
        
        if self.data_Struct.PACE_Message_Type in ('New Trade', 'New Trade From Void'):
            '''--------------------------------------------------------------------------
                                            NEW TRADE
                    FIXED_TERM_DEPOSIT - Only New Trade
                    CALL_DEPOSIT - New Trade and all CashFlows releated to the trade
                    needs to be sent as DEPOSIT, WITHDRAWAL or INTEREST_REINVESTMENT
            --------------------------------------------------------------------------'''
            for t in trades:
                if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                    paceMessageList.append(self.__construct_message(t, 'NEW'))
                elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                    paceMessageList.append(self.__construct_message(t, 'NEW'))
                    cashFlows = self.__get_cashflows(t)
                    for c in cashFlows:
                        message_type = self.__get_CashFlow_Message_Type_ACM(t, c)
                        paceMessageList.append(self.__construct_message(t, message_type, c))
        elif self.data_Struct.PACE_Message_Type == 'New Trade Acknowledgement':
            '''--------------------------------------------------------------------------
                                        NEW TRADE ACKNOWLEDGEMENT
                    FIXED_TERM_DEPOSIT - Only ACKNOWLEDGE
                    CALL_DEPOSIT - ACKNOWLEDGE and all CashFlows releated to the trade
                    needs to be sent as DEPOSIT, WITHDRAWAL or INTEREST_REINVESTMENT
                    except when the initial cashflow that will have an External ID equal to
                    the Optional Key of the trade.
            --------------------------------------------------------------------------'''
            for t in trades:
                if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                    paceMessageList.append(self.__construct_message(t, 'ACKNOWLEDGE', None, 'NEW'))
                elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                    paceMessageList.append(self.__construct_message(t, 'ACKNOWLEDGE', None, 'NEW'))
                    cashFlows = self.__get_cashflows(t)
                    for c in cashFlows:
                        message_type = None
                        underlying_type = ''
                        if Utils.is_Initial_PACE_CF(c):
                            message_type = 'ACKNOWLEDGE'
                            underlying_type = self.__get_CashFlow_Message_Type_ACM(t, c)
                        if not message_type:
                            message_type = self.__get_CashFlow_Message_Type_ACM(t, c)
                        
                        paceMessageList.append(self.__construct_message(t, message_type, c, underlying_type))
        elif self.data_Struct.PACE_Message_Type == 'Cancellation':
            '''--------------------------------------------------------------------------
                                            CANCEL
                            FIXED_TERM_DEPOSIT - Only CANCEL
                                CALL_DEPOSIT - Only CANCEL
            --------------------------------------------------------------------------'''
            for t in trades:
                paceMessageList.append(self.__construct_message(t, 'CANCEL', None, 'NEW'))
        elif self.data_Struct.PACE_Message_Type == 'Cancellation - Acknowledgement':
            '''--------------------------------------------------------------------------
                                            CANCEL ACKNOWLEDGEMENT
                            FIXED_TERM_DEPOSIT - Only ACKNOWLEDGE
                                CALL_DEPOSIT - Only ACKNOWLEDGE
            --------------------------------------------------------------------------'''
            for t in trades:
                paceMessageList.append(self.__construct_message(t, 'ACKNOWLEDGE', None, 'CANCEL'))
        elif self.data_Struct.PACE_Message_Type == 'Trade Amendment':
            '''--------------------------------------------------------------------------
                                            AMENDMENT
                            FIXED_TERM_DEPOSIT - Only AMENDMENT
                            CALL_DEPOSIT - AMENDMENT for each valid CashFlow
            --------------------------------------------------------------------------'''
            for t in trades:
                if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                    paceMessageList.append(self.__construct_message(t, 'AMENDMENT', None, 'NEW'))
                elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                    cashFlows = self.__get_cashflows(t)
                    for c in cashFlows:
                        message_type = self.__get_CashFlow_Message_Type_ACM(t, c)
                        paceMessageList.append(self.__construct_message(t, 'AMENDMENT', c, message_type))
        elif self.data_Struct.PACE_Message_Type == 'Instrument Amendment':
            '''--------------------------------------------------------------------------
                                            AMENDMENT
                            FIXED_TERM_DEPOSIT - Only AMENDMENT
                                CALL_DEPOSIT - Only for Reinvest change
            --------------------------------------------------------------------------'''
            for t in trades:
                paceMessageList.append(self.__construct_message(t, 'AMENDMENT', None, 'NEW'))
        elif self.data_Struct.PACE_Message_Type == 'Instrument Amendment Rate Change':
            '''--------------------------------------------------------------------------
                                            AMENDMENT
                            FIXED_TERM_DEPOSIT - N/A
                        CALL_DEPOSIT - AMENDMENT for NEW Call Deposit and for 
                                Valid Cashflows when the rate changes
            --------------------------------------------------------------------------'''
            for t in trades:
                paceMessageList.append(self.__construct_message(t, 'AMENDMENT', None, 'NEW'))
                for c in self.data_Struct.cashFlowList:
                    message_type = self.__get_CashFlow_Message_Type(t, c)
                    if message_type != 'INVALID_CASH_FLOW':
                        cfType = ''
                        if message_type in ('ACKNOWLEDGE', 'CANCEL', 'AMENDMENT'):
                            cfType = self.__get_CashFlow_Type(t, c)
                            if cfType == 'INVALID_CASH_FLOW':
                                cfType = self.__get_CashFlow_Type(t, c, 1)
                        paceMessageList.append(self.__construct_message(t, message_type, c, cfType))
        elif self.data_Struct.PACE_Message_Type == 'Call Trading':
            '''--------------------------------------------------------------------------
                            DEPOSIT, WITHDRAWAL, INTEREST_REINVESTMENT
                                    FIXED_TERM_DEPOSIT - N/A
                                CALL_DEPOSIT - For Valid CashFlows only
            --------------------------------------------------------------------------'''
            for t in trades:
                for c in self.data_Struct.cashFlowList:
                    message_type = self.__get_CashFlow_Message_Type(t, c)
                    if message_type != 'INVALID_CASH_FLOW':
                        cfType = ''
                        if message_type in ('ACKNOWLEDGE', 'CANCEL', 'AMENDMENT'):
                            cfType = self.__get_CashFlow_Type(t, c)
                            if cfType == 'INVALID_CASH_FLOW':
                                cfType = self.__get_CashFlow_Type(t, c, 1)
                        paceMessageList.append(self.__construct_message(t, message_type, c, cfType))
        elif self.data_Struct.PACE_Message_Type == 'NOT_ACKNOWLEDGE':
            '''--------------------------------------------------------------------------
                                            NOT_ACKNOWLEDGE
                                FIXED_TERM_DEPOSIT - Based on underlying event
                                CALL_DEPOSIT - Based on underlying event
            --------------------------------------------------------------------------'''
            event_type = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'EVENT_TYPE').strip()
            if event_type == 'DEPOSIT/WITHDRAWAL':
                data = AMBA_Utils.object_by_name(self.data_Struct.message, [''], 'DATA')
                amount = AMBA_Utils.get_AMBA_Object_Value(data, 'AMOUNT').strip()
                event_type = 'DEPOSIT'
                if amount < 0:
                    event_type = 'WITHDRAWAL'
                    
            paceMessageList.append(self.__construct_message(None, self.data_Struct.PACE_Message_Type, None, event_type))

        return paceMessageList
