import acm
from DealPackageDevKit import DealPackageDefinition, Object, CounterpartyChoices, Bool, Action, Str, Int, Settings
from QuoteRequestStatistics_SalesTrading import QuoteRequestStatistics
from OrderStatistics_SalesTrading import OrderStatistics
from StiwCustomization import Filters

AS_GET_METHOD = 'VAL_IF_CALL_IS_GET_METHOD'


@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class ClientStatistics(DealPackageDefinition):
    
    
    client =                    Object(                 label='Client',
                                                        domain='FParty',
                                                        choiceListSource=CounterpartyChoices(),
                                                        onChanged='@OnClientChanged',
                                                        recreateCalcSpaceOnChange=True,
                                                        width=26,
                                                        maxWidth=26)

    underlying =                Object(                 label='Underlying',
                                                        domain='FInstrument',
                                                        choiceListSource='@UnderlyingChoices',
                                                        onChanged='@OnUnderlyingChanged',
                                                        recreateCalcSpaceOnChange=True,
                                                        visible='@HasUnderlyingChoices',
                                                        editable='@AllowChangedWhenClientSelected',
                                                        width=26,
                                                        maxWidth=26)
                                                        
    showQuoteRequestStats =     Bool(                   label='Quote Requests',
                                                        defaultValue=True,
                                                        onChanged='@OnShowQuoteRequestStatsChanged',
                                                        editable='@AllowChangedWhenClientSelected',
                                                        width=18,
                                                        maxWidth=18)
    
    showOrderStats =            Bool(                   label='Orders',
                                                        defaultValue=True,
                                                        onChanged='@OnShowOrderStatsChanged',
                                                        editable='@AllowChangedWhenClientSelected',
                                                        width=18,
                                                        maxWidth=18)
                                                        
    accepted =                  Str(                    label='Accepted',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)
                                                        
    hitRate =                   Str(                    label='Hit Rate',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)
                                                        
    total =                     Str(                    label='Total',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)
    
    minMargin =                 Str(                    label='Min Margin',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)
                                                        
    averageMargin =             Str(                    label='Avg Margin',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)
                                                        
    maxMargin =                 Str(                    label='Max Margin',
                                                        visible='@ShowStatsSection',
                                                        width=12,
                                                        maxWidth=12)  
                                                                
    orderStats =                OrderStatistics(        clientMethodName='Client',
                                                        underlyingMethodName='Underlying',
                                                        showStatsMethodName='ShowOrderStats')
    
    quoteRequestStats =         QuoteRequestStatistics( clientMethodName='Client',
                                                        underlyingMethodName='Underlying',
                                                        showStatsMethodName='ShowQuoteRequestStats')

    refresh =                   Action(                 label='Refresh',
                                                        action='@OnRefreshButton',
                                                        editable='@AllowChangedWhenClientSelected')
                                                        
    closeDialog =               Action(                 label='Close',
                                                        action='@OnCloseDialog')

    '''********************************************************************
    * Publics
    ********************************************************************'''                    
    def OnInit(self, *args):
        self._doubleFormatter = f = acm.GetDomain('double').DefaultFormatter()
        self._intFormatter = f = acm.GetDomain('int').DefaultFormatter()
        self._underlyingChoices = Filters.Underlyings()
        
    def OnDismantle(self):
        pass
        
    def Refresh(self, *args):
        self.UpdateSummaryStatistics()

    '''********************************************************************
    * Update Summary
    ********************************************************************'''                                        
    def UpdateSummaryStatistics(self):
        if self.ShowStatsSection():
            self.HitRateCalculation()
            self.AcceptedCalculation()
            self.TotalCalculation()
            self.MinMarginCalculation()
            self.AvgMarginCalculation()
            self.MaxMarginCalculation()
            self.quoteRequestStats
            self.orderStats
            
    '''********************************************************************
    * Objects
    ********************************************************************'''                                
    def Client(self):
        return self.client
        
    def Underlying(self):
        return self.underlying
        
    def ShowQuoteRequestStats(self):
        return self.showQuoteRequestStats
        
    def ShowOrderStats(self):
        return self.showOrderStats
        
    '''********************************************************************
    * Calc Utils
    *******************************************************************'''
    def IsValidValue(self, val):
        return val is not None
        
    def MinOf(self, val1, val2):
        minVal = 0
        if self.IsValidValue(val1) and self.IsValidValue(val2):
            minVal = val1 if val1 < val2 else val2
        elif self.IsValidValue(val1) or self.IsValidValue(val2):
            minVal = val1 if val1 else val2
        return minVal
        
    def MaxOf(self, val1, val2):
        maxVal = 0
        if self.IsValidValue(val1) and self.IsValidValue(val2):
            maxVal = val1 if val1 > val2 else val2
        elif self.IsValidValue(val1) or self.IsValidValue(val2):
            maxVal = val1 if val1 else val2
        return maxVal
        
    def Sum(self, val1, val2):
        sum = 0
        if self.IsValidValue(val1) and self.IsValidValue(val2):
            sum = val1 + val2
        elif self.IsValidValue(val1) or self.IsValidValue(val2):
            sum = val1 if val1 else val2
        return sum
            
    '''********************************************************************
    * Editable
    ********************************************************************'''
    def AllowChangedWhenClientSelected(self, *args):
        return self.client is not None
        
    '''********************************************************************
    * Choices
    ********************************************************************'''
    def UnderlyingChoices(self, *args):
        return self._underlyingChoices
    
    '''********************************************************************
    * Visible
    ********************************************************************'''
    def ShowStatsSection(self, *args):
        return self.showQuoteRequestStats and self.showOrderStats
                     
    def HasUnderlyingChoices(self, *args):
        return self._underlyingChoices is not None
        
    '''********************************************************************
    * Calculations
    ********************************************************************'''    
    def ValidateCalculatedValue(self, qrCalcVal, orderCalcVal):
        hasCalculation = False
        if self.client:
            try:
                hasCalculation = (qrCalcVal and qrCalcVal.Value() is not None) or (orderCalcVal and orderCalcVal.Value() is not None)
            except:
                hasCalculation = False
        return hasCalculation
        
    def AcceptedCalculation(self):
        try:
            accepted = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.accepted, self.orderStats.accepted):
                sum = self.Sum(self.quoteRequestStats.accepted.Value(), self.orderStats.accepted.Value())
                accepted = self._intFormatter.Format(sum)
            self.SetAttribute('accepted', accepted)
        except:
            pass
                
    def HitRateCalculation(self):
        try:
            ratio = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.total, self.orderStats.total):
                hitRatio = self._doubleFormatter.Parse(self.accepted) / float(self._doubleFormatter.Parse(self.total)) * 100.0
                ratio = self._doubleFormatter.Format(hitRatio)
            self.SetAttribute('hitRate', ratio)
        except Exception as e:
            pass
            
    def TotalCalculation(self):
        try:
            total = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.total, self.orderStats.total):
                sum = self.Sum(self.quoteRequestStats.total.Value(), self.orderStats.total.Value())
                total = self._intFormatter.Format(sum)
            self.SetAttribute('total', total)
        except:
            pass
      
    def MinMarginCalculation(self):
        try:
            minMagin = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.minMargin, self.orderStats.minMargin):
                min = self.MinOf(self.quoteRequestStats.minMargin.Value(), self.orderStats.minMargin.Value())
                minMagin = self._doubleFormatter.Format(min)
            self.SetAttribute('minMargin', minMagin)
        except:
            pass
        
    def AvgMarginCalculation(self):
        try:
            averageMargin = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.avgMarginAsList, self.orderStats.avgMarginAsList):
                quoteRequestMargins = self.quoteRequestStats.avgMarginAsList.Value()
                orderMargins = self.orderStats.avgMarginAsList.Value()
                totals = acm.FArray()
                if quoteRequestMargins:
                     totals.AddAll(quoteRequestMargins)
                if orderMargins:
                    totals.AddAll(orderMargins)
                averageMargin = self._doubleFormatter.Format(sum(totals)/len(totals))
            self.SetAttribute('averageMargin', averageMargin)
        except Exception as e:
            pass
        
    def MaxMarginCalculation(self):
        try:
            maxMargin = ''
            if self.ValidateCalculatedValue(self.quoteRequestStats.maxMargin, self.orderStats.maxMargin):
                max = self.MaxOf(self.quoteRequestStats.maxMargin.Value(), self.orderStats.maxMargin.Value())
                maxMargin = self._doubleFormatter.Format(max)
            self.SetAttribute('maxMargin', maxMargin)
        except:
            pass

    '''********************************************************************
    * On Changed
    ********************************************************************'''                    
    def OnClientChanged(self, *args):
        self.quoteRequestStats.OnClientChanged()
        self.orderStats.OnClientChanged()
        self.UpdateSummaryStatistics()
        
    def OnUnderlyingChanged(self, *args):
        self.quoteRequestStats.OnUnderlyingChanged()
        self.orderStats.OnUnderlyingChanged()
        self.UpdateSummaryStatistics()
    
    def OnShowOrderStatsChanged(self, attributeName, oldValue, newValue, *args):
        self.orderStats.ShowStatsChanged(newValue)
        
    def OnShowQuoteRequestStatsChanged(self, attributeName, oldValue, newValue, *args):
        self.quoteRequestStats.ShowStatsChanged(newValue)
        
    def OnRefreshButton(self, *args):
        self.quoteRequestStats.OnRefreshButton()
        self.orderStats.OnRefreshButton()
        
    def OnCloseDialog(self, *args):
        self.CloseDialog()        
        
    '''********************************************************************
    * Layout
    ********************************************************************'''                    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_ClientStatistics")
