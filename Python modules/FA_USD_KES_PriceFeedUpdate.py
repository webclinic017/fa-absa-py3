import acm

def updatePriceFeed(curves):
    for curve in curves:
        for benchmark in curve.Benchmarks():
            insaddr=str(benchmark.Instrument().Oid())
            pld=acm.FPriceDefinition.Select('instrument='+insaddr)
            for pricedef in pld:
                if pricedef.Data0()[-6:]==' * 100':
                    pricedef.Data0=pricedef.Data0()[:-6]
                    pricedef.Commit()
                    print 'Price link changed to '+pricedef.Data0()+' for benchmark '+benchmark.Instrument().Name()

def updatePrices(curves):
    for curve in curves:
        for benchmark in curve.Benchmarks():
            for price in benchmark.Instrument().Prices():
                price.Ask=price.Ask()/100
                price.Bid=price.Bid()/100
                price.Last=price.Last()/100
                price.Settle=price.Settle()/100
                price.Commit()
            for price in benchmark.Instrument().HistoricalPrices():
                price.Ask=price.Ask()/100
                price.Bid=price.Bid()/100
                price.Last=price.Last()/100
                price.Settle=price.Settle()/100
                price.Commit()
                
curves=[acm.FYieldCurve['KES-FX_CURVE'], acm.FYieldCurve['KES-FX_CURVE/PriceTesting']]        
updatePriceFeed(curves)
updatePrices(curves)

