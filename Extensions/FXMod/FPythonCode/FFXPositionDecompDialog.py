

import acm
import FUxCore
from math import floor
from math import log10
from math import fabs
import FBDPRollback
import FBDPString
from PositionDecompCallBackFuncs import *
from PositionDecompHelpFuncs import *
from PositionDecompCreateTrades import *
from PositionDecompBasePosDecompDialog import *
logme = FBDPString.logme

scriptName = 'Position Move/Split'

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
    
# For PM positions
class PMPosDecompDialog( BasePosDecompDialog ):

    def ToPairDomain(self):
        return acm.GetDomain('FPreciousMetalPair')

    def ToInstrumentPairs(self):
        return [cp for cp in self.RowCurrencyPair().AllTriangulatingPreciousMetalPairs() if (cp != self.RowCurrencyPair())]

    def BreakEvenRateForSelectedPosition( self ):
        projectedPaymentForCurr1, projectedPaymentForCurr2 = self.ProjectedPayments()
        commodityContractSize = self.RowCurrency1().ContractSizeInQuotation()
        if projectedPaymentForCurr1 and projectedPaymentForCurr2:            
            return fabs(projectedPaymentForCurr2 / (projectedPaymentForCurr1 * commodityContractSize))
        return 0

    def GetAmount2( self ):
        rate = self.GetCtrlValueOrZero('FromPairRate')
        amount1 = self.GetCtrlValueOrZero('Amount1')
        commodityQuantity = self.GetCtrlValueOrZero('Amount1')
	commodityContractSize = self.RowCurrency1().ContractSizeInQuotation()
        if self.SelectedInstrument() == self.RowCurrency1():
            return - amount1 * rate * commodityContractSize
        elif rate:
            return - amount1 / (rate * commodityContractSize)
        return 0.0
    
    def Rate(self, insPair, date):
        return PMRate(insPair, date)
    

def StartDialog( invocationInfo ):
    logme.setLogmeVar(scriptName, 1, 1, 0, None, 0, 0, 0)
    shell = invocationInfo.ExtensionObject().Shell()
    activeSheet = invocationInfo.ExtensionObject().ActiveSheet()
    customDialog = 0
    
    if DetermineIfFxOrPreciousMetal(activeSheet) == StartFXPositionMoveSplit:
        customDialog = FXPosDecompDialog(activeSheet)
    elif DetermineIfFxOrPreciousMetal(activeSheet) == StartPMPositionMoveSplit:
        customDialog = PMPosDecompDialog(activeSheet)
    elif DetermineIfFxOrPreciousMetal(activeSheet) == 0:
        print ("Not supported!")
        
    message = customDialog.ErrorMessageIfInvalid()
    if message:
        acm.UX().Dialogs().MessageBoxInformation(shell, message)
        return

    builder = customDialog.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDialog)



    


