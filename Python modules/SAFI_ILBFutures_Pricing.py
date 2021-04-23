'''
Date                    : 2011-07-05
Purpose                 : This script is required to correctly price Bond Futures.
Department and Desk     : Front Office - Fixed Income
Requester               : Talia Petousis/ Kelly Hattingh
Developer               : Anwar Banoo
CR Number               : 707647
'''

import ael, acm


ael_gui_parameters = { 'windowCaption':'ILBond Futures AIP Update'}
ael_variables = [ ('Instruments', 'Instruments: ', 'FInstrument', None, None, 0, 1, 'List of Instruments')]
REPOCURVE = 'ZAR_Bond_repo_GC'

def amendPrice(price, newRate, date):
    price.Last(newRate)
    price.Settle(newRate)
    price.Ask(newRate)
    price.Bid(newRate)
    price.Day(date)
    try:
        price.Commit()
        print price.Instrument().Name() + ' Price Committed'
    except Exception, e:
        print e

def createPrice(ins, newRate, date):
    priceNew = acm.FPrice()
    priceNew.Last(newRate)
    priceNew.Settle(newRate)
    priceNew.Ask(newRate)
    priceNew.Bid(newRate)
    priceNew.Day(date)
    priceNew.Instrument(ins)
    priceNew.Market(acm.FParty['SPOT'])
    priceNew.Currency(ins.Currency())
    try:
        priceNew.Commit()
        print ins.Name() + ' Price Created'
    except Exception, e:
        print e

def changePrice(ins, newRate, date):
    price = None
    prices = ins.Prices()
    if prices:
        for p in prices:
            if p.Market().Name() == 'SPOT':
                price = p
                
        if price:
            amendPrice(price, newRate, date)
        else:
            createPrice(ins, newRate, date)
    else:
        createPrice(ins, newRate, date)

def GetAllInEndPrice(ins):
    i = ael.Instrument[ins.Name()]
    return i.und_insaddr.dirty_from_yield(i.exp_day, None, None, i.ref_price)
    
def FixBondFuturePrice(ins):
    today = acm.Time().DateToday()
    expDate = ins.ExpiryDateOnly()
    try:
        ref_ins = ins.AdditionalInfo().Underlying_BSB()    
    
        if ref_ins and ref_ins.InsType() == 'BuySellback':
            RefCal = ref_ins.Currency().Calendar()
            tPlus3 = RefCal.AdjustBankingDays(today, 3)        
            ref_und = ref_ins.Underlying()

            t = ref_ins.Trades().At(0)
            ael_trade = ael.Trade[t.Oid()]
            calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

            price= ref_und.Calculation().MarketPrice(calcSpace).Number()
            curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()
            
            if not curve.IsKindOf(acm.FYCAttribute):
                rate =  ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent().Rate(tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365')*100
            else:
                curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()
                curve = curve.IrCurveInformation(curve.UnderlyingCurve().IrCurveInformation(), acm.Time().DateToday())
                rate =  curve.Rate(tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365', 'Spot Rate')*100
       
            t.Price(price)
            ref_ins.Rate(rate)
            ref_ins.StartDate(tPlus3)
            
            ref_ins.RefPrice(ael_trade.buy_sellback_ref_price())
            ref_ins.RefValue(ael_trade.buy_sellback_ref_value(1))

            allInPrice = GetAllInEndPrice(ref_ins)
            print allInPrice
            
            try:
                changePrice(ins, allInPrice, today)
            except:
                ael.log('SPOT price update failed for %s' %(ins.Name()))
        else:
            ael.log('Missing underlying for %s' %(ins.Name()))
    except Exception, e:
        ael.log('Error processing %s, %s' %(ins.Name(), e.message))


def ael_main(data):
    for ins in data['Instruments']: 
        ael.log('Process instrument, %s' %(ins.Name()))
        FixBondFuturePrice(ins)
    ael.log('All processing complete')
