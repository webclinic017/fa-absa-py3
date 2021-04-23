import acm
  

class RFQTimerDefaultSettings(object):
    gtd = 'Good Till Date'
    gtc = 'Good Till Cancelled'
    timeSpan = 'Time Span'
    defaultReplyTimeoutType = timeSpan
    defaultReplyExpiry = acm.Time().TodayAt(23, 59, 59, 0, False)
    defaultReplyTime = 180 / (24.0 * 3600.0)
    defaultNegotiationTimeoutType = gtd
    defaultNegotiationExpiry = acm.Time().TodayAt(23, 59, 59, 0, False)
    defaultNegotiationTime = 300 / (24.0 * 3600.0)
    defaultWireTime = 90 / (24.0 * 3600.0)
    
def DefaultSalesPortfolio():
    return acm.FPhysicalPortfolio['SALES']

def DefaultSalesAcquirer(portfolio=None, *args):
    owner = None
    if portfolio:
        owner = portfolio.PortfolioOwner()
    return owner if owner else acm.FParty['FCS']
    
def IsYieldQuoted(tradingInterface, instrument):
    YieldQuotationTypes=['Yield', 'Simple Rate', 'Discount Rate']
    if tradingInterface:
        quotation = tradingInterface.PriceFeed().Quotation()
    else:
        quotation = OrderBookCreation.Quotation(instrument, tradingInterface)
    return quotation.QuotationType() in YieldQuotationTypes
   
'''********************************************************************
*  The function ButtonLabels returns an array with labels for the Buy, 2Way, Sell, Hit and Lift buttons 
*  The function FullLabel returns the label that is displayed in the Top Panel of the RFQ/Sales Order window as well as in the Summary.
********************************************************************'''    
class ButtonLabels(object):
    @staticmethod
    def AskLabelFromInstrument(instrument):
        label = 'Buy'
        if instrument.IsSwap():
            label = 'Pay'
            if instrument.SwapType() == 'Float/Float':
                label += ' ' + instrument.FirstPayLeg().RollingPeriod().title()
        elif instrument.InsType() == 'SecurityLoan':
            label = 'Borrow'
        return label

    @staticmethod
    def BidLabelFromInstrument(instrument):
        label = 'Sell'
        if instrument.IsSwap():
            label = 'Receive'
            if instrument.SwapType() == 'Float/Float':
                label += ' ' + instrument.FirstPayLeg().RollingPeriod().title()
        elif instrument.InsType() == 'SecurityLoan':
            label = 'Lend'
        return label

    @staticmethod
    def ButtonLabels(instrument, *args):
        askLabel = ButtonLabels.AskLabelFromInstrument(instrument)
        bidLabel = ButtonLabels.BidLabelFromInstrument(instrument)
        return [bidLabel, '2Way', askLabel, 'Accept', 'Accept']
    
    @staticmethod
    def FullLabel(direction, instrument, *args):
        labels = ButtonLabels.ButtonLabels(instrument)
        label = labels[1]
        if direction == 'Ask':
            label = labels[2]
        elif direction == 'Bid':
            label = labels[0]
        label = label.title()
        if instrument.IsSwap() and direction:
            if instrument.SwapType() == 'Float/Float':
                label = label + ' Float'
            else:
                label = label + ' Fixed'
        return label

'''********************************************************************
* Methods to specify properties sending a Request For Quote on an OTC 
*  product with available no Order Book
********************************************************************'''    
class OrderBookCreation(object):
    @staticmethod
    def ValidMarkets():
        return ['IM']

    @staticmethod
    def DefaultMarket(instrument):
        return 'IM'

    @staticmethod
    def MarketSegmentId(instrument):
        return 150000

    @staticmethod
    def TickSizeId(instrument):
        return 1001
    
    @staticmethod
    def IsPriceBased(instrument):
        isPriceBased = True
        if instrument.InsType() in ['Deposit', 'FRA', 'Swap', 'CurrSwap', 'TotalReturnSwap', 'IndexLinkedSwap', 'SecurityLoan', 'Repo/Reverse', 'BasketRepo/Reverse', 'BasketSecurityLoan']:
            isPriceBased = False
        return isPriceBased
        
    @staticmethod
    def Quotation(instrument, tradingInterface=None):
        if tradingInterface:
            return tradingInterface.PriceFeed().Quotation()
        else:
            quotation = instrument.Quotation()
            if not OrderBookCreation.IsPriceBased(instrument):
                instrument = instrument.Clone()
                instrumentDecorator = acm.FBusinessLogicDecorator.WrapObject(instrument)
                instrumentDecorator.Generic(True)
                quotation = instrument.Quotation()
            return quotation
        
        
'''********************************************************************
* Methods to specify how the sales spread should be treated.
- PriceDifferenceFromMargin accepts the value of the Sales Spread field in the
RFQ Sales Dialog and returns the absolute price difference between the All-In Price
and the Trader Price
- MarginFromPriceDifference is the inverse of MarginToPriceDifference
********************************************************************'''  
class PriceAndMarginConversions(object):
    @staticmethod
    def PriceDifferenceFromMargin(margin, tradingInterface, instrument):
        if instrument.IsSpreadInBasisPoints():
            margin /= 100.0
        return margin

    @staticmethod
    def MarginFromPriceDifference(priceDiff, tradingInterface, instrument):
        if instrument.IsSpreadInBasisPoints():
            priceDiff *= 100.0
        return priceDiff

'''********************************************************************
* Return the tick size for Price and Nominal Fields when using the spinn button,
*   Please note that the tradingInterface will not be available when called from a not yet saved Instrument
********************************************************************'''
class TickSizeSettings(object):
    @staticmethod
    def PriceTickSize(instrument, tradingInterface, currentValue):
        minimumTick = 0.01
        tick = minimumTick
        if tradingInterface:
            tick = tradingInterface.TickSizeList().TickSizeAt(currentValue)
        return minimumTick if tick < minimumTick else tick
        
    @staticmethod
    def NominalTickSize(instrument, tradingInterface, currentValue):
        roundLot = 1
        if tradingInterface:
            roundLot = tradingInterface.RoundLot()
        contractSize = instrument.ContractSize()
        return roundLot * contractSize
        
    @staticmethod
    def SalesSpreadTickSize(instrument, tradingInterface, currentValue, currentPrice):
        minimumTick = 0.01
        tick = minimumTick
        if tradingInterface:
            tick = tradingInterface.TickSizeList().TickSizeAt(currentPrice)
        return minimumTick if tick < minimumTick else tick

    @staticmethod
    def MarginAmountTickSize(instrument, tradingInterface, currentValue):
        return 1000
    
'''********************************************************************
* Methods to specify Trade Creation Settings

- TradeSettingDisplayNames - The display names of the different trade creation settings. 
        [0] - Create new instrument/instrument package and trade/deal package
        [1] - Create new trade/deal package only
        [2] - Update existing trade/deal package
        [3] - Manual handling
        
- DefaultValueOverride - Returns the value the trade creation setting should be initialized to. Return
                         an element from the TradeSettingNames array. Return None to fall back on core logic.
********************************************************************'''  
class TradeCreation(object):    
    @staticmethod
    def TradeSettingDisplayNames(isOnDp):
        return ['Create New', 
                'Create New Deal Package' if isOnDp else 'Create New Trade',
                'Update',
                'Manual']

    @staticmethod
    def DefaultValueOverride(isOnOriginalTradeOrDealPackage, multiTradingEnabled, insType, dealPackageType):
        return None
            
    @staticmethod        
    def SettingVisibleInDialog(insType, dealPackageType):
        return True    

    @staticmethod
    def CreateTradesOnRequest(insType, dealPackageType):
        return dealPackageType is not None

'''********************************************************************
* Default Customer Request Name
********************************************************************'''
def SuggestDefaultCustomerRequestName(client):
    name = ""
    if client:
        timeNowAsString = acm.GetDomain('datetime').DefaultFormatter().Format(acm.Time().TimeNow())
        name = client.Name() + ' ' + timeNowAsString
    return name   

'''********************************************************************
* Limits
********************************************************************'''
class Limits(object):
    @staticmethod
    def CheckLimitsRequired(trade, dealPackage):
        return False

'''********************************************************************
* Trade Statuses
********************************************************************'''
def NonConfirmedTradeStatuses():
        return ['Simulated', 'Reserved', 'Void', 'Confirmed Void', 'Inactive']
