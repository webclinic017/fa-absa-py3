'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_TAL_Override
PURPOSE                 :       This AEL contains the class that would do the Trade Account Link override.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       Linton Behari-Ram
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       603220
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-09-14      603220          Heinrich Cronje                 Initial Implementation
2014-10-14                      Matthias Riedel                 Adjust for Non ZAR
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF AEL:

    This AEL contains the class that would do the Trade Account Link override.
    The account number will come in from PACE MM and tthis class will try and override the Trade Account Link.
----------------------------------------------------------------------------------------------------------'''


import acm
import PACE_MM_Parameters as Params

class PACE_MM_TAL_Override():
    def __init__(self, trade, overrideAccount):
        self.__trade = trade
        self.__overrideAccount = overrideAccount
        self.__testSSI = None
        self.__overrideSSI = None
        self.tradeAccountLinkOverride()
    
    def __isHighLevelSSI(self):
        if self.__testSSI.Currency() and self.__testSSI.Currency().Name() in Params.VALID_CURRENCIES  \
            and self.__testSSI.FromParty() and self.__testSSI.FromParty().Name()== Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[self.__testSSI.Currency().Name()][2]\
            and self.__testSSI.InstrumentType() == 'None' and self.__testSSI.UndInsType() == 'None' \
            and self.__testSSI.CashSettleCashFlowType() == 'None' and not self.__testSSI.SettleCategoryChlItem() \
            and self.__testSSI.OtcInstr() == 'OTC':
                return True
        return False
        
    def __isLowLevelSSI(self):
        if self.__testSSI.Currency() and self.__testSSI.Currency().Name() in Params.VALID_CURRENCIES  \
            and self.__testSSI.FromParty() and self.__testSSI.FromParty().Name() == Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[self.__testSSI.Currency().Name()][2] \
            and self.__testSSI.InstrumentType() == 'Deposit' and self.__testSSI.UndInsType() == 'None' \
            and self.__testSSI.CashSettleCashFlowType() == 'Fixed Amount' and not self.__testSSI.SettleCategoryChlItem() \
            and self.__testSSI.OtcInstr() == 'OTC':
                return True
        return False
    
    def __hasValidSSIRule(self):
        for ssiRule in self.__testSSI.Rules():
            if not ssiRule.EffectiveTo() and ssiRule.EffectiveFrom() == '1970-01-01':
                if ssiRule.CashAccount():
                    return ssiRule.CashAccount().Account()
        return None
        
    def __getValidSSI(self, party):
        highLevelSSIDict = acm.FDictionary()
        lowLevelSSIDict = acm.FDictionary()
         
        for ssi in party.SettleInstructions():
            self.__testSSI = ssi
            if self.__isHighLevelSSI():
                validAccount = self.__hasValidSSIRule()
                if validAccount:
                    highLevelSSIDict[validAccount] = self.__testSSI
            elif self.__isLowLevelSSI():
                validAccount = self.__hasValidSSIRule()
                if validAccount:
                    lowLevelSSIDict[validAccount] = self.__testSSI

        return highLevelSSIDict, lowLevelSSIDict
        
    def __clearTradeAccountLinks(self):
        if self.__trade.AccountLinks():
            for tal in self.__trade.AccountLinks():
                self.__testSSI = tal.SettleInstruction()
                if self.__isHighLevelSSI() or self.__isLowLevelSSI():
                    tal.Delete()

    def __addTradeAccountLink(self):
        newTAL = acm.FTradeAccountLink()
        newTAL.PartyType(1)
        newTAL.SettleInstruction(self.__overrideSSI)
        newTAL.Trade(self.__trade)
        newTAL.Commit()
    
    def tradeAccountLinkOverride(self):
        validHighLevelSSI, validLowLevelSSI = self.__getValidSSI(self.__trade.Counterparty())
        if self.__overrideAccount in validLowLevelSSI.Keys() or self.__overrideAccount in validHighLevelSSI.Keys():
            if self.__overrideAccount in validLowLevelSSI.Keys():
                self.__overrideSSI = validLowLevelSSI[self.__overrideAccount]
            else:
                self.__overrideSSI = validHighLevelSSI[self.__overrideAccount]
            if self.__overrideSSI:
                self.__clearTradeAccountLinks()
                self.__addTradeAccountLink()
