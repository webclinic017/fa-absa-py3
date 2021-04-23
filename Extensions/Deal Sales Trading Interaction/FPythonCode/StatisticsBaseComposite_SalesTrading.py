import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object, CalcVal, Str

AS_GET_METHOD = 'VAL_IF_CALL_IS_GET_METHOD'


class StatisticsBaseComposite(CompositeAttributeDefinition):
    def CommonBaseAttributes(self):
        attributes = {}
            
        ''' Top Section '''
        attributes.update({
            
            'accepted':                CalcVal(        label='Accepted',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':IsTraded',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),
                                                        
            'total':                   CalcVal(        label='Total',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':CustomerRequestCounter',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),
                                                        
            'hitRate':                 Str(            label='Hit Rate',
                                                        objMapping=self.UniqueCallback('HitRate'),
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),

            'minMargin':               CalcVal(        label='Min Margin',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':MinSalesMargin',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),

            'avgMargin':               CalcVal(        label='Avg Margin',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':AvgSalesMargin',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),

            'avgMarginAsList':         CalcVal(        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':SalesMarginAsList',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),

            
            'maxMargin':               CalcVal(        label='Max Margin',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':MaxSalesMargin',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=12,
                                                        maxWidth=12),

            'mostFreq':                CalcVal(        label='Most Freq',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':FrequentlyTraded',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=30),
            
            'lastTraded':              CalcVal(        label='Last Traded',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':RecentlyTraded',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=30),
        })
        return attributes
        
    def OnInit(self, clientMethodName, underlyingMethodName, showStatsMethodName):
        self._clientMethodName = clientMethodName
        self._underlyingMethodName = underlyingMethodName
        self._showStatsMethodName = showStatsMethodName
        self._subscriptionObject = None
        self._calcObject = None
        self._needToRefreshCalcSpace = False
        self._doubleFormatter = acm.GetDomain('double').DefaultFormatter()
        
    def Client(self):
        return self.GetMethod(self._clientMethodName)()
        
    def Underlying(self):
        return self.GetMethod(self._underlyingMethodName)()
        
    def ShowStats(self, *args):
        return self.GetMethod(self._showStatsMethodName)()
                
    '''********************************************************************
    * Obj Mapping
    ********************************************************************'''                    
    def HitRate(self, val = AS_GET_METHOD):
        ratio = ''
        if val == AS_GET_METHOD:
            try:
                if self.Client() and self.total:
                    hitRatio = self.accepted.Value() / float(self.total.Value()) * 100.0
                    ratio = self._doubleFormatter.Format(hitRatio)
            except:
                pass
        return ratio
            
    '''********************************************************************
    * Calculations
    ********************************************************************'''                    
    def CalcObject(self):
        return self._calcObject
        
    def CreateAndSetCalcObject(self):
        self._calcObject = self.CreateCalcObject()
      
    '''********************************************************************
    * On Changed
    ********************************************************************'''   
    def OnClientChanged(self):
        self.CreateAndSetCalcObject()
       
    def OnUnderlyingChanged(self):
        self.CreateAndSetCalcObject()
        
    def OnRefreshButton(self):
        self.CreateAndSetCalcObject()
 
    def ShowStatsChanged(self, show):
        if show:        
            self.CreateAndSetCalcObject()
        else:
            self._calcObject = None
        
    '''********************************************************************
    * Layout
    ********************************************************************'''                    
    def GetLayout(self):
        return self.UniqueLayout(
                    '''
                    hbox(;
                        vbox(;
                            accepted;
                            hitRate;
                            total;
                            );
                        vbox(;
                            minMargin;
                            avgMargin;
                            maxMargin;
                            );
                        vbox(;
                            mostFreq;
                            lastTraded;
                            lastCustomerRequest;
                            );
                        );
                    ''')

 

