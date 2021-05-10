import acm
import FUxCore
from math import floor
from math import log10
from math import fabs
import FBDPRollback
import FBDPString
from CurrSplitCallBackFuncs import *
from CurrSplitHelpFuncs import *
from CurrSplitCreateNewTrades import *

logme = FBDPString.logme

colName_ProjectedPaymentsPerCurrPair            = acm.FSymbol('Projected Payments - Instrument Pair')
colName_ProjectedPaymentsPerCurr                = acm.FSymbol('Projected Payments - Per Instrument')
colName_ProjectedPaymentsDiscountedPerCurrPair  = acm.FSymbol('Projected Payments Discounted – Currency Pair')
colName_ProjectedPaymentsDiscountedPerCurr      = acm.FSymbol('Projected Payments Discounted – Per Currency')
colName_ProjectedRiskflowsPerCurrencyPair       = acm.FSymbol('Projected Riskflows - Currency Pair')
colName_PriceDeltaCurrPair                      = acm.FSymbol('Price Delta - Currency Pair')
colName_PriceDelta                              = acm.FSymbol('Price Delta')

columnNames = [
    colName_ProjectedPaymentsPerCurrPair.Text(),
    colName_ProjectedPaymentsPerCurr.Text(),
    colName_ProjectedPaymentsDiscountedPerCurrPair.Text(),
    colName_ProjectedPaymentsDiscountedPerCurr.Text(),
    colName_ProjectedRiskflowsPerCurrencyPair.Text(),
    colName_PriceDeltaCurrPair.Text(),
    colName_PriceDelta.Text()
    ]


# vvvvvv Help Functions vvvvvv

class CallbackDisabler():

    def __init__( self ):
        self.disabled = False

    def Disable( self, dirty ):
        self.disabled = dirty
        
    def NotDisabled( self ):
        return not self.disabled

# ^^^^^^ Help Functions ^^^^^^

# This is suppose to be an abstract base class, python dose'nt support this concept but please treat this class as if it was an ABC
class BasePosDecompDialog( FUxCore.LayoutDialog ):
    BTN_MAIN_RATE =             'btnMainRate'
    BTN_TO_PAIR_RATE =          'btnToPairRate'
    LBL_SPLIT_CURR =            'lblSplitCurrency'
    LBL_SPLIT_PORT =            'lblSplitPortfolio'
    LBL_TO_PORT =               'lblToPortfolio'
    TO_PAIR =                   'toPair'
    FROM_PAIR =                 'fromPair'
    FROM_PAIR_RATE =            'fromPairRate'
    TO_PAIR_RATE =              'toPairRate'
    SPLIT_PAIR_RATE =           'splitPairRate'
    
    
    def __init__( self, activeSheet ):
        self.m_bindings = acm.FUxDataBindings()
        self.m_activeSheet = activeSheet
        self.m_selectedCell = self.m_activeSheet.Selection().SelectedCell()
        self.m_selectedCellColumnName = self.m_activeSheet.Selection().SelectedCell().Column().ColumnName()
        self.m_gridBuilder = activeSheet.GridBuilder()
        
        self.m_useMarketRates = False        
        self.callbackDisabler = CallbackDisabler()
        
        self.m_splitCurrencyCtrl = 0
        self.m_splitPortfolio = None;
        self.m_splitPortfolioCtrl = 0
        self.m_splitAcquirerBinder = 0
        
        self.m_splitPairBinder = 0
        self.m_splitPairPointsBinder = 0
        self.m_splitPairRateBinder = 0
        self.m_splitPairRateCtrl = 0
        
        self.m_toPortfolio = 0
                    
    def ErrorMessageIfInvalid( self ):
        port = self.RowPortfolio()
        if not port:
            return scriptName + ' is only possible on portfolio level. Grouping must be per portfolio in case of trade filters or compound portfolios'
        acq = self.GroupedPerTradeAttr('Acquirer') or port.PortfolioOwner()
        if not acq:
            return scriptName + ' is only possible on a portfolio that have a portfolio owner, or on positions grouped per acquirer.'
        if not self.RowCurrencyPair():
            return scriptName + ' is only possible on a portfolio with a Currency Pair, or on positions grouped per currency/position pair.'
        if self.IsRestBucketRow():
            return scriptName + ' on Rest Bucket is not supported.'
        if self.ColumnOnlyValidForNonBucketedRows() and (not self.IsNonBucketedRow()):
            return scriptName + ' only support non-bucketed rows for' + \
                   '\ncolumn ' + self.SelectedColumn().ColumnName().Text() + '.'
        return None
    
    def Tree(self):
        return self.SelectedCell().Tree()
    
    def GroupedPerCore( self, *methods ):
        try:
            if self.Tree() :
                it = self.Tree()
                root = self.m_gridBuilder.RowTreeIterator().Root().Tree()
                                
                while(it and not it.IsEqual(root) ):
                    row = it.Item()
                    g = None
                    try:
                        g = row.GrouperOnLevel()
                    except:
                        pass
                    if g and g.IsKindOf(acm.FAttributeGrouper):
                        if str(g.Method()) in methods:
                            t = row.Trades().AsList()[0]
                            return t
                    it = it.Parent()
        except:
            pass
        return None
    
    def SelectedCell(self):
        return self.m_selectedCell

    def ToPairDomain(self):
        raise NotImplementedError("Subclasses should implement this!")

    def ToInstrumentPairs(self):
        raise NotImplementedError("Subclasses should implement this!")

    def CreateLayout( self ):
        bindings = self.m_bindings
        portfolioFieldWidth = self.PortfolioFieldWidth()

        doubleDomain = acm.GetDomain('double')
        portDomain = acm.GetDomain('FPhysicalPortfolio')
        acqDomain = acm.GetDomain('FParty')
        toPairDomain = self.ToPairDomain()
        splitPairDomain = acm.GetDomain('FInstrumentPair')
        stringDomain = acm.GetDomain('string')
        dateDomain = acm.GetDomain('date')

        acquirers = self.AllAcquirers()
        toInstrumentPairs = self.ToInstrumentPairs()

        addBinder = bindings.AddBinderAndBuildLayoutPart

        fullPrecFormatter = acm.Get('formats/FullPrecision')
        self.m_mainFormatter = CurrencyObjectFormatter(self.RowCurrencyPair())
        self.m_amount1Formatter = CurrencyObjectFormatter(self.SelectedInstrument())
        self.m_amount2Formatter = CurrencyObjectFormatter(self.NonSelectedInstrument())
        self.m_toPairFormatter = CurrencyObjectFormatter(0)
        self.m_splitPairFormatter = CurrencyObjectFormatter(0)
        self.m_pointsFormatter = CurrencyObjectFormatter(2)

        mainRateLabel = self.MainRateLabel()

        amount1Label = self.Amount1Label()
        amount2Label = self.Amount2Label()

        b = acm.FUxLayoutBuilder()
        b. BeginVertBox('None')
        b.   BeginVertBox('EtchedIn')
        self.  m_fromPortfolioBinder = addBinder(b, 'fromPortfolio', "From Portfolio", portDomain)
        self.  m_fromAcquirerBinder = addBinder(b, 'fromAcquirer', "From Acquirer", acqDomain, None, acquirers)
        
        # vvvvvv From Pair Swap Fields vvvvvv
        
        b.     BeginHorzBox('None')
        b.       AddOption(self.FROM_PAIR, 'From Pair')
        b.       AddButton(self.BTN_MAIN_RATE, 'Use Market Rate')
        b.     EndBox()

        b.     BeginHorzBox('None')
        self.    m_fromPairRateBinder = addBinder(b, self.FROM_PAIR_RATE, 'From Pair Rate', doubleDomain, fullPrecFormatter)
        b.     EndBox()
        
        # ^^^^^^ From Pair Swap Fields ^^^^^^       
    
        self.  m_amount1Binder = addBinder(b, 'amount1', amount1Label, doubleDomain, fullPrecFormatter)  #JB
        self.  m_amount2Binder = addBinder(b, 'amount2', amount2Label, doubleDomain, fullPrecFormatter)  #JB
        b.     AddOption(self.LBL_TO_PORT, "To Portfolio", portfolioFieldWidth)
        self.  m_toPairBinder = addBinder(b, self.TO_PAIR, 'To Pair', toPairDomain, None, toInstrumentPairs)
        self.  m_toAcquirerBinder = addBinder(b, 'toAcquirer', "To Acquirer",acqDomain, None, acquirers)

        b.     AddInput(self.LBL_SPLIT_CURR, "Split against")
        b.     AddOption(self.LBL_SPLIT_PORT, "Split Portfolio", portfolioFieldWidth)
        self.  m_splitAcquirerBinder = addBinder(b, 'splitAcquirer', "Split Acquirer",acqDomain, None, acquirers)
        
        
        # vvvvvv To Pair Swap Fields vvvvvv
        b.     BeginHorzBox('None')
        self.    m_toPairRateBinder = addBinder(b, self.TO_PAIR_RATE, 'To Pair Rate', doubleDomain, fullPrecFormatter)
        b.     EndBox()
        # ^^^^^^ To Pair Swap Fields ^^^^^^
        
        
        # vvvvvv Split Pair Swap Fields vvvvvv

        self.  m_splitPairBinder = addBinder(b, 'splitPair', 'Split Pair', splitPairDomain)
        b.     BeginHorzBox('None')
        self.    m_splitPairRateBinder = addBinder(b, self.SPLIT_PAIR_RATE, 'Split Pair Rate', doubleDomain, fullPrecFormatter)
        b.     EndBox()
    
        # ^^^^^^ Split Pair Swap Fields ^^^^^^
        
        b.     BeginHorzBox('None')
        b.      AddCheckbox('cash_payment', 'Sweep PnL?' )
        b.     EndBox()
        
        b.   EndBox()
        b.   BeginHorzBox('None')
        b.     AddFill()
        b.     AddButton('commit', 'OK')
        b.     AddButton('cancel', 'Cancel')
        b.   EndBox()
        b. EndBox()

        self.m_ctrlDictionary = {'FromPortfolio' : self.m_fromPortfolioBinder,
            'FromAcquirer' : self.m_fromAcquirerBinder,
            'FromPairRate' : self.m_fromPairRateBinder,
            'Amount1' : self.m_amount1Binder,
            'ToAcquirer' : self.m_toAcquirerBinder,
            'SplitAcquirer' : self.m_splitAcquirerBinder,
            'ToPair' : self.m_toPairBinder,
            'ToPairRate' : self.m_toPairRateBinder,
            'SplitPair' : self.m_splitPairBinder,                      
            'SplitPairRate' : self.m_splitPairRateBinder }
        
        return b
    
    def GroupedPerPositionOrCurrencyPair( self ):
        coreResult = self.GroupedPerCore('Trade.PositionOrCurrencyPair', 'Trade.CurrencyPair', 'Trade.PositionPair', 'Trade.PositionOrInstrumentPair')
        if coreResult:
            return coreResult.CurrencyPair()
        return None

    def CheckIsValidDeltaHedgeColumn( self, column ):
        return self.ColumnIsPriceDelta(column.ColumnName())

    def ColumnOnlyValidForNonBucketedRows( self):
        columnName = self.SelectedColumn().ColumnName()
        return self.ColumnIsProjectedPaymentsDiscounted(columnName) or self.ColumnIsPriceDelta(columnName)

    def CheckValidColumns( self ):
        columnName = self.SelectedColumn().ColumnName()
        return self.SelectedCurrencyIsValid() and \
               (self.ColumnIsProjectedPayment(columnName) or \
                self.ColumnIsProjectedPaymentsDiscounted(columnName) or \
                self.ColumnIsProjectedRiskflow(columnName) or \
                self.ColumnIsPriceDelta(columnName))

    def ColumnIsProjectedPaymentsDiscounted( self, columnName ):
        return columnName in(colName_ProjectedPaymentsDiscountedPerCurrPair, colName_ProjectedPaymentsDiscountedPerCurr)

    def ColumnIsPriceDelta( self, columnName ):
        return columnName in(colName_PriceDeltaCurrPair, colName_PriceDelta)

    def ColumnIsProjectedPayment( self, columnName ):
        return columnName in(colName_ProjectedPaymentsPerCurrPair, colName_ProjectedPaymentsPerCurr)

    def ColumnIsProjectedRiskflow( self, columnName ):
        return columnName in(colName_ProjectedRiskflowsPerCurrencyPair)

    def IsRestBucketRow( self ):
        timeBucket = self.TimeBucket()
        return timeBucket and timeBucket.IsRest()

    def IsRootBucketRow( self ):
        timeBucket = self.TimeBucket()
        node = self.Tree()
        return timeBucket and node and node.Parent() and not self.TimeBucketFromNode(node.Parent())


    def IsNonBucketedRow( self ):
        timeBucket = self.TimeBucket()
        return not ( timeBucket and not self.IsRootBucketRow() )


    def SelectedCurrencyIsValid( self ):
        selectedCurrency = self.SelectedInstrument()
        currencyPair = self.RowCurrencyPair()
        return selectedCurrency in(currencyPair.Instrument1(), currencyPair.Instrument2())

    def TimeBucket( self ):
        return self.TimeBucketFromNode(self.Tree())

    def TimeBucketFromNode( self, tree ):
        if tree and tree.Item() and tree.Item().IsKindOf(acm.FTimeBucketAndObject):
            return tree.Item().TimeBucket()
        return None

    def UseCurrency1AsSelectedCurrency( self ):
        return self.SelectedColumn().ColumnName() == colName_PriceDelta 
        
    def IsValuationParameterReportDateToday(self):
        mappedValuationParameters = acm.GetFunction("mappedValuationParameters", 0)().Parameter()
        return mappedValuationParameters.ReportDate() == "Today"

    def _GetCtrlAndAddChangedCallBack(self, layout, ctrlName, changedFunc, callbackType = 'Changed'):
        ctrl = layout.GetControl(ctrlName)
        ctrl.AddCallback(callbackType, changedFunc, self)
        return ctrl
    
    def HandleCreate( self, dialog, layout ):
        self.m_fuxDlg = dialog
        self.m_fuxDlg.Caption(scriptName)
    
        self.m_toPortfolioCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.LBL_TO_PORT, OnToPortfolioChanged)
        self.m_fromPairCtrl = layout.GetControl(self.FROM_PAIR)

        self.m_toPairCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.TO_PAIR, OnToPairChanged)
        self.m_fromPairRateCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.FROM_PAIR_RATE, OnFromPairRateChanged)               
        self.m_amount1Ctrl = self._GetCtrlAndAddChangedCallBack(layout, 'amount1', OnAmount1Changed)        
        self.m_btnUseMainRateSpot = self._GetCtrlAndAddChangedCallBack(layout, self.BTN_MAIN_RATE, OnUseMainRateMarketClicked, 'Activate')
        self.m_splitPortfolioCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.LBL_SPLIT_PORT, OnSplitPortfolioChanged)       
        okBtn = self._GetCtrlAndAddChangedCallBack(layout, 'commit', OnOkButtonClicked, 'Activate')
        self.m_toPairRateCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.TO_PAIR_RATE, OnToPairRateChanged)
        self.m_splitPairRateCtrl = self._GetCtrlAndAddChangedCallBack(layout, self.SPLIT_PAIR_RATE, OnSplitPairRateChanged)

        self.m_splitCurrencyCtrl = layout.GetControl(self.LBL_SPLIT_CURR)
        self.m_cashPayment = layout.GetControl("cash_payment")
        
        self.m_bindings.AddLayout(layout)
        self.Init()

    # vvvvvv Init Methods vvvvvv

    def Init( self ):
        self.callbackDisabler.Disable(True)
        
        self.InitFromFields()
        self.InitControls()
        currencyPair = self.RowCurrencyPair()
        self.SetMainRate(self.DefaultMainRate())
        self.SetAmount1(self.SelectedCell().Value().Number())
        if self.DefaultMainRate() == 0 or fabs(self.GetAmount2()) < 20:
            self.m_cashPayment.Enabled(1)
            self.m_cashPayment.Checked(1)
        else:
            self.m_cashPayment.Checked(0)
            self.m_cashPayment.Enabled(1)
        self.InitToPortfolioPopulation()
        self.SetToPortfolio(self.RowPortfolio())
        self.callbackDisabler.Disable(False)

    def InitFromFields( self ):
        port = self.RowPortfolio()
        acq = self.GroupedPerTradeAttr('Acquirer') or port.PortfolioOwner()
        self.m_fromPortfolioBinder.SetValue(port)
        self.m_fromPortfolioBinder.Enabled(False)
        self.SetFromAcquirer(acq)
        self.SetFromPair(self.RowCurrencyPair())

        
    def InitControls( self ):
        self.m_splitCurrencyCtrl.Enabled(0)
        self.m_amount2Binder.Enabled(0)
        self.m_splitPairRateBinder.Enabled(0)
        self.m_fromPairCtrl.Enabled(0)
        self.m_toPairBinder.Enabled(0)
        self.m_splitPairBinder.Enabled(0)

    def InitAcquirerPopulation(self, acqCtrl):
        for acq in acm.FInternalDepartment.Select(''):
            acqCtrl.AddItem(acq)

    def InitToPortfolioPopulation( self ):
        for portfolio in self.PortfoliosSortedForToPortfolio():
            self.m_toPortfolioCtrl.AddItem(portfolio)

    # ^^^^^^ Init Methods ^^^^^^

    # vvvvvv Field Get Methods vvvvvv

    def GetCtrlValue(self, ctrlName):
        return self.m_ctrlDictionary[ctrlName].GetValue()

    def GetCtrlValueOrZero(self, ctrlName):
        try:
            if self.m_ctrlDictionary[ctrlName] and self.m_ctrlDictionary[ctrlName].GetValue():
                return self.m_ctrlDictionary[ctrlName].GetValue()
        except:
            pass
        return 0
        
    def GetCtrlValueOrNone(self, ctrlName):
        if self.m_ctrlDictionary[ctrlName] and self.m_ctrlDictionary[ctrlName].GetValue():
            return self.m_ctrlDictionary[ctrlName].GetValue()        
        return None

    def GetFromPair( self ):
        return self.m_fromPair

    def GetToPortfolio( self ):
        return self.m_toPortfolio

    def GetSplitPortfolio( self ):
        return self.m_splitPortfolio    

    def GetTriangulatedFromPairRate():
        if self.GetFromPair() and self.GetCtrlValueOrNone('SplitPair'):
            return self.GetFromPair().TriangulateRate(self.GetCtrlValueOrNone('ToPair'), self.GetCtrlValueOrZero('ToPairRate'), self.GetCtrlValueOrNone('SplitPair'), self.GetCtrlValueOrZero('SplitPairRate'))
        return 0.0
        
    def GetAmount2( self ):
        raise NotImplementedError("Subclasses should implement this!")

        
    def GetTriangulatedToPairRate( self ):
        if self.GetFromPair() and self.GetCtrlValueOrNone('ToPair') and self.GetCtrlValueOrNone('SplitPair') and self.GetCtrlValueOrZero('FromPairRate') and self.GetCtrlValueOrZero('SplitPairRate'):
            return self.GetCtrlValueOrNone('ToPair').TriangulateRate(self.GetFromPair(), self.GetCtrlValueOrZero('FromPairRate'), self.GetCtrlValueOrNone('SplitPair'), self.GetCtrlValueOrZero('SplitPairRate'))
        return 0.0
        
    def GetTriangulatedSplitPairRate( self ):
        if self.GetFromPair() and self.GetCtrlValueOrNone('ToPair') and self.GetCtrlValueOrNone('SplitPair') and self.GetCtrlValueOrZero('FromPairRate') and self.GetCtrlValueOrZero('ToPairRate'):
            return self.GetCtrlValueOrNone('SplitPair').TriangulateRate(self.GetFromPair(), self.GetCtrlValueOrZero('FromPairRate'), self.GetCtrlValueOrNone('ToPair'), self.GetCtrlValueOrZero('ToPairRate'))
        return 0.0

    def GetSplitCurrency( self ):
        insPair = self.GetCtrlValueOrNone('ToPair')
        if insPair and insPair != self.RowCurrencyPair():
            if insPair.Instrument1() in(self.RowCurrency1(), self.RowCurrency2()):
                return insPair.Instrument2()
            elif insPair.Instrument2() in(self.RowCurrency1(), self.RowCurrency2()):
                return insPair.Instrument1()
        return None

    # ^^^^^^ Field Get Methods ^^^^^^

    # vvvvvv Field Set Methods vvvvvv
    def AssertInput( self, value):
        return value <> None

    def SetCtrValue(self, ctrlName, value):
        if self.AssertInput(value):
            self.m_ctrlDictionary[ctrlName].SetValue(value)
            
    def SetDefaultFromPairRate( self ):
        if self.m_useMarketRates:
            price = self.DefaultMainMarketRate()
            self.SetCtrValue('FromPairRate', price)
        else:
            price = self.DefaultMainRate()
            self.SetCtrValue('FromPairRate', price)
        
    def SetFromPair(self, currencyPair):
        self.m_fromPair = currencyPair
        self.m_fromPairCtrl.AddItem(currencyPair)
        self.m_fromPairCtrl.SetData(currencyPair)
        
    def SetFromAcquirer( self, acq):
        self.m_fromAcquirerBinder.Enabled(False)
        self.m_fromAcquirerBinder.SetValue(acq)        

    def SetMainRate( self, mainRate ):
        if mainRate <> None:
            self.SetCtrValue('FromPairRate', mainRate)
            self.UpdateAmount2Field()

    def SetAmount1( self, amount1 ):
        if amount1 <> None: 
            self.m_amount1Binder.SetValue(amount1)
            self.UpdateAmount2Field()
            self.UpdateSplitPairRateField()

    def SetToPortfolio( self, toPortfolio ):
        if self.m_toPortfolioCtrl.ItemExists(toPortfolio):
            self.m_toPortfolio = toPortfolio
        self.m_toPortfolioCtrl.SetData(toPortfolio)
        self.EnableToPair()
        self.SetCtrValue('ToAcquirer', toPortfolio and toPortfolio.PortfolioOwner())
        
        newToPair = self.CurrencyPairForToPortfolio()
        oldToPair = self.GetCtrlValueOrNone('ToPair')
        if not self.RowCurrencyPair().IsEqual(newToPair):
            self.SetToPair(newToPair, oldToPair)
        elif oldToPair:
            self.SetToPair(None, oldToPair)
        self.UpdateAppearance()

    def SetSplitPortfolio( self, splitPortfolio ):
        if self.m_splitPortfolioCtrl.ItemExists(splitPortfolio):
            self.m_splitPortfolio = splitPortfolio
            self.SetSplitAcquirer(splitPortfolio and splitPortfolio.PortfolioOwner())
        
        if None == splitPortfolio:
            self.SetSplitAcquirer(None)
            
        self.m_splitPortfolioCtrl.SetData(self.m_splitPortfolio)
        self.UpdateSplitPortfolioField()

    def SetSplitAcquirer( self, acq ):
        self.m_splitAcquirerBinder.SetValue(acq)
        self.UpdateSplitAcquirerField()
                    
    def SetDefalultToPairRate( self ):
        insPair = self.GetCtrlValueOrNone('ToPair')
        if insPair:
            date = self.MoveDate() if AdjustingForDifferentSpotDaysEnabled() else self.BucketDate(insPair)
            price = self.Rate(insPair, date)
            self.SetCtrValue('ToPairRate', price)
        else:
            self.SetCtrValue('ToPairRate', self.GetCtrlValueOrZero('FromPairRate'))                

   
    def GetPoints(self, insPair, outrightDate):
        points = 0.0
	if insPair and insPair.PointValue():
                precision = PrecisionForCurrencyObject(insPair)
		
		spotRate = self.Rate(insPair, insPair.SpotDate(acm.Time().DateToday())) 
		spotRate = round(spotRate, precision)
		
		outrightRate = self.Rate(insPair, outrightDate)
		outrightRate = round(outrightRate, precision)		
		points = (outrightRate - spotRate) / insPair.PointValue()		
	return points 
    
    def SetRates( self ):
        self.SetDefaultFromPairRate()
        self.UpdateAmount2Field()
        self.SetDefalultToPairRate()
        self.SetCtrValue('SplitPairRate', self.GetTriangulatedSplitPairRate())
        
    # ^^^^^^ Field Set Methods ^^^^^^

    # vvvvvv Field Update Methods vvvvvv

    def SetToPair( self, newToPair, oldToPair=None ):
        if not newToPair or oldToPair <> newToPair:
            self.m_toPairBinder.SetValue(newToPair)
            self.m_toPairRateBinder.Enabled(None != self.GetSplitCurrency())
            insPair = self.m_toPairBinder.GetValue() or self.RowCurrencyPair()
            self.m_toPairFormatter.NumDecimals(PrecisionForCurrencyObject(insPair))
            
            self.UpdateSplitCurrencyField()
            self.UpdateSplitPortfolioPopulation()
            splitPair = self.InstrumentPairForSplitPortfolio()
            splitPort = self.RowPortfolio()
            self.SetSplitPortfolio(splitPort)
            
            self.UpdateSplitPair()
            
            self.SetRates()
   
    def UpdateToPairRate( self ):
        self.SetCtrValue('ToPairRate', DeriveRateFromPoints(self.GetCtrlValueOrNone('ToPair'), self.GetCtrlValueOrZero('ToPairSpot'), self.GetCtrlValueOrZero('ToPairPoints'), False))
    
    def UpdateSplitPair( self ):
        self.m_splitPairBinder.SetValue(self.InstrumentPairForSplitPortfolio())
        insPair = self.m_splitPairBinder.GetValue()
        if insPair:
            self.m_splitPairFormatter.NumDecimals(PrecisionForCurrencyObject(insPair))
  
    def UpdateSplitPairRate( self ):
        self.SetCtrValue('SplitPairRate', DeriveRateFromPoints(self.InstrumentPairForSplitPortfolio(), self.GetCtrlValueOrZero('SplitPairSpot'), self.GetCtrlValueOrZero('SplitPairPoints'), False))
    
    def UpdateTriangulatedToPairPrices( self ):
        self.SetCtrValue('ToPairRate', self.GetTriangulatedToPairRate())
        self.UpdateToPairSpot()
        
    def UpdateTriangulatedSplitPairPrices( self ):
        self.SetCtrValue('SplitPairRate', self.GetTriangulatedSplitPairRate())
        self.UpdateSplitPairSpot()
        
    def UpdateSplitCurrencyField( self ):
        splitCurrency = self.GetSplitCurrency()
        if splitCurrency:
            self.m_splitCurrencyCtrl.SetData(splitCurrency)
        else:
            self.m_splitCurrencyCtrl.SetData("no split")

    def UpdateSplitPairRateField( self ):
        self.SetCtrValue('SplitPairRate', self.GetTriangulatedSplitPairRate())
        self.m_splitPairBinder.SetValue(self.InstrumentPairForSplitPortfolio())

    def UpdateAppearance( self ):
        self.UpdateSplitPortfolioField()
        self.UpdateSplitAcquirerField()
        self.UpdateToPairRateField()
        
    def UpdateSplitPortfolioField( self ):
        self.m_splitPortfolioCtrl.Enabled(None != self.GetSplitCurrency())

    def UpdateSplitAcquirerField( self ):
        self.m_splitAcquirerBinder.Enabled(None != self.GetSplitCurrency())
    
    def UpdateToPairRateField( self ):
        self.m_toPairRateBinder.Enabled(None != self.GetSplitCurrency())
        
    def UpdateSplitPortfolioPopulation( self ):
        self.m_splitPortfolioCtrl.Clear()
        if self.GetSplitCurrency():
            for portfolio in self.PortfoliosSortedForSplitPortfolio():
                self.m_splitPortfolioCtrl.AddItem(portfolio)

    def UpdateAmount2Field( self ):
        self.m_amount2Binder.SetValue(self.GetAmount2())
        if self.DefaultMainRate() == 0 or fabs(self.GetAmount2()) < 20:
            self.m_cashPayment.Enabled(1)
            self.m_cashPayment.Checked(1)
        else:
            self.m_cashPayment.Enabled(1)
            self.m_cashPayment.Checked(0)


    # ^^^^^^ Field Update Methods ^^^^^^

    # vvvvvv Field Label Methods vvvvvv

    def Amount1Label( self ):
        return "%s Amount" % self.SelectedInstrument().Name()

    def Amount2Label( self ):
        return "%s Amount" % self.NonSelectedInstrument().Name()

    def MainRateLabel( self ):
        return "%s Rate" % self.RowCurrencyPair().Name()

    def ToPairRateLabel( self ):
        if self.GetCtrlValueOrNone('ToPair')():
            return "%s Rate" % self.GetCtrlValueOrNone('ToPair').Name()
        return "Decompose Rate1"

    def SplitPairRateLabel( self ):
        if self.InstrumentPairForSplitPortfolio():
            return "%s Rate" % self.InstrumentPairForSplitPortfolio().Name()
        return "Decompose Rate2"

    # ^^^^^^ Field Label Methods ^^^^^^

    # vvvvvv Help Methods vvvvvv

    def AllPortfolios( self ):
        setOfPortfolios = acm.FPhysicalPortfolio.Select("compound = 0")
        return callFilterHook(setOfPortfolios.AsList())

    def AllAcquirers( self ):
        setOfAcquirers = acm.FInternalDepartment.Select('')
        return callFilterHook(setOfAcquirers.AsList())
  
    def BucketDate( self , currPair):
        if self.ColumnIsProjectedPaymentsDiscounted(self.SelectedColumn().ColumnName()):
            if self.IsValuationParameterReportDateToday():
                return acm.Time.DateToday()
            else:
                return self.SpotDate(currPair)
        if self.TimeBucket() and (not self.IsRootBucketRow()):
            return self.TimeBucket().BucketDate()
        return self.SpotDate(currPair)

    def CellValueFromIterators( self, rowIterator, columnIterator ):
        cell = self.m_activeSheet.GetCell(rowIterator, columnIterator)
        if cell.Value():
            return cell.Value().Number()
        return 0

    def InstrumentPairForSplitPortfolio( self ):
        splitCurrency = self.GetSplitCurrency()
        if splitCurrency:
            pair1 = self.SelectedInstrument().InstrumentPair(splitCurrency, True)
            pair2 = self.NonSelectedInstrument().InstrumentPair(splitCurrency, True)
            if self.GetCtrlValueOrNone('ToPair') == pair1:
                return pair2
            return pair1
        return None

    def CurrencyPairForToPortfolio( self ):
        currPair = None
        if self.GetToPortfolio():
            currPair = self.GetToPortfolio().CurrencyPair()
        if not currPair:
            currPair = self.RowCurrencyPair()
            if self.IsSpotTrade():
                if currPair.SpotSplitPair():
                    currPair = currPair.SpotSplitPair()
            else:
                if currPair.ForwardSplitPair():
                    currPair = currPair.ForwardSplitPair()
        return currPair
    
    def EnableToPair( self ):
        enable = False
        if self.GetToPortfolio():
            enable = self.GetToPortfolio().CurrencyPair() == None
        
        self.m_toPairBinder.Enabled(enable)

    def DefaultMainRate( self ):
        return self.BreakEvenRateForSelectedPosition()
    
    def DefaultMainMarketRate( self ):
        date = self.BucketDate(self.RowCurrencyPair())
        return self.Rate(self.RowCurrencyPair(), date)

    def DefaultPortfolioForCurrencyPair( self, currencyPair ):
        if currencyPair:
            if self.IsSpotTrade():
                return currencyPair.SpotPortfolio()
            return currencyPair.ForwardPortfolio()
        return None            

    def BreakEvenRateForSelectedPosition( self ):
        raise NotImplementedError("Subclasses should implement this!")

    def IsSpotTrade( self ):
        return self.BucketDate(self.RowCurrencyPair()) == self.SpotDate(self.RowCurrencyPair())
        
    def IsPositionMoveAndSplit( self ):
        return None != self.GetSplitCurrency()

    def PortfolioFieldWidth( self ):
        portfWidths = [len(p.Name()) for p in self.AllPortfolios()]
        maxWidth = portfWidths and max(portfWidths) or 10
        return max(5, maxWidth) + 7

    def PortfoliosSortedByName( self ):
        portfolios = self.AllPortfolios()
        return sorted(portfolios, key = lambda p: p.Name())

    def PortfoliosSortedForToPortfolio( self, includeFromPortfolio = True ):
        instrumentPair = self.RowCurrencyPair()
        currencyPairMatchPortfolios = []
        currency1MatchPortfolios    = []
        currency2MatchPortfolios    = []
        noMatchPortfolios           = []
        for portfolio in self.PortfoliosSortedByName():
            if portfolio.CurrencyPair():
                if instrumentPair == portfolio.CurrencyPair():
                    currencyPairMatchPortfolios.append(portfolio)
                elif (portfolio.CurrencyPair().Currency1() in (instrumentPair.Instrument1(), instrumentPair.Instrument2())):
                    currency1MatchPortfolios.append(portfolio)
                elif (portfolio.CurrencyPair().Currency2() in (instrumentPair.Instrument1(), instrumentPair.Instrument2())):
                    currency2MatchPortfolios.append(portfolio)
            else:
                noMatchPortfolios.append(portfolio)
        return currencyPairMatchPortfolios + currency1MatchPortfolios + currency2MatchPortfolios + noMatchPortfolios

    def PortfoliosSortedForSplitPortfolio( self ):
        insPair = self.InstrumentPairForSplitPortfolio()
        if insPair:
            portfolios = self.PortfoliosSortedByName()
            currencyPairMatchPortfolios = [p for p in portfolios if (insPair == p.CurrencyPair())]
            noMatchPortfolios           = [p for p in portfolios if (not p.CurrencyPair())]
            return currencyPairMatchPortfolios + noMatchPortfolios
        return []

    def ProjectedPaymentsColumnName( self ):
        return self.m_selectedCellColumnName

    def ProjectedPayments( self ):
        rowTreeIterator = self.RowTreeIterator()        
        
        gridColumnIterator = self.m_activeSheet.GridBuilder().GridColumnIterator().First()
        while gridColumnIterator and gridColumnIterator.GridColumn().ColumnName() <> (self.ProjectedPaymentsColumnName()):
            gridColumnIterator = gridColumnIterator.Next()
        projectedPaymentForCurr1 = self.CellValueFromIterators(rowTreeIterator, gridColumnIterator)
        
        gridColumnIterator.Next()
        projectedPaymentForCurr2 = self.CellValueFromIterators(rowTreeIterator, gridColumnIterator)
            
        return projectedPaymentForCurr1, projectedPaymentForCurr2

    def QuantityIsDerived( self ):
        if self.GetSplitCurrency():
            return self.RowCurrency2() in(self.SelectedInstrument(), self.GetSplitCurrency())
        return self.SelectedInstrument() == self.RowCurrency2()

    def Row( self ):
        return self.SelectedCell().RowObject()

    def RowCurrency1( self ):
        return self.RowCurrencyPair().Instrument1()

    def RowCurrency2( self ):
        return self.RowCurrencyPair().Instrument2()

    def RowCurrencyPair( self ):
        currPair = None
        insPair = self.GroupedPerPositionOrCurrencyPair() 
        if insPair:
            currPair = insPair
        if not currPair and self.RowPortfolio():
            currPair =  self.RowPortfolio().CurrencyPair()
        return currPair

    def GroupedPerTradeAttr( self, tradeAttr ):
        coreResult = self.GroupedPerCore("Trade.%s" % tradeAttr)
        if coreResult:
            return coreResult.GetProperty(tradeAttr)
        return None

    def RowPortfolio( self ):
        port = self.GroupedPerTradeAttr('Portfolio')
        if not port and self.Row():
            if self.Row().IsKindOf(acm.FTimeBucketAndObject):
                try:
                    port = self.Row().Object().Portfolio()
                except:
                    pass
            else:
                port = self.Row().Portfolio()

            if port and ( port.IsKindOf(acm.FTradeSelection) or port.Compound() ):
                port = None
        return port

    def RowTreeIterator( self ):
        rowTreeIterator = self.m_activeSheet.GridBuilder().RowTreeIterator()
        return rowTreeIterator.Find(self.Row())

    def SelectedCell( self ):
        return self.m_activeSheet.Selection().SelectedCell()

    def SelectedColumn( self ):
        return self.SelectedCell().Column()

    def SelectedInstrument( self ):
        if self.m_selectedCell:
            if self.UseCurrency1AsSelectedCurrency():
                return self.RowCurrencyPair().Instrument1()
            else:
                unit = self.SelectedCell().Value().Unit().AsString()
                if unit == self.RowCurrencyPair().Instrument1().Name() or\
                    unit == "'" + self.RowCurrencyPair().Instrument1().Name() + "'" :
                    return self.RowCurrencyPair().Instrument1()
                elif unit == self.RowCurrencyPair().Instrument2().Name() or\
                    unit == "'" + self.RowCurrencyPair().Instrument2().Name() + "'" :
                    return self.RowCurrencyPair().Instrument2()
        return None

        
    def NonSelectedInstrument( self ):
        if self.SelectedInstrument() == self.RowCurrency1():
            return self.RowCurrency2()
        return self.RowCurrency1()

    def SplitAmount( self ):
        splitCurrency = self.GetSplitCurrency()
        toPair = self.GetCtrlValueOrNone('ToPair')
        toPairRate = self.GetCtrlValueOrZero('ToPairRate')
        amount1  = self.NonSplitAmount(toPair)
        if toPair:
            if splitCurrency == toPair.Instrument2():
                return -amount1 * toPairRate
            elif toPairRate:
                return -amount1 / toPairRate
        return 0.0

    def NonSplitAmount( self, insPair ):
        if insPair:
            if self.SelectedInstrument() in (insPair.Instrument1(), insPair.Instrument2()):
                return self.GetCtrlValueOrZero('Amount1') * insPair.Instrument1().ContractSizeInQuotation()
            elif self.NonSelectedInstrument() in (insPair.Instrument1(), insPair.Instrument2()):
                return self.GetAmount2() * insPair.Instrument1().ContractSizeInQuotation()
        return None

    def SplitCurrencyPair2( self ):
        splitCurrency = self.GetSplitCurrency()
        if splitCurrency:
            return self.NonSelectedInstrument().CurrencyPair(splitCurrency, True)
        return None
        
    def SpotDate( self, currPair ):
        if(AdjustingForDifferentSpotDaysEnabled()):
            return currPair.SpotDate(acm.Time.DateToday())
        else:
            return self.RowCurrencyPair().SpotDate(acm.Time.DateToday())

    def FromPairSpotDate( self ):
        return self.SpotDate(self.RowCurrencyPair())
        
    def ToPairSpotDate( self ):
        if self.GetCtrlValueOrNone('ToPair'):
            return self.GetCtrlValueOrNone('ToPair').SpotDate(acm.Time.DateToday())
        return None

    def SplitPairSpotDate( self ):
        if self.InstrumentPairForSplitPortfolio():
            return self.InstrumentPairForSplitPortfolio().SpotDate(acm.Time.DateToday())
        return None

    def MoveDate( self ):
        def CheckForMoveDate():
            if AdjustingForDifferentSpotDaysEnabled():
                if self.IsSpotTrade() and self.FromPairSpotDate() and self.ToPairSpotDate() and self.SplitPairSpotDate():
                    return True
            return False
                
        moveDate = self.BucketDate(self.RowCurrencyPair())
        # The move date/cross date is the most common spot date of the three currency pairs and the date that the positions will be moved/split on. #
        if CheckForMoveDate():
            if moveDate == self.ToPairSpotDate() or moveDate == self.SplitPairSpotDate():
                return moveDate
            else:
                return self.ToPairSpotDate()
        else:
            return moveDate
        
    def ShouldCreateMoveSwap( self ):
        if(AdjustingForDifferentSpotDaysEnabled()):
            retValue = self.IsSpotTrade() and self.IsPositionMoveAndSplit() and \
                       (NeedsSwap(self.IsSpotTrade(), self.FromPairSpotDate(), self.MoveDate()) or \
                        NeedsSwap(self.IsSpotTrade(), self.ToPairSpotDate(), self.MoveDate()) or \
                        NeedsSwap(self.IsSpotTrade(), self.SplitPairSpotDate(), self.MoveDate()))
            return retValue
        else:
            return False                            

    def TradeProcessNumber( self ):
        if self.IsSpotTrade():
            return 4096 # spot
        return 8192 # forward

    def UseFxBreakEvenRateAsDefault( self ):
        return self.SelectedColumn().ColumnName() == colName_ProjectedPaymentsPerCurrPair

    def AssertPortfoliosAndAcquirers( self ):

        def AssertToPortAndAcq():
            return self.GetToPortfolio() and self.GetCtrlValue('ToAcquirer')
            
        def AssertSplitPortAndAcq():
            return (self.GetSplitPortfolio() and self.GetCtrlValue('SplitAcquirer')) or not self.GetSplitCurrency() or not self.GetToPortfolio().CurrencyPair()
            
        def AssertFromPairSwap():
            return False if NeedsSwap(self.IsSpotTrade(), self.FromPairSpotDate(), self.MoveDate()) and (not self.GetCtrlValue('FromFwdPortfolio') or not self.GetCtrlValue('FromFwdAcquirer')) else True
            
        def AssertToPairSwap():
            return False if NeedsSwap(self.IsSpotTrade(), self.ToPairSpotDate(), self.MoveDate()) and (not self.GetCtrlValue('ToFwdPortfolio') or not self.GetCtrlValue('ToFwdAcquirer')) else True
            
        def AssertSplitPairSwap():
            return False if NeedsSwap(self.IsSpotTrade(), self.SplitPairSpotDate(), self.MoveDate()) and (not self.GetCtrlValue('SplitFwdPortfolio') or not self.GetCtrlValue('SplitFwdAcquirer')) else True                
            
        if not AssertToPortAndAcq():
            return [False, 'To']
            
        if not AssertSplitPortAndAcq():
            return [False, 'Split']
        
        if not AssertFromPairSwap():
            return [False, 'From pair swap']
            
        if not AssertToPairSwap():
            return [False, 'To pair swap']
            
        if not AssertSplitPairSwap():
            return [False, 'Split pair swap']

        return [True, '']
    
    def HandleApply( self ):
        ok, msg = self.AssertPortfoliosAndAcquirers()
        if ok:
            CreateTrades(self.createParameters())
            self.m_fuxDlg.CloseDialogCancel()
        else:
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Please select ' + msg + ' portfolio and acquirer.')

    def createParameters(self):
        parameters = {}
        parameters['fromPortfolio'] = self.GetCtrlValue('FromPortfolio')
        parameters['fromAcquirer'] = self.GetCtrlValue('FromAcquirer')
        parameters['toPortfolio'] = self.GetToPortfolio()
        parameters['toAcquirer'] = self.GetCtrlValue('ToAcquirer')
        parameters['splitPortfolio'] = self.GetSplitPortfolio()
        parameters['splitAcquirer'] = self.GetCtrlValue('SplitAcquirer')
        parameters['splitCurrency'] = self.GetSplitCurrency()
        parameters['fromCurrencyPair'] = self.GetFromPair()
        parameters['toCurrencyPair'] = self.GetCtrlValue('ToPair')
        parameters['splitCurrencyPair'] = self.GetCtrlValue('SplitPair')
        parameters['mainRate'] = self.GetCtrlValueOrZero('FromPairRate')
        
        if self.GetCtrlValueOrZero('FromPairSpot') != 0:
            parameters['mainSpotRate'] = self.GetCtrlValueOrZero('FromPairSpot')            
        else:
            parameters['mainSpotRate'] = self.Rate(self.GetFromPair(), self.GetFromPair().SpotDate(acm.Time.DateToday()))
        
        parameters['toPairRate'] = self.GetCtrlValueOrZero('ToPairRate')
        parameters['splitPairRate'] = self.GetCtrlValueOrZero('SplitPairRate')
        parameters['toPairSpotRate'] = self.GetCtrlValueOrZero('ToPairSpot')
        parameters['splitPairSpotRate'] = self.GetCtrlValueOrZero('SplitPairSpot')
        parameters['rowCurrency1'] = self.RowCurrency1()
        parameters['rowCurrency2'] = self.RowCurrency2()
        parameters['selectedCurrency'] = self.SelectedInstrument()
        parameters['nonSelectedCurrency'] = self.NonSelectedInstrument()
        parameters['amount1'] = self.GetCtrlValueOrZero('Amount1')
        parameters['amount2'] = self.GetAmount2()
        parameters['nonSplitAmountToPair'] = self.NonSplitAmount(parameters['toCurrencyPair'])
        parameters['nonSplitAmountSplitPair'] = self.NonSplitAmount(parameters['splitCurrencyPair'])
        parameters['splitAmount'] = self.SplitAmount()
        parameters['tradeProcessNumber'] = self.TradeProcessNumber()
        parameters['quantityIsDerived'] = self.QuantityIsDerived()
        
        parameters['fromCurrencyPair'] = self.GetFromPair()
        parameters['moveDate'] = self.MoveDate()
        parameters['cashPayment'] = self.m_cashPayment.Checked()
        return parameters

    def HandleDestroy( self ):
        self.m_fromPairRateBinder.RemoveDependent(self)
        self.m_amount1Binder.RemoveDependent(self)
        self.m_toPairRateBinder.RemoveDependent(self)
        self.m_fromAcquirerBinder.RemoveDependent(self)
        self.m_toAcquirerBinder.RemoveDependent(self)
        self.m_splitAcquirerBinder.RemoveDependent(self)

def callFilterHook(sel):
    try:
        import FBDPHook
        reload(FBDPHook)
    except ImportError:
        return sel
    try:
        return FBDPHook.pos_move_split_filter_selection(sel)
    except:
        return sel

StartFXPositionMoveSplit = 1

def DetermineIfFx(activeSheet):
    baseComp = BasePosDecompDialog(activeSheet)
    if baseComp.RowCurrencyPair().IsKindOf(acm.FCurrencyPair):
        return StartFXPositionMoveSplit
    return 0
