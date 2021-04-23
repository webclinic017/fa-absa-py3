import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Label, Object, CalcVal, PortfolioChoices, CounterpartyChoices, AcquirerChoices, TradeStatusChoices, ReturnDomainDecorator, DealPackageUserException
from CompositeAttributes import PaymentsDialog, BuySell, OpenObject   
from CompositePremiumTranslationDefinition import PremiumTranslation                   

class TradeDefinition(CompositeAttributeDefinition):
    def OnInit(self, trade, showBuySell=True, included=None, excluded=None, buySellLabels=None, **kwargs):
        self._trade = trade
        self._showBuySell = showBuySell 
        self._included = included
        self._excluded = excluded
        self._buySellLabels = buySellLabels if buySellLabels else ["B", "S", "-"]
        self._mirrorPortfolioChoices = DealPackageChoiceListSource()
        self._collateralAgreementChoices = DealPackageChoiceListSource()
            
    def Attributes(self):
        attrDict = { 'acquireDay'              : Object( label='Acquire Day',
                                                         objMapping=self._trade+'.AcquireDay',
                                                         transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                         visible='@IsShowModeTradeDetail'),
                 'acquirer'                    : Object( label='Acquirer',
                                                         objMapping=self._trade+'.Acquirer',
                                                         choiceListSource = AcquirerChoices(),
                                                         onChanged=self.UniqueCallback('@UpdateCollateralAgreementChoices')),
                 'allInPrice'                  : Object( objMapping=self.UniqueCallback('AllInPrice')),
                 'boTrdnbr'                    : Object( label='BO No',
                                                         objMapping=self.UniqueCallback('BoTrdnbr')),
                 'broker'                      : Object( label='Broker',
                                                         objMapping=self._trade+'.Broker',
                                                         visible='@IsShowModeTradeDetail'),
                 'cashAmount'                  : BuySell(label='Cash Amount',
                                                         buySellLabels=["Deposit", "Loan", "-"],
                                                         choiceListWidth=10,
                                                         objMapping=self._trade+'.CashAmount',
                                                         showBuySell=self._showBuySell),
                 'fee'                         : Object( label='Broker Fee',
                                                         objMapping=self._trade+'.Fee',
                                                         formatter='InstrumentDefinitionNominal',
                                                         visible='@IsShowModeTradeDetail'),
                 'collateralAgreement'         : Object( label='Coll Agreem',
                                                         objMapping=self._trade+'.CollateralAgreement',
                                                         choiceListSource=self.UniqueCallback('@CollateralAgreementChoices'),
                                                         visible=self.UniqueCallback('@CollateralAgreementVisible')),
                 'counterparty'                : Object( label='Cpty',
                                                         objMapping=self._trade+'.Counterparty',
                                                         choiceListSource = CounterpartyChoices(),
                                                         onChanged=self.UniqueCallback('@UpdateMirrorPortfolioChoices|@UpdateCollateralAgreementChoices'),
                                                         width=22),
                 'currency'                    : Object( label='Currency',
                                                         objMapping=self._trade+'.Currency',
                                                         visible=self.UniqueCallback('@CurrencyVisible')),
                 'direction'                   : Object (label='Direction',
                                                         objMapping='Trade.Direction'),
                 'endCash'                     : Object (label='End Cash',
                                                         objMapping=self._trade+'.EndCash',
                                                         editable=False),
                 'endInterest'                 : Object (label='End Interest',
                                                         domain='float',
                                                         objMapping=self.UniqueCallback('EndInterest'),
                                                         editable=False),
                 'faceValue'                   : BuySell(label='Face Value',
                                                         buySellLabels=self._buySellLabels,
                                                         objMapping=self._trade+'.FaceValue',
                                                         showBuySell=self._showBuySell),
                 'flatAccrued'                 : Object( label='Flat Accrued',
                                                         objMapping=self._trade+'.FlatAccrued'),
                 'forwardPremium'              : Object( label='Fwd Premium',
                                                         objMapping=self._trade+'.ForwardPremium',
                                                         visible=self.UniqueCallback('@ForwardFieldsVisible')),
                 'forwardValueDate'            : Object( label='Fwd Day',
                                                         objMapping=self._trade+'.ForwardValueDate',
                                                         visible=self.UniqueCallback('@ForwardFieldsVisible')),
                                      
                 'market'                      : Object( label='Market',
                                                         objMapping=self._trade+'.Market',
                                                         visible='@IsShowModeTradeDetail'),
                 'mirrorPortfolio'             : Object( label='Cpty Portfolio',
                                                         objMapping=self._trade+'.MirrorPortfolio',
                                                         choiceListSource=self.UniqueCallback('@MirrorPortfolioChoices'),
                                                         visible=self.UniqueCallback('@MirrorPortfolioVisible')),
                 'nominal'                     : BuySell(label='Nominal',
                                                         buySellLabels=self._buySellLabels,
                                                         objMapping=self._trade+'.Nominal',
                                                         showBuySell=self._showBuySell),
                 'nominalInQuotation'          : BuySell(label='Nom in Quot',
                                                         buySellLabels=self._buySellLabels,
                                                         objMapping=self._trade+'.NominalInQuotation',
                                                         visible=self.UniqueCallback('@NominalInQuotationVisible'),
                                                         showBuySell=self._showBuySell),
                 'openNominal'                 : Object (label='Open Nom',
                                                         objMapping=self._trade+'.OpenNominal',
                                                         visible=self.UniqueCallback('@OpenNominalVisible'),
                                                         formatter='InstrumentDefinitionNominalShowZeroHideNaN',
                                                         editable=False),
                 'optKey1'                     : Object( label=self.OptKeyName('OptKey1'),
                                                         objMapping=self._trade+'.OptKey1',
                                                         choiceListSource=self.OptKeyInstances('OptKey1'),
                                                         visible='@IsShowModeTradeDetail'),
                 'optKey2'                     : Object( label=self.OptKeyName('OptKey2'),
                                                         objMapping=self._trade+'.OptKey2',
                                                         choiceListSource=self.OptKeyInstances('OptKey2'),
                                                         visible='@IsShowModeTradeDetail'),
                 'optKey3'                     : Object( label=self.OptKeyName('OptKey3'),
                                                         objMapping=self._trade+'.OptKey3',
                                                         choiceListSource=self.OptKeyInstances('OptKey3'),
                                                         visible='@IsShowModeTradeDetail'),
                 'optKey4'                     : Object( label=self.OptKeyName('OptKey4'),
                                                         objMapping=self._trade+'.OptKey4',
                                                         choiceListSource=self.OptKeyInstances('OptKey4'),
                                                         visible='@IsShowModeTradeDetail'),
                 'payments'                    : PaymentsDialog( trade=self._trade ),
                 'portfolio'                   : Object( label='Portfolio',
                                                         objMapping=self._trade+'.Portfolio',
                                                         choiceListSource = PortfolioChoices()),
                 'position'                    : Object( label='Position',
                                                         objMapping=self._trade+'.Position',
                                                         enabled=False),
                 'positionPair'                : Object( label='Position Pair',
                                                         objMapping=self._trade+'.PositionPair',
                                                         visible='@IsShowModeTradeDetail'),
                 'premium'                     : Object( label='Premium',
                                                         objMapping=self._trade+'.Premium',
                                                         formatter='InstrumentDefinitionPrice',
                                                         visible=self.UniqueCallback('@PremiumVisible')),
                 'premiumTranslation'          : PremiumTranslation( trade=self._trade,
                                                                     showMode='IsShowModeDetail2'),
                 'price'                       : Object( label='Price',
                                                         objMapping=self._trade+'.Price',
                                                         visible=self.UniqueCallback('@PriceVisible'),
                                                         formatter='InstrumentDefinitionPrice',
                                                         width=12),
                 'quantity'                    : BuySell(label='Quantity',
                                                         buySellLabels=self._buySellLabels,
                                                         objMapping=self._trade+'.Quantity',
                                                         formatter='AbsInstrumentDefinitionQuantity',
                                                         showBuySell=self._showBuySell),
                 'referencePrice'              : Object( label='Spot Price',
                                                         objMapping=self._trade+'.ReferencePrice'),
                 'settleCategoryChlItem'       : Object( label='Settle Cat',
                                                         objMapping=self._trade+'.SettleCategoryChlItem',
                                                         choiceListSource=acm.GetDomain("FChoiceList('TradeSettleCategory')").Instances(),
                                                         visible='@IsShowModeTradeDetail'),
                 'status'                      : Object( label='Status',
                                                         objMapping=self._trade+'.Status',
                                                         choiceListSource = TradeStatusChoices()),
                 'suggestDiscountingType'      : Action( label='Suggest',
                                                         sizeToFit=True,
                                                         action=self.UniqueCallback('@SuggestDiscountingType')),
                 'tradeCategory'               : Object( label='Category',
                                                         objMapping=self._trade+'.TradeCategory'),
                 'trader'                      : Object( label='Trader',
                                                         objMapping=self._trade+'.Trader'),
                 'trdnbr'                      : OpenObject( label='Trade No',
                                                             subjectId=self.UniqueCallback('LeadTrade') + '.Originator.Oid'),
                 'tradeTime'                   : Object( label='Trd Time',
                                                         objMapping=self._trade+'.TradeTime',
                                                         transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                         width=20),
                 'valueDay'                    : Object( label='Value Day',
                                                         objMapping=self._trade+'.ValueDay',
                                                         transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'vegaAmount'                  : Object( label='Vega Amount',
                                                         objMapping=self._trade+'.VegaAmount'),
                 'volatilityStrike'            : Object( label='Vol Strike',
                                                         objMapping=self._trade+'.VolatilityStrike'),                                       
                 'yourRef'                     : Object( label='Cpty Ref',
                                                         objMapping=self._trade+'.YourRef',
                                                         visible='@IsShowModeTradeDetail'),
                 'viceVersa'                   : Object( label='',
                                                         objMapping=self._trade+'.ViceVersa',
                                                         formatter='SixDecimalDetailedTruncateTrailingZeroShowZero',
                                                         width=8)
               }
               
        ''' Sales cover attributes '''
               
        attrDict.update({ 
                
                 'salesCoverEnabled'           : Object( label='B2B Cover',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.SalesCoverEnabled',
                                                         visible=self.UniqueCallback('@SalesCoverEnabledVisible')),
                 'salesMargin'                 : Object( label='Sales Spread',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.SalesMargin',
                                                         formatter='SixDecimalDetailedTruncateTrailingZero',
                                                         visible=self.UniqueCallback('@SalesCoverEnabledVisible'),
                                                         width=12),
                 'traderAcquirer'              : Object( label='Trader Acq',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.TraderAcquirer',
                                                         choiceListSource=AcquirerChoices(),
                                                         visible=self.UniqueCallback('@SalesCoverFieldsVisible')), 
                 'traderPortfolio'             : Object( label='Trader Prf',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.TraderPortfolio',
                                                         choiceListSource=PortfolioChoices(),
                                                         visible=self.UniqueCallback('@SalesCoverFieldsVisible')),    
                 'traderPrice'                 : Object( label='Trader Price',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.TraderPrice',
                                                         formatter='FullPrecision',
                                                         visible=self.UniqueCallback('@SalesCoverFieldsVisible')),
                 'salesCoverViceVersaPrice'    : Object( label='',
                                                         objMapping=self.UniqueCallback('B2BParams') + '.ViceVersaPrice',
                                                         formatter='SixDecimalDetailedTruncateTrailingZero',
                                                         visible=self.UniqueCallback('@SalesCoverFieldsVisible'))
                })
    
        if self._included:
            keys = attrDict.keys()
            self._excluded = [x for x in keys if x not in self._included]
        
        if self._excluded:
            for excluded in self._excluded:
                attrDict.pop(excluded, 'None')
                
        return attrDict
    
            
    # Object Mapping callbacks
    def EndInterest(self, *args):
        return self.Trade().EndCash() + self.Trade().CashAmount()
    
    @ReturnDomainDecorator('string')
    def BoTrdnbr(self, value = '*Reading*'):
        if value == '*Reading*':
            oid = self.LeadTrade().Originator().BoTrdnbr()
            return oid if oid > 0 else ''
    
    @ReturnDomainDecorator('double')
    def AllInPrice(self, value='*READING*'):
        if value != '*READING*':
            price = self.price
            margin = value - price
            shouldSubtractSpread = self.quantity_value > 0.0 # If we are buying from customer, customer price should be lower than trader price
            signCorrection = -1 if shouldSubtractSpread else 1
            self.SetAttribute('salesCoverEnabled', True)
            self.SetAttribute('salesMargin', signCorrection * margin)

    # Action callbacks
    def SuggestDiscountingType(self, *args):
        self.Trade().SuggestDiscountingType()
        
    # Visible callbacks
    def CollateralAgreementVisible(self, attributeName):
        return self.IsShowModeDetail2() or self._collateralAgreementChoices.Source().Size()
        
    def CurrencyVisible(self, attributeName):
        return self.IsShowModeDetail2() or self.Trade().Currency() != self.Trade().Instrument().Currency()
        
    def ForwardFieldsVisible(self, attributeName):    
        return self.Trade().Instrument().PayType() in ['Forward', 'Contingent']
            
    def MirrorPortfolioVisible(self, attributeName):
        counterparty = self.Trade().Counterparty()
        return self.IsShowModeDetail2() or self.Trade().MirrorPortfolio() or (counterparty and counterparty.OwnedPortfolios().Size())
        
    def NominalInQuotationVisible(self, attributeName):
        if self.Trade().Instrument().UnderlyingType() != 'Average Future/Forward':
            return (self.Trade().Instrument().IsBasedOnCommodity() and self.IsShowModeDetail2())
        
    def OpenNominalVisible(self, attributeName):
        visible = self.IsShowModeDetail2()
        if not self.Trade().IsInfant():
            original = self.Trade().Originator()
            opening = acm.FBusinessLogicDecorator.WrapObject(original.ContractTrade())
            if self.Trade().Instrument().InsType() == 'Deposit':
                if -opening.OpenNominal() != original.Nominal() and original.Status() not in ['Simulated', 'Reserved']:
                    visible = True
            else:
                if opening.OpenNominal() != original.Nominal() and original.Status() not in ['Simulated', 'Reserved']:
                    visible = True
        return visible

    def PremiumVisible(self, attributeName):
        return self.IsShowModeDetail2() or self.Trade().Premium()
    
    def PriceVisible(self, attributeName):
        return self.IsShowModeDetail2() or self.Trade().Price()
    
    def SalesCoverEnabledVisible(self, attributeName):
        if self.Trade().IsB2BSalesCover():
            return True
        elif self.Trade().IsSalesCoverChild():
            return False
        else:
            return self.IsShowModeDetail2()
            
    def SalesCoverFieldsVisible(self, attributeName):
        return self.Trade().IsB2BSalesCover()
        
        
    # Choices
    def MirrorPortfolioChoices(self, attributeName):
        if self._mirrorPortfolioChoices.IsEmpty():
            self.UpdateMirrorPortfolioChoices()
        return self._mirrorPortfolioChoices
        
    def CollateralAgreementChoices(self, attributeName):
        if self._collateralAgreementChoices.IsEmpty():
            self.UpdateCollateralAgreementChoices()
        return self._collateralAgreementChoices
        
    # Changed
    def UpdateMirrorPortfolioChoices(self, *args):
        self._mirrorPortfolioChoices.Clear()
        counterparty = self.LeadTrade().Counterparty()
        if counterparty:
            self._mirrorPortfolioChoices.AddAll(counterparty.OwnedPortfolios())
            
    def UpdateCollateralAgreementChoices(self, *args):
        self._collateralAgreementChoices.Clear()
        collateralAgreements = acm.Risk().CollateralAgreements(self.LeadTrade().Counterparty(), self.LeadTrade().Acquirer())
        self._collateralAgreementChoices.AddAll(collateralAgreements)
    
        
    # Transform
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    # Color callback    
    def QuantityColor(self, attributeName):
        return 'BkgTickerOwnBuyTrade' if self.quantity >= 0 else 'BkgTickerOwnSellTrade'
        
    # Util
    def Trade(self):
        return self.GetMethod(self._trade)()
    
    def LeadTrade(self):
        trade = self.Trade()
        if hasattr(trade, '__iter__'):
            trade = trade[0]
        return trade
            
    def B2BParams(self):
        return self.GetMethod('B2BTradeParamsAt')('Trade')
                
    def OptKeyName(self, key): 
        return acm.FTrade.GetMethod(key, 0).Domain().Name().Split('"')[1]
    
    def OptKeyInstances(self, key): 
        return acm.FTrade.GetMethod(key, 0).Domain().Instances()
        
    def GetLayout(self):
        return self.UniqueLayout(
                    """
                    hbox(;
                        vbox{;
                            nominal;
                            direction;
                            hbox(;
                                salesMargin;
                                salesCoverViceVersaPrice;
                            );
                            price;
                            premium;
                            currency;
                            portfolio;
                            settleCategoryChlItem;
                        };
                        vbox{;
                            counterparty;
                            mirrorPortfolio;
                            yourRef;
                            collateralAgreement;
                            valueDay;
                            acquireDay;
                            tradeTime;
                            acquirer;
                            trader;
                        };
                        );
                        hbox(;
                            vbox{;
                                salesCoverEnabled;
                                traderPortfolio;
                            };
                            vbox{;
                                traderPrice;
                                traderAcquirer; 
                            };
                        );
                    hbox(;
                        vbox{;
                            optKey1;
                            optKey2;
                        );
                        vbox{;
                            optKey3;
                            optKey4;
                        );
                    );
                    hbox(;
                        vbox{;
                            trdnbr;
                            status;
                        };
                        vbox{;
                            boTrdnbr;
                            payments;
                        };
                    );
                    """
                )
