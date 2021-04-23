from __future__ import print_function
import acm
from DealPackageDevKit import CompositeAttributeDefinition, Action, Object, Str, CounterpartyChoices, PortfolioChoices, AcquirerChoices, Float
from DealPackageUtil import IsIterable

class ValueNotSet():
    pass

class B2BCompositeAttribute(CompositeAttributeDefinition):
    def OnInit(self, b2bName):
        self._b2bName = b2bName
              
    def B2BAttributes(self):
        return {

                'b2bEnabled':          Object( defaultValue=False,
                                                label='B2B Cover',
                                                objMapping=self.B2B() + '.SalesCoverEnabled'),
                                                
                'b2bMargin':           Float(  defaultValue=0.0,
                                                label='Margin',
                                                objMapping=self.UniqueCallback('SalesMargin'),
                                                formatter='FullPrecision',
                                                visible=self.UniqueCallback('@IsB2BEnabled')),
                                        
                'b2bPrice':            Float(  defaultValue=0.0,
                                                label='Trader Price',
                                                objMapping=self.UniqueCallback('TraderPrice'),
                                                formatter='FullPrecision',
                                                visible=self.UniqueCallback('@IsB2BEnabled')),
                                        
                'b2bPrf':              Object( label='Trader Portfolio',
                                                objMapping=self.B2B() + '.TraderPortfolio',
                                                choiceListSource=PortfolioChoices(),
                                                visible=self.UniqueCallback('@IsB2BEnabled')),
                         
                'b2bAcq':              Object( label='Trader Acquirer',
                                                objMapping=self.B2B() + '.TraderAcquirer',
                                                choiceListSource=AcquirerChoices(),
                                                visible=self.UniqueCallback('@IsB2BEnabled')),
                
               }    
     
    '''*******************************************************
    * Override method
    *******************************************************'''                                
    def Attributes(self):
        return dict(self.B2BAttributes())
     
    '''*******************************************************
    * B2B get methods
    *******************************************************'''                                
    def B2B(self):
        return self._b2bName
    
    def IsB2BEnabled(self, attributeName):
        return self.b2bEnabled
    
    '''*******************************************************
    * B2B object mapping methods
    *******************************************************'''                                
    def GetB2BObjAsIterable(self):
        b2bObj = self.GetMethod(self.B2B())()
        if not IsIterable(b2bObj):
            b2bObj = [b2bObj]
        return b2bObj

        
    def TraderPrice(self, price = ValueNotSet()):
        try:
            b2bObj = self.GetB2BObjAsIterable()
            quantity = b2bObj[0].Trade().Quantity()
            for obj in b2bObj[1:]:
                if abs(obj.Trade().Quantity()) < quantity:
                   quantity = abs(obj.Trade().Quantity())

            if isinstance(price, ValueNotSet):
                return sum([obj.TraderPrice() * obj.Trade().Quantity() for obj in b2bObj]) / quantity if quantity else 0.0
            else:
                premiumSum = sum([obj.Trade().Price() * obj.Trade().Quantity() for obj in b2bObj])
                for obj in b2bObj:
                    obj.TraderPrice = price * (obj.Trade().Price() * obj.Trade().Quantity() / premiumSum if premiumSum else 1.0 / len(b2bObj)) * quantity / obj.Trade().Quantity()
        except Exception as e:
            print ('failure on traderprice', e)
            raise
            
    def SalesMargin(self, margin = ValueNotSet()):
        try:
            b2bObj = self.GetB2BObjAsIterable()
            quantity = min([abs(obj.Trade().Quantity()) for obj in b2bObj])

            if isinstance(margin, ValueNotSet):
                return sum([obj.SalesMargin() * abs(obj.Trade().Quantity()) for obj in b2bObj]) / quantity if quantity else 0.0
            else:
                premiumSum = sum([obj.Trade().Price() * abs(obj.Trade().Quantity()) for obj in b2bObj])
                for obj in b2bObj:
                    obj.SalesMargin = margin * (obj.Trade().Price() * abs(obj.Trade().Quantity()) / premiumSum if premiumSum else 1 / len(b2bObj)) * quantity / abs(obj.Trade().Quantity())
        except Exception as e:
            print ('failure on SalesMargin', e)
            raise
        
    '''*******************************************************
    * Layout
    *******************************************************'''                                    
    def GetLayout(self):
        return self.UniqueLayout('''vbox[B2B Cover;
                                        b2bEnabled;
                                        b2bMargin;
                                        b2bPrice;
                                        b2bPrf;
                                        b2bAcq;                                          
                                      ];
                                 ''')
