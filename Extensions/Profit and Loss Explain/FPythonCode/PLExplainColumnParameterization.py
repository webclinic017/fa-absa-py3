
import FUxUtils
import FUxCore
import acm

from ColumnParameterization import ColumnParameterizationDialog

class PLExplainColumnParameterizationDialog(ColumnParameterizationDialog):
        
    def HandleCreate(self, dlg, layout):
        ColumnParameterizationDialog.HandleCreate( self, dlg, layout )
        
        #Volatility Time Buckets
        try:
            for control in self._flatControls():
                if str(control.Name()) in ["PortfolioProfitAndLossExplainVolatilityTimeBucketsFromStructure", "PortfolioProfitAndLossExplainVolatilityTimeBuckets"]:
                    control.AddChangedCallback( self.UpdateControls, layout )
        except Exception:
            pass

        self.UpdateControls()

    def OkButtonEnabled( self ):
        return ColumnParameterizationDialog.OkButtonEnabled( self ) and self.m_okButtonEnabled
        
    def UpdateControls(self, *args, **kwargs):

        #Volatility Time Buckets
        tbCtrl = None
        tbFromStructure = None
        tb = None
        for control in self._flatControls():
            control_name = str(control.Name())
            value = control.GetValue()
            if control_name == "PortfolioProfitAndLossExplainVolatilityTimeBucketsFromStructure":
                tbFromStructure = value
            elif control_name == "PortfolioProfitAndLossExplainVolatilityTimeBuckets":
                tb = value
                tbCtrl = control
        
        if tbCtrl:
            tbCtrl.Enabled(tbFromStructure == False)
            if tbFromStructure:
                tbCtrl.Clear()

        self.m_okButtonEnabled = tb is not None or tbFromStructure
        ColumnParameterizationDialog.UpdateControls( self )
            
    def _initalControlValues(self):
        params = self.m_parameters.At(acm.FSymbol('columnParameterNamesAndInitialValues'))
        if not params:
            return {acm.FSymbol("PortfolioProfitAndLossExplainVolatilityTimeBucketsFromStructure") : True}
        return params


def ael_custom_dialog_show(shell, params):
    dlg = PLExplainColumnParameterizationDialog(FUxUtils.UnpackInitialData(params))
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    
def ael_custom_dialog_main(parameters, dictExtra):
    return parameters
