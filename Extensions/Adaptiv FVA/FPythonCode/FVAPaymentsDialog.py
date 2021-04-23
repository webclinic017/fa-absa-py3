""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/FVAPaymentsDialog.py"
from __future__ import print_function
import acm
import FUxCore
from FVAUtils import FVAAttributeMapper, FVAStateChartConstants
import traceback
import sys

PAYMENT_KEYS = FVAStateChartConstants.PAYMENT_KEYS


def get_exception():
    """
    Returns last exception as string
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    d = traceback.format_exception(exc_type, exc_value, exc_traceback)
    msg = ''.join(d)
    return msg

def OnAssignButtonClicked(self, arg):
    self.m_dlg.CloseDialogOK()

class SafeResetOfUpdateInProgress():
    def __init__(self, dialog):
        self.m_dialog = dialog
    def __enter__(self):
        self.m_dialog.m_updateInProgress = True
    def __exit__(self, type, value, traceback):
        self.m_dialog.m_updateInProgress = False


class FVAPaymentsDialog( FUxCore.LayoutDialog ):
    def __init__( self, shell ):
        self.m_updateInProgress    = False
        self.m_shell               = shell
        self.m_spaceCollection     = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        self.m_paymentsDict        = acm.FDictionary()
        
        self.m_notes = None
        self.m_uxNotesLabel = None

        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        formatterTwo = acm.FNumFormatter('').Clone()
        formatterTwo.NumDecimals(2)
        formatterSix = acm.FNumFormatter('').Clone()
        formatterSix.NumDecimals(6)
        
        self.m_serverCurrName           = None
        self.m_serverAmountLabelCtrl    = None
        self.m_serverAmountCalcBinding  = self.m_bindings.AddBinder('serverAmountCalc', acm.GetDomain('double'), formatterTwo)
        self.m_serverAmountCalcValue    = 0.0
        self.m_serverAmountModBinding   = self.m_bindings.AddBinder('serverAmountMod', acm.GetDomain('double'), formatterTwo)
        self.m_serverAmountModValue     = 0.0
        allCurrencies                   = acm.FCurrency.Select('').AsList()
        self.m_currBinding              = self.m_bindings.AddBinder('currency', acm.GetDomain('FCurrency'), None, allCurrencies)
        self.m_currObject               = None
        self.m_currCalcBinding          = self.m_bindings.AddBinder('currCalc', acm.GetDomain('double'), formatterSix)
        self.m_currCalcValue            = 0.0 
        self.m_clientAmountLabelCtrl    = None
        self.m_clientAmountCalcBinding  = self.m_bindings.AddBinder('clientAmountCalc', acm.GetDomain('double'), formatterTwo)
        self.m_clientAmountCalcValue    = 0.0
        self.m_clientAmountModBinding   = self.m_bindings.AddBinder('clientAmountMod', acm.GetDomain('double'), formatterTwo)
        self.m_clientAmountModValue     = 0.0
        
        return

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      AddLabel('notesLabel', 'Notes:')
        b.      AddText('notes', 200, 100)
        b.      BeginHorzBox()
        b.              BeginVertBox()
        b.                      AddLabel('serverAmountLabel', 'FVA ( XYZ ) ')
        self.                   m_currBinding.BuildLayoutPart(b, 'Currency')
        b.                      AddLabel('clientAmountLabel', 'FVA ( XYZ ) ')
        b.              EndBox()
        b.              BeginVertBox()
        self.                   m_serverAmountCalcBinding.BuildLayoutPart(b, None)
        self.                   m_currCalcBinding.BuildLayoutPart(b, None)
        self.                   m_clientAmountCalcBinding.BuildLayoutPart(b, None)
        b.              EndBox()
        b.              BeginVertBox()
        self.                   m_serverAmountModBinding.BuildLayoutPart(b, None)
        b.                      AddLabel('fillLabel', '')
        self.                   m_clientAmountModBinding.BuildLayoutPart(b, None)
        b.              EndBox()
        b.      EndBox() 
        b.      BeginHorzBox()
        b.              AddFill()
        b.              AddButton('assign', 'Assign')
        b.              AddButton('cancel', 'Cancel')
        b.      EndBox()
        b.EndBox()
        return b

    def OnServerAmountChanged( self, value ):
        if value is None:
            self.m_serverAmountModValue = self.m_serverAmountCalcValue
        else:
            self.m_serverAmountModValue = value

        self.m_clientAmountModValue  = self.m_currCalcValue * self.m_serverAmountModValue
        
        self.UpdateControls()
        return

    def OnCurrencyChanged( self, currency ):
        self.m_currObject            = currency
        self.m_currCalcValue         = self.GetFxRate()
        self.m_clientAmountCalcValue = self.m_currCalcValue * self.m_serverAmountCalcValue
        self.m_clientAmountModValue  = self.m_currCalcValue * self.m_serverAmountModValue
        
        self.UpdateControls()
        return

    def OnClientAmountChanged( self, value ):
        if value is None:
            self.m_clientAmountModValue = self.m_clientAmountCalcValue
        else:
            self.m_clientAmountModValue = value

        if self.m_currCalcValue:
            self.m_serverAmountModValue = self.m_clientAmountModValue / self.m_currCalcValue
        else:
            self.m_serverAmountModValue = 0.0
        self.UpdateControls()
        return

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        try:
            if str(aspectSymbol) == 'ControlValueChanged':
                if not self.m_updateInProgress:
                    if parameter == self.m_serverAmountModBinding:
                        with SafeResetOfUpdateInProgress(self):
                            self.OnServerAmountChanged( self.m_serverAmountModBinding.GetValue() )
                    if parameter == self.m_clientAmountModBinding:
                        with SafeResetOfUpdateInProgress(self):
                            self.OnClientAmountChanged( self.m_clientAmountModBinding.GetValue() )
                    if parameter == self.m_currBinding:
                        with SafeResetOfUpdateInProgress(self):
                            self.OnCurrencyChanged( self.m_currBinding.GetValue() )
        except Exception as e:
            print(get_exception())
            

    def HandleApply( self, *args ):
        mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
        #cvaCalculationType = mappedValuationParameter().Parameter().CvaCalculationType()
        
        self.m_paymentsDict.AtPut(PAYMENT_KEYS.PAYMENT_TYPE,              float( self.m_clientAmountModValue ))
        self.m_paymentsDict.AtPut(PAYMENT_KEYS.PAYMENT_CURRENCY,          str( self.m_currObject.Name() ))
        self.m_paymentsDict.AtPut(PAYMENT_KEYS.PAYMENT_ORIGINAL_VALUE,    float( self.m_serverAmountCalcValue ))
        self.m_paymentsDict.AtPut(PAYMENT_KEYS.PAYMENT_ORIGINAL_CURRENCY, str( self.m_serverCurrName ) )
        self.m_paymentsDict.AtPut(PAYMENT_KEYS.FX_RATE,                   float( self.m_currCalcValue ) )
        #self.m_paymentsDict.AtPut(PAYMENT_KEYS.CALCULATION_TYPE,          str( cvaCalculationType ) )
        
        return True

    def HandleCancel( self ):
        return True
        
    def HandleCreate( self, dlg, layout ):

        try:
            self.m_serverCurrName, self.m_serverAmountCalcValue = self._suggestFVA()
            
            self.m_dlg = dlg
            
            dlg.Caption( 'FVA Charge' )
            self.m_bindings.AddLayout(layout)

            self.m_notesLabelCtrl = layout.GetControl( 'notesLabel' )
            self.m_notesLabelCtrl.Visible( bool(self.m_notes) )
            
            self.m_notesCtrl = layout.GetControl( 'notes' )
            self.m_notesCtrl.Visible( bool(self.m_notes) )
            self.m_notesCtrl.Editable( False )

            self.m_uxAssignBtn = layout.GetControl( 'assign' )
            self.m_uxAssignBtn.AddCallback('Activate', OnAssignButtonClicked, self)

            self.m_serverAmountLabelCtrl = layout.GetControl( 'serverAmountLabel' )
            self.m_clientAmountLabelCtrl = layout.GetControl( 'clientAmountLabel' )

            self.m_currObject = acm.FCurrency[ acm.UsedAccountingCurrency().AsString() ]
            self.m_serverAmountModValue  = self.m_serverAmountCalcValue
            self.m_currCalcValue         = self.GetFxRate()
            self.m_clientAmountCalcValue = self.m_currCalcValue * self.m_serverAmountCalcValue
            self.m_clientAmountModValue  = self.m_currCalcValue * self.m_serverAmountModValue

            self.m_serverAmountCalcBinding.Enabled( False )
            self.m_currCalcBinding.Enabled( False )
            self.m_clientAmountCalcBinding.Enabled( False )
            with SafeResetOfUpdateInProgress(self):
                self.UpdateControls()
        except Exception as e:
            print(get_exception())

        return
        
    def GetFxRate( self ):
        serverCurr = acm.FCurrency[ self.m_serverCurrName ]
        return serverCurr.Calculation().FXRate(self.m_spaceCollection, self.m_currObject).Number()
                
        
    def UpdateControls(self):
        self.m_notesCtrl.SetData( self.m_notes )
        serverCurrLabel = 'FVA ( %s )' % self.m_serverCurrName
        self.m_serverAmountLabelCtrl.Label( serverCurrLabel )
        self.m_serverAmountCalcBinding.SetValue( self.m_serverAmountCalcValue )
        self.m_serverAmountModBinding.SetValue( self.m_serverAmountModValue )
        
        self.m_currBinding.SetValue( self.m_currObject )
        self.m_currCalcBinding.SetValue( self.m_currCalcValue )
        
        clientCurrLabel = 'FVA ( %s )' % self.m_currObject.Name()
        self.m_clientAmountLabelCtrl.Label( clientCurrLabel )
        self.m_clientAmountCalcBinding.SetValue( self.m_clientAmountCalcValue )
        self.m_clientAmountModBinding.SetValue( self.m_clientAmountModValue )
        
        return
        
    def _suggestFVA( self ):
        fvaCurr = ''
        fvaAmount = None
                
        try:
            denomValue = self.m_mapper.GetIncrementalFVA( self.m_trade )
            fvaAmount = denomValue.Number()
            fvaCurr = str(denomValue.Unit())
        except Exception as e:
            print('Exception:', e)
            fvaCurr = self.m_trade.CreditBalance().Currency().Name()
            fvaAmount = 0.0
        
        return (fvaCurr, fvaAmount)

    def ShowFVAPaymentsDialog( self, trade, notes='' ):
        self.m_trade      = trade
        self.m_notes      = notes
        self.m_mapper = FVAAttributeMapper()
        builder = self.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialogModal(self.m_shell, builder, self)
        
        return self.m_paymentsDict


class FVAReRequestPaymentsDialog( FUxCore.LayoutDialog ):
    def __init__(self, shell):
        self.m_shell    = shell
        self.m_uxReason = None
        self.m_paymentsDict = {}
        self.m_reasonText = ''

    def HandleApply( self, *args ):
        self.m_reasonText = self.m_uxReason.GetData().strip()
        return bool(self.m_reasonText)
        
    def HandleCancel( self ):
        self.m_reasonText = ''
        return True

    def HandleCreate( self, dlg, layout ):
        dlg.Caption( 'Request FVA Charge' )
        
        self.m_uxOkBtn = layout.GetControl( 'ok' )
        self.m_uxOkBtn.Enabled(False)
        
        self.m_uxReason = layout.GetControl( 'reason' )
        self.m_uxReason.AddCallback( 'Changed', self._OnReasonUpdated, None )
        
    def _OnReasonUpdated( self, _arg1, _arg2 ):
        self.m_uxOkBtn.Enabled( len(self.m_uxReason.GetData().strip()) > 0 )
        

    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      AddLabel('reasonLabel', 'Request Reason:')
        b.      AddText('reason', 400, 200)
        b.      BeginHorzBox()
        b.              AddFill()
        b.              AddButton('ok', 'OK')
        b.              AddButton('cancel', 'Cancel')
        b.      EndBox()
        b.EndBox()
        return b

    def ShowFVAReRequestPaymentsDialog( self ):
        builder = self.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialogModal( self.m_shell, builder, self )
        
        return self.m_reasonText
