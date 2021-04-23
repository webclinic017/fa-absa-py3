""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTSecuritiesSettlement.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMTSecuritiesSettlement - Module that implements the functionality
    required for generating 54x series of messages

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

--------------------------------------------------------------------------"""
import acm
import FSwiftMTBase
import FSwiftUtils
import xml.dom.minidom as dom

from FSettlementEnums import SettlementType
from FOperationsEnums import InsType
from FSwiftMTBase import GetOptionValue, GetRelatedEntityMessage, GetFieldValue, GetPartyBic
from FSettlementEnums import RelationType, PartialSettlementType

def Init():
    pass

def CalculateCashAmount(settlement):
    amount = 0
    if settlement.Type() == SettlementType.SECURITY_DVP:
        amount = settlement.CashAmount()
    else:
        amount = _PremiumAmount(settlement)
    curr = settlement.Currency().Name()
    return FSwiftUtils.ApplyCurrencyPrecision(curr, amount)

def GetPartyOption(dummyPartyDetails, settlement):
    if dummyPartyDetails.At('qualifier') in ['BUYR', 'SELL']:
        return 'P'
    elif dummyPartyDetails.At('datasourcescheme') != '':
        return 'R'
    else:
        return GetOptionValue('PARTY', settlement)

def GetPartySafekeepingOption(dummyPartyDetails, settlement):
    return GetOptionValue('SAFEKEEPING_ACCOUNT', settlement)

def GetPartyIdentifierCode(partyDetails):
    return partyDetails['bic']

def GetPartyProprietaryCode(partyDetails):
    return partyDetails['partyproprietarycode']

def GetPartyQualifier(partyDetails):
    return partyDetails['qualifier']

def GetPartyCountryCode(partyDetails):
    return partyDetails['countrycode']

def GetPartyFullName(partyDetails):
    return partyDetails['name']

def GetPartyAddress(partyDetails):
    return partyDetails['address']

def GetPartySafekeepingAccount(partyDetails):
    return partyDetails['safekeepingaccount']

def GetPartySafekeepingQualifier(partyDetails):
    if partyDetails['safekeepingaccount'] != '':
        return 'SAFE'
    else:
        return ''

def GetDataSourceScheme(partyDetails):
    return partyDetails['datasourcescheme']

def GetAccountOption(settlement):
    return GetOptionValue('ACCOUNT', settlement)

def GetAccountNumber(settlement):
    module = GetMTModule(settlement)
    return module.GetAccountNumber(settlement)

def GetAccountQualifier():
    return 'SAFE'

def GetMTModule(settlement):
    mt = FSwiftMTBase.GetSwiftMessageType(settlement)
    moduleName = 'FSwiftMT' + str(mt)
    return __import__(moduleName)

def GetFunctionOfMessage(settlement):
    '''This is a mandatory field 23G in seq A'''

    if IsCancellationSettlement(settlement):
        return 'CANC'
    else:
        return 'NEWM'

def GetLinkageQualifier(settlement):
    if IsCancellationSettlement(settlement):
        return 'PREV'
    else:
        return ''

def GetLinkageReference(settlement):
    if IsCancellationSettlement(settlement):
        return GetRelatedRef(settlement)
    else:
        return ''

def IsCancellationSettlement(settlement):
    isSecuritySettlement = True if settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT] else False
    return isSecuritySettlement

def GetSettlementDatetimeOption(settlement):
    return GetOptionValue('SETTLEMENT_DATETIME', settlement)

def GetSettlementDatetimeQualifier():
    return 'SETT'

def GetSettlementDatetimeDate(settlement):
    return settlement.ValueDay()

def GetTradeDatetimeQualifier():
    return 'TRAD'

def GetTradeDatetimeDate(settlement):
    allDates = set()
    _GetTradeValueDays(settlement, allDates)
    return sorted(allDates, reverse=True).pop()

def GetInstrument(settlement):
    trade = settlement.Trade()
    if trade:
        return trade.Instrument()
    else:
        return settlement.Instrument()

def GetInstrumentISIN(settlement):
    ''' Mandatory field 35B in seq B '''

    instrument = GetInstrument(settlement)
    if instrument.Isin() == "" and instrument.Underlying():
        return 'ISIN ' + instrument.Underlying().Isin()
    else:
        return 'ISIN ' + instrument.Isin()

def GetDescriptionOfSecurity(settlement):
    assert settlement.Instrument(), "Settlement has no security instrument or trade referenced by the settlement has no instrument"
    productType = settlement.Instrument().ProductTypeChlItem()
    if productType:
        return productType.Name()
    else:
        return ''

def GetQuantityTypeCode():
    return 'FAMT'

def GetQuantity(settlement):
    return abs(settlement.Amount())

def GetMandatoryQualifier():
    return 'SETR'

def GetMandatoryIndicator(settlement):
    if settlement.Instrument() != None:
        if ParentOrAllChildrenHaveInstrumentType(settlement, InsType.REPO_REVERSE):
            if settlement.Trade():
                if settlement.Trade().Quantity() >= 0:
                    return 'RVPO'
                else:
                    return 'REPU'
        elif ParentOrAllChildrenHaveInstrumentType(settlement, InsType.SECURITY_LOAN):
            return 'SECL'
        elif ParentOrAllChildrenHaveInstrumentType(settlement, InsType.COLLATERAL):
            if settlement.Amount() >= 0:
                return 'COLI'
            else:
                return 'COLO'

    return 'TRAD'

def GetPartialSettlementTypeQualifier():
    return 'STCO'

def GetQualifier(pair):
    return pair.First()

def GetIndicator(pair):
    return pair.Second()

def GetIndicators(settlement):
    indicatorsList = acm.FList()
    partialSettlementType = settlement.PartialSettlementType()

    if(partialSettlementType != PartialSettlementType.NONE):
        pair = acm.FPair()
        first = acm.FSymbol(GetPartialSettlementTypeQualifier())
        second = acm.FSymbol(partialSettlementType)
        pair.First(first)
        pair.Second(second)
        indicatorsList.Add(pair)

    pair = acm.FPair()
    first = acm.FSymbol(GetMandatoryQualifier())
    second = acm.FSymbol(GetMandatoryIndicator(settlement))
    pair.First(first)
    pair.Second(second)
    indicatorsList.Add(pair)

    return indicatorsList


def ParentOrAllChildrenHaveInstrumentType(settlement, instrumentType):
    parentHasInstrument = False
    if instrumentType == InsType.COLLATERAL:
        if settlement.Trade() != None:
            if settlement.Trade().TradeInstrumentType() == InsType.COLLATERAL:
                parentHasInstrument = True
    else:
        assert settlement.Instrument(), "Settlement has no security instrument or trade referenced by the settlement has no instrument"
        if settlement.Instrument().InsType() == instrumentType:
            parentHasInstrument = True

    if parentHasInstrument:
        return parentHasInstrument

    if len(settlement.Children()) == 0:
        childrenHasInstrument = False
    else:
        childrenHasInstrument = True

    for child in settlement.Children():
        childrenHasInstrument = childrenHasInstrument and ParentOrAllChildrenHaveInstrumentType(child, instrumentType)

    return childrenHasInstrument

def GetPartyDetails(settlement):
    module = GetMTModule(settlement)
    return module.GetPartyDetails(settlement)

def GetRelatedRef(settlement):
    relatedRef = ''
    relatedSettlement = settlement.Children()[0]
    relatedSettlementMessage = GetRelatedEntityMessage(relatedSettlement)
    field = '20C'
    fieldValue = GetFieldValue(relatedSettlementMessage, field)

    start = fieldValue.find("FAS-")
    relatedRef = fieldValue[start:]

    return relatedRef

def GetAmountQualifier():
    ''' Mandatory field 19A in sub seq E3'''

    return 'SETT'

def GetCurrencyCode(settlement):
    assert settlement.CashCurrency(), "Settlement has no cash currency"
    return settlement.CashCurrency().Name()

def GetAmount(settlement):
    return abs(CalculateCashAmount(settlement))

def GetPartyInfo(qualifier, bic, party, account, dataSourceScheme, safekeepingAccount):
    partyInfo = dict()
    partyInfo['qualifier'] = qualifier
    partyInfo['bic'] = bic
    partyInfo['countrycode'] = bic[4:6]
    partyInfo['partyproprietarycode'] = account
    partyInfo['datasourcescheme'] = dataSourceScheme
    partyInfo['name'] = FSwiftMTBase.GetPartyFullName(party)
    partyInfo['address'] = FSwiftMTBase.GetPartyAddress(party)
    partyInfo['safekeepingaccount'] = safekeepingAccount
    return partyInfo

def GetApplicablePartyDetails(option, partyDetails):
    applicablePartyDetails = list()
    for partyInfo in partyDetails:
        applicablePartyInfo = dict.fromkeys(['countrycode', 'bic', 'name', 'address', 'safekeepingaccount', 'datasourcescheme', 'partyproprietarycode'], '')
        applicablePartyInfo['qualifier'] = partyInfo['qualifier']

        if applicablePartyInfo['qualifier'] in ['SELL', 'BUYR']:
            applicablePartyInfo['bic'] = partyInfo['bic']
            applicablePartyInfo['safekeepingaccount'] = partyInfo['safekeepingaccount']
        if option == 'C':
            applicablePartyInfo['countrycode'] = partyInfo['countrycode']
        elif option == 'P':
            if partyInfo['datasourcescheme'] != '':
                applicablePartyInfo['datasourcescheme'] = partyInfo['datasourcescheme']
                applicablePartyInfo['partyproprietarycode'] = partyInfo['partyproprietarycode']
            else:
                applicablePartyInfo['bic'] = partyInfo['bic']
                applicablePartyInfo['safekeepingaccount'] = partyInfo['safekeepingaccount']
        elif option == 'Q':
            applicablePartyInfo['name'] = partyInfo['name']
            applicablePartyInfo['address'] = partyInfo['address']
        applicablePartyDetails.append(applicablePartyInfo)

    return applicablePartyDetails

def _PremiumAmount(settlement):
    if settlement.Trade() != None:
        return settlement.Trade().Premium()
    else:
        amount = 0
        for child in settlement.Children():
            amount = amount + _PremiumAmount(child)
        return amount

def _GetTradeValueDays(settlement, allDates):
    if settlement.Trade():
        allDates.add(acm.Time.AsDate(settlement.Trade().TradeTime()))
    else:
        for s in settlement.Children():
            _GetTradeValueDays(s, allDates)
        if settlement.SplitParent():
            _GetTradeValueDays(settlement.SplitParent(), allDates)

def GetPlaceOfSafekeepingOption():
    return ''

def GetPlaceOfSafekeepingQualifier():
    return ''

def GetPlaceOfSafekeepingPlaceCode():
    return ''

def GetPlaceOfSafekeepingIdentifierCode():
    return ''

def SetInitiatingPartyDetails(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''

    party = account.Party()
    bic = GetPartyBic(account)
    if account.DataSourceScheme():
        dss = account.DataSourceScheme().Alias()
    partyproprietarycode = account.Account()
    partyInfo = GetPartyInfo(qualifier, bic, party, partyproprietarycode if dss != '' else '', dss, partyproprietarycode)
    details.append(partyInfo)

def SetCustodianDetails(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank3():

        if account.DataSourceScheme2():
            partyproprietarycode = account.Account2()
            dss = account.DataSourceScheme2().Alias()
        else:
            if account.Bic():
                bic = account.Bic().Alias()
            safekeepingaccount = account.Account2()
        party = account.CorrespondentBank()

        partyInfo = GetPartyInfo(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
        details.append(partyInfo)

def SetIntermediate1Details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5() or account.CorrespondentBank4():
        if account.CorrespondentBank4():
            if account.DataSourceScheme3():
                partyproprietarycode = account.Account3()
                dss = account.DataSourceScheme3().Alias()
            else:
                if account.Bic2():
                    bic = account.Bic2().Alias()
                safekeepingaccount = account.Account3()
            party = account.CorrespondentBank2()

            partyInfo = GetPartyInfo(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
            details.append(partyInfo)

def SetIntermediate2Details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5():
        if account.CorrespondentBank4() and account.DataSourceScheme4():
            partyproprietarycode = account.Account4()
            dss = account.DataSourceScheme4().Alias()
        else:
            if account.Bic3():
                bic = account.Bic3().Alias()
            safekeepingaccount = account.Account4()
        party = account.CorrespondentBank3()

        partyInfo = GetPartyInfo(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
        details.append(partyInfo)

def SetAgentDetails(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5():
        if account.DataSourceScheme5():
            partyproprietarycode = account.Account5()
            dss = account.DataSourceScheme5().Alias()
        else:
            safekeepingaccount = account.Account5()
            if account.Bic4():
                bic = account.Bic4().Alias()
        party = account.CorrespondentBank4()

    elif account.CorrespondentBank4():
        if account.DataSourceScheme4():
            partyproprietarycode = account.Account4()
            dss = account.DataSourceScheme4().Alias()
        else:
            safekeepingaccount = account.Account4()
            if account.Bic3():
                bic = account.Bic3().Alias()
        party = account.CorrespondentBank3()

    elif account.CorrespondentBank3():
        if account.DataSourceScheme3():
            partyproprietarycode = account.Account3()
            dss = account.DataSourceScheme3().Alias()
        else:
            safekeepingaccount = account.Account3()
            if account.Bic2():
                bic = account.Bic2().Alias()
        party = account.CorrespondentBank2()

    elif account.CorrespondentBank2():
        if account.DataSourceScheme2():
            partyproprietarycode = account.Account2()
            dss = account.DataSourceScheme2().Alias()
        else:
            safekeepingaccount = account.Account2()
            if account.Bic():
                bic = account.Bic().Alias()
        party = account.CorrespondentBank()

    elif account.CorrespondentBank():
        if account.DataSourceScheme():
            partyproprietarycode = account.Account()
            dss = account.DataSourceScheme().Alias()
        else:
            safekeepingaccount = account.Account()
            if account.NetworkAlias():
                bic = account.NetworkAlias().Alias()
        party = account.CorrespondentBank()

    partyInfo = GetPartyInfo(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
    details.append(partyInfo)

def SetPSETDetails(qualifier, account, details):
    bic = ''
    party = ''

    if account.Bic5():
        bic = account.Bic5().Alias()
        party = account.CorrespondentBank5()
    elif account.Bic4():
        bic = account.Bic4().Alias()
        party = account.CorrespondentBank4()
    elif account.Bic3():
        bic = account.Bic3().Alias()
        party = account.CorrespondentBank3()
    elif account.Bic2():
        bic = account.Bic2().Alias()
        party = account.CorrespondentBank2()
    elif account.Bic():
        bic = account.Bic().Alias()
        party = account.CorrespondentBank()

    partyInfo = GetPartyInfo(qualifier, bic, party, '', '', '')
    details.append(partyInfo)

def GetTagsFromOldSwiftBlock(settlement):
    oldXml = ''
    oldSwiftTag = ''
    cancelledSettl = settlement.Children()[0]
    opsDocuments = cancelledSettl.Documents()
    if opsDocuments:
        oldXml = GetXmlFromOpsDocument(opsDocuments[0])
        if oldXml:
            oldSwiftTag = GetModifiedOldSwiftTag(oldXml)
    return oldSwiftTag

def GetXmlFromOpsDocument(opsDocument):
    xml = ''
    dataFromOpsDoc = opsDocument.Data()
    if dataFromOpsDoc:
        dataInZlibFormat = dataFromOpsDoc.decode('hex')
        xml = dataInZlibFormat.decode('zlib')
    return xml

def GetModifiedOldSwiftTag(oldXml):
    oldXml = dom.parseString(oldXml)
    oldSwiftTag = ''
    oldSwiftTags = oldXml.getElementsByTagName('SWIFT')
    if oldSwiftTags:
        oldSwiftTag = oldSwiftTags[0]
        tagsToBeDeleted = ['FUNCTION_OF_MESSAGE', 'LINKAGE']
        for aTag in tagsToBeDeleted:
            nodesToBeDeleted = oldSwiftTag.getElementsByTagName(aTag)
            if nodesToBeDeleted:
                nodeToBeDeleted = nodesToBeDeleted[0]
                nodeToBeDeleted.parentNode.removeChild(nodeToBeDeleted.previousSibling)
                nodeToBeDeleted.parentNode.removeChild(nodeToBeDeleted)
        oldSwiftTag = oldSwiftTag.toxml()
    return oldSwiftTag

def IsSecurityCancellation(settlement):
    securityCancellation = False
    if IsCancellationSettlement(settlement) and settlement.IsSecurity():
        securityCancellation = True

    return securityCancellation

def IsXMLStored(settlement):
    from FDocumentationParameters import xmlStoredInOperationsDocument as xmlStored

    xmlIsStored = False
    cancelledSettl = settlement.Children()[0]
    opsDocuments = cancelledSettl.Documents()

    if len(opsDocuments):
        if opsDocuments[0].Data() and xmlStored:
            xmlIsStored = True
    return xmlIsStored
