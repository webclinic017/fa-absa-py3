import acm
import at_time
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

class ROLLBACK_PROCESS():
    def __init__(self, queryFolder, reportDate):
        self.__queryFolder = queryFolder
        self.__reportDate = reportDate
        self.__rolloutTrades = None
        self.__tradePackatesToVoid = []
        self.__getTrades()
        self.__setTradePacketsToBeVoided()
    
    def __getTrades(self):
        trades = self.__queryFolder.Query().Select()
        self.__getRolloutTrades(trades)
    
    def __getRolloutTrades(self, trades):
        validTrades = []
        for trade in trades:
            if trade.CreateTime() >= at_time.to_timestamp(self.__reportDate) and trade.Type() == 'Spot Roll' and trade.Status() != 'Void':
                validTrades.append(trade)
        self.__rolloutTrades = validTrades

    def getTradePackets(self):
        return self.__tradePackatesToVoid

    def __getTrueConnectedTrade(self, trade):
        trades = acm.FTrade.Select('connectedTrdnbr = %s and oid <> %s' %(trade.Oid(), trade.Oid()))
        return trades

    def __setTradePacketsToBeVoided(self):
        for trade in self.__rolloutTrades:
            if trade.ConnectedTrade() == trade:
                tradePacket = []
                tradePacket.append(trade)
                tradePacket.append(trade.TrueMirror())
                connectedTrades = self.__getTrueConnectedTrade(trade)
                for connectedTrade in connectedTrades:
                    tradePacket.append(connectedTrade)
                    tradePacket.append(connectedTrade.TrueMirror())
                self.__tradePackatesToVoid.append(tradePacket)
    
    def voidTradePackets(self):
        for tradePacket in self.__tradePackatesToVoid:
            self.__voidTradePacket(tradePacket)
    
    def __voidTradePacket(self, tradePacket):
        acm.BeginTransaction()
        for trade in tradePacket:
            if trade:
                trade.Status('Void')
                trade.Commit()
                Summary().ok(trade, Summary().UPDATE, trade.Oid())
        try:
            acm.CommitTransaction()
        except Exception as e:
            Logme()('Aborting Voiding the trade and its constellation: %s' %str(e), 'ERROR')
            acm.AbortTransaction()
    
#cl = ROLLBACK_PROCESS(acm.FPhysicalPortfolio['ACX'], '2017-10-26')
#print cl.getTradePackets()
#cl.voidTradePackets()
