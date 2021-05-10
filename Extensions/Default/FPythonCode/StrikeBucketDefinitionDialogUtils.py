
import acm

#------------------------------------------------------------------------------
# FParameterGUIDefinitionWrapper
#------------------------------------------------------------------------------
class FParameterGUIDefinitionWrapper( object ):
    
    #------------------------------------------------------------------------------
    def __init__( self, parameterGUIDefinition ):        
        __import__(str( parameterGUIDefinition.At( 'Module' ) ))
        
        self.m_parameterGUIDefinition = parameterGUIDefinition
        self.m_scriptParams = None
        
        self.m_pythonModule = acm.FPythonModule[str( parameterGUIDefinition.At( 'Module' ) )]
    
    #------------------------------------------------------------------------------
    def RunGUI( self, shell, initialParams ):
        if hasattr( self.m_pythonModule, 'ael_custom_dialog_show' ):
            scriptParams = self.m_pythonModule.ael_custom_dialog_show( shell, initialParams )
    
            if not scriptParams:
                raise Exception( 'Parameters could not be created for {}'.format( self.m_parameterGUIDefinition.DisplayName() ) )
                
            self.m_scriptParams = scriptParams
    
    #------------------------------------------------------------------------------
    def StrikeBucketGenerationInfo( self ):
        return acm.Risk().CreateStrikeBucketGenerationInfo( self.m_parameterGUIDefinition, self.m_scriptParams )
            
#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def GetFParameterGUIDefinitions( group ):
    parameterGUIDefinitionByDisplayName = {}

    extensions = acm.GetDefaultContext().GetAllExtensions( 'FParameterGUIDefinition', 'FObject', True, True, group )
        
    for e in extensions:
        parameterGUIDefinitionByDisplayName[str( e.DisplayName() )] = e
        
    return parameterGUIDefinitionByDisplayName
