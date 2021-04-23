
import acm
from SP_DealPackageHelper import CreateBusinessEventAndLinks
from DealPackageUtil import UnDecorate

ET_CASH = 'Exercise Cash'
ET_PHYSICAL = 'Exercise'
CLOSE_TYPES = ('Closing', 'Novated')
IGNORE_STATUSES = ['Void', 'Confirmed Void', 'Terminated', 'Reserved']

def FindParentPackage(package, tradeTypeAttr):
    parentPackage = package.ParentDealPackage()
    if parentPackage and parentPackage.HasAttribute(tradeTypeAttr) and parentPackage.GetAttribute(tradeTypeAttr) in CLOSE_TYPES:
        return FindParentPackage(parentPackage, tradeTypeAttr)
    return parentPackage

def CalculateOpenAmount(trade, date = None, tradeType = 'tradeInput_tradeType', status = 'tradeInput_status', quantity = 'tradeInput_quantity_value', valueDay = 'tradeInput_valueDay', tradeTime = 'tradeInput_tradeTime'):
    openAmount = trade.Quantity()
    if trade.DealPackage():
        for lifeCyclePackage in trade.DealPackage().AllLifeCyclePackages():
            if ( lifeCyclePackage.GetAttribute(tradeType) in CLOSE_TYPES and
                 FindParentPackage(lifeCyclePackage, tradeType) == trade.DealPackage() and 
                 lifeCyclePackage.GetAttribute(status) not in IGNORE_STATUSES and
                 # Have to go via Originator to pick up trade time
                 (date is None or acm.Time().DateDifference(date, lifeCyclePackage.Originator().Edit().GetAttribute(tradeTime)) >= 0) ):
                openAmount += lifeCyclePackage.GetAttribute(quantity)
    return openAmount

def CalculateOpenPart(trade, date = None, tradeType = 'tradeInput_tradeType', status = 'tradeInput_status', quantity = 'tradeInput_quantity_value', valueDay = 'tradeInput_valueDay', tradeTime = 'tradeInput_tradeTime'):
    return CalculateOpenAmount(trade, date, tradeType, status, quantity, valueDay, tradeTime) / trade.Quantity()

def IsExercised(trade, ee):
    
    trade = trade.DecoratedObject() if hasattr(trade, 'DecoratedObject') else trade
    ins = trade.Instrument()
    isExercised = False
    
    if not ee:
        return None

    if "Cash" == ins.SettlementType():
        for p in trade.Payments():
            sameType = p.Type() == ET_CASH
            sameDate = p.ValidFrom() == ee.Date()
            if sameType and sameDate:
                isExercised = True
            
    elif "Physical Delivery" == ins.SettlementType():
        oid = trade.Originator().Oid()
        candidates = acm.FTrade.Select('contractTrdnbr = %s and type = "%s"' % (oid, ET_PHYSICAL))
        for t in candidates:
            sameDate = not acm.Time.DateDifference(ee.Date(), t.TradeTime())
            if sameDate and t.Status() not in IGNORE_STATUSES:
                isExercised = True

    return isExercised

def _CopyTradeFields(newTrade, originalTrade, date, settlementDate):
    attrsToCopy = ['Counterparty', 'Portfolio', 'Trader', 'Acquirer']
    for attr in attrsToCopy:
        setattr(newTrade, attr, getattr(originalTrade, attr)())
    newTrade.ContractTrdnbr(originalTrade.Originator().Oid())
    newTrade.Status('Simulated' if originalTrade.Status() == 'Simulated' else 'FO Confirmed')
    
    if 0 != acm.Time.DateDifference(date, acm.Time.DateToday()):
        newTrade.TradeTime(date)
    newTrade.ValueDay(settlementDate)
    newTrade.AcquireDay(settlementDate)

    return newTrade

def CreateB2BPayments(trade, origPayment):
    trade = UnDecorate(trade)
    constellation = acm.FX.ConstellationFromTrade(trade)
    for t in constellation.AllTrades(False):
        if t.Originator() == trade.Originator():
            continue
        if t.Portfolio() == trade.Portfolio():
            b2b1Amount = -origPayment.Amount()
        else:
            b2b1Amount = origPayment.Amount()
        paymentB2b1 = CreateExerciseCashPayment(t, b2b1Amount, origPayment.Currency(), origPayment.PayDay(), origPayment.ValidFrom())
        busEventB2b1 = _CreateExerciseBusinessEventAndLinks([t.Originator()], [paymentB2b1])
        paymentB2b2 = CreateExerciseCashPayment(t.MirrorTrade(), -b2b1Amount, origPayment.Currency(), origPayment.PayDay(), origPayment.ValidFrom())
        busEventB2b2 = _CreateExerciseBusinessEventAndLinks([t.MirrorTrade().Originator()], [paymentB2b2])
        return [paymentB2b1, busEventB2b1, paymentB2b2, busEventB2b2]
        
def CreateExerciseCashPayment(trade, amount, currency, payDay, validFrom):

    payment = acm.FPayment()
    payment.Trade(trade.Originator())
    payment.RegisterInStorage()
    payment.Type(ET_CASH)
    payment.Party(trade.Counterparty())
    payment.Amount(amount)
    payment.PayDay(payDay)
    payment.Currency(currency)
    payment.ValidFrom(validFrom)
    return payment

def AddExerciseCashPayment(trade, ee, amount, settlementDate, currency = None):
    ccy = trade.Instrument().Currency() if currency is None else currency
    payment = CreateExerciseCashPayment(trade, amount, ccy, settlementDate, ee.Date())
    
    busEvent = _CreateExerciseBusinessEventAndLinks([trade.Originator()], [payment])
    returnObjects = [payment, busEvent]
    
    if trade.IsB2BSalesCover():
        b2bObjects = CreateB2BPayments(trade, payment)
        for object in b2bObjects:
            returnObjects.append(object)

    return returnObjects

def _CreateExerciseBusinessEventAndLinks(exTrades, exPayments = []):
    return CreateBusinessEventAndLinks('Exercise/Assign', trades = exTrades, payments = exPayments)

def BarrierIsCrossedOnDate(ins, date):
    return (ins.Exotic() and 
            ins.Exotic().BarrierCrossedStatus() == 'Confirmed' and
            acm.Time().DateDifference(ins.Exotic().BarrierCrossDate(), date) == 0)

def CloseDealPackage(dealPackage, date, settlement, tradeTimeAttribute= None):
    actionCommand = dealPackage.TradeActionAt('close')
    actionDp = actionCommand.Invoke()[0]
    statusAttr = actionDp.GetAttribute('statusAttr')
    newStatus = 'Simulated' if dealPackage.GetAttribute(statusAttr) == 'Simulated' else 'FO Confirmed'
    actionDp.SetAttribute('status', newStatus)
    actionDp.SetAttribute('valueDay', settlement)
    actionDp.SetAttribute('acquireDay', settlement)
    actionDp.SetAttribute('closingPayType', 'None')
    actionDp.SetAttribute('closingAmount', 0)
    if acm.Time.DateDifference(date, acm.Time.DateNow()) != 0:
        if tradeTimeAttribute is None:
            for t in actionDp.ChildDealPackageAt('original').ChildDealPackageAt('Close1').Trades():
                t.TradeTime(date)
        else:
            actionDp.ChildDealPackageAt('original').ChildDealPackageAt('Close1').SetAttribute(tradeTimeAttribute, date)
    return actionDp

def CreatePhysicalDeliveryExerciseTrade(trade, ee, quantity, strike, settlementDate):
    t = acm.DealCapturing().CreateNewTrade(trade.Instrument().Underlying())
    t = acm.FBusinessLogicDecorator.WrapObject(t)
    
    t.Quantity(quantity)
    t.Price(strike)
    t.Type(ET_PHYSICAL)
    
    t = _CopyTradeFields(t, trade, ee.Date(), settlementDate)
    
    tNonDecorated = t.DecoratedObject()
    
    busEvent = _CreateExerciseBusinessEventAndLinks([trade, tNonDecorated])
    
    return [tNonDecorated, busEvent]

def CreateB2bTrades(b2bParams, excTrade):
    params = acm.FFxTradeConstellationParameters(excTrade)
    params.RegisterInStorage()
    decoParams = acm.FBusinessLogicDecorator.WrapObject(params)
    decoParams.SalesCoverEnabled = True
    decoParams.TradersPortfolio = b2bParams.TraderPortfolio()
    decoParams.TradersAcquirer = b2bParams.TraderAcquirer()
    allocationResult = decoParams.AllocateFXRisk()
    b2bObjects = allocationResult.ArtifactsToBeCommitted()
    return b2bObjects


# Amount 1 and amount 2 should be denominated values
def CreatePhysicalDeliveryFxSpotExerciseTrade(trade, amount1, amount2, settlementDate, b2bParams = None):
    # FX Cash should be entered as a standard Curr Pair
    # Amount entered will be amount1
    if acm.FCurrency[str(amount1.Unit())].CurrencyPair(str(amount2.Unit())).Currency1().Name() == str(amount1.Unit()):
        quantity = amount1
        premium = amount2
        setQuantity = True
    else:
        quantity = amount2
        premium = amount1
        setQuantity = False

    excTrade = acm.DealCapturing.CreateNewCustomTrade('FX Cash', quantity.Unit())
    excTrade = acm.FBusinessLogicDecorator.WrapObject(excTrade)

    excTrade = _CopyTradeFields(excTrade, trade, amount1.DateTime(), settlementDate)

    excTrade.Currency(premium.Unit())
    excTrade.Type(ET_PHYSICAL)
    excTrade.IsFxSpot(True)

    excTrade.Price(-premium.Number() / quantity.Number())
    if setQuantity is True:
        excTrade.Quantity(quantity.Number())
    else:
        excTrade.Premium(premium.Number())

    tNonDecorated = excTrade.DecoratedObject()
    busEvent = _CreateExerciseBusinessEventAndLinks([trade, tNonDecorated])

    # If original was B2B, exercise should also be B2B
    if trade.IsB2BSalesCover():
        b2bTrades = CreateB2bTrades(b2bParams, tNonDecorated)
        returnObjects = []
        for obj in b2bTrades:
            returnObjects.append(obj)
        events = _CreateExerciseBusinessEventAndLinksForB2B(trade, b2bTrades)
        for event in events:
            returnObjects.append(event)
    else:
        returnObjects = [tNonDecorated, busEvent]

    return returnObjects

def _CreateExerciseBusinessEventAndLinksForB2B(origTrade, b2bTrades):
    businessEvents = []
    for t in b2bTrades:
        if t.ContractTrade() and t.ContractTrade().Oid() == origTrade.Oid():
            event = _CreateExerciseBusinessEventAndLinks([origTrade, t])
            businessEvents.append(event)
    return businessEvents

def TodayIsLastExpiry(ins, date):
    lastExpiry = acm.Time().SmallDate()
    for ee in ins.ExerciseEvents():
        if acm.Time().DateDifference(ee.Date(), lastExpiry) > 0:
            lastExpiry = ee.Date()
    return acm.Time().DateDifference(date, lastExpiry) == 0

def TodayIsLastEventOfKind(ins, date, kind):
    lastExpiry = acm.Time().SmallDate()
    for ee in ins.GetExoticEventsOfKind(kind):
        if acm.Time().DateDifference(ee.Date(), lastExpiry) > 0:
            lastExpiry = ee.Date()
    return acm.Time().DateDifference(date, lastExpiry) == 0

def TodayIsLastPriceFixing(ins, date):
    return TodayIsLastEventOfKind(ins, date, 'Price Fixing')

def TodayIsLastTrfExpiry(ins, date):
    return TodayIsLastEventOfKind(ins, date, 'TRF Expiry')
