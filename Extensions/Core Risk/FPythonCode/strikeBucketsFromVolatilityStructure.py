
import acm
import FUxCore

#------------------------------------------------------------------------------
def ael_custom_label( parameters, dictExtra ):
    vs =  parameters.At('volatility structure')
    if vs:
       return '(' + vs.StringKey() + ')'
    return None

#------------------------------------------------------------------------------
def ael_custom_dialog_show( shell, params ):
    structures = acm.FVolatilityStructure.Select('').SortByProperty('Name')
    
    structure =  acm.UX().Dialogs().SelectObject(shell, 'Select Volatility Structure', 'Volatility Structures', structures, None)
    parameters = acm.FDictionary()
    
    if structure: 
        parameters.AtPut('volatility structure', structure)
        return parameters
    else:
        return None
        
#------------------------------------------------------------------------------
def ael_custom_dialog_main( parameters, dictExtra ):
    vs = parameters.At('volatility structure')
    
    return GenerateMidStrikeFromVolatilityStructure( vs )

#------------------------------------------------------------------------------
def GenerateMidStrikeFromVolatilityStructure( volStructure ):
    pointStrikes = set()
    for p in volStructure.Points():
        if p.Benchmark() and p.Benchmark().StoredStrikeType() == volStructure.StrikeType():
            pointStrikes.add( p.Benchmark().StrikePrice() )
        else:
            pointStrikes.add( p.Strike() )

    points = sorted( list(pointStrikes) )

    return [acm.Risk().CreateStrikeBucketDefinition( point ) for point in points]
