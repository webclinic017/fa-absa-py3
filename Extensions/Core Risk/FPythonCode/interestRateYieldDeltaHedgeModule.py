
from __future__ import print_function
import acm
import FUxCore
import math
import FUxUtils
import HedgeCalculationSpace


def inputHookForColumnHedgeTradeQuantity(row, col, calcval, strValue, operation):
    if str(operation) == 'remove':
        row.SingleTrade().Quantity( 0 )
        
def OnCurrencyClicked(self, cd):
    currencies = acm.FArray()
    currencies.Add(None)
    currencies.AddAll(acm.FCurrency.Instances())
    currency = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(), 'Currency', 'FCurrency', currencies, self.GetParameter('Currency'))
    self.AddParameter('Currency', currency)
    self.ControlSetDataDefault( self.m_currencyText, 'Currency', '' )

def OnTimeBucketsClicked(self, cd):
    timeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_fuxDlg.Shell(), self.GetParameter('Stored Time Buckets'))
    if timeBuckets:
        self.AddParameter('Stored Time Buckets', timeBuckets)
        self.AddParameter('Time Buckets', timeBuckets.TimeBuckets())
        self.ControlSetDataDefault( self.m_timeBucketsText, 'Time Buckets', '' )
    self.UpdateControls()


def OnAdvancedHedgeModeClicked( self, cd ):
    self.m_advancedHedgeModeEnabled = not self.m_advancedHedgeModeEnabled
    self.UpdateControls()

class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_okBtn = None
        self.m_currencyBtn = None
        self.m_timeBucketsBtn = None
        self.m_parameters = None
        self.m_currencyText = None
        self.m_currencyLabel = None
        self.m_advancedHedgeModeBtn = None
        self.m_advancedHedgeModeEnabled = False
        self.m_timeBucketsText = None
        self.m_timeBucketsLabel = None
        self.m_transactionCost = None
        self.m_shortVolatility = None
        self.m_longVolatility = None
        self.m_shortCorrelation = None
        self.m_longCorrelation = None
        
    def CreateToolTip(self):
        self.m_currencyText.ToolTip('Only curves having a yield curve definition Currency matching this value will be shifted in the yield delta calculations for the positions (if not set all used curves will be shifted). This field does not affect the yield delta for the selected benchmark instruments (nor which cash flows or payments to include for positions to be hedged).')
        self.m_currencyLabel.ToolTip('Only curves having a yield curve definition Currency matching this value will be shifted in the yield delta calculations for the positions (if not set all used curves will be shifted). This field does not affect the yield delta for the selected benchmark instruments (nor which cash flows or payments to include for positions to be hedged).')
        self.m_currencyBtn.ToolTip('Select a currency for filtering which yield curves to shift in the yield delta calculation for the positions.')
        self.m_timeBucketsText.ToolTip('The time buckets defining for which buckets the risk should be hedged. Using \'Generate > Benchmark Dates From Query Folder\' on the query folder corresponding to the hedge instrument will imply that the subsequent five parameters are of no interest. The \'Advanced\' mode is not recommended in such a case.')
        self.m_timeBucketsLabel.ToolTip('The time buckets defining for which buckets the risk should be hedged. Using \'Generate > Benchmark Dates From Query Folder\' on the query folder corresponding to the hedge instrument will imply that the subsequent five parameters are of no interest. The \'Advanced\' mode is not recommended in such a case.')
        self.m_timeBucketsBtn.ToolTip('Select time buckets defining for which buckets the risk should be hedged.')
        self.m_transactionCost.ToolTip('Defines whether paying fixed transaction cost or accepting residual risk is preferable. This transaction cost is expressed in basis points of the nominal amount.')
        self.m_shortVolatility.ToolTip('The volatility of the one-day rate. The volatility values applied to the different buckets are interpolated between the short-rate volatility and the 10-year volatility.')      
        self.m_longVolatility.ToolTip('The volatility of the 10-year point. The volatility values applied to the different buckets are interpolated between the short-rate volatility and the 10-year volatility. Buckets later than the 10-year volatility are extrapolated.')
        self.m_shortCorrelation.ToolTip('The correlation between the one-day and the one-year points. The correlation between any two buckets is interpolated between the short-rate correlation and the 10-year correlation.')
        self.m_longCorrelation.ToolTip('The correlation between the 10-year and the 11-year points. The correlation between any two buckets is interpolated between the short-rate correlation and the 10-year correlation.')
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Hedge - Interest Rate Yield Delta' )
        self.m_okBtn = layout.GetControl("ok")
        self.m_currencyBtn = layout.GetControl("currency")
        self.m_timeBucketsBtn = layout.GetControl("timeBuckets")
        self.m_currencyText = layout.GetControl("currencyText")
        self.m_currencyLabel = layout.GetControl("currencyLabel")
        self.m_advancedHedgeModeBtn = layout.GetControl("advancedHedgeMode")
        self.m_advancedHedgeModeBtn.AddCallback( "Activate", OnAdvancedHedgeModeClicked, self )
        self.m_advancedHedgeModeEnabled = self.GetParameter('Advanced Hedge Mode Enabled')
        self.m_timeBucketsText = layout.GetControl("timeBucketsText")
        self.m_timeBucketsLabel = layout.GetControl("timeBucketsLabel")
        self.m_transactionCost = layout.GetControl("transactionCost")
        self.m_shortVolatility = layout.GetControl("shortVolatility")
        self.m_longVolatility = layout.GetControl("longVolatility")
        self.m_shortCorrelation = layout.GetControl("shortCorrelation")
        self.m_longCorrelation = layout.GetControl("longCorrelation")
        self.m_currencyBtn.AddCallback( "Activate", OnCurrencyClicked, self )
        self.m_timeBucketsBtn.AddCallback( "Activate", OnTimeBucketsClicked, self )
        self.ControlSetDataDefault( self.m_currencyText, 'Currency', '' )
        self.ControlSetDataDefault( self.m_timeBucketsText, 'Time Buckets', '' )
        self.ControlSetData( self.m_transactionCost, 'Transaction Cost' )
        self.ControlSetData( self.m_shortVolatility, 'Short Volatility' )
        self.ControlSetData( self.m_longVolatility, 'Long Volatility' )
        self.ControlSetData( self.m_shortCorrelation, 'Short Correlation' )
        self.ControlSetData( self.m_longCorrelation, 'Long Correlation' )
        self.m_currencyText.Editable( False )
        self.m_timeBucketsText.Editable( False )
        self.UpdateControls()
        self.CreateToolTip()
        
    def UpdateControls(self):
        self.m_timeBucketsText.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_timeBucketsLabel.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_timeBucketsBtn.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_transactionCost.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_shortVolatility.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_longVolatility.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_shortCorrelation.Visible( self.AdvancedHedgeModeEnabled() )
        self.m_longCorrelation.Visible( self.AdvancedHedgeModeEnabled() )
        
        if self.AdvancedHedgeModeEnabled():
            self.m_advancedHedgeModeBtn.Label('Normal <<')
            self.m_advancedHedgeModeBtn.ToolTip('Normal Yield Delta Hedge - The time buckets defining for which buckets the risk should be hedged is taken directly from the actual hedge instruments. Note that the time bucket structure in the Vertical Portfolio sheet is not used as input to the hedge calculations.')
        else:
            self.m_advancedHedgeModeBtn.Label('Advanced >>')
            self.m_advancedHedgeModeBtn.ToolTip('Advanced Yield Delta Hedge - An arbitrary set of time buckets can be chosen to define for which buckets the risk should be hedged. If these time buckets does not equal the time buckets of the chosen hedge instruments five separate input parameters will be used in the optimization problem. Note that the time bucket structure in the Vertical Portfolio sheet is not used as input to the hedge calculations.')
            
        if self.AdvancedHedgeModeEnabled():
            if self.GetParameter('Time Buckets'):
                self.m_okBtn.Enabled(True)
            else:
                self.m_okBtn.Enabled(False)
        else:
            self.m_okBtn.Enabled(True)

    def HandleApply(self):
        if self.ValidateControls():
            return self.m_parameters;
        return None
            
    def ValidateControls(self):
        ok = True
        self.AddParameter('Advanced Hedge Mode Enabled', self.AdvancedHedgeModeEnabled() )
        ok = self.ControlGetDataAndSetParameter( self.m_transactionCost, 'Transaction Cost', True ) and ok
        ok = self.ControlGetDataAndSetParameter( self.m_shortVolatility, 'Short Volatility', True ) and ok
        ok = self.ControlGetDataAndSetParameter( self.m_longVolatility, 'Long Volatility', True ) and ok
        ok = self.ControlGetDataAndSetParameter( self.m_shortCorrelation, 'Short Correlation', False ) and ok
        ok = self.ControlGetDataAndSetParameter( self.m_longCorrelation, 'Long Correlation', False ) and ok
        return ok
    
    def AdvancedHedgeModeEnabled(self):
        return self.m_advancedHedgeModeEnabled
    
    def AddParameters(self, initData):
        currency = None
        timeBuckets = None
        advancedHedgeModeEnabled = False
        transactionCost = 0.0
        shortVolatility = 10.0
        longVolatility = 7.0
        shortCorrelation = 0.6
        longCorrelation = 0.95
        
        if initData:
            advancedHedgeModeEnabled = initData.At('Advanced Hedge Mode Enabled')
            currency = initData.At('Currency')
            timeBuckets = initData.At('Time Buckets')
            transactionCost = initData.At('Transaction Cost')
            shortVolatility = initData.At('Short Volatility')
            longVolatility = initData.At('Long Volatility')
            shortCorrelation = initData.At('Short Correlation')
            longCorrelation = initData.At('Long Correlation')
            
        self.AddParameter('Advanced Hedge Mode Enabled', advancedHedgeModeEnabled)
        self.AddParameter('Currency', currency)
        self.AddParameter('Time Buckets', timeBuckets)
        self.AddParameter('Transaction Cost', transactionCost)
        self.AddParameter('Short Volatility', shortVolatility)
        self.AddParameter('Long Volatility', longVolatility)
        self.AddParameter('Short Correlation', shortCorrelation)
        self.AddParameter('Long Correlation', longCorrelation)
                
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox('None')
        b.      AddLabel('currencyLabel', 'Currency:')
        b.      AddSpace(37)
        b.      AddInput('currencyText', '', 20, -1, 40, "Default", False)
        b.      AddButton('currency', '...', False, True)
        b.    EndBox()
        b.      AddButton('advancedHedgeMode', 'Advanced >>')
        b.      BeginHorzBox('None')
        b.      AddLabel('timeBucketsLabel', 'Time Buckets:')
        b.      AddSpace(14)
        b.      AddInput('timeBucketsText', '', 20, -1, 40, "Default", False)
        b.      AddButton('timeBuckets', '...', False, True)
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddInput('transactionCost', 'Transaction Cost')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddInput('shortVolatility', 'Short Volatility')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddInput('longVolatility', 'Long Volatility')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddInput('shortCorrelation', 'Short Correlation')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddInput('longCorrelation', 'Long Correlation')
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
            
    def ControlGetDataAndSetParameter( self, control, dataKey, mustBeLargerThanOrEqualToZero ):
        value = control.GetData()
        if value:
            try:
                floatValue = float(value)
                if mustBeLargerThanOrEqualToZero:
                    if floatValue < 0.0:
                        print (dataKey, "can not be less than", 0.0)
                        return False
                self.AddParameter(dataKey, floatValue)
            except:
                print ('Only numeric values accepted for', dataKey)
                return False
        else:
            print ("Value not set for", dataKey)
            return False
        return True
        
ael_variables = [['Currency'], ['Time Buckets']]

def ael_custom_dialog_show(shell, params):
    dialogData = FUxUtils.UnpackInitialData(params)
    customDlg = myCustomDialog()
    customDlg.AddParameters(dialogData)
    return acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )
        
def ael_custom_label( parameters, dictExtra ):
    return parameters.At('Currency')

def instrumentGetDates(instruments):
    dates = []
    for instrument in instruments:
        dates.append(instrument.LastIRSensDay())
    dates.sort()
    return dates

def objectIRYDelta(advancedHedgeModeEnabled, object, timeBuckets, calcSpace, filterCurrency, deltaFxRate):
    delta = []
    dict = {}
    dict['curveFilterCurrency'] = filterCurrency

    if advancedHedgeModeEnabled:
        dict['timeBuckets'] = timeBuckets
    else:
        dict['timeBuckets'] = HedgeCalculationSpace.create_timebuckets(timeBuckets)
    dvArray = object.Calculation().InterestRateYieldDeltaBucketsParams(calcSpace, dict).Value()
    for dv in dvArray:
        delta.append(dv.Number() * deltaFxRate)
    return delta

def objectFxRate(object, calcSpace, deltaCurrency):
    deltaValueCurrency = object.Currency()
    if deltaValueCurrency != deltaCurrency:
        deltaFxRate = deltaValueCurrency.Calculation().FXRate(calcSpace, deltaCurrency).Value()
        if deltaFxRate.Number() != 0.0:
            return deltaFxRate.Number()
    return 1.0
    
def generateMatrix(timeBuckets, currency, shortVolatility, longVolatility, shortCorrelation, longCorrelation):
    calcSpace = HedgeCalculationSpace.scsc
    irCurveInformation = currency.Calculation().MappedDiscountCurve(calcSpace)
    rates = []
    valDay = acm.Time.DateNow()
    myMatrixFunction = acm.GetFunction('generateCovarianceMatrix', 7)
    return myMatrixFunction (timeBuckets, irCurveInformation, shortVolatility, longVolatility, shortCorrelation, longCorrelation, valDay)

def ael_custom_dialog_main( parameters, dictExtra ):
    eii = dictExtra.At('customData')
    hedgeDict = eii.ExtensionObject()
    instruments = hedgeDict.At('instruments')
    position = hedgeDict.At('position')
    calcSpace = HedgeCalculationSpace.scsc
    deltaCurrency = None
    
    advancedHedgeModeEnabled = parameters['Advanced Hedge Mode Enabled']
    
    if advancedHedgeModeEnabled:
        timeBuckets = parameters['Time Buckets']
        if not timeBuckets:
            print ('No Time Buckets specified')
            return
        transactionCost = parameters['Transaction Cost']
        shortVolatility = parameters['Short Volatility']
        longVolatility = parameters['Long Volatility']
        shortCorrelation = parameters['Short Correlation']
        longCorrelation = parameters['Long Correlation']        
    else:
        timeBuckets = instrumentGetDates(instruments)
        
    filterCurrency = parameters['Currency']
    
    deltaCurrency = position.Currency()
    if not deltaCurrency:
        mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
        deltaCurrency = mappedValuationParameter().Parameter().AccountingCurrency()
    
    portDelta = objectIRYDelta(advancedHedgeModeEnabled, position, timeBuckets, calcSpace, filterCurrency, 1.0)
    
    hedgeDelta = []
    for instrument in instruments:
        deltaFxRate = objectFxRate(instrument, calcSpace, deltaCurrency)
        hedgeDelta.append(objectIRYDelta(advancedHedgeModeEnabled, instrument, timeBuckets, calcSpace, None, deltaFxRate))
        
    if advancedHedgeModeEnabled:
        covariancMatrix = generateMatrix(timeBuckets, deltaCurrency, shortVolatility, longVolatility, shortCorrelation, longCorrelation)
            
        myHedge = acm.GetFunction('hedge', 4)
        quantities = myHedge(portDelta, hedgeDelta, covariancMatrix, transactionCost)
        return quantities
    else:
        myHedge = acm.GetFunction('hedge', 3)
        quantities = myHedge(portDelta, hedgeDelta, None)
        return quantities
