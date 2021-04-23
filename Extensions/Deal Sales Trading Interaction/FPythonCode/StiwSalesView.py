import acm
import FIntegratedWorkbench
import StiwUtils
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem


def ReloadWorkbench():
    import StiwEvents
    reload(StiwEvents)
    import StiwHandler
    reload(StiwHandler)
    import StiwUtils
    reload(StiwUtils)
    import StiwCustomization
    reload(StiwCustomization)
    import StiwQuoteRequestSubscriber
    reload(StiwQuoteRequestSubscriber)
    import StiwNotifyUserOnQuoteRequestUpdate
    reload(StiwNotifyUserOnQuoteRequestUpdate)
    import StiwSheets
    reload(StiwSheets)
    import StiwMenuCommands
    reload(StiwMenuCommands)
    import StiwWorkbookPanel
    reload(StiwWorkbookPanel)
    import StiwClientInformationPanel
    reload(StiwClientInformationPanel)
    
    
def EnsureMarketConnection():
    market = StiwUtils.Market()
    if not market.IsConnected():
        market.Connect(1000)

class StiwSalesViewMenuItem(IntegratedWorkbenchMenuItem):
    
    WORKBOOK = 'Sales Trading Interaction Workbench'

    def __init__(self, extObj):
        IntegratedWorkbenchMenuItem.__init__(self, extObj,
            view='StiwSalesView')

    def Enabled(self):
        return True

    def Invoke(self, eii):
        try:
            ReloadWorkbench()
        except ImportError as e:
            print ('Error reloading workbench:', e)
        try:
            EnsureMarketConnection()
            self.StartView()
        except Exception as e:
            print ('Error loading workbench:', e)
            
    def StartView(self):
        # TODO: Hack to workaround FQuoteRequestPriceSheet not being able to be created
        # by the integrated workbench on initialisation:
        wb = acm.FWorkbook.Select01('name="' + self.WORKBOOK + '" and user=None', None)
        if wb:
            acm.StartApplication('Trading Manager', wb)
        else:
            FIntegratedWorkbench.LaunchView(self._view)


def CreateSalesViewMenuItem(eii):
    return StiwSalesViewMenuItem(eii)

