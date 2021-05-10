
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, CompositeAttributeDefinition, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, ReturnDomainDecorator
from SP_DealPackageHelper import DatePeriodToDate, DatePeriodToDateTime, TradeTypeChoices
from CompositeComponentBase import CompositeBaseComponent
from CompositeAttributes import BuySell, PaymentsDialog
from functools import partial


# ### The trade input part is only a trade entry screen for 
# the product. It can represent one or several actual trades.
# The component TradeInput will always have a one to one mapping between
# product quantity and trade quantity.
# The component StructuredTradeInput can have a more complex quantity
# mapping, either fix or depending on other attributes.


class TradeInput(CompositeBaseComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    _quantityMapping = 'Trades.Quantity'
    _buySellLabels = ["B", "S", "-"]
    _buySellChoiceListWidth = 6

    def Attributes(self):

        self._valueDayMapping = self.UniqueCallback('DateTrade') + '.ValueDay'
        self._acquireDayMapping = self.UniqueCallback('DateTrade') + '.AcquireDay'
    
        return {    
        
                    'quantity'            : BuySell( objMapping = self._quantityMapping,
                                                     label = '',
                                                     buySellLabels = self._buySellLabels,
                                                     choiceListWidth=self._buySellChoiceListWidth ),

                    'status'              : Object ( objMapping = "Trades.Status",
                                                     label = 'Status',
                                                     choiceListSource = TradeStatusChoices() ),
                                                     
                    'portfolio'           : Object ( objMapping = "Trades.Portfolio",
                                                     label = 'Portfolio',
                                                     choiceListSource = PortfolioChoices() ),
                                                     
                    'counterparty'        : Object ( objMapping = "Trades.Counterparty",
                                                     label = 'Counterparty',
                                                     choiceListSource = CounterpartyChoices() ),
                                                     
                    'acquirer'            : Object ( objMapping = "Trades.Acquirer",
                                                     label = 'Acquirer',
                                                     choiceListSource = AcquirerChoices() ),
                    
                    'tradeTime'           : Object ( objMapping = "Trades.TradeTime",
                                                     label = 'Trade Time',
                                                     transform = self.UniqueCallback('@CalendarDayPeriodToDateTime') ),
                    
                    'valueDay'            : Object ( objMapping = self._valueDayMapping,
                                                     label = 'Value Day',
                                                     transform = self.UniqueCallback('@BankingDayPeriodToDateFromTradeTimePlusSpot'),
                                                     onChanged = self.UniqueCallback('@SetValueDays') ),
                    
                    'acquireDay'          : Object ( objMapping = self._acquireDayMapping,
                                                     label = 'Acquire Day',
                                                     transform = self.UniqueCallback('@CalendarDayPeriodToDate'),
                                                     onChanged = self.UniqueCallback('@SetAcquireDays') ),
                    
                    'tradeType'           : Object ( objMapping = 'Trades.Type',
                                                     label = 'Trade Type',
                                                     choiceListSource = TradeTypeChoices() ),
                    
                    'payments'            : PaymentsDialog( trade = 'LeadTrade' )
                    
                }

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
                {'quantity_value'   : dict(label = ''),
                 'quantity_buySell' : dict(label = 'Quantity')})


    def SetValueDays(self, *rest):
        for t in self.GetMethod('Trades')():
            if t.ValueDay() != self.valueDay:
                t.ValueDay(self.valueDay)
    
    def SetAcquireDays(self, *rest):
        for t in self.GetMethod('Trades')():
            if t.AcquireDay() != self.acquireDay:
                t.AcquireDay(self.acquireDay)

    def DateTrade(self):
        # By default, the Lead Trade will be used to determine
        # value day and aquire day. To override this behaviour the
        # deal package must implement method DateTrade.
        try:
            return self.GetMethod('DateTrade')()
        except AttributeError:
            leadTrade = self.GetMethod('LeadTrade')()
            if leadTrade is None:
                raise DealPackageException ( 'No LeadTrade method defined' )
            return leadTrade

    def OnInit(self, priceLayout = None, **kwargs):
        self._priceLayout = priceLayout
        
    def GetLayout(self):
        priceLayout = self.GetMethod(self._priceLayout)() if self._priceLayout else ''

        if priceLayout.find('payments') >= 0:
            addPayments = ''
        else:
            addPayments =    """
                                hbox{;
                                    fill;
                                    payments;
                                };
                            """

        baseLayout = self.UniqueLayout( """
                                        hbox(;
                                            vbox{;
                                                quantity;
                                                portfolio;
                                                counterparty;
                                                acquirer;
                                                };
                                            vbox{;
                                                tradeTime;
                                                valueDay;
                                                acquireDay;
                                                status;
                                                };
                                            );
                                            %s
                                            %s
                                """ % (priceLayout, addPayments) )
        return baseLayout

    # -----------------------------------------------
    # ##### Other class methods ###### #
    # -----------------------------------------------

    def CalendarDayPeriodToDate(self, attrName, newDate, *rest):
        return DatePeriodToDate(newDate)

    def CalendarDayPeriodToDateTime(self, attrName, newDate, *rest):
        return DatePeriodToDateTime(newDate)

    def BankingDayPeriodToDateFromTradeTimePlusSpot(self, attrName, newDate, *rest):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            leadTrade = self.GetMethod('LeadTrade')()
            if leadTrade:
                tradeDate = acm.Time.AsDate(self.tradeTime)
                tradeDatePlusSpot = leadTrade.Currency().Calendar().AdjustBankingDays(tradeDate, leadTrade.Instrument().SpotBankingDaysOffset())
                if acm.Time().DatePeriodUnit(newDate) == 'Days':
                    #if period is days it should add banking days
                    date = leadTrade.Currency().Calendar().AdjustBankingDays(tradeDatePlusSpot, acm.Time().DatePeriodCount(newDate))
                else:
                    # If period is not days, simply add the period and adjust to next banking day
                    date = acm.Time().DateTimeAdjustPeriod(tradeDatePlusSpot, newDate, leadTrade.Currency().Calendar(), 'Following')
        return date
        

class StructuredTradeInput(TradeInput):



    def Attributes(self):

        self._quantityMapping = 'DealPackage.AdditionalInfo.ProductQuantity|' + self.UniqueCallback('Quantity')

        return super(StructuredTradeInput, self).Attributes()

    # The method sent as "quantityMappingName" should be return a list of 
    # dictionaries. Each dictionary should have the keys 'trade' and 
    # "quantityFactor'. The quantity factor is the relationship
    # between the product quantity and the trade quantity.
    def OnInit(self, quantityMappingName, priceLayout = None, **kwargs):
        super(StructuredTradeInput, self).OnInit(priceLayout, **kwargs)
        self._quantityMappingName = quantityMappingName

    @ReturnDomainDecorator('double')
    def Quantity(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.GetMethod("DealPackage")().AdditionalInfo().ProductQuantity()
        else:
            for trade in self.TradeQuantityMapping():
                tradeForQuantity = self.GetMethod(trade['trade'])()
                quantityFactor = trade['quantityFactor']()
                tradeForQuantity.Quantity( quantityFactor * float(value) )

    def TradeQuantityMapping(self):
        return self.GetMethod(self._quantityMappingName)()

    def SetUp(self, definitionsSetUp):
        from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp
        definitionsSetUp.AddSetupItems(
                                    AddInfoSetUp(
                                        recordType      = 'DealPackage',
                                        fieldName       = 'ProductQuantity',
                                        dataType        = 'Double',
                                        description     = 'Trade quantity of structured product',
                                        dataTypeGroup   = 'Standard',
                                        subTypes        = [],
                                        defaultValue    = 1.0,
                                        mandatory       = False
                                        ))

    def IsValid(self, exceptionAccumulator, aspect):
        
        if aspect == 'DealPackage':
        
            # Verify that the trade quantaties are not updated in an incorrect way
            
            for tradeData in self.TradeQuantityMapping():
                trade = self.GetMethod(tradeData['trade'])()
                diff = abs(trade.Quantity() - (tradeData['quantityFactor']() * self.quantity_value))
                if diff > 1e-5:
                    exceptionAccumulator('Trade %i must have trade quantity %f'
                                                    % ( trade.OriginalOrSelf().Oid(),
                                                        tradeData['quantityFactor']() * self.quantity_value ) )


class TradeB2B(CompositeBaseComponent):

    def Attributes(self):

        return {    


            'b2bEnabled'      : Object( label=self.UniqueCallback('@B2BLabel'),
                                        objMapping = self._b2bTradeParamsName+'.SalesCoverEnabled' ),

            'b2bMargin'       : Object( label='Margin',
                                        objMapping = self._b2bTradeParamsName+'.SalesMargin',
                                        formatter='FullPrecision',
                                        enabled=self.UniqueCallback('@IsB2B') ),
                                    
            'b2bPrice'        : Object( label='Trader Price',
                                        objMapping = self._b2bTradeParamsName+'.TraderPrice',
                                        formatter='FullPrecision',
                                        enabled=self.UniqueCallback('@IsB2B') ),
                                    
            'b2bPrf'          : Object( label='Trader Portfolio',
                                        objMapping = self._b2bTradeParamsName+'.TraderPortfolio',
                                        choiceListSource=PortfolioChoices(),
                                        enabled=self.UniqueCallback('@IsB2B') ),
                     
            'b2bAcq'          : Object( label='Trader Acquirer',
                                        objMapping = self._b2bTradeParamsName+'.TraderAcquirer',
                                        choiceListSource=AcquirerChoices(),
                                        enabled=self.UniqueCallback('@IsB2B') )
        }
        
        
    def B2BLabel(self, attrName):
        return 'B2B Cover ' + self._uiLabel

    def OnInit(self, uiLabel, b2bTradeParamsName, priceLayout = None, **kwargs):
        self._uiLabel = uiLabel
        self._b2bTradeParamsName = b2bTradeParamsName

    def IsB2B(self, attrName):
        return self.b2bEnabled

    def GetLayout(self):
        
        return self.UniqueLayout( """
                                        vbox[;
                                            b2bEnabled;
                                            hbox{;
                                                vbox(;
                                                    b2bPrice;
                                                    b2bMargin;
                                                    );
                                                vbox(;
                                                    b2bPrf;
                                                    b2bAcq;
                                                    );
                                                );
                                            ];
                                        """)
