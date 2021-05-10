import acm
from DealPackageDevKit import DealPackageDefinition, Str, Object, Text, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class AttributeObjectMappingAddInfo(DealPackageDefinition):
    """Examples showing how to add additional info to the deal package, instrument and trade."""
    ipName            = Object( label='Name',
                                objMapping='InstrumentPackage.Name') 
                                
    addInfo_String    = Object( label='String test',
                                objMapping='Trade.AdditionalInfo.DPEx_String')
                            
    addInfo_Char      = Object( label='Char test',
                                objMapping='Trade.AdditionalInfo.DPEx_Char')
    
    addinfo_Integer   = Object( label='Int test',
                                objMapping='Trade.AdditionalInfo.DPEx_Integer')
                            
    addinfo_Date      = Object( label='Date test',
                                objMapping='Instrument.AdditionalInfo.DPEx_Date',
                                formatter='DateOnly')
 
    addinfo_Bool      = Object( defaultValue=False,
                                label='Bool test',
                                objMapping='DealPackage.AdditionalInfo.DPEx_Boolean')
                            
    addinfo_Double    = Object( label='Double test',
                                objMapping='DealPackage.AdditionalInfo.DPEx_Double')
                                
    addinfo_RecordRef = Object( label='Record ref test',
                                objMapping='Instrument.AdditionalInfo.DPEx_RecordRef')
    
    addinfo_Enum      = Object( label='Enum test',
                                objMapping='Trade.AdditionalInfo.DPEx_Enum')
 
    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=80)

    # ####################### #
    #   Interface Overrides   #
    # ####################### #  

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_AttributeObjectMappingAddInfo_DPE')

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Stock', 'stockTrade')
         
    def SuggestName(self):
        import time
        package = self.DealPackage()
        timeStr = time.strftime('%Y%m%d%H%M%S', time.gmtime())
        insName = 'IP_AOMAI_' + timeStr
        return insName
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Trade(self):
        return self.TradeAt('stockTrade')
        
    def Instrument(self):
        return self.TradeAt('stockTrade').Instrument()
    
    @classmethod
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import  AddInfoSetUp
        definitionSetUp.AddSetupItems(
                            AddInfoSetUp( recordType='Trade',
                                          fieldName='DPEx_Integer',
                                          dataType='Integer',
                                          description='DealPackageExample Integer Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),
                                          
                            AddInfoSetUp( recordType='Trade',
                                          fieldName='DPEx_Char',
                                          dataType='Char',
                                          description='DealPackageExample Char Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),
        
                            AddInfoSetUp( recordType='Trade',
                                          fieldName='DPEx_String',
                                          dataType='String',
                                          description='DealPackageExample String Test',
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

                            AddInfoSetUp( recordType='DealPackage',
                                          fieldName='DPEx_Boolean',
                                          dataType='Boolean',
                                          description='DealPackageExample Bool Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),

                            AddInfoSetUp( recordType='Instrument',
                                          fieldName='DPEx_Date',
                                          dataType='Date',
                                          description='DealPackageExample Date Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),

                            AddInfoSetUp( recordType='Instrument',
                                          fieldName='DPEx_Time',
                                          dataType='Time',
                                          description='DealPackageExample Time Test',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue=None,
                                          mandatory=False),

                            AddInfoSetUp( recordType='Instrument',
                                          fieldName='DPEx_RecordRef',
                                          dataType='User',
                                          description='DealPackageExample RecordRef Test',
                                          dataTypeGroup='RecordRef',
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
