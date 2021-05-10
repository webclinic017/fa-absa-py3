import acm
from DealPackageDevKit import DealPackageDefinition, Settings, NoTradeActions

@NoTradeActions
@Settings( GraphApplicable=False,
           SheetApplicable=False )
class TradeActionBase(DealPackageDefinition):
    pass
