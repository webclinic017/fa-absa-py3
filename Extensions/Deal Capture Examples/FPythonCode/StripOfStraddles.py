
import acm
from DealPackageDevKit import DealPackageDefinition, Date, DatePeriod, Str, Object, Float, DealPackageException, CalcVal, Delegate, Bool, Action, Settings, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand
import FUxCore

@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed'),
               novate = NovateCommand(nominal='nominal'),
               close = CloseCommand(nominal='nominal'),
               mirror = MirrorCommand(statusAttr='status', newStatus='Simulated') )
@Settings(GraphApplicable=False,
          MultiTradingEnabled=True)
class StripOfStraddlesDefinition(DealPackageDefinition):
    '''******************************************************************************************
    * Attribute Declarations
    ******************************************************************************************'''   
    ''' Strip Dates '''
    
    ipName   =          Object(     label='Name',
                                    objMapping='InstrumentPackage.Name') 
    
    
    startDate =         Date(       defaultValue='1m',
                                    label="Start Date",
                                    toolTip="The first straddles fx option expiry",
                                    validate="@ValidateStartDateSpan",
                                    transform="@TransformPeriodToDate")
                                    
    endDate =           Date(       defaultValue='3m',
                                    label="End Date",
                                    toolTip="The last straddles fx option expiry",
                                    validate="@ValidateEndDateSpan",
                                    transform="@TransformPeriodToDate")
                                    
    rolling =           DatePeriod( defaultValue='2m',
                                    objMapping="DealPackage.StripDatePeriod",
                                    toolTip="The rolling frequency of the Straddles", 
                                    label="Rolling")
                                    
    regenerate =        Action(     label='Regenerate',
                                    action="@RegenerateStrip")
    
    ''' Attributes delegated to child deal packages (The Straddle Attribute expiry should not be part of this list '''
    currency1 =         Delegate(   attributeMapping="LiveOrOpeningDealPackages.currency1")
    currency2 =         Delegate(   attributeMapping="LiveOrOpeningDealPackages.currency2")
    strike =            Delegate(   attributeMapping="LiveOrOpeningDealPackages.strike")
    nominal =           Delegate(   attributeMapping="LiveOrOpeningDealPackages.nominal")
    counterparty =      Delegate(   attributeMapping="LiveOrOpeningDealPackages.counterparty")
    portfolio =         Delegate(   attributeMapping="LiveOrOpeningDealPackages.portfolio")
    acquirer =          Delegate(   attributeMapping="LiveOrOpeningDealPackages.acquirer")
    tradeTime =         Delegate(   attributeMapping="LiveOrOpeningDealPackages.tradeTime")
    status =            Delegate(   attributeMapping="LiveOrOpeningDealPackages.status")
    setPrices =         Delegate(   attributeMapping="LiveOrOpeningDealPackages.setPrices")
    
    '''******************************************************************************************
    * Attribute based Changed/Default/Transform/Validate Callbacks 
    ******************************************************************************************'''   
    def TransformPeriodToDate(self, attributeName, dateOrPeriod):
        date = dateOrPeriod
        if acm.Time().PeriodSymbolToDate(dateOrPeriod):
            date = self.FirstCallFxo().FxoExpiryDateFromPeriod(dateOrPeriod)
        return date
        
    def ValidateStartDateSpan(self, attributeName, value):
        if not acm.Time().PeriodSymbolToDate(self.endDate):
            if acm.Time().DateDifference(value, self.endDate) > 0:
                raise DealPackageException('Start Date must be prior to End Date.')
        
    def ValidateEndDateSpan(self, attributeName, value):
        if not acm.Time().PeriodSymbolToDate(self.startDate):
            if acm.Time().DateDifference(self.startDate, value) > 0:
                raise DealPackageException('Start Date must be prior to End Date.')
        
    '''******************************************************************************************
    * Convenience Functions
    ******************************************************************************************'''  
    def FirstCallFxo(self):
        return self.ChildDealPackageAt("straddle_1").InstrumentAt("Call")
    
    def AddStraddleParts(self):
        count = 1
        for date in self.GetStripDates():
            linkName = 'straddle_' + str(count)
            straddlePart = acm.DealPackage().NewAsDecorator('Straddle')
            straddlePart.SetAttribute("expiry", date)
            straddlePart.GetAttribute("setPrices")()
            self.DealPackage().AddChildDealPackage(straddlePart, linkName)
            count = count + 1
            
    def RegenerateStrip(self, *args):
        self.DealPackage().RemoveAllChildDealPackages(False)
        insPackage = self.DealPackage().InstrumentPackage()
        for child in insPackage.ChildInstrumentPackages():
            insPackage.RemoveChildInstrumentPackage(child)
        
        self.AddStraddleParts()
        self._DelegateAttributeMappingValuesToChildren()
        
    def GetStripDates(self):
        cal = acm.FArray()
        cal.Add(self.currency1.Calendar())
        cal.Add(self.currency2.Calendar())
        return acm.DealCapturing().GenerateStripOfOptionDates(self.startDate, self.endDate, self.rolling, self.endDate, "Mod. Following", cal, True)
        
    '''******************************************************************************************
    * Deal Package Function Overrides 
    ******************************************************************************************'''
    def OnOpen(self):
        def dateSort(date1, date2):
            return acm.Time().DateDifference(date1, date2)

        dates = []
        for dpChild in self.DealPackage().OpeningDealPackages():
            dates.append(dpChild.GetAttribute("expiry"))
        if len(dates) > 0:
            dates.sort(dateSort)
            self.startDate = dates[0]
            self.endDate = dates[-1]
        
    def AssemblePackage(self):
        self.DealPackage().AddNewChildDealPackage("Straddle", "straddle_1") # We need a straddle to start off with
        
    def CustomPanes(self):
        return [ {'General' : '''ipName;
                                   hbox(;
                                     vbox[Strip Dates;
                                       startDate;
                                       endDate;
                                       rolling;
                                       hbox(;
                                          setPrices;
                                          regenerate;
                                       );
                                       );
                                   vbox[Straddle;
                                       currency1;
                                       currency2;
                                       strike;
                                       nominal;
                                     );
                                   );
                                   vbox[Trades;
                                       counterparty;
                                       portfolio;
                                       acquirer;
                                       tradeTime;
                                       status;
                                   );'''}]
    
    def LeadTrade(self):
        candidate = None
        for key in self.DealPackage().ChildDealPackageKeys().Sort():
            if key.startswith('straddle_'):
                candidate = key
        return self.DealPackage().ChildDealPackageAt(candidate).TradeAt("Call")
    
    def LiveOrOpeningDealPackages(self):
        allOpening = self.OpeningDealPackages()
        livePackages = allOpening.Filter(self.HasLiveTrades)
        if livePackages:
            return livePackages
        return allOpening
    
    def IsLiveTrade(self, trade):
        return not trade.Instrument().IsExpired()
    
    def HasLiveTrades(self, dp):
        return dp.AllTrades().Filter(self.IsLiveTrade).Size() > 0
    
    @classmethod
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import  AddInfoSetUp, CustomMethodSetUp
        definitionSetUp.AddSetupItems(
                            AddInfoSetUp( recordType='DealPackage',
                                          fieldName='StripRollingFreq',
                                          dataType='String',
                                          description='Strip Rolling Period',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue='2m',
                                          mandatory=False),
                                          
                            CustomMethodSetUp( className='FDealPackage',
                                               customMethodName='SetStripDatePeriod',
                                               methodName='StripDatePeriod'),
                            
                            CustomMethodSetUp( className='FDealPackage',
                                               customMethodName='GetStripDatePeriod',
                                               methodName='StripDatePeriod')
                            )
                               

def StartStripOfStraddlesApplication(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'StripOfStraddles') 
    



'''******************************************************************************************
* Deal Package Function Overrides 
******************************************************************************************'''
def GetStripDatePeriod(dealPackage):
    try:
        datePeriod = dealPackage.AdditionalInfo().StripRollingFreq()
        if not datePeriod:
            datePeriod = "2m"
        return datePeriod
    except:
        raise DealPackageException("Missing Additional Info StripRollingFreq")
    
def SetStripDatePeriod(dealPackage, period):
    try:
        dealPackage.AdditionalInfo().StripRollingFreq(period)
    except:
        raise DealPackageException("Missing Additional Info StripRollingFreq")
    
