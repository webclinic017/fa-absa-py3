'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SELECTION_AEL_ASQL
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the implementation of a data selection method using the asql
                                function on the ael module to select data.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import ael

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS

'''----------------------------------------------------------------------------------------------------------
Class containing methods to do the data selection.
----------------------------------------------------------------------------------------------------------'''
class FC_DATA_SELECTION_AEL_ASQL():
    def __init__(self, selectionType, scopeNumber, scopeName, isEOD, tradeCreateCutOffDate):
        self._selectionType = selectionType
        self._scopeNumber = scopeNumber
        self._scopeName = scopeName
        self._isEOD = isEOD
        if self._isEOD == True:
            self._exclusionTrades = UTILS.Parameters.fcGenericParameters.invalidEODTradeStatuses
            self._tradeCreateCutOffDateTime = '%s %s' %(FC_UTILS.dateStringFromISODateTimeString(tradeCreateCutOffDate), UTILS.Parameters.fcGenericParameters.TradeEODCreateCutOffTime)
        else:
            self._exclusionTrades = UTILS.Parameters.fcGenericParameters.invalidTradeStatuses
            self._tradeCreateCutOffDateTime = '%s %s' %(FC_UTILS.dateStringFromISODateTimeString(tradeCreateCutOffDate), UTILS.Parameters.fcGenericParameters.TradeCreateCutOffTime)
    
    def getAelASQLDataSelection(self):
        if not self._selectionType:
            return []
        elif (not self._scopeNumber) and (not self._scopeName):
            return []
        elif self._selectionType == UTILS.Constants.fcGenericConstants.SINGLE_SETTLEMENT:
            return self.__selectAelSingleSettlement()            
        elif self._selectionType == UTILS.Constants.fcGenericConstants.SINGLE_TRADE:
            return self.__selectAelSingleTrade()
        elif self._selectionType == UTILS.Constants.fcGenericConstants.INSTRUMENT_TRADES:
            return self.__selectAelInstrumentTrades()
        elif self._selectionType == UTILS.Constants.fcGenericConstants.PORTFOLIO_TRADES:
            return self.__selectAelPortfolioTrades()
        elif self._selectionType == UTILS.Constants.fcGenericConstants.INSTRUMENT_SENSITIVITIES:
            return self.__selectAelPortfolioInstruments()
        elif self._selectionType == UTILS.Constants.fcGenericConstants.PORTFOLIO_SENSITIVITIES:
            return self.__selectAelSinglePortfolio()
        else:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.THE_SELECTION_TYPE_IS_NOT_IMPLEMENTED %(self._selectionType, __name__))
            return []
    
    def __selectAelSingleTrade(self):
        if self._scopeNumber and self._scopeName:
            try:
                return self.__selectAelSingleTradeFromId()
            except:
                return self.__selectAelSingleTradeFromName()
        elif self._scopeNumber:
            return self.__selectAelSingleTradeFromId()
        elif self._scopeName:
            return self.__selectAelSingleTradeFromName()
        else:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_SCOPE_NAME_NUMBER_SUPPLIER %(aels._selectionType, __name__))
            return []
    
    def __selectAelInstrumentTrades(self):
        if self._scopeNumber and self._scopeName:
            try:
                return self.__selectAelInstrumentTradesFromId()
            except:
                return self.__selectAelInstrumentTradesFromName()
        elif self._scopeNumber:
            return self.__selectAelInstrumentTradesFromId()
        elif self._scopeName:
            return self.__selectAelInstrumentTradesFromName()
        else:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_SCOPE_NAME_NUMBER_SUPPLIER %(aels._selectionType, __name__))
            return []

    def __selectAelPortfolioTrades(self):
        if self._scopeNumber and self._scopeName:
            try:
                return self.__selectAelPortfolioTradesFromId()
            except:
                return self.__selectAelPortfolioTradesFromName()
        elif self._scopeNumber:
            return self.__selectAelPortfolioTradesFromId()
        elif self._scopeName:
            return self.__selectAelPortfolioTradesFromName()
        else:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_SCOPE_NAME_NUMBER_SUPPLIER %(aels._selectionType, __name__))
            return []

    def __selectAelSinglePortfolio(self):
        dataSelection = ael.asql(r'''SELECT p.prfnbr
                                     FROM   Portfolio p
                                     WHERE p.prfnbr = '%s'
                                     ''' %(self._scopeNumber))
        dataSelection.sort()
        return dataSelection[0][0]

    def __selectAelPortfolioInstruments(self):
        dataSelection = ael.asql(r'''SELECT i.insaddr,i.insid
                                     FROM   Instrument i, trade t
                                     WHERE  i.insaddr = t.insaddr and t.prfnbr = %s
                                     group by 1
                                     ''' %(self._scopeNumber))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelSingleTradeFromId(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                        from
                                        Trade t
                                        WHERE t.trdnbr = %s and t.status not in %s and t.creat_time <= '%s'
                            ''' %(self._scopeNumber, self._exclusionTrades, self._tradeCreateCutOffDateTime))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelSingleTradeFromName(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                        from
                                        Trade t
                                        WHERE t.trdnbr = '%s' and t.status not in %s and t.creat_time <= '%s'
                            ''' %(self._scopeName, self._exclusionTrades, self._tradeCreateCutOffDateTime))
        dataSelection.sort()
        return dataSelection[0][0]

    def __selectAelInstrumentTradesFromId(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                        from
                                        Trade t
                                        WHERE t.insaddr = %s and t.status not in %s and t.creat_time <= '%s'
                            ''' %(self._scopeNumber, self._exclusionTrades, self._tradeCreateCutOffDateTime))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelInstrumentTradesFromName(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                        from
                                        Trade t,
                                        Instrument i
                                        WHERE t.insaddr = i.insaddr and i.insid = '%s' and t.status not in %s and t.creat_time <= '%s'
                            ''' %(self._scopeName, self._exclusionTrades, self._tradeCreateCutOffDateTime))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelPortfolioTradesFromId(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                        from
                                        Trade t
                                        WHERE t.prfnbr = %s  and t.trdnbr NOT IN (87083353,87083354) and t.status not in %s and t.creat_time <= '%s'
                            ''' %(self._scopeNumber, self._exclusionTrades, self._tradeCreateCutOffDateTime))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelPortfolioTradesFromName(self):
        dataSelection = ael.asql(r'''SELECT t.trdnbr
                                     from 
                                     Trade t,
                                     Portfolio p 
                                     WHERE t.prfnbr = p.prfnbr and t.trdnbr NOT IN (87083353,87083354) and p.prfid = '%s' and t.status not in %s and t.creat_time <= '%s'
                             ''' %(self._scopeName, self._exclusionTrades, self._tradeCreateCutOffDateTime))
                             
        dataSelection.sort()
        return dataSelection[0][0]
        
    def __selectAelSingleSettlement(self):
        if self._scopeNumber and self._scopeName:
            try:
                return self.__selectAelSingleSettlementFromId()
            except:
                return self.__selectAelSingleSettlementFromName()
        elif self._scopeNumber:
            return self.__selectAelSingleSettlementFromId()
        elif self._scopeName:
            return self.__selectAelSingleSettlementFromName()
        else:
            UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.NO_SCOPE_NAME_NUMBER_SUPPLIER %(aels._selectionType, __name__))
            return []        

    def __selectAelSingleSettlementFromId(self):
        dataSelection = ael.asql(r'''SELECT s.seqnbr
                                        from
                                        Settlement s
                                        WHERE s.seqnbr = %s
                            ''' %(self._scopeNumber))
        dataSelection.sort()
        return dataSelection[0][0]
    
    def __selectAelSingleSettlementFromName(self):
        dataSelection = ael.asql(r'''SELECT s.seqnbr
                                        from
                                        Settlement s
                                        WHERE s.seqnbr = '%s'
                            ''' %(self._scopeName))
        dataSelection.sort()
        return dataSelection[0][0]
