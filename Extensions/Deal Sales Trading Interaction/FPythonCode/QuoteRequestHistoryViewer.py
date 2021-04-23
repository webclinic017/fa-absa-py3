import acm
from SalesTradingCustomizations import OrderBookCreation

def Market():
    return acm.FMarketPlace[OrderBookCreation.DefaultMarket(None)]

class QuoteRequestHistoryQueryHandler(object):
    def __init__(self, market, historyListCompletedCB):
        self._market = market
        self._historyItems = []
        self._historyListCompletedCB = historyListCompletedCB
        self._activeQuoteRequestQuery = acm.Trading().CreateQuoteRequestQuery(self.__Market())
        self._activeCustomerRequestQuery = acm.Trading().CreateQuoteRequestQuery(self.__Market())
        
    def __HistoryItems(self):
        return self._historyItems
        
    def __CustomerRequestId(self):
        customerRequestId = None
        if len(self._historyItems):
            customerRequestId = self._historyItems[0].CustomerRequest().Id()
        return customerRequestId

    def __Market(self):
        return self._market

    def __HandleQueryResult(self, queryResult):
        try:
            if queryResult:
                for i in range(queryResult.Size()):
                    current = queryResult.At(i)
                    self._historyItems.append(current)
        except Exception as e:
            print ('__HandleQueryResult Failed', e)

    def __CustomerRequestQueryResultCompleted(self, task):
        try:
            self.__HandleQueryResult(task.ResultOrThrow())
            if self._historyListCompletedCB:
                self._historyListCompletedCB(self._historyItems)
            return True
        except Exception as e:
            print ('Customer Request Query Result not completed', e)

    def _QuoteRequestQueryResultCompleted(self, task):
        try:
            self.__HandleQueryResult(task.ResultOrThrow())
            customerRequestId = self.__CustomerRequestId()
            if customerRequestId:
                self._historyItems = []
                self._activeCustomerRequestQuery.CustomerRequestId(customerRequestId)
                self._activeCustomerRequestQuery.Send().ContinueWith(self.__CustomerRequestQueryResultCompleted)
            elif self._historyListCompletedCB:
                self._historyListCompletedCB(self._historyItems)
            return True
        except Exception as e:
            print ('Quote Request Query Result not completed', e)

    def QueryForRequest(self, requestId):
        if requestId and self.__Market():
            self._activeQuoteRequestQuery.QuoteRequestId(requestId)
            self._activeQuoteRequestQuery.Send().ContinueWith(self._QuoteRequestQueryResultCompleted)


class QuoteRequestHistoryViewer(object):
    def __init__(self, shell, market):
        self._shell = shell
        self._market = market
        
    def Shell(self):
        return self._shell
        
    def Market(self):
        return self._market
        
    def __HistoryListCompletedCB(self, quoteRequestHistoryList):
        acm.DealCapturing().UX().QuoteRequestViewerDialog(self.Shell(), quoteRequestHistoryList)
        
    def Show(self, quoteRequestId):
        historyQueryHandler = QuoteRequestHistoryQueryHandler(self.Market(), self.__HistoryListCompletedCB)
        historyQueryHandler.QueryForRequest(quoteRequestId)


def OpenQuoteRequestHistoryViewer(quoteRequestId, shell):
    if not quoteRequestId:
        raise Exception('Quote Request Id missing')
    QuoteRequestHistoryViewer(shell, Market()).Show(quoteRequestId)
    
def OpenQuoteRequestHistoryViewerFromTrade(trade, shell):
    quoteRequestId = GetQuoteRequestId(trade)
    OpenQuoteRequestHistoryViewer(quoteRequestId, shell)
    
def GetQuoteRequestId(trade):
    addInfos = trade.AdditionalInfo()
    return hasattr(addInfos, "QuoteRequestId") and addInfos.QuoteRequestId()   
