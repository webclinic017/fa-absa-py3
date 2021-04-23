

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
from CurrSplitBaseDialog import *
logme = FBDPString.logme

scriptName = 'Currency Split'

# For FX positions
class FXPosDecompDialog( BasePosDecompDialog ):
    def ToPairDomain(self):
        return acm.GetDomain('FCurrencyPair')

    def ToInstrumentPairs(self):
        return [cp for cp in self.RowCurrencyPair().AllTriangulatingInstrumentPairs() if (cp != self.RowCurrencyPair())]

    def BreakEvenRateForSelectedPosition( self ):
        projectedPaymentForCurr1, projectedPaymentForCurr2 = self.ProjectedPayments()
        if projectedPaymentForCurr1 and projectedPaymentForCurr2:
            return fabs(projectedPaymentForCurr2 / projectedPaymentForCurr1)
        return 0

    def GetAmount2( self ):
	rate = self.GetCtrlValueOrZero('FromPairRate')
	amount1 = self.GetCtrlValueOrZero('Amount1')
	if self.SelectedInstrument() == self.RowCurrency1():
		return - amount1 * rate
	elif rate:
		return - amount1 / rate
	return 0.0        

    def Rate(self, insPair, date):
        return FxRate(insPair, date)    


def StartDialog( invocationInfo ):
    logme.setLogmeVar(scriptName, 1, 1, 0, None, 0, 0, 0)
    shell = invocationInfo.ExtensionObject().Shell()
    activeSheet = invocationInfo.ExtensionObject().ActiveSheet()
    customDialog = 0
    
    if DetermineIfFx(activeSheet) == StartFXPositionMoveSplit:
        customDialog = FXPosDecompDialog(activeSheet)
    else:
        print ("Not supported!")
        
    message = customDialog.ErrorMessageIfInvalid()
    if message:
        acm.UX().Dialogs().MessageBoxInformation(shell, message)
        return

    builder = customDialog.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDialog)



    


