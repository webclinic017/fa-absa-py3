""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRDealsXMLCreator.py"
def appendInstrumentDealXML(dealXMLArray, instrumentDealString):
    dealXMLArray.append('<Deal>')
    dealXMLArray.append(instrumentDealString)
    dealXMLArray.append('</Deal>')

def createSACCRCreditBalanceDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments):
    nettingSetXMLIntro = ''.join(['<Deal> <Properties>', nettingSetString, '</Properties><Deals>'])
    nettingSetXMLOutro = '</Deals></Deal>'

    creditBalanceDealXMLArray = []
    if nettingBetweenInstruments:
        creditBalanceDealXMLArray.append(nettingSetXMLIntro)
        for instrumentDealStrings in dealStrings:
            for instrumentDealString in instrumentDealStrings:
                appendInstrumentDealXML(creditBalanceDealXMLArray, instrumentDealString)
        creditBalanceDealXMLArray.append(nettingSetXMLOutro)
    else:
        for index in range(len(dealStrings)):
            instrumentDealStrings = dealStrings[index]
            instrument = instruments[index]
            #Special handling for FX Cash according to SPR 368219
            if 'FFxRate' == str(instrument.ClassName()):
                for instrumentDealString in instrumentDealStrings:
                    creditBalanceDealXMLArray.append(nettingSetXMLIntro)
                    appendInstrumentDealXML(creditBalanceDealXMLArray, instrumentDealString)
                    creditBalanceDealXMLArray.append(nettingSetXMLOutro)
            else:
                creditBalanceDealXMLArray.append(nettingSetXMLIntro)
                for instrumentDealString in instrumentDealStrings:
                    appendInstrumentDealXML(creditBalanceDealXMLArray, instrumentDealString)
                creditBalanceDealXMLArray.append(nettingSetXMLOutro)
    return ''.join(creditBalanceDealXMLArray)


def createSACCRDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments):
    dealXMLArray = ['<Deals Tag_Titles=\"Netting ID,Counterparty,AssetClass,CCY Pair,panProduct,IsCounterpartyCCP\">']
    dealXMLArray.append(createSACCRCreditBalanceDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments))
    dealXMLArray.append('</Deals>')
    return ''.join(dealXMLArray)