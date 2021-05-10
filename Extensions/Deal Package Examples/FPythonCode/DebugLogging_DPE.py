import acm
from DealPackageDevKit import DealPackageDefinition, Action, Text, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False,  
          LogMode='Verbose') # Valid Modes: Verbose, Warning, Error
class DebugLogging(DealPackageDefinition):
    """
    To ease the development and error investigations in production it 
    often help to print log messages. If no LogMode is specified, it will 
    default to "Error".

    The Deal Package can be in the following logging modes:
        * Verbose: Log all messages
        * Warning: Log messages of type Warning and Error
        * Error: Only log messages of type Error
    """

    verbose   = Action( label='Verbose',
                        action='@VerboseLog',
                        toolTip='Prints a message to the log if the dealpackage log mode is Verbose')
                        
    warning   = Action( label='Warning',
                        action='@WarningLog',
                        toolTip='Prints a message to the log if the dealpackage log mode is Verbose or Warning')
    
    error     = Action( label='Error',
                        action='@ErrorLog',
                        toolTip='Prints a message to the log if the dealpackage log mode is Verbose, Warning or Error')
                        
    doc       = Text(   defaultValue=cleandoc(__doc__),
                        editable=False,
                        height=130)  
                        
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                hbox(;
                                    verbose;
                                    warning;
                                    error;
                                );
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );	
                                """
                    }
                ]

    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def VerboseLog(self, attrName):
        """Prints a message to the log if the dealpackage log mode is Verbose"""
        self.Log().Verbose('Verbose button pressed')
    
    def WarningLog(self, attrName):
        """Prints a message to the log if the dealpackage log mode is Verbose or Warning"""
        self.Log().Warning('Warning button pressed')
    
    def ErrorLog(self, attrName):
        """Prints a message to the log if the dealpackage log mode is Verbose, Warning or Error"""
        self.Log().Error('Error button pressed')
