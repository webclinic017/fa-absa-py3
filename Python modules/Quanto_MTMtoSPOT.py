import ael, acm
def getGreeks2(instr, column, *rest):
    acm_ins = acm.FInstrument[instr.insid]
    calcSpace = acm.FCalculationSpace('FOrderBookSheet' )
    calc = calcSpace.CreateCalculation( acm_ins, 'Price Theor' )
    return calc.Value().Number()

def populateSpot(ins):
    pval = getGreeks2(ins, 'Price Theor')
    for p in ins.prices():
        if p.ptynbr.ptyid == 'SPOT':
            pc = p.clone()
            pc.settle = pval
            pc.last = pval
            pc.day == ael.date_today()
            print pc.pp()
            pc.commit()
populateSpot(ael.Instrument['QuantoHedge_Test'])    
