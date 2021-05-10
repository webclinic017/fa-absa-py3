""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AADealsXMLCreator.py"
def appendInstrumentDealXML(dealXMLArray, instrumentDealString):
    dealXMLArray.append('<Deal>')
    dealXMLArray.append(instrumentDealString)
    dealXMLArray.append('</Deal>')

def createCreditBalanceDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments):
    nettingSetXMLIntro = ''.join(['<Deal>', nettingSetString, '<Deals>'])
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

def createDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments):
    dealXMLArray = ['<Deals>']
    dealXMLArray.append(createCreditBalanceDealsXML(dealStrings, nettingSetString, nettingBetweenInstruments, instruments))
    dealXMLArray.append('</Deals>')
    return ''.join(dealXMLArray)

def createPFEDealsXML(creditBalanceDealsXMLArray):
    dealXMLArray = []
    dealXMLArray.append('<Deals>')
    for creditBalanceDealsXML in creditBalanceDealsXMLArray:
        dealXMLArray.append(creditBalanceDealsXML)
    dealXMLArray.append('</Deals>')
    return ''.join(dealXMLArray)
