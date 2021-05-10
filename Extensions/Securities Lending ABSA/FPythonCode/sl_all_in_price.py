
import acm

CALENDAR = acm.FCalendar['ZAR Johannesburg']
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def sl_all_in_price(instrument, mtm_date):
    if instrument.InsType() == 'CD':
        return 1.0
    curr = instrument.Currency()
    price_date = CALENDAR.AdjustBankingDays(mtm_date, instrument.SpotBankingDaysOffset())
    if instrument.InsType() in ['Bond', 'IndexLinkedBond']:
        if curr != acm.FCurrency['ZAR']:
            bond_mtm_price = instrument.UsedPrice(mtm_date, curr.Name(), 'internal')
            price_date = mtm_date
        else:   
            bond_mtm_price = instrument.UsedPrice(mtm_date, curr.Name(), 'SPOT_BESA')
    else:
        bond_mtm_price = instrument.UsedPrice(mtm_date, curr.Name(), 'SPOT')
    if not bond_mtm_price:
        bond_mtm_price = instrument.UsedPrice(mtm_date, curr.Name(), 'internal')

    all_in_price = instrument.Calculation().PriceToUnitValue(CALC_SPACE, 
                                                      bond_mtm_price, 
                                                      instrument.Quotation(), 
                                                      price_date, 
                                                      False)
    if all_in_price:
        return round(all_in_price.Number(), 7)
    return 0.0
