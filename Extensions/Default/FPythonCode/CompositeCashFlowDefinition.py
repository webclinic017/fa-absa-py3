import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, List, ReturnDomainDecorator
from CompositeAttributes import AmortisingDialog
from DealPackageUtil import UnDecorate

COLUMNS = [ 'Cash Analysis Nominal', 
            'Cash Analysis Period Days',
            'Cash Analysis Forward Rate',
            'Cash Analysis Projected',
            'Portfolio Present Value' ]

class MoneyFlowHolder():
    def __init__(self, leg, trade):
        self._leg = leg
        self._trade = trade
        self._moneyFlows = acm.FArray()
        self._regenerate = True
        self.calcSpace = None
        
    def Leg(self):
        return self._leg
        
    def MoneyFlows(self):
        if self._regenerate:
            self._regenerate = False
            self.calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FMoneyFlowSheet' )
            self._moneyFlows.Clear()
            cashFlows = self.SortedCashFlows()
            for cashFlow in cashFlows:
                moneyFlow = acm.Risk.CreateMoneyFlowFromObject(cashFlow, self._trade)
                pair = acm.FPair()
                pair.First = moneyFlow
                self.AppendCalculations(moneyFlow, pair)
                self._moneyFlows.Add(pair)
            self._leg.AddDependent(self)
            self._leg.Instrument().AddDependent(self)
            self._trade.AddDependent(self)
        return self._moneyFlows
        
    def SortedCashFlows(self):
        def SortCashFlows(cf1, cf2):
            if cf1.PayDate() > cf2.PayDate():
                return 1
            elif cf1.PayDate() < cf2.PayDate():
                return -1
            if cf1.CashFlowType() > cf2.CashFlowType():
                return 1
            elif cf1.CashFlowType() < cf2.CashFlowType():
                return -1
            return 0
        
        comparator = acm.FBlockComparator(SortCashFlows)
        return self._leg.CashFlows().Sort(comparator)
        
    def Regenerate(self):
        return self._regenerate
    
    def AppendCalculations(self, moneyFlow, pair):
        for column in COLUMNS:
            calc = self.calcSpace.CreateCalculation(moneyFlow, column )
            newPair = acm.FPair()
            newPair.First = calc
            pair.Second = newPair
            pair = newPair
        
    def AppendCalculation(self, moneyFlow, columnId, pair):
        calc = self.calcSpace.CreateCalculation(moneyFlow, columnId )
        newPair = acm.FPair()
        newPair.First = calc
        pair.Second = newPair
        return newPair
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self._regenerate = True
        self._moneyFlows.Changed()
        
        
class CashFlowDefinition(CompositeAttributeDefinition):
    def OnInit(self, leg, trade, **kwargs):
        self._leg = leg 
        self._trade = trade
        self._moneyFlowHolder = None
        self._selectedCashFlow = acm.FCashFlow()
        self._selectedReset = acm.FReset()
        
    def Attributes(self):
        attr = { 'amortisation': AmortisingDialog( self._leg ),
                 'cashFlows': Object( label='Cash Flows',
                                                  objMapping=self.UniqueCallback('MoneyFlows'),
                                                  columns=self.UniqueCallback('@Columns'),
                                                  onSelectionChanged=self.UniqueCallback('@SetSelectedCashFlow'),
                                                  dialog=AttributeDialog( label='Update Cash Flow', 
                                                                          customPanes=self.UniqueCallback('@UpdateCashFlowDialogCustomPanes'))),
                 'editEndDate': Object( label='End Date',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.EndDate',
                                                  visible=self.UniqueCallback('@EditDatesVisible')),
                 'editFixedRate': Object( label='Rate',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.FixedRate',
                                                  visible=self.UniqueCallback('@EditFixedRateVisible'),
                                                  formatter='FullPrecision'),
                 'editFloatRateOffset': Object( label='Offset',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.FloatRateOffset',
                                                  visible=self.UniqueCallback('@EditFloatFieldsVisible'),
                                                  formatter='FullPrecision'),
                 'editFloatRateFactor': Object( label='Float Factor',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.FloatRateFactor',
                                                  visible=self.UniqueCallback('@EditFloatFieldsVisible'),
                                                  formatter='FullPrecision'),
                 'editNominalFactor': Object( label='Nominal Factor',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.NominalFactor',
                                                  visible=self.UniqueCallback('@EditNominalVisible'),
                                                  formatter='FullPrecision'),
                 'editPayDate': Object( label='Pay Date',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.PayDate',
                                                  transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'editSpread': Object( label='Spread',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.Spread',
                                                  visible=self.UniqueCallback('@EditFloatFieldsVisible'),
                                                  formatter='FullPrecision'),
                 'editStrike': Object( label='Strike',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.StrikePrice',
                                                  visible=self.UniqueCallback('@EditStrikeVisible'),
                                                  formatter='FullPrecision'),
                 'editStartDate': Object( label='Start Date',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.StartDate',
                                                  visible=self.UniqueCallback('@EditDatesVisible'),
                                                  transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'editResetDate': Object( label='Date',
                                                  objMapping=self.UniqueCallback('SelectedReset')+'.Day',
                                                  transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'editResetEndDate': Object( label='End',
                                                  objMapping=self.UniqueCallback('SelectedReset')+'.EndDate',
                                                  transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'editResetValue': Object( label='Value',
                                                  objMapping=self.UniqueCallback('SelectedReset')+'.FixFixingValue'),
                 'editResetStartDate': Object( label='Start',
                                                  objMapping=self.UniqueCallback('SelectedReset')+'.StartDate',
                                                  transform=self.UniqueCallback('@TransformPeriodToDate')),
                 'regenerate': Action( action=self.UniqueCallback('@Regenerate'),
                                                  noDealPackageRefreshOnChange=True),
                 'resets': Object( label='Resets',
                                                  objMapping=self.UniqueCallback('SelectedCashFlow')+'.Resets',
                                                  columns=[{'methodChain': 'ResetType',      'label': 'Type'}, 
                                                           {'methodChain': 'Day',            'label': 'Date'}, 
                                                           {'methodChain': 'FixFixingValue', 'label': 'Value', 'formatter' : 'DetailedHideNaN'}],
                                                  sortIndexCallback=self.UniqueCallback('@ResetSortingCallback'),
                                                  addNewItem =['Last', 'Sorted'],
                                                  visible=self.UniqueCallback('@ResetsVisible'),
                                                  onSelectionChanged=self.UniqueCallback('@SetSelectedReset'),
                                                  dialog=AttributeDialog( label='Update Reset', 
                                                                          customPanes=self.UniqueCallback('@UpdateResetDialogCustomPanes'))),
               }
        self.Owner().RegisterCallbackOnAttributeChanged(self.AttributeChanged, last=True)
        return attr
               
    # Visible callbacks
    def EditDatesVisible(self, attributeName):
        return self.SelectedCashFlow().CashFlowType() not in ['Fixed Amount', 'Aggregated Fixed Amount', 'Dividend', 'Redemption Amount', 'Interest Reinvestment']
    
    def EditFixedRateVisible(self, attributeName):
        return self.SelectedCashFlow().CashFlowType() not in ['Fixed Amount', 'Aggregated Fixed Amount', 'Aggregated Coupon', 'Dividend', 'Redemption Amount', 'Interest Reinvestment']
    
    def EditFloatFieldsVisible(self, attributeName):
        return self.SelectedCashFlow().CashFlowType() in ['Caplet', 'Floorlet', 'Digital Caplet', 'Digital Floorlet', 'Float Rate', 'Call Float Rate']
    
    def EditNominalVisible(self, attributeName):
        return self.SelectedCashFlow().CashFlowType() not in ['Redemption Amount']
    
    def EditStrikeVisible(self, attributeName):
        return self.SelectedCashFlow().CashFlowType() in ['Caplet', 'Floorlet', 'Digital Caplet', 'Digital Floorlet']
    
    def ResetsVisible(self, attributeName):
        return self.EditFloatFieldsVisible(attributeName) or self.SelectedCashFlow().CashFlowType() == "Total Return" or not self.SelectedCashFlow().Resets().IsEmpty()
    
    # OnSelectionChanged callbacks
    def SetSelectedCashFlow(self, attributeName, selectedPair):
        if selectedPair and selectedPair.First().CashFlow():
            self._selectedCashFlow = selectedPair and selectedPair.First().CashFlow()
        
    def SetSelectedReset(self, attributeName, selectedReset):
        if selectedReset:
            self._selectedReset = selectedReset
        
    # Transform
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    # Action
    def Regenerate(self, attributeName):
        pass # Just needed to trigger refresh of attributes

    # Sort
    def ResetSortingCallback(self, attrName, columnNbr, value1, formatter, obj):
        return str(acm.Time.DateDifference(obj.Day(), acm.Time.SmallDate())) + obj.ResetType()
        
    # Util
    def Leg(self):
        return self.GetMethod(self._leg)()
        
    def Trade(self):
        return self.GetMethod(self._trade)()
            
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if self._moneyFlowHolder and self._moneyFlowHolder.Regenerate() and self.regenerate:
            self.regenerate()
            
    def Columns(self,*args):
        columns=[{'methodChain': 'First.CashFlowType',                        'label': 'Type'},
                 {'methodChain': 'First.Currency',                            'label': 'Curr'}, 
                 {'methodChain': self.GetCalc('Cash Analysis Nominal'),       'label': 'Nominal'},
                 {'methodChain': 'First.StartDate',                           'label': 'Start Day'},
                 {'methodChain': self.GetCalc('Cash Analysis Period Days'),   'label': 'Days'},
                 {'methodChain': 'First.EndDate',                             'label': 'End Day'},
                 {'methodChain': 'First.PayDate',                             'label': 'Pay Day'},
                 {'methodChain': self.GetCalc('Cash Analysis Forward Rate'),  'label': 'Forw'},
                 {'methodChain': self.GetCalc('Cash Analysis Projected'),     'label': 'Proj'},
                 {'methodChain': self.GetCalc('Portfolio Present Value'),     'label': 'PV', 'formatter': 'Detailed'}]
        return columns
         
       
    @ReturnDomainDecorator('FArray(FPair)')
    def MoneyFlows(self):
        if not self._moneyFlowHolder or UnDecorate(self._moneyFlowHolder.Leg()) != UnDecorate(self.Leg()):
            self._moneyFlowHolder = MoneyFlowHolder(self.Leg(), self.Trade())
        return self._moneyFlowHolder.MoneyFlows()
    
    def SelectedCashFlow(self):
        return self._selectedCashFlow
        
    def SelectedReset(self):
        return self._selectedReset
        
    def GetCalc(self, columnId):
        methodChain = 'Second'
        for column in COLUMNS:
            if column == columnId:
                methodChain += '.First.FormattedValue'
                break
            else:
                methodChain += '.Second'
        return methodChain
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                     cashFlows;
                     resets;
                     amortisation;
                   """
               )
               
    def UpdateCashFlowDialogCustomPanes(self, attrName):
        layout = self.UniqueLayout(
                    """
                    editNominalFactor;
                    editStartDate;
                    editEndDate;
                    editPayDate;
                    editFixedRate;
                    editFloatRateOffset;
                    editFloatRateFactor;
                    editSpread;
                    editStrike;
                    """
                )
        return [{'Update Cash Flow' : layout}]
        
    def UpdateResetDialogCustomPanes(self, attrName):
        layout = self.UniqueLayout(
                    """
                    editResetDate;
                    editResetValue;
                    editResetStartDate;
                    editResetEndDate;
                    """
                )
                
        return [{'Update Reset' : layout}]
