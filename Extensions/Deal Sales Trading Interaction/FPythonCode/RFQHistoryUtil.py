import acm
from RFQUtils import Direction, Status, Time
from DealPackageUtil import SalesTradingInteraction

TRADING = 'Trading'

class FromRequest(object):
    @staticmethod
    def WrapRequest(request, previousWrappedRequest, quantityToNominalCb):
        entry = acm.FAccount()
        previousStatus = previousWrappedRequest.Account2() if previousWrappedRequest else None
        entry.Account = FromRequest.Initiator(request, previousStatus)
        entry.Account2 = FromRequest.StatusAsText(request)
        entry.Account3 = FromRequest.Price(request)
        entry.Account5 = FromRequest.TextMessage(request)
        entry.Depository = FromRequest.Direction(request)
        entry.Depository2 = FromRequest.Time(request)
        entry.Depository3 = FromRequest.OrderBookName(request)
        return entry

    @staticmethod
    def RequestIsSalesSide(request):
        return request.Role() == 'Sales'

    @staticmethod
    def ShouldSalesSideRequestBeIncluded(request, previousRequest):
        include = False
        currentStatus = FromRequest.StatusName(request)
        previousStatus = FromRequest.StatusName(previousRequest) if previousRequest else ''
        if currentStatus in [Status.firm, Status.countered, Status.accepting, Status.stream, Status.cancelled]:
            include = True
        elif currentStatus in [Status.subject] and previousStatus in [Status.pending, Status.subjAccept]:
            include = True
        return include
    
    @staticmethod
    def ShouldTradingSideRequestBeIncluded(request, previousRequest):
        include = True
        currentStatus = FromRequest.StatusAsText(request)
        previousStatus = FromRequest.StatusName(previousRequest) if previousRequest else ''
        if previousRequest:
            if currentStatus == previousStatus and \
               request.ToBrokerId() != previousRequest.ToBrokerId():
                include = False
        return include
            
    @staticmethod
    def ItemsEqual(wrappedRequest, request, previousRequest):
        return request == previousRequest or (wrappedRequest.Depository2() == FromRequest.Time(request) and wrappedRequest.Account2() == FromRequest.StatusAsText(request) and wrappedRequest.Account() == FromRequest.Initiator(request, FromRequest.StatusAsText(previousRequest) if previousRequest else None))

    @staticmethod
    def Initiator(request, previousStatus):
        def TradingSideInitiator(request, previousStatus):
            status = FromRequest.StatusName(request)
            
            auto = [Status.noAnswer, Status.expired, Status.accepted]
            traderUpdates = [Status.rejected, Status.firm, Status.subject, Status.stream]
            salesUpdates = [Status.pending, Status.cancelled, Status.passed, Status.subjAccept, Status.countered]

            initiator = ''
            if status == Status.accepting:
                initiator = 'Sales' if previousStatus in [Status.firm, Status.stream, Status.proposed, Status.accepted] else 'Trader'
            elif status in auto:
                initiator = 'Auto'
            elif status in traderUpdates:
                initiator = 'Trader'
            elif status in salesUpdates:
                initiator = 'Sales'
            else:
                print(('Status update, status: ' + str(status) + ' unhandled'))
            return initiator

        def SalesSideInitiator(request):
            status = FromRequest.StatusName(request)
            initiator = 'Sales'
            if status == Status.accepting:
                initiator = 'Client'
            return initiator

        if FromRequest.RequestIsSalesSide(request):
            return SalesSideInitiator(request)
        else:
            return TradingSideInitiator(request, previousStatus)

    @staticmethod
    def TextMessage(request):
        def TradingSideTextMessage(request):
            status = FromRequest.StatusName(request)
            text = ''
            if status == Status.pending:
                text = request.Message()
            elif status in [Status.firm, Status.stream]:
                text = request.Answer().Message()
            return text

        def SalesSideTextMessage(request):
            text = ''
            if not FromRequest.StatusName(request) == Status.accepting and not FromRequest.StatusName(request) == Status.cancelled:
                text = 'Proposed to Client' if FromRequest.StatusName(request) in [Status.firm, Status.subject, Status.stream] else 'Counter proposal'
            return text

        if FromRequest.RequestIsSalesSide(request):
            return SalesSideTextMessage(request)
        else:
            return TradingSideTextMessage(request)


    @staticmethod
    def StatusName(request):
        s = ''
        if request.State():
            s = str(request.State().GetDisplayName('FQuotePrice'))
        return s
    
    @staticmethod
    def OrderBookName(request):
        return request.TradingInterface().StringKey() if FromRequest.StatusAsText(request) != 'Proposed' and request.TradingInterface() else ''

    @staticmethod
    def StatusAsText(request):
        status = FromRequest.StatusName(request)
        if FromRequest.RequestIsSalesSide(request):
            status = Status.proposed if status in [Status.firm, Status.countered, Status.subject, Status.stream] else status
        return status

    @staticmethod
    def UseAnswerToAccessPriceAndNominal(request, status):
        answer = None
        if status not in [Status.countered]:
            answer = request.Answer()
        return answer

    @staticmethod
    def Price(request):
        def FormatPrice(price):
            priceFormatter = acm.FNumFormatter('VeryDetailedShowZeroHideNaN')
            return priceFormatter.Format(price) if acm.Math.IsFinite(price) else ''

        status = FromRequest.StatusName(request)
        answer = FromRequest.UseAnswerToAccessPriceAndNominal(request, status)

        shouldShowPrice = status not in [Status.pending, Status.cancelled, Status.rejected, Status.accepted]
        priceDict = FromRequest.PriceDict(request)
        prices = {Direction.ask : FormatPrice(priceDict[Direction.ask]), Direction.bid : FormatPrice(priceDict[Direction.bid])}
        if request.BidOrAsk() == Direction.twoWay:
            priceString = prices[Direction.bid] + '/' + prices[Direction.ask] if answer and shouldShowPrice else ''
        else:
            priceString = prices[request.BidOrAsk()] if shouldShowPrice else ''
        return priceString

    @staticmethod
    def PriceDict(request):
        status = FromRequest.StatusName(request)
        answer = FromRequest.UseAnswerToAccessPriceAndNominal(request, status)
        
        if answer:
            askPrice = answer.AskPrice()
            bidPrice = answer.BidPrice()
        else:
            askPrice = request.Price()
            bidPrice = request.Price()
        
        priceDict = {Direction.ask : askPrice, Direction.bid : bidPrice}
        
        return priceDict
    
    @staticmethod
    def QuantityDict(request):
        status = FromRequest.StatusName(request)
        answer = FromRequest.UseAnswerToAccessPriceAndNominal(request, status)
        
        if answer:
            askQuantity = answer.AskQuantity()
            bidQuantity = answer.BidQuantity()
        else:
            askQuantity = request.Quantity()
            bidQuantity = request.Quantity()
        
        quantityDict = {Direction.ask : askQuantity, Direction.bid : bidQuantity}
        
        return quantityDict

    @staticmethod
    def Nominal(request, quantityToNominalCb):
        def FormatNominal(nominal):
            nominalFormatter = acm.FNumFormatter('InstrumentDefinitionNominalShowZero')
            return nominalFormatter.Format(nominal) if acm.Math.IsFinite(nominal) else ''

        status = FromRequest.StatusName(request)
        answer = FromRequest.UseAnswerToAccessPriceAndNominal(request, status)
        
        if answer:
            askNominal = quantityToNominalCb(answer.AskQuantity())
            bidNominal = quantityToNominalCb(answer.BidQuantity())
        else:
            askNominal = quantityToNominalCb(request.Quantity())
            bidNominal = askNominal
        nominals = {Direction.ask : FormatNominal(askNominal), Direction.bid : FormatNominal(bidNominal)}
        if request.BidOrAsk() == Direction.twoWay:
            nominalString = nominals[Direction.ask] # Both nominals will be the same in this case
        else:
            nominalString = nominals[request.BidOrAsk()]
        return nominalString

    @staticmethod
    def Direction(request):
        return 'Bid/Ask' if request.BidOrAsk() == Direction.twoWay else request.BidOrAsk()

    @staticmethod
    def Time(request):
        return Time.OnlyIfTodayFormat(request.DateTime())



class QuoteRequestHistoryHelper(object):
    @staticmethod
    def LastProposed(quoteRequestDict, isPrice):
        time = 0
        salesDict = None
        salesQrDict = quoteRequestDict.get(SalesTradingInteraction.SALES_NAME)
        if salesQrDict:
            for qr in salesQrDict:
                if FromRequest.StatusAsText(qr) == 'Proposed':
                    if not salesDict:
                        salesDict = FromRequest.PriceDict(qr) if isPrice else FromRequest.QuantityDict(qr)
                        time = qr.DateTime()
                    elif salesDict and salesDict == FromRequest.PriceDict(qr):
                        time = qr.DateTime() # Update to earliest proposed time for this price
                    else:
                        break
        if salesDict:
            salesDict['time'] = time
        return salesDict

    @staticmethod
    def LastProposedPrice(quoteRequestDict):
        return QuoteRequestHistoryHelper.LastProposed(quoteRequestDict, True)
    
    @staticmethod
    def LastProposedQuantity(quoteRequestDict):
        return QuoteRequestHistoryHelper.LastProposed(quoteRequestDict, False)
    
    @staticmethod
    def LastTraderPrice(quoteRequestDict, name):
        traderPriceDict = None
        salesPriceDict = QuoteRequestHistoryHelper.LastProposedPrice(quoteRequestDict)
        if salesPriceDict:
            traderPriceDict = {Direction.ask : 0, Direction.bid : 0}
            time = salesPriceDict['time']
            if time:
                for qr in quoteRequestDict[name]:
                    if qr.DateTime() <= time:
                        traderPriceDict = FromRequest.PriceDict(qr)
                        break
        return traderPriceDict
