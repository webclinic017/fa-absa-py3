import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object, CalcVal, Str
import StiwUtils
from StiwCustomization import Filters
from StatisticsBaseComposite_SalesTrading import StatisticsBaseComposite


class OrderStatistics(StatisticsBaseComposite):
    def Attributes(self):
        attributes = self.CommonBaseAttributes()
            
        attributes.update({
            
            'lastCustomerRequest':     CalcVal(        label='Last Order',
                                                        calcMapping=self.UniqueCallback('CalcObject') + ':FOrderSheet:RecentlyOrder',
                                                        valuationDetails=False,
                                                        visible=self.UniqueCallback('@ShowStats'),
                                                        width=30),


        })

        return attributes

    def SheetType(self):
        return 'FOrderSheet'
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self._needsRefresh = True

    def Unsubscribe(self):
        if self._subscriptionObject:
            self._subscriptionObject.RemoveDependent(self)
        
    def Subscribe(self, orders):
        if self._subscriptionObject:
            self._subscriptionObject.RemoveDependent(self)
        if orders:
            self._subscriptionObject = orders
            self._subscriptionObject.AddDependent(self)
        
    def GetOrderFilter(self, client, underlying):
        return Filters.OrderSheet(client, underlying)
         
    def GetOrders(self, orderFilter):
        orders = acm.Trading().GetOrders(orderFilter)
        self.Subscribe(orders)
        return orders

    def CreateTreeSpec(self, orders):
        treeSpec = acm.FTreeSpecification()
        treeSpec.OriginObject(orders)
        treeSpec.GroupingSubjectClass(acm.FOrderGrouperSubject)
        return treeSpec
        
    def CreateCalcObject(self):
        client = self.Client()
        underlying = self.Underlying()
        orderFilter = self.GetOrderFilter(client, underlying)
        orders = self.GetOrders(orderFilter)
        return self.CreateTreeSpec(orders)

