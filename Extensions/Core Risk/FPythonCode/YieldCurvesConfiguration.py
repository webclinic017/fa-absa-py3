
import acm


class ConfigCreator( object ):

    _s_ExtensionAttributeSym = acm.FSymbol("ExtensionAttribute")

    def __init__( self, dimensionDefinitions ):
        self.m_dimensionDefinitions = dimensionDefinitions
        
    def CreateConfig( self, path ):
        params = {}
        for dimDef, item in zip( self.m_dimensionDefinitions, path ):
            params[ dimDef[ self._s_ExtensionAttributeSym ] ] = item
        config = acm.Sheet().Column().ConfigurationFromExtensionAttributeValues( params, None )
        return config
        
def Create( dimensionDefinitions ):
    return ConfigCreator( dimensionDefinitions )
