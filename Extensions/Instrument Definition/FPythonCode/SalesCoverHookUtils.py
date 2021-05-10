import acm

def IsFixedDeposit(artifacts):
    for art in artifacts.ArtifactsToBeCommitted():
        if art.IsKindOf(acm.FTrade) and art.TradeInstrumentType() == 'Deposit':
            return art.Instrument().FirstFixedLeg() is not None
            
    return False

def PostAllocateRisk_Deposit(artifacts, args):
    parentTrade = None
    childTrade = None
    for art in artifacts.ArtifactsToBeCommitted():
        if art.IsKindOf(acm.FTrade):
            if art.IsSalesCoverParent():
                parentTrade = art
            elif art.IsSalesCoverChild():
                childTrade = art
    
    if not (parentTrade or childTrade):
        return
        
    childInstrument = childTrade.Instrument()
    fixedLeg = childInstrument.FirstFixedLeg()

    quantityFromEndCash = parentTrade.QuantityFromEndCash(
                                parentTrade.EndCash(),
                                fixedLeg.FixedPrice(),
                                fixedLeg.StartDate(),
                                fixedLeg.EndDate(),
                                fixedLeg.DayCountMethod()
                            )
    childTrade.Quantity(quantityFromEndCash)
    childTrade.Premium(-childTrade.Quantity() * childInstrument.ContractSize())
    fixedLeg.GenerateCashFlows(fixedLeg.FixedPrice(), False, True)
