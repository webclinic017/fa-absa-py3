import acm   

def UpdateDefaultInstrument(ins):
    ins.Generic(True)
    ins.UnderlyingType('Commodity Variant')
    ins.Quotation('Coupon')
    ins.OpenEnd('None')
    
    leg = ins.RecLeg()
    leg.LegType('Fixed')
    leg.RollingPeriod('0d')

def StartPreciousMetalSwap(eii):
    acm.StartApplication('Instrument Definition', acm.FSymbol("PreciousMetalSwap"))
