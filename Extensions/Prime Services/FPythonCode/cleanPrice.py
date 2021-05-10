import acm
import ps_gen_swift_mt515_client_trade
import QuoteToValue

calculationSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

def cleanPricePLDate(object, date):
    try:
        if(object.Trade().HedgeTrade() and object.Trade().Instrument().InsType() == 'IndexLinkedBond'):
            cleanprice = ps_gen_swift_mt515_client_trade._getCleanPricePLDate(object.Trade().HedgeTrade(), date)
        else:
            cleanprice = ps_gen_swift_mt515_client_trade._getCleanPricePLDate(object.Trade(), date)
        return cleanprice
    except ps_gen_swift_mt515_client_trade.IrrelevantInstrumentError:
        return None # Do not raise when queried for irrelevant instruments.

def cleanPrice(object):
    try:
        if(object.Trade().HedgeTrade() and object.Trade().Instrument().InsType() == 'IndexLinkedBond'):
            cleanprice = ps_gen_swift_mt515_client_trade._getCleanPrice(object.Trade().HedgeTrade())
        else:
            cleanprice = ps_gen_swift_mt515_client_trade._getCleanPrice(object.Trade())
        return cleanprice
    except ps_gen_swift_mt515_client_trade.IrrelevantInstrumentError:
        return None # Do not raise when queried for irrelevant instruments.

def cleanConsiderationLeg1(object):
# Clean Consideration (Cash) for BSB Leg 1
    trade = object.Trade()
    instrument = trade.Instrument()
    if instrument.InsType() == 'BuySellback':
        und = instrument.Underlying()
        cleanConsiderationLeg1 = QuoteToValue.convertPriceForInstrument(
                calculationSpace, und, trade.ValueDay(), trade.Price(), 
                und.Quotation().Name(), "Clean") / 100
    else:
        cleanConsiderationLeg1 = ps_gen_swift_mt515_client_trade._getCleanPrice(trade)
    return cleanConsiderationLeg1

def cleanConsiderationLeg2(object):
# Clean Consideration (Cash) for BSB Leg 2
    trade = object.Trade()
    instrument = trade.Instrument()
    if instrument.InsType() == 'BuySellback':
        und = instrument.Underlying()
        cleanConsiderationLeg1 = QuoteToValue.convertPriceForInstrument(
                calculationSpace, und, instrument.ExpiryDate(), 
                instrument.RefPrice(), und.Quotation().Name(), "Clean") / 100
    else:
        cleanConsiderationLeg1 = ps_gen_swift_mt515_client_trade._getCleanPrice(trade)
    return cleanConsiderationLeg1
