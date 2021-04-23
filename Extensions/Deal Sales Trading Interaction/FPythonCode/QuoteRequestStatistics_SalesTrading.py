import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object, CalcVal, Str
import StiwUtils
from StiwCustomization import Filters
from StatisticsBaseComposite_SalesTrading import StatisticsBaseComposite


class QuoteRequestStatistics(StatisticsBaseComposite):
    def Attributes(self):
        attributes = self.CommonBaseAttributes()
            
        ''' Top Section '''
        attributes.update({
            
            'lastCustomerRequest':     CalcVal(        label=self.UniqueCallback('@LastCustomerRequestLabel'),
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':' + self.SheetType() + ':RecentlyRFQ',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=30),
        })
        return attributes
        
    def SheetType(self):
        return 'FQuoteRequestPriceSheet'
        
    def LastCustomerRequestLabel(self, *args):
        return 'Last QR'
        
    def RefreshQuoteRequestPriceSheet(self):
        try:
            if self._needToRefreshCalcSpace:
                dpCalc = self.Owner()._dealPackageCalculations
                if dpCalc:
                    calc = dpCalc.Calculation(self.PrefixedName('lastCustomerRequest'))
                    if calc and (calc._currentCalcObject == self._calcObject):
                        calcSpace = dpCalc.CalcSpace(self.SheetType()).Refresh()
        except:
            pass
            
    def CalcObject(self):
        self.RefreshQuoteRequestPriceSheet()
        return self._calcObject
        
    def AdvancedFilter(self, underlying):
        return Filters.QuoteRequestAdvancedFilter(underlying)
        
    def CreateCalcObject(self):
        self._needToRefreshCalcSpace = True
        client = self.Client()
        underlying = self.Underlying()
        filter = None
        try:
            if client:
                filter = acm.FQuoteRequestFilter()
                filter.MarketPlaces([StiwUtils.Market(),])
                filter.Client(client.Name())
                filter.FilterName(client.Name())
                filter.Latest(True)
                filter.AdvancedFilter(self.AdvancedFilter(underlying))
        except Exception as e:
            print ("Quote Request Query filter failed", str(e))
            filter = None
        return filter

    def Unsubscribe(self):
        pass
