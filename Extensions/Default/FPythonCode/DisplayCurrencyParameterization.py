
import FUxUtils
import FUxCore
import acm

from ColumnParameterization import ColumnParameterizationDialog

aggCurrChoicePopulator = acm.FChoiceListPopulator()
aggCurrChoicePopulator.SetChoiceListSource(['Accounting Curr', 'Portfolio Curr', 'Fixed Curr'])

histFxChoicePopulator = acm.FChoiceListPopulator()
histFxDayPopulator = acm.FChoiceListPopulator()
histFxCurrencyPopulator = acm.FChoiceListPopulator()
tradePlLevelPopulator = acm.FChoiceListPopulator()

histFxChoicePopulator.SetChoiceListSource(['None', 'Payment Date', 'RPL Date', 'None, Exclude FX Payment', 'Payment Date FX Matching'])
histFxDayPopulator.SetChoiceListSource(['Trade Time', 'Pay Day', 'Pay Day Unadjusted', 'Trade Time - 1d'])
histFxCurrencyPopulator.SetChoiceListSource(['Portfolio Curr', 'Instrument Curr', 'Accounting Curr'])
tradePlLevelPopulator.SetChoiceListSource(['Trade', 'Tax Lot'])

class DisplayCurrencyParameterizationDialog(ColumnParameterizationDialog):
        
    def HandleCreate(self, dlg, layout):
        ColumnParameterizationDialog.HandleCreate( self, dlg, layout )
        
        # Display curreny
        displayCurrencyControlsNames = ["AggCurrChoice", "PosCurrChoice", "FixedCurr"]
        try:        
            displayCurrencyControls = [layout.GetControl(name) for name in displayCurrencyControlsNames]
        except Exception:
            displayCurrencyControls = []

        for control in displayCurrencyControls:
            control.AddCallback("Changed", self.UpdateControls, None)
        
        histFxControlsNames = ["HistoricalFxChoice", "HistoricalFxDay", "HistoricalFxCurrency"]
        
        # Historical FX
        try:        
            histFxControls = [layout.GetControl(name) for name in histFxControlsNames]
        except Exception:
            histFxControls = []

        for control in histFxControls:
            control.AddCallback("Changed", self.UpdateControls, None)
        
        self.UpdateControls()
        
        try:
            tradePlLevel = layout.GetControl('TradePlLevel')
            sheetClassName = self.m_parameters.At( acm.FSymbol('sheetClassName') )
            tradePlLevel.Visible( sheetClassName == acm.FSymbol('FTradeSheet') )
        except Exception:
            pass
        

    def OkButtonEnabled( self ):
        return ColumnParameterizationDialog.OkButtonEnabled( self ) and self.m_okButtonEnabled
        
    def UpdateControls(self, *args, **kwargs):        
        # Display currency
        aggrCurrencyChoice = None
        posCurrChoice = None
        fixedCurrCtrl = None
        fixedCurr = None
        
        for control in self._flatControls():
            control_name = str(control.Name())
            value = control.GetValue()
            
            if control_name == "AggCurrChoice":
                aggrCurrencyChoice = value
            elif control_name == "PosCurrChoice":
                posCurrChoice = value
            elif control_name == "FixedCurr":
                fixedCurr = value
                fixedCurrCtrl = control
        
        if fixedCurrCtrl is not None:
            if ("Fixed Curr" not in [aggrCurrencyChoice, posCurrChoice]):
                fixedCurrCtrl.Enabled(False)
                fixedCurrCtrl.Clear()
            else:
                fixedCurrCtrl.Enabled(True)
        
        isFixedCurrMissing = ("Fixed Curr" in [aggrCurrencyChoice, posCurrChoice] and fixedCurr is None)

        histFxChoice = None
        histFxDay = None
        histFxCurrency = None
    
        # Historical FX
        for control in self._flatControls():
            control_name = str(control.Name())
            value = control.GetValue()
            
            if control_name == "HistoricalFxChoice":
                histFxChoice = value
            elif control_name == "HistoricalFxDay":
                histFxDay = value
                histFxDayControl = control
            elif control_name == "HistoricalFxCurrency":
                histFxCurrency = value
                histFxCurrencyControl = control

        if histFxChoice:
            if "None" in str(histFxChoice):
                histFxDayControl.Enabled(False)
                histFxCurrencyControl.Enabled(False)
                histFxDayControl.Clear()
                histFxCurrencyControl.Clear()
            else:
                histFxDayControl.Enabled(True)
                histFxCurrencyControl.Enabled(True)
        
        case1 = ('None' in str(histFxChoice) and histFxChoice is not None) or not any([histFxChoice, histFxDay, histFxCurrency])
        case2 = ('None' not in str(histFxChoice) and histFxChoice is not None) and all([histFxDay, histFxCurrency])
        
        self.m_okButtonEnabled = not(isFixedCurrMissing) and (case1 or case2)
        ColumnParameterizationDialog.UpdateControls( self )
            
    def _customPopulator( self, columnParameterDefinition ):
    
        if not columnParameterDefinition:
            return None
        # Display currency
        if str(columnParameterDefinition.Name()) == "AggCurrChoice":
            return aggCurrChoicePopulator
            
        # Historical FX
        if str(columnParameterDefinition.Name()) == "HistoricalFxChoice":
            return histFxChoicePopulator
        if str(columnParameterDefinition.Name()) == "HistoricalFxDay":
            return histFxDayPopulator
        if str(columnParameterDefinition.Name()) == "HistoricalFxCurrency":
            return histFxCurrencyPopulator
        
        # Trade P/L Level
        if str(columnParameterDefinition.Name()) == "TradePlLevel":
            return tradePlLevelPopulator
        
        return None

def ael_custom_dialog_show(shell, params):
    dlg = DisplayCurrencyParameterizationDialog(FUxUtils.UnpackInitialData(params))
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    
def ael_custom_dialog_main(parameters, dictExtra):
    return parameters
