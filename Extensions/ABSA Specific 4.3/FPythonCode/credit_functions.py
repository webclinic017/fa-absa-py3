import acm

hedge_eq_list =[item.Instrument().Name() for item in acm.FPhysInstrGroup['YieldDeltaHedge'].InstrGroupMaps()]


def _getCompanion(ins):
    if ins.InsType() in ('Bond', 'FRN', 'IndexLinkedBond'):
        ycc = ins.MappedDiscountLink().Link().YieldCurveComponent()
        if ins.Name() in hedge_eq_list:
            grp = ins
        elif hasattr(ycc, 'Benchmark') and ycc.Benchmark() <> None:
            grp = ycc.Benchmark()
        elif hasattr(ycc, 'UnderlyingYieldCurve'): 
            grp = ycc.UnderlyingYieldCurve()
        else:
            grp = 'NoCompanion'
            
    elif ins.InsType() in ('Swap', 'Deposit'):
        disclinkname = ins.MappedDiscountLink().LinkName()
        grp = disclinkname
    else:
        grp = 'Other'
    
    return grp


