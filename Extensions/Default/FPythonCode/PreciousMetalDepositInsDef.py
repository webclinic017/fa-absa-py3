
def UpdateDefaultInstrument(ins):
    ins.UnderlyingType = 'Commodity Variant'
    ins.ContractSize = 1.0
    leg = ins.Legs().First()
    leg.NominalScaling = 'Initial Price'
    
