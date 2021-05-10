import acm
import DealPackageUtil
from RFQUtils import Direction

from SalesTradingCustomizations import DefaultSalesPortfolio
from DealPackageAsDialog import OpenDealPackageDialogWithNoButtons

def StartSalesDialog(shell, content, reOpening, dpName, dialogLabel, initialAttrs=None, wrapDeal=True):
    gui = acm.FBusinessLogicGUIShell()
    gui.SetFUxShell(shell)      
    arguments = acm.FDictionary()
    arguments.AtPut('content', content)
    arguments.AtPut('reOpening', reOpening)
    arguments.AtPut('wrapDeal', wrapDeal)
    dealPackage = acm.DealPackage().NewAsDecorator(dpName, gui, arguments)
    for k in initialAttrs or {}:
        dealPackage.SetAttribute(k, initialAttrs[k])
    dealPackage = OpenDealPackageDialogWithNoButtons(shell, dealPackage, dialogLabel, False)

