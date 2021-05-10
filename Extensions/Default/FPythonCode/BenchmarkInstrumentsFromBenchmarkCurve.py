
import acm

class VectorCreator( object ):
    def __init__( self ):
        pass

    def Vector( self, path ):
        if path and len(path) > 0:
            bInstruments = acm.FArray()
            bInstruments.AddAll(path[0].BenchmarkInstruments())
            bInstruments.SortByProperty('LastIRSensDay', True)
            return bInstruments
        return None

    def Labels( self, path ):
        return self.Vector( path )

def Create( dimensionDefinitions ):
    if dimensionDefinitions and len(dimensionDefinitions) > 0:
        for dimDef in dimensionDefinitions:
            if str(dimDef.Name()) == "Interest Rate Benchmark Curves":
                return VectorCreator()
    raise Exception( "Dimension Benchmark Instruments requires dimension 'Yield Curve'" )
