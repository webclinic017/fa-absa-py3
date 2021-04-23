
import acm
from DealPackageDevKit import DealPackageDefinition, Text, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class DefinitionSetup(DealPackageDefinition):
    """Example on how to work with Definition SetUp. The SetUp method is 
       available to simplify deployment. It is called when instantiating  
       the Deal Package. It perform the following four steps:\n
       1. Validates if all the needed additional entities (add info, context link, 
           choice list) are available in the database
       2. If entities are missing, a dialog is shown asking if the user 
           would like to run setup.
       3. If the user decide to run the setup, all the listed entities will 
           be saved in the database.
       4. Validates if the user need to restart the Prime session
    """
    
    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=180) 
                                
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
         
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                 doc;
                                 """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Stock', 'aStock')

    @classmethod
    def SetUp(cls, definitionSetUp):
        print ('Method SetUp was called')
        from DealPackageSetUp import  AddInfoSetUp, ChoiceListSetUp, ContextLinkSetUp, CustomMethodSetUp
        definitionSetUp.AddSetupItems(
                            ChoiceListSetUp(
                                list='Valuation Extension', 
                                entry='DP_ValExten_SetUp', 
                                descr='Deal Package Definition SetUp'
                                ),
                            ChoiceListSetUp(
                                list='ValGroup', 
                                entry='DP_ValGroup_SetUp', 
                                descr='Deal Package Definition SetUp'
                                ),
                            ContextLinkSetUp(
                                context='Global',
                                type='Valuation Extension',
                                name='DP_ValExten_SetUp',
                                mappingType='Val Group',
                                chlItem='DP_ValGroup_SetUp'
                                ),
                            AddInfoSetUp( 
                                recordType='DealPackage',
                                fieldName='aDP_double',
                                dataType='Double',
                                description='Deal Package Definition SetUp',
                                dataTypeGroup='Standard',
                                subTypes=[],
                                defaultValue=None,
                                mandatory=False
                                ))
                                
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')
       
