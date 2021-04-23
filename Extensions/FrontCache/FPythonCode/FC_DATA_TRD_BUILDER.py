
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_BUILDER
PROJECT                 :       Front Cache
PURPOSE                 :       Trade data builder for creating trade objects
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
from datetime import datetime
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_TRD import FC_DATA_TRD as fcDataTrade
from FC_DATA_TRD_STATIC import FC_DATA_TRD_STATIC as fcDataTradeStatic
from FC_DATA_TRD_SCALAR import FC_DATA_TRD_SCALAR as fcDataTradeScalar
from FC_DATA_TRD_INS import FC_DATA_TRD_INS as fcDataTradeInstrument
import FC_DATA_TRD_LEG
import FC_DATA_TRD_INS_UND
import FC_DATA_TRD_UND_KEYS
import FC_DATA_TRD_MF
import FC_DATA_TRD_SC

#*********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_TRD_BUILDER():

    #Fields
    _innerTrade = None
    
    #Constructor
    def __init__(self, tradeNumber):
        self._innerTrade = fcDataTrade(tradeNumber)
    
    #Methods
    #Create the trade static data
    def CreateStatic(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.Static = fcDataTradeStatic(self._innerTrade.FTrade)
            
        return self

    #Create the trade scalar data
    def CreateScalar(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.Scalar = fcDataTradeScalar(self._innerTrade.FTrade)
            
        return self
        
    #Create the trade instrument data
    def CreateInstrument(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.Instrument = fcDataTradeInstrument(self._innerTrade.FTrade)
            
        return self
        
    #Create the trade leg data
    def CreateLegs(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.Legs = FC_DATA_TRD_LEG.CreateAllForTrade(self._innerTrade.FTrade)
        return self
    
    #Create the trade underrlying instrument data
    def CreateUnderlyingInstruments(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.UnderlyingInstruments = FC_DATA_TRD_INS_UND.CreateAllForTrade(self._innerTrade.FTrade)
        return self

    #Create the trade underrlying instrument data
    def CreateUnderlyingKeys(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.UnderlyingKeys = FC_DATA_TRD_UND_KEYS.CreateAllForTrade(self._innerTrade.FTrade)
        return self
        
    #Create the trade moneyflow data 
    #Historical cashFlowRange (days):
    #   -1: Include all
    #   0-n: Include only historical cashflows updated within this range
    def CreateMoneyflows(self, reportDate, historicalCashflowRange):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.Moneyflows = FC_DATA_TRD_MF.CreateAllForTrade(reportDate, self._innerTrade.FTrade, historicalCashflowRange)
        return self
        
    #Create the trade sales credit data 
    def CreateSalesCredits(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            self._innerTrade.SalesCredits = FC_DATA_TRD_SC.CreateAllForTrade(self._innerTrade.FTrade)
        return self
        
    #Calls calculate on the inner trade container and return the container
    def CalculateAndBuild(self):
        if not self._innerTrade:
            raise Exception(UTILS.Constants.fcExceptionConstants.INNER_TRADE_DNE)
        else:
            startTime = datetime.now()
            self._innerTrade.Calculate()
            endTime = datetime.now()
            self._innerTrade.TradeBuildTime = FC_UTILS.getLapsedTimeInSeconds(startTime, endTime)
            return self._innerTrade
        
        
        
 
