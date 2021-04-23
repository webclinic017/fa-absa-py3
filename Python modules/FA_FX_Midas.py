#--------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module creates an xml message to be sent to midas via MQ for Fx Swap.
#  Department and Desk : Fx Desk
#  Requester           : Justin Nichols
#  CR Number           : CR 431665
#--------------------------------------------------------------------------------------------------

import ael,acm,amb,os

from Midas_AddInfos        import setAdditionalInfo
from TMS_TradeWrapper_Base import *
from TMS_AMBA_Message      import _processElement

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

def ProcessAMBMessage(tradeId,Outpath):
    
    if tradeId:
        trade = ael.Trade[tradeId]
        
        # Fx Swap
        if trade.trade_process in (16384,32768):
            return ProcessFXSwap(tradeId,Outpath)
        
        # Fx Spot and Outright Forward  
        elif trade.trade_process in (4096,8192):
            return ProcessFXSpotOutright(tradeId,Outpath)
        
def getHeader():

    new_msg = amb.mbf_start_message(
                    None,
                    "INSERT_TRADE",
                    "1.0",
                    None,
                    "FRONT ARENA")
    return new_msg
   
def ProcessFXSpotOutright(tradeId,Outpath):

    if tradeId:
        trades = []
        trade = ael.Trade[tradeId]
        trades.append(trade)
       
        for x in range(2):
                
            new_msg = getHeader()
            wrapper = getTradeXMLMessage(trades,x)
            _processElement(new_msg,wrapper)
            writeXMLFile(new_msg,trade.trdnbr,x,Outpath)
         
def ProcessFXSwap(tradeId,Outpath):
    
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
            writeXMLFile(new_msg,trade.trdnbr,x,Outpath)

def writeXMLFile(msg,trdnbr,flag,Outpath):
    
    try:
        Type  = ''
        trade = ael.Trade[trdnbr] 
        if trade.trade_process in (16384,32768):
            Type = 'FxSwap'
        elif trade.trade_process in (4096,8192):
            Type = 'SPOT_FORWARD'
        
        if flag:
            file_name = os.path.join(Outpath,Type + "_BTB_" + str(trdnbr) + ".xml")
        else:
            file_name = os.path.join(Outpath,Type + "_Client_" + str(trdnbr)+ ".xml")
       
        outfile = open(file_name,'w')
        xmlMsg  = msg.mbf_object_to_string_xml()
            
        outfile.write(xmlMsg)
        outfile.close()
        
    except Exception, e:
        print e
    
    print 'Output Complete'
    print 'Wrote secondary output to::: ' + file_name
    
def TrdFilter():

    tradeFilters = []
    
    for tf in acm.FTradeSelection.Select(''):
        tradeFilters.append(tf.Name())  
    tradeFilters.sort()
    
    return tradeFilters

    
ael_variables = [('TrdFilter','Trade Filter','string',TrdFilter(),'FX_FA_to_Midbase',1),
                 ('Path', 'Output Directory','string', '', 'F:\FA_FX_Midas',1)]   

def ael_main(dict):

    try:
        Outpath = dict['Path']
        tf      =  ael.TradeFilter[dict['TrdFilter']].trades().members()
        
        for t in tf:
            
            if t.creat_usrnbr and t.creat_usrnbr.userid not in ('FORE_FRONT_PRD','FORE_FRONT_TST'):
            
                if ael.date_from_time(t.creat_time)== ael.date_today():
                    
                    if t.add_info('MIDAS_MSG') == 'Not Sent':
                        
                        # Spot and Outright
                        if t.trade_process in (4096,8192): 
                            
                            if acm.FTrade[t.trdnbr].CurrencyPair():
                            
                                ProcessAMBMessage(t.trdnbr,Outpath) 
                                setAdditionalInfo(t,'MIDAS_MSG','Sent')
                            else:
                                setAdditionalInfo(t,'MIDAS_MSG','Not Sent_Invalid Currency Pair')
                                
                        # Fx Swap
                        elif t.trade_process in (16384,32768):
                            
                            if acm.FTrade[t.trdnbr].CurrencyPair():
                                ProcessAMBMessage(t.trdnbr,Outpath) 
                                setAdditionalInfo(t,'MIDAS_MSG','Sent')
                            else:
                                setAdditionalInfo(t,'MIDAS_MSG','Not Sent_Invalid Currency Pair')  

    except Exception, e:
            print e
        
    
