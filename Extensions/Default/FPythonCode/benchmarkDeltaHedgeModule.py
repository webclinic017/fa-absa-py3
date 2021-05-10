


import acm
import FUxCore
import FUxUtils
import math
import HedgeCalculationSpace

def OnBenchmarkCurveClicked(self, cd):
    benchmarkCurves = acm.FArray()
    benchmarkCurves.Add(None)
    benchmarkCurves.AddAll(acm.FBenchmarkCurve.Instances())
    benchmarkCurves.AddAll(acm.FSpreadCurve.Instances())
    benchmarkCurves.AddAll(acm.FInflationCurve.Instances())
    benchmarkCurves.SortByProperty("Name")
    benchmarkCurve = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(), 'Benchmark Curve', 'Benchmark/Inflation/Spread Curves', benchmarkCurves, self.GetParameter('BenchmarkCurve'))
    self.AddParameter('BenchmarkCurve', benchmarkCurve)
    self.ControlSetDataDefault( self.m_benchmarkCurveText, 'BenchmarkCurve', '' )

def OnCalculationCurrencyClicked(self, cd):
    currencies = acm.FArray()
    currencies.AddAll(acm.FCurrency.Instances())
    currency = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(), 'Calculation Currency', 'FCurrency', currencies, self.GetParameter('CalculationCurrency'))
    self.AddParameter('CalculationCurrency', currency)
    self.ControlSetDataDefault( self.m_calculationCurrencyText, 'CalculationCurrency', '' )
    self.UpdateControls()

class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_binder = None
        self.m_okBtn = None
        self.m_benchmarkCurveBtn = None
        self.m_calculationCurrencyBtn = None
        self.m_parameters = None
        self.m_calculationCurrencyText = None
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Hedge - Benchmark Delta' )
        self.m_okBtn = layout.GetControl("ok")
                
        self.m_benchmarkCurveBtn = layout.GetControl("benchmarkCurve")
        self.m_benchmarkCurveText = layout.GetControl("benchmarkCurveText")
        self.m_benchmarkCurveLbl = layout.GetControl("benchmarkCurveLabel")
        self.m_benchmarkCurveBtn.AddCallback( "Activate", OnBenchmarkCurveClicked, self )
        self.ControlSetDataDefault( self.m_benchmarkCurveText, 'BenchmarkCurve', '' )
        
        self.m_calculationCurrencyBtn = layout.GetControl("calculationCurrency")
        self.m_calculationCurrencyText = layout.GetControl("calculationCurrencyText")
        self.m_calculationCurrencyLbl = layout.GetControl("calculationCurrencyLabel")
        self.m_calculationCurrencyBtn.AddCallback( "Activate", OnCalculationCurrencyClicked, self )
        
        if None == self.GetParameter('CalculationCurrency'):
            mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
            accountingCurrency = mappedValuationParameter().Parameter().AccountingCurrency()
            self.AddParameter('CalculationCurrency', accountingCurrency)
            self.ControlSetDataDefault( self.m_calculationCurrencyText, 'CalculationCurrency', accountingCurrency)
        else:
            self.ControlSetData( self.m_calculationCurrencyText, 'CalculationCurrency')
        
        self.m_benchmarkCurveText.Editable( False )
        self.m_calculationCurrencyText.Editable( False )
        
        self.CreateToolTip()
        
        self.UpdateControls()
        
    def CreateToolTip(self):
        benchmarkCurveToolTip = 'The hedge will only take into account benchmark deltas attributed to the selected benchmark curve. The curve should be set to the same curve as the hedge folder is applied to in \'Interest Rate Benchmark Delta Per Yield Curve\'.'
        self.m_benchmarkCurveText.ToolTip(benchmarkCurveToolTip )
        self.m_benchmarkCurveLbl.ToolTip(benchmarkCurveToolTip )
        self.m_benchmarkCurveBtn.ToolTip(benchmarkCurveToolTip )        
        
        calculationCurrencyToolTip = 'The currency in which the benchmark deltas will be calculated. Recommended to be set to the display currency of the hedge instruments in the sheet.'
        self.m_calculationCurrencyText.ToolTip(calculationCurrencyToolTip)
        self.m_calculationCurrencyLbl.ToolTip(calculationCurrencyToolTip)
        self.m_calculationCurrencyBtn.ToolTip(calculationCurrencyToolTip)
        
    def UpdateControls(self):
        if self.GetParameter('CalculationCurrency'):
            self.m_okBtn.Enabled(True)
        else:
            self.m_okBtn.Enabled(False)

    def HandleApply(self):
        if self.ValidateControls():
            return self.m_parameters;
        return None

    def ValidateControls(self):
        if self.GetParameter('CalculationCurrency'):
            return True
        return False
        
    def AddParameters(self, initData):
        calculationCurrency = None
        benchmarkCurve = None

        if initData:
            benchmarkCurve = initData.At('BenchmarkCurve')
            calculationCurrency = initData.At('CalculationCurrency')
            
        self.AddParameter('BenchmarkCurve', benchmarkCurve)
        self.AddParameter('CalculationCurrency', calculationCurrency)
        
                
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox('None')
        b.      AddLabel('benchmarkCurveLabel', 'Benchmark Curve:')
        b.      AddSpace(19)
        b.      AddInput('benchmarkCurveText', '', 20, -1, 40, "Default", False)
        b.      AddButton('benchmarkCurve', '...', False, True)
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddLabel('calculationCurrencyLabel', 'Calculation Currency:')
        b.      AddSpace(7)
        b.      AddInput('calculationCurrencyText', '', 20, -1, 40, "Default", False)
        b.      AddButton('calculationCurrency', '...', False, True)
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
        
    def AddParameter(self, key, value):
        if not self.m_parameters:
            self.m_parameters = acm.FDictionary()
        self.m_parameters.AtPut(key, value)
        
    def GetParameter(self, key):
        if self.m_parameters and self.m_parameters.Includes(key):
            return self.m_parameters[key]
        return None
        
    def ControlSetDataDefault( self, control, dataKey, defaultValue):
        parameterValue = self.GetParameter(dataKey)
        if parameterValue:
            control.SetData( parameterValue )
        else:
            control.SetData( defaultValue )

    def ControlSetData( self, control, dataKey ):
        parameterValue = self.GetParameter(dataKey)
        control.SetData( parameterValue )
                

def ael_custom_dialog_show(shell, params):
    dialogData = FUxUtils.UnpackInitialData(params)
    customDlg = myCustomDialog()
    customDlg.AddParameters(dialogData)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
    
def ael_custom_label( parameters, dictExtra ):
    benchmarkCurve = parameters.At('BenchmarkCurve')
    calculationCurrency = parameters.At('CalculationCurrency')
    label = ""
    if None != benchmarkCurve:
        label = benchmarkCurve.Name()
    if None != calculationCurrency:
        label = label + " - " + calculationCurrency.Name()
    return label
    
def instrumentGetDates(instruments):
    dates = []
    for instrument in instruments:
        dates.append(instrument.LastIRSensDay())
    dates.sort()
    return dates

def objectBenchmarkDelta(object, calcSpace, instruments, dates, benchmarkCurve, calculationCurrency):
    delta = []
    if(None != dates):
        timeBuckets = HedgeCalculationSpace.create_timebuckets(dates)
        delta =  object.Calculation().InterestRateBenchmarkDeltaBuckets(calcSpace,
            calculationCurrency, None, timeBuckets, benchmarkCurve)
    else:
        delta = object.Calculation().InterestRateBenchmarkDeltaInstruments(
            calcSpace, calculationCurrency, None, instruments, benchmarkCurve)
    return delta
  
def ael_custom_dialog_main( parameters, dictExtra ):
    eii = dictExtra.At('customData')
    hedgeDict = eii.ExtensionObject()
    instruments = hedgeDict.At('instruments')
    position = hedgeDict.At('position')
    dates = instrumentGetDates(instruments)
    calcSpace = HedgeCalculationSpace.scsc
    benchmarkCurve = parameters['BenchmarkCurve']
    calculationCurrency = parameters['CalculationCurrency']
    portDelta = objectBenchmarkDelta(position, calcSpace, None, dates, benchmarkCurve, calculationCurrency)
    hedgeDelta = []
    for instrument in instruments:
        hedgeDelta.append(objectBenchmarkDelta(instrument, calcSpace, instruments, None, benchmarkCurve, calculationCurrency))
        
    myHedge = acm.GetFunction('hedge', 3)
    quantities = myHedge(portDelta, hedgeDelta, None)
    return quantities
