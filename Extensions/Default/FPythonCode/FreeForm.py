import acm
from DealPackageDevKit import DealPackageDefinition, Settings, NoTradeActions

@NoTradeActions
@Settings(IncludeTradeActionTrades=True)
class FreeFormDefinition(DealPackageDefinition):
    def IsValid(self, exceptionAccumulator, aspect):
        pass
