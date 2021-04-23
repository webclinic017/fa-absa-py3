import acm
from RFQUtils import Direction, QuoteRequest, MethodDirection
from RFQHistoryUtil import FromRequest
from DealPackageUtil import SalesTradingInfo

class QrQueryHandler(object):
    def __init__(self):
        self._observers = []
        self._queryResult = acm.FArray()
        self._queryResultDict = {}

    def AddObserverCallback(self, observerCb):
        if not observerCb in self._observers:
            self._observers.append(observerCb)

    def RemoveObserverCallback(self, observerCb):
        if observerCb in self._observers:
            self._observers.remove(observerCb)
    
    def _QueryResult(self):
        return self._queryResult

    def QueryResultDict(self):
        return self._queryResultDict

    def AddQuoteRequestToHistory(self, request):
        self._QueryResult().AtInsert(0, request.Clone())
        copyOfObservers = list(self._observers)
        self._HandleResult(copyOfObservers)
        
    def ExecuteQuery(self, request):
        if request and request.MarketPlace():
            query = acm.Trading().CreateQuoteRequestQuery(request.MarketPlace())
            query.CustomerRequestId(str(request.Id()))
            
            # As this is an asynch call, someone might remove observers before the result is done.
            copyOfObservers = list(self._observers)
            # Add id as first argument and a copy as of observers as second argument to _QueryResultCompleted
            def partial_wrapper(func, observers):
                def partial_func(task):
                    return func(observers, task)
                return partial_func
            
            query.Send().ContinueWith( partial_wrapper(self._QueryResultCompleted, copyOfObservers) )

    def _QueryResultCompleted(self, copyOfObservers, task):
        try:
            self._queryResult = task.ResultOrThrow()
        except Exception as e:
            print ('Query Result not completed', e)
        else:
            self._HandleResult(copyOfObservers)
    
    def _HandleResult(self, copyOfObservers):
        self._SplitAndSortQuoteRequests()
        self._NotifyObservers(copyOfObservers)

    def _NotifyObservers(self, copyOfObservers):
        for observer in copyOfObservers:
            try:
                observer(self.QueryResultDict())
            except Exception as e:
                print ("Notify Observer failed on %s"%str(observer), e) 

    def _SplitAndSortQuoteRequests(self):
        def _QuoteRequestSort(qr1, qr2):
            if qr1.DateTime() != qr2.DateTime():
                return -1 if qr2.DateTime() < qr1.DateTime() else 1
            else:
                return -1 if FromRequest.StatusAsText(qr2) > FromRequest.StatusAsText(qr1) else 1
                    
        quoteRequests = {}
        result = self._QueryResult()
        if result:
            # Split per quote request name
            for qr in result:
                name = QuoteRequest.GetQuoteRequestName(qr)
                if not name in quoteRequests:
                    quoteRequests[name] = []
                quoteRequests[name].append(qr)
            
            # Sort by time, latest first
            for qrKey in quoteRequests:
                quoteRequests[qrKey].sort(cmp = _QuoteRequestSort)

        self._queryResultDict = quoteRequests


class QrHistoryHandler(object):
    def __init__(self, addNewListItemsCb, quantityToNominalCb):
        self._addNewListItemsCb = addNewListItemsCb
        self._quantityToNominalCb = quantityToNominalCb
        self.__wrappedRequests = acm.FDictionary()
        self._queryNeeded = False
    
    def QueryNeeded(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._queryNeeded
        else:
            self._queryNeeded = val

    def OnQueryResult(self, queryResults):
        try:
            if queryResults:
                self.QueryNeeded(False)
                for qrKey in queryResults:
                    queryResult = queryResults[qrKey]
                    for i in range(len(queryResult)-1, -1, -1):
                        current = queryResult[i]
                        previous = queryResult[i+1] if len(queryResult) > i + 1 else None      
                        self.__Add(current, previous)
        except Exception as e:
            print ('__HandleQueryResult Failed', e)

    def __Add(self, request, previousRequest):
        name = QuoteRequest.GetQuoteRequestName(request)
        if not self.__wrappedRequests.At(name):
            self.__wrappedRequests.AtPut(name, acm.FArray())
        if self.__ItemShouldBeIncluded(request, previousRequest):
            self.__AddAsWrappedRequest(request)

    def __AddToHistoryList(self, wrappedRequest):
        self._addNewListItemsCb(wrappedRequest)    
        
    def __AddAsWrappedRequest(self, request):
        if not request.State():
            self.QueryNeeded(True) # If the request has no state, it means it is not yet updated on the IM. Not possible to add to history list. This will make it retry queries until State has been updated.
        else:
            name = QuoteRequest.GetQuoteRequestName(request)
            previousWrappedRequest = None if self.__wrappedRequests.At(name).IsEmpty() else self.__wrappedRequests.At(name).Last()
            wrappedRequest = FromRequest.WrapRequest(request, previousWrappedRequest, self._quantityToNominalCb)
            self.__wrappedRequests.At(name).Add(wrappedRequest)
            self.__AddToHistoryList(wrappedRequest)

    def __ItemsEqual(self, wrappedRequest, request, previousRequest):
        return FromRequest.ItemsEqual(wrappedRequest, request, previousRequest)
        
    def __ItemShouldBeIncluded(self, request, previousRequest):
        include = False
        if self.__IsNewItem(request, previousRequest):
            include = True
            if FromRequest.RequestIsSalesSide(request):
                include = FromRequest.ShouldSalesSideRequestBeIncluded(request, previousRequest)
            else:
                include = FromRequest.ShouldTradingSideRequestBeIncluded(request, previousRequest)
        return include

    def __IsNewItem(self, request, previousRequest):
        for name in self.__wrappedRequests:
            for wrappedRequest in self.__wrappedRequests.At(name):
                if self.__ItemsEqual(wrappedRequest, request, previousRequest):
                    return False 
        return True
