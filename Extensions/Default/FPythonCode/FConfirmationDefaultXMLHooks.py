""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationDefaultXMLHooks.py"
import acm
import math


# Helpfunctions that can be used when populating XML tags

def __GetCounterpartyAccount(confirmation):
    return __GetAccount(confirmation, True)

def __GetAcquirerAccount(confirmation):
    return __GetAccount(confirmation, False)

def __GetAccount(confirmation, isCounterparty):
    moneyFlows = confirmation.Trade().MoneyFlows(confirmation.Trade().ValueDay(), None)
    moneyFlows.SortByProperty('PayDate')

    for moneyflow in moneyFlows:
        if isCounterparty:
            if moneyflow.Counterparty() == confirmation.Trade().Counterparty():
                return moneyflow.CounterpartyAccount()
        else:
            if moneyflow.Acquirer() == confirmation.Trade().Acquirer():
                return moneyflow.AcquirerAccount()
    return None

def __GetSpace():
    m_calculationSpaceCollection = acm.FCalculationSpaceCollection()
    space = m_calculationSpaceCollection.GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())
    return space

def __IsBuyTrade(trade):
    return (trade.Quantity() >= 0.0)

# Following functions are by default called from FConfirmationDefaultXMLTemplates
# when creating XML content. If the function is taking one input parameter
# then this function is to be used from XML tag that uses "acmCode method".
# If the function is taking two input parameters then XML tag is within loop.
# Functions with two parameters are implemented to use fobject and sourceObject.
# First parameter, fobject, can be different classes depending on the loop.
# Second parameter, sourceObject, is the confirmation row that triggered
# XML creation.

def GetNominal(confirmation):
    return confirmation.Trade().Nominal()

def GetProjectedFixedAmount(fObject):
    amount = 0.0
    if fObject.IsKindOf(acm.FConfirmation):
        m_calculationSpaceCollection = acm.FCalculationSpaceCollection()
        space = m_calculationSpaceCollection.GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())

        for i in fObject.Trade().MoneyFlows(None, None):
            if i.Type() == "Fixed Amount":
                amount = amount + space.CalculateValue(i, 'Cash Analysis Projected').Number()
    return amount

def GetFloatRateSettlementAmount(fObject):
    amount = 0.0
    if fObject.IsKindOf(acm.FConfirmation):
        m_calculationSpaceCollection = acm.FCalculationSpaceCollection()
        space = m_calculationSpaceCollection.GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())

        for i in fObject.Trade().MoneyFlows(None, None):
            if i.Type() == "Float Rate":
                if i.SourceObject().IsKindOf(acm.FCashFlow):
                    if None != fObject.Reset():
                        if fObject.Reset().CashFlow().Oid() == i.SourceObject().Oid():
                            amount = amount + space.CalculateValue(i, 'Cash Analysis Projected').Number()
    return amount

def GetFloatRateSettlementPayDay(fObject):
    payDay = ''
    if fObject.IsKindOf(acm.FConfirmation):
        for i in fObject.Trade().MoneyFlows(None, None):
            if i.Type() == "Float Rate":
                if i.SourceObject().IsKindOf(acm.FCashFlow):
                    if None != fObject.Reset():
                        if fObject.Reset().CashFlow().Oid() == i.SourceObject().Oid():
                            payDay = fObject.Reset().CashFlow().PayDate()
    return payDay


def ProjectedForAllFlows(fObject):
    amount = 0.0
    if fObject.IsKindOf(acm.FConfirmation):
        m_calculationSpaceCollection = acm.FCalculationSpaceCollection()
        space = m_calculationSpaceCollection.GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())

        for i in fObject.Trade().MoneyFlows(None, None):
            if i.Type() == "Call Fixed Rate":
                amount = amount + space.CalculateValue(i, 'Cash Analysis Projected').Number()
    return amount

def ABSPremium(fObject):
    return math.fabs(fObject.Trade().Premium())

def ABSQuantity(fObject):
    return math.fabs(fObject.Trade().Quantity())

def GetCounterpartyCorrespondentBankForValueDay(confirmation):
    account = __GetCounterpartyAccount(confirmation)
    if account:
        return account.CorrespondentBank().Name()
    return ""

def GetCounterpartyBICForValueDay(confirmation):
    account = __GetCounterpartyAccount(confirmation)
    if account and account.Bic():
        return account.Bic().Name()
    return ""

def GetCounterpartyAccountForValueDay(confirmation):
    account = __GetCounterpartyAccount(confirmation)
    if account:
        return account.Account()
    return ""

def GetCounterpartyNetworkAliasForValueDay(confirmation):
    account = __GetCounterpartyAccount(confirmation)
    if account and account.NetworkAlias():
        return account.NetworkAlias().Name()
    return ""

def GetAcquirerCorrespondentBankForValueDay(confirmation):
    account = __GetAcquirerAccount(confirmation)
    if account:
        return account.CorrespondentBank().Name()
    return ""

def GetAcquirerBICForValueDay(confirmation):
    account = __GetAcquirerAccount(confirmation)
    if account and account.Bic():
        return account.Bic().Name()
    return ""

def GetAcquirerAccountForValueDay(confirmation):
    account = __GetAcquirerAccount(confirmation)
    if account:
        return account.Account()
    return ""

def GetAcquirerNetworkAliasForValueDay(confirmation):
    account = __GetAcquirerAccount(confirmation)
    if account and account.NetworkAlias():
        return account.NetworkAlias().Name()
    return ""

def GetCounterpartyName(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Fullname()
    return ""

def GetCounterpartyAddress(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Address()
    return ""

def GetCounterpartyAddress2(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Address2()
    return ""

def GetCounterpartyZipCode(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Zipcode()
    return ""

def GetCounterpartyCity(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.City()
    return ""

def GetCounterpartyCountry(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Country()
    return ""

def GetCounterpartyTelephone(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Telephone()
    return ""

def GetCounterpartyFax(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Fax()
    return ""

def GetCounterpartyEmail(confirmation):
    contact = GetContactCounterparty(confirmation)
    if contact:
        return contact.Email()
    return ""

def GetSeller(confirmation):
    seller = ''
    trade = confirmation.Trade()
    if __IsBuyTrade(trade) == True:
        seller = trade.Counterparty().Name()
    else:
        seller = trade.Acquirer().Name()
    return seller

def GetBuyer(confirmation):
    buyer = ''
    trade = confirmation.Trade()
    if __IsBuyTrade(trade) == True:
        buyer = trade.Acquirer().Name()
    else:
        buyer = trade.Counterparty().Name()
    return buyer

def GetContactCounterparty(confirmation):
    return confirmation.CounterpartyContactRef()

def StartDateCashflow(cashflow):
    return cashflow.StartDate()

def EndDateCashflow(cashflow):
    return cashflow.EndDate()

def PayDateCashflow(cashflow):
    return cashflow.PayDate()

def FixedLeg(instrument):
    leg = None
    legs = FixedLegs(instrument)
    if len(legs) > 0:
        leg = legs[0]
    return leg

def FloatLeg(instrument):
    leg = None
    legs = FloatLegs(instrument)
    if len(legs) > 0:
        leg = legs[0]
    return leg

def FixedLegs(instrument):
    fixedLegs = acm.FList()
    for leg in instrument.Legs():
        if leg.IsFixedLeg():
            fixedLegs.Add(leg)
    return fixedLegs

def FloatLegs(instrument):
    floatLegs = acm.FList()
    for leg in instrument.Legs():
        if leg.IsFloatLeg():
            floatLegs.Add(leg)
    return floatLegs

def PayLegs(instrument):
    legs = acm.FList()
    for leg in instrument.Legs():
        if leg.PayLeg() == True:
            legs.Add(leg)
    return legs

def RecLegs(instrument):
    legs = acm.FList()
    for leg in instrument.Legs():
        if leg.PayLeg() == False:
            legs.Add(leg)
    return legs

def GetFirstResetDate(cashflow):
    for i in cashflow.Resets():
        return i.StartDate()
    return None

def CfAmount(cf, sourceObject):
    ret = 0
    calcValue = cf.Calculation().Projected(acm.Calculations().CreateStandardCalculationsSpaceCollection(), sourceObject.Trade())
    if calcValue and calcValue.Value():
        ret = calcValue.Value().Number()
    return ret

def CfPeriod(cf):
    daysBetween = acm.GetFunction('days_between', 4)
    cal = acm.FCalendar[cf.Leg().Currency().Name()]
    return int(daysBetween(cf.StartDate(), cf.EndDate(), cf.Leg().DayCountMethod(), cal))

def CfCurr(cf):
    return cf.Leg().Currency().Name()

def CfNominal(cf, sourceObject):
    space = __GetSpace()
    moneyFlows = sourceObject.Trade().MoneyFlows(cf.EndDate(), cf.PayDate())
    for mf in moneyFlows:
        if mf.SourceObject() == cf:
            cv = space.CalculateValue(mf, 'Cash Analysis Nominal')
            if cv:
                return cv.Number()
    return ""

