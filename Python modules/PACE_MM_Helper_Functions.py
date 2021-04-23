'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Helper_Functions
PROJECT                 :       PACE MM
PURPOSE                 :       This module contains functions that are being used throughout the entire solution.
DEPARTMENT AND DESK     :       Money Market and IT
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

2012-11-22      603220          Heinrich Cronje                 PACE MM EOD Deployment - Added section
                                                                set_payment_instructions for SSI implementation.
2013-03-09      851429          Heinrich Cronje                 Added the Notice Call Deposit section to the 
                                                                PACE_MM Client Check and Loan Check section
2014-10-14                      Matthias Riedel                 Replace PACE IDs by BARX IDs
2015-11-10      BARXMM-64       Kirsten Good                    Fix index out of bounds exception in 
                                                                set_payment_instructions when payment_instructions
                                                                length = 4
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Various helper functions that are used by various modules for the PACE MM implementation.
'''

import acm, ael
import PACE_MM_Parameters as Params
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils

class PACE_MM_Helper_Functions():
    
    enumDict = {}
    
    @classmethod
    def get_SDS_AddInfo(self, counterparty_SDS):
        counterpartySDSQuery = acm.CreateFASQLQuery(acm.FAdditionalInfo, 'AND')
        counterpartySDSQuery.AddAttrNode('FieldValue', 'EQUAL', counterparty_SDS)
        counterpartySDSQuery.AddAttrNode('AddInf.Oid', 'EQUAL', acm.FAdditionalInfoSpec['BarCap_SMS_CP_SDSID'].Oid())
        counterpartySDS = counterpartySDSQuery.Select()
        return counterpartySDS
        
    @classmethod
    def get_Counterparty(self, counterparty_SDS_AddInfos):
        validParty = []
        for addInfo in counterparty_SDS_AddInfos:
            party = acm.FParty[addInfo.Recaddr()]
            if (not party.NotTrading()) and party.add_info('FICA_Compliant') == 'Yes' and party.add_info('PACE_MM_Client') == 'Yes':
                validParty.append(party)
        return validParty
    
    @classmethod
    def set_Properties(self, entity, dict):
        for property, value in dict.items():
            if value not in (None, ''):
                entity.SetProperty(property, value)
        return entity
    
    @classmethod
    def get_ChoiceList_ACM(self, choiceList, value):
        for i in choiceList:
            if i.Name() == value:
                return i
        return None

    @classmethod
    def GetEnum(self, enumType, enumValue):
        enum = -1
        foundInCache = False
        enumDictKey = str(enumType) + '.' + str(enumValue)
        if (PACE_MM_Helper_Functions.enumDict.has_key(enumDictKey)):
            foundInCache = True
            enum = PACE_MM_Helper_Functions.enumDict[enumDictKey]    # Get it from the cache dict
        
        if not foundInCache:
            enums = [d for d in acm.FEnumeration.Select('') if d.AsString() == 'enum(%s)' %enumType][0]
            assert enums != None, 'The enum-type could not be found in ACM.'
            enum = enums.Enumeration(enumValue)
            PACE_MM_Helper_Functions.enumDict[enumDictKey] = enum    # Cache the enum value
        return enum

    @classmethod
    def is_Loan(self, trdnbr, type):
        if type == 'string':
            trade = acm.FTrade[trdnbr]
        elif type == 'object':
            trade = trdnbr
        
        if trade:
            if trade.Instrument().OpenEnd() == 'Open End':
                if trade.Quantity() == 1:
                    return False
            else:
                if trade.Nominal() < 0:
                    return False
        return True

    
    @classmethod
    def is_PACE_Party(self, partyOid):
        partyQuery = acm.CreateFASQLQuery(acm.FParty, 'AND')
        partyQuery.AddAttrNode('Oid', 'EQUAL', partyOid)
        partyQuery.AddAttrNode('NotTrading', 'EQUAL', 0)
        partyQuery.AddAttrNode('AdditionalInfo.FICA_Compliant', 'EQUAL', 1)
        partyQuery.AddAttrNode('AdditionalInfo.PACE_MM_Client', 'EQUAL', 1)
        partyQuery.AddAttrNode('AdditionalInfo.BarCap_SMS_CP_SDSID', 'NOT_EQUAL', '')
        
        party = partyQuery.Select()
        if party:
            party = party[0].Oid()
        return party

        
    @classmethod
    def get_Common_Trade_Selection(self, tradeQuery):
        '''-------------------------------------------------------------------
                            Valid Instrument Types
        -------------------------------------------------------------------'''
        instrumentType = tradeQuery.AddOpNode('OR')
        for instype in Params.VALID_INSTRUMENT_TYPE:
            instrumentType.AddAttrNode('Instrument.InsType', 'EQUAL', instype)

        '''-------------------------------------------------------------------
                                Valid Acquirers
        -------------------------------------------------------------------'''
        validAcquirers = tradeQuery.AddOpNode('OR')
        for acquirer in Params.VALID_ACQUIRER:
            validAcquirers.AddAttrNode('Acquirer.Name', 'EQUAL', acquirer)

        '''-------------------------------------------------------------------
                                In-Valid Trade Statuses
        -------------------------------------------------------------------'''
        for non_valid_status in Params.CANCELLATION_TRADE_STATUS:
            tradeQuery.AddAttrNode('Status', 'NOT_EQUAL', PACE_MM_Helper_Functions.GetEnum('TradeStatus', non_valid_status))

        '''-------------------------------------------------------------------
                                Valid Trade Statuses
        -------------------------------------------------------------------'''
        validTradeStatus = tradeQuery.AddOpNode('OR')
        for valid_status in Params.VALID_TRADE_STATUS:
            validTradeStatus.AddAttrNode('Status', 'EQUAL', PACE_MM_Helper_Functions.GetEnum('TradeStatus', valid_status))

        trades = tradeQuery.Select()
        
        '''-------------------------------------------------------------------
                PACE_MM Client Check, Loan Check and Notice Call Deposit
        -------------------------------------------------------------------'''
        tradeList = acm.FSortedCollection()
        for t in trades:
            if PACE_MM_Helper_Functions.is_PACE_Party(t.Counterparty().Oid()):
                if not PACE_MM_Helper_Functions.is_Loan(t, 'object'):
                    if t.add_info('Funding Instype') not in Params.NOTICE_CALL_DEPOSIT:
                        tradeList.Add(t)

        return tradeList

    @classmethod
    def get_Common_Trade_Selection_PACE(self, tradeQuery):
        '''-------------------------------------------------------------------
                            Existance in PACE MM Check
        -------------------------------------------------------------------'''
        tradeQuery.AddAttrNode('OptionalKey', 'RE_LIKE_NOCASE', '*BARXMM*')
        tradeQuery.AddAttrNode('OptionalKey', 'RE_LIKE_NOCASE', '*MMG*')
        
        return PACE_MM_Helper_Functions.get_Common_Trade_Selection(tradeQuery)
        
    @classmethod
    def get_Trades(self, insaddr, noPACE = False):
        tradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        tradeQuery.AddAttrNode('Instrument.Oid', 'EQUAL', insaddr)
        
        if noPACE:
            return PACE_MM_Helper_Functions.get_Common_Trade_Selection(tradeQuery)
        else:
            return PACE_MM_Helper_Functions.get_Common_Trade_Selection_PACE(tradeQuery)

    @classmethod
    def is_Valid_Optional_Key(self, optionalKey):
        if optionalKey:
            return optionalKey.__contains__('BARXMM') and optionalKey.__contains__('MMG')
        return False
    
    @classmethod
    def is_Valid_Status(self, status):
        return status in Params.VALID_TRADE_STATUS and status not in Params.CANCELLATION_TRADE_STATUS
    
    @classmethod
    def is_Valid_Cancel_Status(self, status):
        return status in Params.CANCELLATION_TRADE_STATUS
    
    @classmethod
    def get_CF_BARXMM_ID(self, cf):
        cf_BarxMM_ID = cf.ExternalId()
        return cf_BarxMM_ID
        
    @classmethod
    def is_Initial_PACE_CF(self, cf):
        if cf:
            cf_addInfo = PACE_MM_Helper_Functions.get_CF_BARXMM_ID(cf)
            if PACE_MM_Helper_Functions.is_Valid_Optional_Key(cf_addInfo):
                return True
        return False
    
    @classmethod
    def get_Valid_CF_From_Date(self, instrument, date):
        cfList = acm.FSortedCollection()
        cfQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cfQuery.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', instrument.Oid())
        cf_Type = cfQuery.AddOpNode('OR')
        cf_Type.AddAttrNode('CashFlowType', 'EQUAL', PACE_MM_Helper_Functions.GetEnum('CashFlowType', 'Fixed Amount'))
        cf_Type.AddAttrNode('CashFlowType', 'EQUAL', PACE_MM_Helper_Functions.GetEnum('CashFlowType', 'Interest Reinvestment'))
        cf = cfQuery.Select()
        for c in cf:
            if ael.date(c.PayDate()) >= date and abs(round(c.FixedAmount(), 2)) > 0.00:
                cfList.Add(c)
        return cfList
        
    @classmethod
    def get_first_FA_CF(self, instrument):
        cfQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cfQuery.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', instrument.Oid())
        cfQuery.AddAttrNode('CashFlowType', 'EQUAL', PACE_MM_Helper_Functions.GetEnum('CashFlowType', 'Fixed Amount'))
        cf = cfQuery.Select()
        return cf[0]
    
    @classmethod
    def get_Message_Event_Code(self, instrumentType, eventType, underlyingEvent):
        messageCodeString = instrumentType + '_' + eventType + '_' + underlyingEvent
        try:
            messageCode = Params.MESSAGE_EVENT_CODES[messageCodeString]
        except:
            messageCode = 'MMEVUNKNOWN'
        
        return messageCode

    @classmethod
    def set_payment_instructions(self, payment_instructions):
        if not payment_instructions:
            payment_instructions = 'Settle'
        else:
            paymentInstructionPiece = payment_instructions.split('-')
            if len(paymentInstructionPiece) == 2:
                if len(paymentInstructionPiece[0].strip()) == 4:
                    accountNumberPiece = paymentInstructionPiece[1].strip().split(' ')
                    if len(accountNumberPiece) >= 2:
                        payment_instructions = accountNumberPiece[0] + ' ' + accountNumberPiece[1]
        return payment_instructions
