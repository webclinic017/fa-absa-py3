import acm

'''Returns an order book price finding type from an price finding type.'''

def getOrderBookPriceType(priceFindType):
    if priceFindType == "Bid":
        return ["AverageBidPrice"]
    if priceFindType == "Ask":
        return ["AverageAskPrice"]
    if priceFindType == "Last":
        return ["LastPrice"]
    if priceFindType == "Close":
        return ["ClosePrice"]
    return ["SpreadAveragePrice"]
