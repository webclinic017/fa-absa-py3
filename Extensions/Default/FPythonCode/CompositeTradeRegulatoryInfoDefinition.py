import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, Object, Bool
from ChoicesExprRegInfo import clearingBrokers, clearingHouses, middlewares, originalCounterparties, repositories
from CompositeAttributes import MultiEnum

class TradeRegulatoryInfoDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, tradeRegInfo, **kwargs):
        self._tradeRegInfo = tradeRegInfo
        self._ourCls = None
        self._theirCls = None
        
    def Attributes(self):
        return { 
                 'clearingHouse': Object( label='Clr House',
                                                          objMapping=self._tradeRegInfo+'.ClearingHouse',
                                                          choiceListSource =  clearingHouses() ),              
                 'clearingBroker': Object( label='Clr Broker',
                                                          objMapping=self._tradeRegInfo+'.ClearingBroker',
                                                          choiceListSource =  clearingBrokers() ),
                 'middleware': Object( label='Middleware',
                                                          objMapping=self._tradeRegInfo+'.Middleware',
                                                          choiceListSource =  middlewares() ),              
                 'repository': Object( label='Repository',
                                                          objMapping=self._tradeRegInfo+'.Repository',
                                                          choiceListSource =  repositories() ),              
                 'originalCounterparty': Object( label='Original Cpty',
                                                          objMapping=self._tradeRegInfo+'.OriginalCounterparty',
                                                          choiceListSource =  originalCounterparties() ), 
                 'branchMembership': Object( label='Branch Mbr',
                                                          objMapping=self._tradeRegInfo+'.BranchMembership',
                                                          choiceListSource =  originalCounterparties() ), 
                 'tradingCapacity': Object( label='Capacity',
                                                          objMapping=self._tradeRegInfo+'.TradingCapacity'), 
                 'confirmationTime': Object( label='Confirmation',
                                                          objMapping=self._tradeRegInfo+'.ConfirmationTime'), 
                 'clearingTime': Object( label='Clearing',
                                                          objMapping=self._tradeRegInfo+'.ClearingTime'), 
                 'tradeTimeWithTimePrecision': Object( label='Trade Time',
                                                          editable=False,
                                                          formatter='HighResolutionDateTime',
                                                          objMapping=self._tradeRegInfo+'.TradeTimeWithTimePrecision'),
                 'reportDeferToTime': Object( label='Report Defer',
                                                          objMapping=self._tradeRegInfo+'.ReportDeferToTime'),
                 'waiver': MultiEnum( label='Waiver',
                                                             objMapping=self._tradeRegInfo+'.WaiverString',
                                                             domain='enum(Waiver)'),
                 'otcPti': MultiEnum( label='OTC PTI',
                                                             objMapping=self._tradeRegInfo+'.OtcPostTradeIndicatorString',
                                                             domain='enum(OtcPostTradeIndicator)'),
                 'isHedge': Object( label='Hedge',
                                                          visible=self.UniqueCallback('@IsHedgeVisible'),
                                                          objMapping=self._tradeRegInfo+'.IsHedge' ),     
                 'directedOrder': Object( label='Directed Order',
                                                          objMapping=self._tradeRegInfo+'.DirectedOrder' ),
                 'ourOrganisation': Object( label='Organisation',
                                                          onChanged=self.UniqueCallback('@UpdateOurContacts'),
                                                          objMapping=self._tradeRegInfo+'.OurOrganisation' ),
                 'ourTrader': Object( label='Trader',
                                                          editable=False,
                                                          objMapping=self._tradeRegInfo+'.OurTrader' ),
                 'ourTransmittingOrganisation': Object( label='Transmit Org',
                                                          objMapping=self._tradeRegInfo+'.OurTransmittingOrganisation' ),
                 'ourInvestmentDecider': Object( label='Inv Decider',
                                                          choiceListSource=self.UniqueCallback('@OurContacts'),
                                                          enabled=self.UniqueCallback('@IsOurOrganisationSeleted'),
                                                          objMapping=self._tradeRegInfo+'.OurInvestmentDeciderName' ),
                 'theirOrganisation': Object( label='Organisation',
                                                          onChanged=self.UniqueCallback('@UpdateTheirContacts'),
                                                          objMapping=self._tradeRegInfo+'.TheirOrganisation' ),  
                 'theirTrader': Object( label='Trader',
                                                          choiceListSource=self.UniqueCallback('@TheirContacts'),
                                                          enabled=self.UniqueCallback('@IsTheirOrganisationSeleted'),
                                                          objMapping=self._tradeRegInfo+'.TheirTraderName' ),
                 'theirInvestmentDecider': Object( label='Inv Decider',
                                                          choiceListSource=self.UniqueCallback('@TheirContacts'),
                                                          enabled=self.UniqueCallback('@IsTheirOrganisationSeleted'),
                                                          objMapping=self._tradeRegInfo+'.TheirInvestmentDeciderName' ),
                 
               }
               
    # Label callbacks

    # ChoiceListSource callbacks
    def OurContacts(self, attrName):
        if self._ourCls is None:
            self.UpdateOurContacts()
        return self._ourCls
    
    def TheirContacts(self, attrName):
        if self._theirCls is None:
            self.UpdateTheirContacts()
        return self._theirCls
    
    def UpdateOurContacts(self, *args):
        self._ourCls = self._UpdateContacts(self._ourCls, self.ourOrganisation)
    
    def UpdateTheirContacts(self, *args):
        self._theirCls = self._UpdateContacts(self._theirCls, self.theirOrganisation)
    
    def _UpdateContacts(self, dpCls, org):
        if dpCls is None:
            dpCls = DealPackageChoiceListSource()
        dpCls.Clear()
        if org:
            dpCls.Add("")
            dpCls.AddAll( org.Contacts() )
        return dpCls
    
    # Visible callbacks
    
    def IsHedgeVisible(self, attrName):
        i = self.Trade().Instrument()
        return i.IsCommodityRelated()
    
    def IsOurOrganisationSeleted(self, attrName):
        return bool(self.ourOrganisation)
    
    def IsTheirOrganisationSeleted(self, attrName):
        return bool(self.theirOrganisation)
    
    # Util
    def RegulatoryInfo(self):
        return self.GetMethod(self._tradeRegInfo)()
        
    def Trade(self):
        return self.RegulatoryInfo().Trade()

    def GetLayout(self):
        return self.UniqueLayout(
                """
                vbox(;
                    hbox(;
                        vbox{;
                            clearingHouse;
                            clearingBroker;
                            middleware;
                            repository;
                            originalCounterparty;
                            branchMembership;
                        };
                        vbox(;
                            vbox{;
                                tradingCapacity;
                            };
                            vbox[Time;
                                confirmationTime;
                                clearingTime;
                                tradeTimeWithTimePrecision;
                                reportDeferToTime;
                            ];
                        );
                    );
                    vbox{;
                        hbox(;
                            otcPti;
                            waiver;
                        );
                        hbox(;
                            isHedge;
                            directedOrder;
                        );
                    };
                    hbox(;
                        vbox[Our Info;
                            ourOrganisation;
                            ourTrader;
                            ourTransmittingOrganisation;
                            ourInvestmentDecider;
                        ];
                        vbox[Their Info;
                            theirOrganisation;
                            theirTrader;
                            theirInvestmentDecider;
                        ];
                    );
                );
                """
        )
