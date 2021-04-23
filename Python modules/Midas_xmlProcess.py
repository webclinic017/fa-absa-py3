#--------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module creates an xml message to be sent to midas via MQ for Fx Swap.
#  Department and Desk : Fx Desk
#  Requester           : Justin Nichols
#  CR Number           : CR 431665, CR 587810
#--------------------------------------------------------------------------------------------------

import ael,acm,amb,os

from Midas_AddInfos        import setAdditionalInfo
from TMS_TradeWrapper_Base import *
from TMS_AMBA_Message      import _processElement
from MidasConnector        import xmlMessage

class TradeXMLWrapper(Wrapper):

    def __init__(self,trades,flag):
    
        Wrapper.__init__(self)
                
        if trades:
            for t in trades:
                self.insertLegInfo(t.trdnbr,flag)
                                                           
    def getTypeName(self):
    
        return "TRADE"
                   
    def insertLegInfo(self,trdnbr,flagEqOp):
    
        self._addChild(LegXMLWrapper(trdnbr,flagEqOp))
            
class LegXMLWrapper(Wrapper):

    def __init__(self,trdnbr,flagEqOp):
    
        Wrapper.__init__(self)
        
        trade = ael.Trade[trdnbr]
        t     = acm.FTrade[trdnbr]
        
        DEALCO   = t.TraderId()
        SPODAT   = t.spot_date()
        DRATE    = t.Price()
        CUSTNO   = t.Counterparty().Name()
        TDATE    = t.TradeTime()
        VALDTE   = t.ValueDay() 
        SPI1     = t.Name()
               
        Trade_Area = ''
        if t.OptKey1(): 
            Trade_Area = t.OptKey1().Name()
                    
        if self.isFarLeg(trade):
            PURPIPS = self.getFwdPoints(trade)
                   
        PAMT    = 0.0
        SAMT    = 0.0
        PURPIPS = 0.0
        PURSAL  = ''
        PCCY    = ''
        SCCY    = '' 
        
        #Purchase or Sell Indicator
        
        if flagEqOp == 1:  # BTB
            if t.QuantityIsDerived() == True:
                if t.Premium() > 0:
                    PURSAL = 'Sell'
                else:   
                    PURSAL = 'Buy'

            elif t.QuantityIsDerived() == False:
                if t.Premium() > 0:
                    PURSAL = 'Buy'  
                else:
                    PURSAL = 'Sell'
            
        if flagEqOp == 0:  # Client
            if t.QuantityIsDerived() == True:
                if t.Premium() > 0:
                    PURSAL = 'Buy'
                else:   
                    PURSAL = 'Sell'

            elif t.QuantityIsDerived() == False:
                if t.Premium() > 0:
                    PURSAL = 'Sell'  
                else:
                    PURSAL = 'Buy'
        
         # Client Trade
        if flagEqOp == 0:
            if t.Instrument().Name() == t.CurrencyPair().Currency1().Currency().Name():
                if t.Quantity() < 0:
                    PAMT     = t.Premium()
                    SAMT     = t.Quantity()
                    PCCY     = t.CurrencyPair().Currency2().Name()
                    SCCY     = t.CurrencyPair().Currency1().Name()                
                                    
                else:
                    SAMT     = t.Premium()
                    PAMT     = t.Quantity()
                    PCCY     = t.CurrencyPair().Currency1().Name()
                    SCCY     = t.CurrencyPair().Currency2().Name()
                                    
            else:
                if t.Quantity() < 0:
                    PAMT     = t.Premium()
                    SAMT     = t.Quantity()
                    PCCY     = t.CurrencyPair().Currency1().Name()
                    SCCY     = t.CurrencyPair().Currency2().Name()                
                
                else:
                    SAMT     = t.Premium()
                    PAMT     = t.Quantity()
                    PCCY     = t.CurrencyPair().Currency2().Name()
                    SCCY     = t.CurrencyPair().Currency1().Name()
                                    
        # BTB Trade  
        if  flagEqOp == 1: 
            if t.Instrument().Name() == t.CurrencyPair().Currency1().Currency().Name():
                if t.Quantity() > 0:
                    PAMT     = t.Premium() * -1
                    SAMT     = t.Quantity() * -1
                    PCCY     = t.CurrencyPair().Currency2().Name()
                    SCCY     = t.CurrencyPair().Currency1().Name()                
                                        
                else:
                    SAMT     = t.Premium() * -1
                    PAMT     = t.Quantity() * -1
                    PCCY     = t.CurrencyPair().Currency1().Name()
                    SCCY     = t.CurrencyPair().Currency2().Name()                
                
            else:
                if t.Quantity() > 0:
                    PAMT     = t.Premium() * -1
                    SAMT     = t.Quantity() * -1
                    PCCY     = t.CurrencyPair().Currency1().Name()
                    SCCY     = t.CurrencyPair().Currency2().Name()                
                                    
                else:
                    SAMT     = t.Premium() * -1
                    PAMT     = t.Quantity() * -1
                    PCCY     = t.CurrencyPair().Currency2().Name()
                    SCCY     = t.CurrencyPair().Currency1().Name() 
                    
        self._addProperty('DEALCO',DEALCO)
        self._addProperty('SPODAT',SPODAT)
        self._addProperty('DRATE',DRATE)
        self._addProperty('PAMT',PAMT)
        self._addProperty('PCCY',PCCY)     
        self._addProperty('SAMT',SAMT)     
        self._addProperty('SCCY',SCCY)
        self._addProperty('CUSTNO',self.getCounterParty(trade,flagEqOp))
        self._addProperty('TDATE',TDATE)
        self._addProperty('VALDTE',VALDTE)
        self._addProperty('PURSAL',PURSAL)
        self._addProperty('PURPIPS',"%.8f" % round(PURPIPS,8))
        self._addProperty('TRADE_AREA',Trade_Area)
        self._addProperty('Counterparty',CUSTNO)
        self._addProperty('Portfolio',self.getPortfolio(trade,flagEqOp))
        
        if flagEqOp == 1:
            self._addProperty('BTB_CUSSNO',trade.counterparty_ptynbr.ptynbr)
            self._addProperty('SPI1',str(SPI1)+ "_BTB")
        else:    
            self._addProperty('BTB_CUSSNO',0)
            self._addProperty('SPI1',SPI1)
            
    def getTypeName(self):
    
        return "LEG"
        
    def getFwdPoints(self,trade):
        
        other_trade = ael.Trade[trade.connected_trdnbr.trdnbr]
        fwd_points  = 0.0
        return(other_trade and (trade.price - other_trade.price) or fwd_points)
     
        
    def getCounterParty(self,trade,flEqOp):
        
        if flEqOp:
            return "Devon Fx"
        else:
            return trade.counterparty_ptynbr.ptynbr
            
    def getPortfolio(self,trade,flEqOp):
        
        if flEqOp:
            return "OPT"
        else:
            return  trade.prfnbr.prfid
            
    def isFarLeg(self,trade):
        return(trade and trade.trade_process == 32768)
        
def otherLeg(trade):
        
        for t in ael.Trade.select('connected_trdnbr=%s' % (trade.trdnbr)):
            if t.trdnbr != trade.trdnbr:
                return t
                
def getTradeXMLMessage(trades,flag):

    return TradeXMLWrapper(trades,flag)

def ProcessAMBMessage(tradeId):
    
    if tradeId:
        trade = ael.Trade[tradeId]
        
        # Fx Swap
        if trade.trade_process in (16384,32768):
            return ProcessFXSwap(tradeId)
        
        # Fx Spot and Outright Forward  
        elif trade.trade_process in (4096,8192):
            return ProcessFXSpotOutright(tradeId)
        
def getHeader():

    new_msg = amb.mbf_start_message(
                    None,
                    "INSERT_TRADE",
                    "1.0",
                    None,
                    "FRONT ARENA")
    return new_msg
   
def ProcessFXSpotOutright(tradeId):

    if tradeId:
        trades = []
        trade = ael.Trade[tradeId]
        trades.append(trade)
       
        for x in range(2):
                
            new_msg = getHeader()
            wrapper = getTradeXMLMessage(trades,x)
            _processElement(new_msg,wrapper)
            writeXMLFile(new_msg,trade.trdnbr,x)
         
def ProcessFXSwap(tradeId):
    
    if tradeId:
        trades = []
        trade  = ael.Trade[tradeId]
        
        other_trade = otherLeg(trade)
        
        if other_trade == None:
            trade       = ael.Trade[trade.connected_trdnbr.trdnbr]
            other_trade = otherLeg(trade)
            
        if other_trade:
            
            # Fx Swap
            if trade.trade_process in (16384,32768):
                near_trade = ael.Trade[trade.trdnbr]
                far_trade  = ael.Trade[other_trade.trdnbr]
                           
            # Fx Spot and Outright Forward     
            else:
                near_trade = ael.Trade[other_trade.trdnbr]
                far_trade  = ael.Trade[trade.trdnbr]
                
            trades.append(near_trade)
            trades.append(far_trade)
        
        for x in reversed(list(range(2))):
            new_msg = getHeader()
            wrapper = getTradeXMLMessage(trades,x)
            _processElement(new_msg,wrapper)
            writeXMLFile(new_msg,trade.trdnbr,x)

def writeXMLFile(msg,trdnbr,flag):

    xmlMsg  = msg.mbf_object_to_string_xml()
    
    try:
        sendMsg = xmlMessage(xmlMsg)
    except Exception,e:
        print e
    
    
        
    
    
