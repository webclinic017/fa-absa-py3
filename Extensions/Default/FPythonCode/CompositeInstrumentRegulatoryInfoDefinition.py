import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, Object, Bool
from ChoicesExprInstrument import getCategories
from ChoicesExprRegInfo import commodityBaseProducts, commoditySubProducts, commodityFurtherSubProducts

class InstrumentRegulatoryInfoDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, insRegInfo, **kwargs):
        self._insRegInfo = insRegInfo
        self.commodityChoiceLists = {}
        self.commodityChoiceLists['Base'] = None
        self.commodityChoiceLists['Sub'] = None
        self.commodityChoiceLists['FutherSub'] = None
        
    def Attributes(self):
        return { 
                'cfiCode': Object( label='CFI Code',
                                                         objMapping=self._insRegInfo+'.CfiCode'),              
                'largeInScale': Object( label='LIS',
                                                         objMapping=self._insRegInfo+'.LargeInScale'),
                'sizeSpecificToInstrument': Object( label='SSTI',
                                                         objMapping=self._insRegInfo+'.SizeSpecificToInstrument'),
                'averageDailyTurnover': Object( label='ADT',
                                                         objMapping=self._insRegInfo+'.AverageDailyTurnover'),
                'clearingIsMandatory': Object( label='Clearing Mandatory',
                                                         objMapping=self._insRegInfo+'.ClearingIsMandatory'),
                'isSystematicInternaliser': Object( label='Systematic Internaliser',
                                                         objMapping=self._insRegInfo+'.IsSystematicInternaliser'),
                'isLiquid': Object( label='Liquid',
                                                         visible=self.UniqueCallback('@IsNotCommodityRelated'),
                                                         objMapping=self._insRegInfo+'.IsLiquid'),
                'commodityBaseProduct': Object( label='Base Product',
                                                         onChanged=self.UniqueCallback('@UpdateChoiceLists'),
                                                         choiceListSource=self.UniqueCallback('@GetCommodityBaseProductChoices'),
                                                         visible=self.UniqueCallback('@IsCommodityRelated'),
                                                         objMapping=self._insRegInfo+'.CommodityBaseProduct'),
                'commoditySubProduct': Object( label='Sub Product',
                                                         onChanged=self.UniqueCallback('@UpdateChoiceLists'),
                                                         choiceListSource=self.UniqueCallback('@GetCommoditySubProductChoices'),
                                                         visible=self.UniqueCallback('@IsCommodityRelated'),
                                                         objMapping=self._insRegInfo+'.CommoditySubProduct'),
                'commodityFurtherSubProduct': Object( label='Further Sub Prod',
                                                         onChanged=self.UniqueCallback('@UpdateChoiceLists'),
                                                         choiceListSource=self.UniqueCallback('@GetCommodityFurtherSubProductChoices'),
                                                         visible=self.UniqueCallback('@IsCommodityRelated'),
                                                         objMapping=self._insRegInfo+'.CommodityFurtherSubProduct'),
               }
    # Label callbacks

    # ChoiceListSource callbacks
    def GetCommodityBaseProductChoices(self, *args):
        if self.commodityChoiceLists['Base'] is None:
            self.UpdateChoiceLists()
        return self.commodityChoiceLists['Base']

    def GetCommoditySubProductChoices(self, *args):
        if self.commodityChoiceLists['Sub'] is None:
            self.UpdateChoiceLists()
        return self.commodityChoiceLists['Sub']

    def GetCommodityFurtherSubProductChoices(self, *args):
        if self.commodityChoiceLists['FutherSub'] is None:
            self.UpdateChoiceLists()
        return self.commodityChoiceLists['FutherSub']
    
    def UpdateChoiceLists(self, *args):
        for key in self.commodityChoiceLists:
            if self.commodityChoiceLists[key] is None:
                self.commodityChoiceLists[key] = DealPackageChoiceListSource()
            self.commodityChoiceLists[key].Clear()
        
        self.commodityChoiceLists['Base'].AddAll( commodityBaseProducts(self.RegulatoryInfo()) )
        self.commodityChoiceLists['Sub'].AddAll( commoditySubProducts(self.RegulatoryInfo()) )
        self.commodityChoiceLists['FutherSub'].AddAll( commodityFurtherSubProducts(self.RegulatoryInfo()) )
        
        if self.commodityBaseProduct not in self.commodityChoiceLists['Base'].Source():
            self.SetAttribute('commodityBaseProduct', None, silent=True)
        
        if self.commoditySubProduct not in self.commodityChoiceLists['Sub'].Source():
            self.SetAttribute('commoditySubProduct', None, silent=True)
            
        if self.commodityFurtherSubProduct not in self.commodityChoiceLists['FutherSub'].Source():
            self.SetAttribute('commodityFurtherSubProduct', None, silent=True)
    
    # Visible callbacks
    def IsCommodityRelated(self, *args):
        return self.Instrument().IsCommodityRelated()
    
    def IsNotCommodityRelated(self, *args):
        return not self.IsCommodityRelated()
    
    # Util
    def RegulatoryInfo(self):
        return self.GetMethod(self._insRegInfo)()
        
    def Instrument(self):
        return self.RegulatoryInfo().Instrument()
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                    hbox(;
                        vbox{;
                            cfiCode;
                            largeInScale;
                            sizeSpecificToInstrument;
                            averageDailyTurnover;
                        };
                        vbox{;
                            clearingIsMandatory;
                            isSystematicInternaliser;
                            isLiquid;
                        };
                    );
                    vbox[Commodity;
                        commodityBaseProduct;
                        commoditySubProduct;
                        commodityFurtherSubProduct;
                    ];
                   """
               )
