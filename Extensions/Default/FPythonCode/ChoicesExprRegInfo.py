
import acm
import traceback
from contextlib import contextmanager


@contextmanager
def TryExcept():
    try:
        yield None
    except Exception as e:
        print (Exception, e)
        print (traceback.format_exc())
        raise (e)


def clearingBrokers():
    """returns a list of Parties of type Broker"""
    with TryExcept():
        brokers = acm.FParty.Select('type="Broker"')
        return brokers.SortByProperty('StringKey', True)

def clearingHouses():
    """returns a list of Parties of type Clearing House"""
    with TryExcept():
        clearingHouses = acm.FParty.Select('type="Clearing House"')
        return clearingHouses.SortByProperty('StringKey', True)
        
def middlewares():
    """returns a list of Parties of type Middleware"""
    with TryExcept():
        middleware = acm.FParty.Select('type="Middleware"')
        return middleware.SortByProperty('StringKey', True)

def originalCounterparties():
    """returns a list of all Parties"""
    with TryExcept():
        counterparties = acm.FParty.Select('type="Counterparty"')
        markets             = acm.FParty.Select('type="Market"')
        clearingHouses      = acm.FParty.Select('type="Clearing House"')
        parties = acm.FSortedCollection()
        parties.AddAll(counterparties)
        parties.AddAll(markets)
        parties.AddAll(clearingHouses)
        return parties.SortByProperty('StringKey', True)

def repositories():
    """return the list of possible Repositories"""
    with TryExcept():
        repositories = acm.FParty.Select('type="Repository"')
        return repositories.SortByProperty('StringKey', True)    


def ourOrganisations():
    """return the list of possible OurOrganisations"""
    with TryExcept():
        brokers = acm.FParty.Select('type="Broker"')
        counterparties = acm.FParty.Select('type="Counterparty"')
        internalDepartments = acm.FParty.Select('type="Intern Dept"')
        parties = acm.FSortedCollection()
        parties.AddAll(brokers)
        parties.AddAll(counterparties)
        parties.AddAll(internalDepartments)
        return parties.SortByProperty('StringKey', True)

def ourTransmittingOrganisations():
    """return the list of possible OurTransmittingOrganisations"""
    with TryExcept():
        brokers = acm.FParty.Select('type="Broker"')
        counterparties = acm.FParty.Select('type="Counterparty"')
        internalDepartments = acm.FParty.Select('type="Intern Dept"')
        parties = acm.FSortedCollection()
        parties.AddAll(brokers)
        parties.AddAll(counterparties)
        parties.AddAll(internalDepartments)
        return parties.SortByProperty('StringKey', True)

def ourInvestmentDeciders(tradeRegInfo):
    """return the list of possible OurInvestmentDeciders"""
    with TryExcept():
        if tradeRegInfo:
            if trade.OurOrganisation():
                contacts = trade.OurOrganisation().Contacts()
                contacts.SortByProperty('StringKey', True)
                return contacts
        return []
        
def ourTraders(tradeRegInfo):
    """return the list of possible OurTrader"""
    with TryExcept():
        if tradeRegInfo:
            if trade.OurOrganisation():
                contacts = trade.OurOrganisation().Contacts()
                contacts.SortByProperty('StringKey', True)
                return contacts
        return []

def branchMemberships():
    """return the list of possible BranchMemberships"""
    with TryExcept():
        parties  = acm.FArray()
        parties.AddAll(acm.FParty.Select('type="Intern Dept"'))
        parties.AddAll(acm.FParty.Select('type="Counterparty"'))
        parties.AddAll(acm.FParty.Select('type="Broker"'))
        parties.SortByProperty('StringKey', True)
        return parties

def theirOrganisations():
    """return the list of possible theirOrganisations"""
    with TryExcept():
        parties  = acm.FArray()
        parties.AddAll(acm.FParty.Select('type="Clearing House"'))
        parties.AddAll(acm.FParty.Select('type="Counterparty"'))
        parties.SortByProperty('StringKey', True)
        return parties

def theirInvestmentDeciders(tradeRegInfo):
    """return the list of possible TheirInvestmentDeciders"""
    with TryExcept():
        if tradeRegInfo:
            if trade.TheirOrganisation():
                contacts = trade.TheirOrganisation().Contacts()
                contacts.SortByProperty('StringKey', True)
                return contacts
        return []

def theirTraders(tradeRegInfo):
    """return the list of possible Theirtraders"""
    with TryExcept():
        if tradeRegInfo:
            if trade.TheirOrganisation():
                contacts = trade.TheirOrganisation().Contacts()
                contacts.SortByProperty('StringKey', True)
                return contacts
        return []


def commodityBaseProducts(insRegInfo):
    """return the commodity base products"""
    with TryExcept():
        choiceListName = 'CommodityBaseProduct'
        choiceLists = acm.FChoiceList.Select("list=%s"%choiceListName)
        choiceLists.SortByProperty('StringKey', True)
        return choiceLists

def commoditySubProducts(insRegInfo):
    """return the commodity sub products"""
    with TryExcept():
        choiceListParent = insRegInfo.CommodityBaseProduct()
        if choiceListParent:
            choiceLists = acm.FChoiceList.Select("list=%s"%choiceListParent.Name())
            choiceLists.SortByProperty('StringKey', True)
            return choiceLists
        else:
            return []

def commodityFurtherSubProducts(insRegInfo):
    """return the commodity further sub products"""
    with TryExcept():
        choiceListParent = insRegInfo.CommoditySubProduct()
        if choiceListParent:
            choiceLists = acm.FChoiceList.Select("list=%s"%choiceListParent.Name())
            choiceLists.SortByProperty('StringKey', True)
            return choiceLists
        else:
            return []
