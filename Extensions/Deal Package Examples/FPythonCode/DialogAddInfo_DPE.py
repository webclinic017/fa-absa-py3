
import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Action, Settings, AttributeDialog
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class DealPackageDialogAddInfo(DealPackageDefinition):
    """UI Dialog. Please press the button to get a new dialog window."""
    
    ipName            = Object( label='Name',
                                objMapping='InstrumentPackage.Name') 

    myBtn             = Action( label='More Additional Infos',
                                dialog=AttributeDialog(label='DealPackage Example Dialog', 
                                                       customPanes='@AddInfoDialogCustomPanes'),
                                action='@ExampleMethodCalledOnDialogClose')

    addinfo_Double    = Object( label='Double test',
                                objMapping='DealPackage.AdditionalInfo.DPEx_Double')
                                
    addinfo_Enum      = Object( label='Enum test',
                                objMapping='LeadTrade.AdditionalInfo.DPEx_Enum')
                            
    addinfo_Beta      = Object( label='AI_Beta',
                                objMapping='DealPackage.AdditionalInfo.DPEx_Beta')

    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=80) 
                                
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
         
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                ipName;
                                myBtn;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );	
                                """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Stock', 'stockTrade')

    def LeadTrade(self):
        return self.TradeAt('stockTrade')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def ExampleMethodCalledOnDialogClose(self, attrName, dialogValues):
        print ('Dialog Return Values', dialogValues)

    def AddInfoDialogCustomPanes(self, *args):
        return [
                    {'Additional Info' : """
                                addinfo_Double;
                                addinfo_Enum;
                                addinfo_Beta;
                                """
                    }
                ]
    
    @classmethod
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import  AddInfoSetUp
        definitionSetUp.AddSetupItems(
                            AddInfoSetUp( recordType='DealPackage',
                                          fieldName='DPEx_Beta',
                                          dataType='Double',
                                          description='DealPackageExample Double Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),
        
                            AddInfoSetUp( recordType='DealPackage',
                                          fieldName='DPEx_Double',
                                          dataType='Double',
                                          description='DealPackageExample Double Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),
        
                            AddInfoSetUp( recordType='Trade',
                                          fieldName='DPEx_Enum',
                                          dataType='TradeCategory',
                                          description='DealPackageExample Enum Test',
                                          dataTypeGroup='Enum',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False)
                                    )
