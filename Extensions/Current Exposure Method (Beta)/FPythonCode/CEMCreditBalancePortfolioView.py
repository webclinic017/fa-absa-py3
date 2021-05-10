import acm
from CreditBalancePortfolioView import CreditBalancePortfolioMenuItem, CreditBalancePortfolioView

DEFAULT_COLUMN_IDS = ['CEM Asset Class', 'CEM Maturity Bucket', 'CEM Maturity', 'CEM Rating', 'CEM Add-On Factor', 'CEM Notional']

#-------------------------------------------------------------------------
def CreateCreditBalancePortfolioMenuItem(extObj):
    return CreditBalancePortfolioMenuItem(extObj, 'CEM Viewer', 'cemCreditBalancePortfolioViewDockWindow', 'cemCreditBalancePortfolioView')

#-------------------------------------------------------------------------
def CreateCreditBalancePortfolioView(eii) :
    basicApp = eii.ExtensionObject()
    myPanel = CreditBalancePortfolioView(basicApp, DEFAULT_COLUMN_IDS)
    return myPanel

#-------------------------------------------------------------------------
def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    basicApp.RegisterDockWindowType('cemCreditBalancePortfolioViewDockWindow', 'CEMCreditBalancePortfolioView.CreateCreditBalancePortfolioView')

