import acm
from DealPackageDevKit import CompositeAttributeDefinition, Object
from CompositeSecuritiesDefinition import SecuritiesDefinition
from ChoicesExprInstrument import getIncompleteChoices, getExCouponMethods

class InstrumentPropertiesDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, instrument, **kwargs):
        self._instrument = instrument 
        
    def Attributes(self):
        return { 
                 'exCouponMethod'       : Object( label='Method',
                                                  objMapping=self._instrument+'.ExCouponMethod',
                                                  choiceListSource=getExCouponMethods()),
                 'exCouponPeriod'       : Object( label='Period',
                                                  objMapping=self._instrument+'.ExCouponPeriod',
                                                  enabled=self.UniqueCallback('@ExCouponPeriodEnabled')),
                 'expiryDateTimeProp'   : Object( label='Local Expiry',
                                                  objMapping=self._instrument+'.ExpiryDateTimeProp',
                                                  visible=self.UniqueCallback('@ExpiryDateTimePropVisible')),
                 'fixingSource'          : Object( label='Fixing Src',
                                                  objMapping=self._instrument+'.FixingSource', 
                                                  visible=self.UniqueCallback('@ResetNominalFixingVisible')),
                 'fundingGroup'         : Object( label='Funding Group',
                                                  objMapping=self._instrument+'.FundingGroup',
                                                  choiceListSource=acm.GetDomain("FChoiceList('Funding Group')").Instances()),
                 'incomplete'           : Object( label='Instr Status',
                                                  objMapping=self._instrument+'.Incomplete',
                                                  choiceListSource=getIncompleteChoices()),
                 'mtmFromFeed'          : Object( label='MTM From Feed',
                                                  objMapping=self._instrument+'.MtmFromFeed'),
                 'nDOffset'             : Object( label='ND Offset',
                                                  objMapping=self._instrument+'.NDOffset',
                                                  visible=self.UniqueCallback('@NDOffsetVisible')),
                 'originalCurrency'     : Object( label='Original Curr',
                                                  objMapping=self._instrument+'.OriginalCurrency',
                                                  visible='@IsShowModeInstrumentDetail'),
                 'payOffsetMethod'      : Object( label='Pay Offset Type',
                                                  objMapping=self._instrument+'.PayOffsetMethod',
                                                  choiceListSource=['Business Days', 'Calendar Days']),
                 'priceDiffLimitAbs'    : Object( label='Absolute',
                                                  objMapping=self._instrument+'.PriceDiffLimitAbs'),
                 'priceDiffLimitRel'    : Object( label='Relative',
                                                  objMapping=self._instrument+'.PriceDiffLimitRel'),
                 'priceFindingChlItem'  : Object( label='Price Finding',
                                                  objMapping=self._instrument+'.PriceFindingChlItem',
                                                  choiceListSource=acm.GetDomain("FChoiceList('PriceFindingGroup')").Instances()),
                 'realizeType'          : Object( label='Realize Type',
                                                  objMapping=self._instrument+'.RealizeType'),
                 'resetNominalFixingRule': Object(label='Res Nom Offset',
                                                  objMapping=self._instrument+'.ResetNominalFixingRule',
                                                  visible=self.UniqueCallback('@ResetNominalFixingVisible')),
                 'roundingSpecification': Object( label='Rounding',
                                                  objMapping=self._instrument+'.RoundingSpecification'),
                 'securities'           : SecuritiesDefinition( instrument="Instrument" ),
                 'settleCategoryChlItem': Object( label='Settle Category',
                                                  objMapping=self._instrument+'.SettleCategoryChlItem',
                                                  choiceListSource=acm.GetDomain("FChoiceList('Settle Category')").Instances()),
                 'settlementCalendar'   : Object( label='Settle Calendar',
                                                  objMapping=self._instrument+'.SettlementCalendar'),
                 'spotBankingDaysOffset': Object( label='Spot Days',
                                                  objMapping=self._instrument+'.SpotBankingDaysOffset')
               }
        
    # Enabled callbacks
    def ExCouponPeriodEnabled(self, attributeName):
        return self.Instrument().ExCouponMethod() != 'None'
        
    # Visible callbacks
    def ExpiryDateTimePropVisible(self, attributeName):
        return self.Instrument().IsVisible('ExpiryDateTimeProp', self.IsShowModeDetail())
        
    def ResetNominalFixingVisible(self, attributeName):
        return self.Instrument().ResetNominal()
    
    def NDOffsetVisible(self, attributeName):
        return self.Instrument().NonDeliverable()
        
    # Util
    def Instrument(self):
        return self.GetMethod(self._instrument)()
        
    def GetLayout(self):
        return self.UniqueLayout(
                    """
                    hbox(;
                        vbox{;
                            spotBankingDaysOffset;
                            payOffsetMethod;
                            priceFindingChlItem;
                            roundingSpecification;
                            fundingGroup;
                            realizeType;
                            mtmFromFeed;
                        };
                        vbox(;
                            vbox[Trade Price Diff Limit;
                                priceDiffLimitAbs;
                                priceDiffLimitRel;
                            ];
                            vbox{;
                                settleCategoryChlItem;
                                settlementCalendar;
                                incomplete;
                                originalCurrency;
                            };
                        );
                    );
                    """
                )
