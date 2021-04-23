'''--------------------------------------------------------------------------------------------------------
Date                    : 2011-09-06
Purpose                 : This script copies the theoretical price to the Spot price for all Aqua Options
Department and Desk     : Front Office - Equity Derivatives
Requester               : Herman Levin, Stephen Zoio and Andrey Chechin
Developer               : Paul Jacot-Guillarmod
CR Number               : 759644
--------------------------------------------------------------------------------------------------------'''
import acm
import ael

def GetTheoreticalPrice(instrument):
    ''' Calculate the theoretical price for an instrument.
    '''
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calculation = instrument.Calculation()
    theoreticalPrice = calculation.TheoreticalPrice(calculationSpace)
    try:
        return theoreticalPrice.Number()
    except:
        return 0

def AddPriceAel(acmInstrument, acmDate, value):
    ''' Use ael objects to insert or update the SPOT price for a given date.  The equivalent acm code
        sometimes fails to update the price.  The reason for failure hasn't been established yet.
    '''
    instrument = ael.Instrument[acmInstrument.Name()]
    date = ael.date(acmDate)
    market = ael.Party['SPOT']
    
    for p in instrument.prices():
        if p.ptynbr and p.ptynbr.ptyid == market.ptyid and p.day == date:
            price = p.clone()
            break
    else:
        price = ael.Price.new()
        price.insaddr = instrument.insaddr
        price.curr = instrument.curr
        price.day = date
        price.ptynbr = market.ptynbr
        
    price.bid = value
    price.ask = value
    price.settle = value
    price.last = value
    
    print("Copying theoretical price %(price)f to SPOT for %(instrument)s on %(date)s" \
            %{'price':value, 'instrument': instrument.insid, 'date': date})
    try:
        price.commit()
    except Exception as ex:
        print('ERROR: Theoretical price was not copied due to: %(exc)s' %{'exc':str(ex)})

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False
    
    return isNumber
        
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['aquaInstruments', 'Aqua Instruments', 'FInstrument', None, None, 1, 1, 'Aqua instruments that will ', None, 1]]

def ael_main(ael_dict):
    today = acm.Time().DateToday()
    for instrument in ael_dict['aquaInstruments']:
        if instrument.ExpiryDateOnly() > today:
            theoreticalPrice = GetTheoreticalPrice(instrument)
            if _isNumber(theoreticalPrice):
                AddPriceAel(instrument, today, theoreticalPrice)
        
    print('Completed Successfully')
    

