
def getTotalReturnSwap_Und_Or_Itself(instrument):
    und_or_itself = ''
    
    if not instrument:
        return und_or_itself
    
    if instrument.RecordType() == 'Instrument':
        und_or_itself = instrument.Name()
        
        for leg in instrument.Legs():
            if leg.LegType() == 'Total Return':
                return leg.IndexRef().Name()
        
    return und_or_itself
