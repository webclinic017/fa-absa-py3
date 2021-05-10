"""------------------------------------------------------------------------
MODULE
    FSWMLClearingGUI -
DESCRIPTION:
    This file consists of the APIs that are being used while trade attributes are being displayed on the GUI 
VERSION: 1.0.30
--------------------------------------------------------------------------"""
import acm

def getACMVersion():
    version = acm.Version()    
    indexPos = version.find(',')
    if indexPos != -1:
        versionNumber = version[0:indexPos]
        indexPos = versionNumber.find('.')
        indexPos1 = versionNumber.find('.', indexPos + 1)
        if indexPos1 > -1:
            versionNumber = versionNumber[0: indexPos1]
        return float(versionNumber)
    else:
        return float(version)
        
def hello():
    return 'world'

def ccpParties():
    ccps = []
    acmVersion = getACMVersion()
    if acmVersion < 2012.1:
        for p in acm.FParty.Select('type=Counterparty'):
            if p.AdditionalInfo().CCPis_ccp():
                    ccps.append( p.Name())    
    else:
        for p in acm.FParty.Select('type=Clearing House'):
            ccps.append( p.Name())    
    return ccps
    

def counterParties():
    ccps = []
    for p in acm.FParty.Select('type=Counterparty'):
        ccps.append( p.Name())
    return ccps

def mwParties():
    mws = []
    acmVersion = getACMVersion()
    if acmVersion < 2012.1:
        for p in acm.FParty.Select('type=Counterparty'):
            if p.AdditionalInfo().CCPis_middleware():
                    mws.append( p.Name())
    else:
        for p in acm.FParty.Select('type=Middleware'):
            mws.append( p.Name())
    return mws
    

def clrBrokerParties():
    cbs = []
    acmVersion = getACMVersion()
    if acmVersion < 2012.1:
        for p in acm.FParty.Select('type=Counterparty'):
            if p.AdditionalInfo().CCPis_clearing_brok():
                    cbs.append( p.Name())
    else:
        for p in acm.FParty.Select('type=Broker'):
            cbs.append( p.Name())
    return cbs
    

def tdrParties():
    tdrs = []
    try :
        for p in acm.FParty.Select('type=Repository'):
            tdrs.append( p.Name())
    except :
        pass
    for p in acm.FParty.Select('type=Counterparty'):
        if p.AdditionalInfo().CCPis_tdr():
            tdrs.append( p.Name())
    return tdrs

def CCPcpty_trader(trade):
    contacts = []
    counterparty = trade.Counterparty()
    if counterparty:    
        contacts = getContactsOnParty(counterparty)
    return contacts
def getContactsOnParty(party):
    contacts = []
    for p in acm.FParty.Select('name="%s"' %party.Name()):
        for contact in p.Contacts():
            if contact.NetworkAlias() and contact.NetworkAlias().Type().Name() in ['MarkitWireGroup', 'MarkitWireTrader']:
                contacts.append(contact.Name())
            if contact.Network2Alias() and contact.Network2Alias().Type().Name() in ['MarkitWireGroup', 'MarkitWireTrader']:
                contacts.append(contact.Name())
    return contacts
def CCPour_trader(trade):
    contacts = []
    acquirer = trade.Acquirer()
    if acquirer:
        contacts = getContactsOnParty(acquirer)
    return contacts

def getUSIDetails(trade):
    acmVersion = getACMVersion()
    usiDetails = None
    if acmVersion < 2013.1:
        if trade.AdditionalInfo().USI_Identifier():
            usiDetails = trade.AdditionalInfo().USI_Issuer()
        if trade.AdditionalInfo().USI_Issuer():
            usiDetails = usiDetails + trade.AdditionalInfo().USI_Identifier()
    else:
        tradeAlias = acm.FTradeAlias.Select("type = 'USI' and trade = '%d'"%trade.Oid())
        if tradeAlias:
            usiDetails = tradeAlias[0].Alias()
    return usiDetails

def getUTIDetails(trade):
    utiDetails = None
    if trade:
        try:
            if trade.UniqueTradeIdentifier():
                utiDetails = trade.UniqueTradeIdentifier()
        except:
            if trade.AdditionalInfo().UTI_1part():
                utiDetails = trade.AdditionalInfo().UTI_1part()
            if trade.AdditionalInfo().UTI_2part():
                utiDetails = utiDetails + trade.AdditionalInfo().UTI_2part()
    return utiDetails

