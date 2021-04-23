""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/etc/FRegulatoryInfoHelper.py"

import acm

def AddToOtcPostTradeIndicator(tradeRegInfo, additionalOptions):
    otcPti = tradeRegInfo.OtcPostTradeIndicatorString()
    if len(otcPti):
        otcPti = otcPti + "," + additionalOptions
        tradeRegInfo.OtcPostTradeIndicatorString(otcPti)
    else:
        tradeRegInfo.OtcPostTradeIndicatorString(additionalOptions)
    return


def CfiCode(insRegInfo):
    print("FRegulatoryInfoHelper::CfiCode")
    insRegInfo.CfiCode("AAA123")
    return


def DefaultValuesInstrument(insRegInfo):
    print("FRegulatoryInfoHelper::DefaultValuesInstrument")
    instrument = insRegInfo.Instrument()

    return


def DefaultValuesTrade(tradeRegInfo):
    print("FRegulatoryInfoHelper::DefaultValuesTrade")
    trade = tradeRegInfo.Trade()
    instrument = trade.Instrument()
    insRegInfo = instrument.RegulatoryInfos().First()
    
    if not tradeRegInfo.OurOrganisation():
        if trade.Acquirer():
            tradeRegInfo.OurOrganisation(trade.Acquirer())

    if not tradeRegInfo.TheirTrader():
        if trade.Counterparty():
            counterparty = trade.Counterparty()
            tradeRegInfo.TheirOrganisation(counterparty)
            if trade.YourRef():
                st = 'party=%s and fullname="%s"' % (counterparty.Oid(), trade.YourRef())
                contacts = acm.FContact.Select(st)
                if contacts.Size():
                    contact = contacts.First()
                    tradeRegInfo.TheirTrader(contact)

    if insRegInfo.SizeSpecificToInstrument():
        otcPtiNotSet = tradeRegInfo.OtcPostTradeIndicator() == 0
        if instrument.ContractSize() > insRegInfo.SizeSpecificToInstrument():
            if not tradeRegInfo.WaiverString():
                tradeRegInfo.WaiverString("SIZE")
            if otcPtiNotSet:
                tradeRegInfo.OtcPostTradeIndicatorString("SIZE")
        if insRegInfo.LargeInScale():
            if instrument.ContractSize() >= insRegInfo.LargeInScale():
                if otcPtiNotSet:
                    AddToOtcPostTradeIndicator(tradeRegInfo, "LRGS")
        if trade.DealPackage() or trade.Contract():
            if otcPtiNotSet:
                AddToOtcPostTradeIndicator(tradeRegInfo, "TPAC")

    return


