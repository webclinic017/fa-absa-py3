import importlib

def doReload():
    import DealPackageUxUtil
    importlib.reload(DealPackageUxUtil)
    DealPackageUxUtil.ReloadAllModules()
    DealPackageUxUtil.ReloadAllModules()

    import ExtensionPointUtil 
    importlib.reload(ExtensionPointUtil)
    import FXOptionPricerExtensionPoint
    importlib.reload(FXOptionPricerExtensionPoint)
    import InstrumentPairFromStrUtil
    importlib.reload(InstrumentPairFromStrUtil)
    import DateFromStrUtil
    importlib.reload(DateFromStrUtil)
    import PairOptionsUtil
    importlib.reload(PairOptionsUtil)
    import OptionTypeFromStrUtil
    importlib.reload(OptionTypeFromStrUtil)
    import PairOptionsDeltaHedge
    importlib.reload(PairOptionsDeltaHedge)
    import PairOptionsB2B
    importlib.reload(PairOptionsB2B)        
    import PairOptionsFormatters
    importlib.reload(PairOptionsFormatters)
    import DealPackageGridViewModelItem
    importlib.reload(DealPackageGridViewModelItem)
    import PairOptionsPricerGridViewModel
    importlib.reload(PairOptionsPricerGridViewModel)
    import FXCalculations
    importlib.reload(FXCalculations)
    import PMCalculations
    importlib.reload(PMCalculations)
    import PairOptionsOneVolatility
    importlib.reload(PairOptionsOneVolatility)
    import PairOptionsDealPackageBase
    importlib.reload(PairOptionsDealPackageBase)
    import StrategyDealPackageBase
    importlib.reload (StrategyDealPackageBase)
    import SinglePairOptionDealPackage
    importlib.reload(SinglePairOptionDealPackage)
    import FxStrategyDealPackageBase
    importlib.reload(FxStrategyDealPackageBase)
    import FXStrategyDualStrikeDealPackageBase
    importlib.reload(FXStrategyDualStrikeDealPackageBase)
    import FXStraddleDealPackage
    importlib.reload(FXStraddleDealPackage)        
    import FXStrangleDealPackage
    importlib.reload(FXStrangleDealPackage)
    import FXRiskReversalDealPackage
    importlib.reload(FXRiskReversalDealPackage)
    import FXCallPutSpreadDealPackage
    importlib.reload(FXCallPutSpreadDealPackage)
    import FXOptionDealPackage
    importlib.reload(FXOptionDealPackage)
    import PmStrategyDealPackageBase
    importlib.reload(PmStrategyDealPackageBase)
    import PMStraddleDealPackage
    importlib.reload(PMStraddleDealPackage)
    import PMStrangleDealPackage
    importlib.reload(PMStrangleDealPackage)
    import PMRiskReversalDealPackage
    importlib.reload(PMRiskReversalDealPackage)
    import PMOptionDealPackage
    importlib.reload(PMOptionDealPackage)
    import PMCallPutSpreadDealPackage
    importlib.reload(PMCallPutSpreadDealPackage)
    import FXStripGenerateLegs
    importlib.reload(FXStripGenerateLegs)
    import FXStripDealPackage
    importlib.reload(FXStripDealPackage)


def ReloadFXDealPackages():
    doReload()
    doReload()
