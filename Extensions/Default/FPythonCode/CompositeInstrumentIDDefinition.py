import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, Object, Bool
from ChoicesExprInstrument import getCategories, getCombCategories
from CompositeAttributes import AliasTableInst

class InstrumentIDDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, instrument, **kwargs):
        self._instrument = instrument 
        
    def Attributes(self):
        return { 
                 'categoryChlItem'      : Object( label='Category',
                                                  objMapping=self._instrument+'.CategoryChlItem',
                                                  choiceListSource=getCategories()),
                 'externalId1'          : Object( label='External ID 1',
                                                  objMapping=self._instrument+'.ExternalId1'),
                 'externalId2'          : Object( label='External ID 2',
                                                  objMapping=self._instrument+'.ExternalId2'),
                 'freeText'             : Object( label='Free Text',
                                                  objMapping=self._instrument+'.FreeText'),
                 'isin'                 : Object( label='ISIN',
                                                  objMapping=self._instrument+'.Isin'),
                 'productTypeChlItem'   : Object( label='Product Type',
                                                  objMapping=self._instrument+'.ProductTypeChlItem',
                                                  choiceListSource=acm.GetDomain("FChoiceList('Product Type')").Instances()),
                 'insaddr'              : Object( label='Ins No',
                                                  objMapping=self._instrument+'.Insaddr'),
                 'aliases'              : AliasTableInst ( label='Instrument Aliases',
                                                  instrument=self._instrument)           
               }
    # Label callbacks

    # ChoiceListSource callbacks
        
    # Visible callbacks
        
    # Util
    def Instrument(self):
        return self.GetMethod(self._instrument)()
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                   vbox{;
                        isin;
                        externalId1;
                        externalId2;
                        freeText;
                        categoryChlItem;
                        productTypeChlItem;
                        insaddr;
                        aliases;
                    };
                   """
               )
