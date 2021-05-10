import acm


def QueryAttributeIssuanceType(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.Instrument.IssuanceType")


def QueryAttributeCounterparty(ssi):
    return ssi.DisplayStringForQueryAttribute("Counterparty.Name")


def QueryAttributeAcquirer(ssi):
    return ssi.DisplayStringForQueryAttribute("Acquirer.Name")


def QueryAttributeInstrumentType(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.Instrument.InsType")


def QueryAttributeUnderlyingInstrumentType(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.Instrument.Underlying.InsType")


def QueryAttributeCurrency(ssi):
    return ssi.DisplayStringForQueryAttribute("Currency.Name")


def QueryAttributeTradeSettleCategory(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.SettleCategoryChlItem.Name")


def QueryAttributeInstrumentSettleCategory(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.Instrument.SettleCategoryChlItem.Name")


def QueryAttributeCashFlowType(ssi):
    return ssi.DisplayStringForQueryAttribute("Type")


def QueryAttributeInstrumentOtc(ssi):
    return ssi.DisplayStringForQueryAttribute("Trade.Instrument.Otc")


def QueryAttributeSL_G1PartyCode(ssi):
    return ssi.DisplayStringForQueryAttribute("Acquirer.AdditionalInfo.SL_G1PartyCode")
