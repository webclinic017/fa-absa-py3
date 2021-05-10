
import acm, cleanPrice

def dealAmount(object):

    if not object.Instrument().InsType() == 'BuySellback':
        quantity = abs(object.Trade().QuantityOrNominalAmount())

        if object.Instrument().Underlying() != None and object.Instrument().Underlying().Instrument().InsType() in ('Bond', 'IndexLinkedBond'):
            price = cleanPrice.cleanPrice(object)
        else:
            price = object.Trade().Price() * object.Instrument().Quotation().QuotationFactor()

        dealAmount = quantity * price
        return dealAmount
