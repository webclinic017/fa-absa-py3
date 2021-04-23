import acm
from DealPackageDevKit import CompositeAttributeDefinition
from DealPackageDevKit import Text
from RFQUtils import Direction, MethodDirection, Status, PriceAndMarginConversions, Amount
 
class RFQSummary(CompositeAttributeDefinition):

    def Attributes(self):
        attributes = {}
        
        ''' Summary'''
        attributes.update({

                'summary'               : Text( defaultValue='', 
                                                height=140, 
                                                maxHeight=140, 
                                                visible=self.UniqueCallback('@SummaryVisible'),
                                                editable=False)
        })
        
        return attributes
      
    def OnInit(self, **kwargs):
        self._qrData = kwargs['qrDataMethod']
        self._instrument = kwargs['instrumentMethod']
        self._imInterface = kwargs['imInterfaceMethod']
        self._dealPackage = kwargs['dealPackageMethod']
        self._trade = kwargs['tradeMethod']
        self._customAttributes = kwargs['customAttributesMethod']
        self._allInPriceFormatter = acm.FNumFormatter('VeryDetailedShowZeroHideNaN')
     
    def CustomAttributesAttr(self):
        return self.GetMethod(self._customAttributes)()

    def CustomAttributeMethod(self, methodName):
        customAttributes = self.CustomAttributesAttr()
        return getattr(customAttributes, methodName)

    def CreateSummaryText(self):
        try:
            return self.CustomAttributeMethod('SummaryText')(self.CreateSummaryDict())
        except Exception as e:
            print(('Create Summary Text failed', e))
            
    def CreateCopyProposalSummaryText(self, allInPrices):
        try:
            summaryDict = self.CreateSummaryDict()
            direction = self.QRData().Direction()
            if Direction.IsTwoWay(direction):
                allInPrice = self.FormatAllInPrice(allInPrices[Direction.bid]) + '/' + self.FormatAllInPrice(allInPrices[Direction.ask])
            else:
                allInPrice = self.FormatAllInPrice(allInPrices[direction])
            summaryDict.AtPut('allInPrice', allInPrice)
            return self.CustomAttributeMethod('CopyProposalText')(summaryDict)
        except Exception as e:
            print(('Create CopyProposal Summary Text failed', e))

    def FormatAllInPrice(self, allInPrice):
        return self._allInPriceFormatter.Format(allInPrice)
        
    def CreateSummaryDict(self):
        summaryDict = acm.FDictionary()
        summaryDict.AtPut('status', self.CustomerQuoteRequestStatus())
        summaryDict.AtPut('direction', self.Direction())
        summaryDict.AtPut('client', self.ClientName())
        summaryDict.AtPut('amount', self.Amount())
        summaryDict.AtPut('allInPrice', self.AllInPrice())
        summaryDict.AtPut('salesSpread', self.SalesSpread())
        summaryDict.AtPut('traderPrice', self.TraderPrice())
        summaryDict.AtPut('currency', self.Instrument().Currency().Name())
        return summaryDict        
        
    def Refresh(self):
        if self.SummaryVisible():
            if not self.summary:
                self.summary = self.CreateSummaryText()    
        else:
            self.summary = ''
            
    def Instrument(self):
        return self.GetMethod(self._instrument)()

    def Trade(self):
        return self.GetMethod(self._trade)()
        
    def RFQDealPackage(self):
        return self.GetMethod(self._dealPackage)()
        
    def QRData(self):
        return self.GetMethod(self._qrData)()
        
    def CustomerQuoteRequestStatus(self):
        return self.QRData().CustomerQuoteRequestStatus()
        
    def IsAskSide(self):
        return Direction.IsAsk(self.QRData().Direction())
        
    def IsTwoWay(self):
        return Direction.IsTwoWay(self.QRData().Direction())
        
    def IMInterface(self):
        return self.GetMethod(self._imInterface)()
    
    def TradingInterface(self):
        return self.IMInterface().TradingInterface()
    
    def RequestedNomInQuot(self):
        return self.QRData().RequestedNomInQuot()
        
    def ClientName(self):
        return self.QRData().ClientName()
        
    def TraderPrice(self, direction=None):
        if direction is None:
            direction = self.QRData().Direction()
        if Direction.IsTwoWay(direction):
            return self.TraderPrice(Direction.bid) + '/' + self.TraderPrice(Direction.ask)
        else:
            traderPrice = self.QRData().TraderPrice(direction)
            allInPrice = self.QRData().AllInPrice(direction)
            if not acm.Math().IsFinite(allInPrice):
                traderPrice = allInPrice
            return acm.FNumFormatter('VeryDetailedShowZeroHideNaN').Format(traderPrice)
    
    def AllInPrice(self, direction=None):
        if direction is None:
            direction = self.QRData().Direction()
        if Direction.IsTwoWay(direction):
            return self.AllInPrice(Direction.bid) + '/' + self.AllInPrice(Direction.ask)
        else:        
            allInPrice = self.QRData().AllInPrice(direction)
            return self.FormatAllInPrice(allInPrice)
        
    def SalesSpread(self, direction=None):
        if direction is None:
            direction = self.QRData().Direction()
        if Direction.IsTwoWay(direction):
            return self.SalesSpread(Direction.bid) + '/' + self.SalesSpread(Direction.ask)
        else:
            traderPrice = self.QRData().TraderPrice(direction)
            allInPrice = self.QRData().AllInPrice(direction)
            salesSpread = PriceAndMarginConversions.Spread(traderPrice, allInPrice, Direction.IsAsk(direction), self.TradingInterface(), self.Instrument()) 
            return acm.FNumFormatter('VeryDetailedShowZeroHideNaN').Format(salesSpread)

    def Amount(self):
        return Amount.TopAmountLabel(self.RequestedNomInQuot(), self.RFQDealPackage())
     
    def Direction(self):
        return Direction.Label(self.QRData().Direction(), self.Instrument()).title()
        
    def SummaryVisible(self, *args):
        status = self.QRData().QuoteRequestStatus()
        return status in [Status.passed, Status.rejected, Status.cancelled, Status.noAnswer, Status.expired, Status.accepted] and not self.UpdateOrWithdrawRequired()
        
    def UpdateOrWithdrawRequired(self):
        status = self.QRData().QuoteRequestStatus()
        customerStatus = self.QRData().CustomerQuoteRequestStatus()
        return status in [Status.rejected, Status.noAnswer, Status.cancelled] and customerStatus in [Status.pending, Status.subject, Status.subjAccept, Status.stream]

        
    '''********************************************************************
    * Layout
    ********************************************************************'''
    def GetLayout(self):
        return self.UniqueLayout(
                    '''
                    hbox(;
                        summary;
                    );
                    ''')
