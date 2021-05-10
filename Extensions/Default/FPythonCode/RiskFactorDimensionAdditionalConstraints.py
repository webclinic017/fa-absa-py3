
import acm

def IsBasedOnEquity( instrument ):
    cls = instrument.Class()
    return cls == acm.FStock or cls == acm.FEquityIndex or cls == acm.FETF
    
def IsBenchmarkCurve( yieldCurve ):
    cls = yieldCurve.Class()
    return cls == acm.FBenchmarkCurve or cls == acm.FSpreadCurve
