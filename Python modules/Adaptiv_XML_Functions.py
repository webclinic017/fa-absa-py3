"""
Note: Where the phrase "Adaptiv keyword" has been added in comment; take great care in changing this value,
        because within Adaptiv a condition is executed using that exact word/phrase.

HISTORY
When            Change                  Who                     What

2015-09-17      Initial deployment      Sanele Macanda
2015-07-13      ADAFA-31                Lawrence Mucheka        GetCallTradeBalance - Invert the Redemption
                                                                amount for purposes of getting a call a/c balance
2015-11-05      CHNG0003231673          Willie vd Bank          Added functionality to display the long and short pary names
                                                                Added functionality to return the SSI from the adjusted settlement
2016-04-21      ABITFA-4182             Evgeniya Baskaeva       Fixed None in CP fullname
2016-08-04      ABITFA-4389             Marcelo G. Almiron      Refresh email passed to Adaptiv on non-production environments
2016-06-22                              Manan Ghosh             Demat changes
2016-12-05      ABITFA-4597             Willie van der Bank     Production issue code fix to cater for confirmation resends
2017-08-26                              Willie vd Bank          Updated CashFlowBase input parameters as part of 2017 upgrade
                                                                Updated GetCptyAcc and GetAcqrAcc to select a smaller set of money flows
2018-06-19      CHG1000569538           Willie vd Bank          Modified GetCptyAcc to not use the settlement because the settlement
                                                                might not exist when the confirmation is created.
2018-08-07      FAOPS-163               Cuen Edwards            Replaced Barclays in confirmation file names with Absa.
2019-04-26      FAOPS-455               Stuart Wilson           Enhanced the call confirmation funding instype display parameter
2019-06-28      FAOPS-522               Hugo Decloedt           Update to GetCptyAcc to check money flow for for account
                                                                where the CP_AccountRef additional info is not set.
2020-07-24      FAOPS-854               Tawanda Mukhalela       Refactored deposit balance calculation
"""

import re
from datetime import datetime
import traceback

import acm
import ael
import FOperationsUtils as Utils
from at_time import to_date, acm_date
from SAGEN_IT_TM_Column_Calculation import money_flow_value
from demat_functions import mm_instype
from DocumentGeneral import get_fparameter


maxBankingDaysBack = 15

ACQUIRER_EMAIL_GROUP = {'Money Market Desk': 'xraMMConfirmations@absa.africa',
                        'Funding Desk': 'xraMMConfirmations@absa.africa'}

DEFAULT_EMAIL_ADDR = get_fparameter('ABSAConfoEmailConfig', 'DEFAULT_SENDER_ADDR')
DEV_CONF_EMAIL = get_fparameter('ABSAConfoEmailConfig', 'DEV_CONF_ADDR')

# Event Definitions
EVENT_TYPE_ACCOUNT_CEDED = 'Account_Ceded'
EVENT_TYPE_NEW_TRADE = 'New_Trade'
EVENT_TYPE_NEW_TRADE_CALL = 'New_Trade_Call'
EVENT_TYPE_RATE_FIXING = 'Rate_Fixing'
EVENT_TYPE_MATURITY_NOTICE = 'Maturity_Notice'
EVENT_TYPE_RATE_RESET = 'Rate_Reset'
EVENT_TYPE_NOVATION = 'Novation'
EVENT_TYPE_CLOSE = 'Close'
EVENT_TYPE_PARTIAL_CLOSE = 'Partial_Close'
EVENT_TYPE_PROLONG_DEPOSIT = 'Prolong_Deposit'

ABSA_CIB = 'ABSA BANK LTD'

CALL_DEP_FUND_INS_TYPE_MAPPING = {
    'Call Deposit Coll DTI': 'Call Deposit Collateral',
    'Call Deposit Coll NonDTI': 'Call Deposit Collateral',
    'Call Deposit DTI': 'Call Deposit',
    'Call Deposit NonDTI': 'Call Deposit',
    'Call Loan Coll DTI': 'Call Loan Collateral',
    'Call Loan Coll NonDTI': 'Call Loan Collateral',
    'Call Loan DTI': 'Call Loan',
    'Call Loan NonDTI': 'Call Loan'
}

CALL_DEP_FUND_INS_TYPE_DEFAULT = [
    'Access Deposit Note 95d Note 2',
    'Access Deposit Note 95d',
    'Access Deposit Note 370d',
    'Access Income Plus 35d',
    'Call 185 Day notice',
    'Call 277 Day notice',
    'Call 32 Day notice',
    'Call 360 Day notice',
    'Call 48 Hour Notice',
    'Call 63 Day notice',
    'Call 7 Day notice',
    'Call 93 Day notice',
    'Call Access Loan',
    'Call Bond Deposit',
    'Call Bond Loan',
    'Call CFD Funding',
    'FDI Access Income Plus 35d'
]

# Cash flow functions
# --------------------------------------------------------------------------------------------------


def GetCFPayDay(cashflow, confirmation):
    del confirmation
    return cashflow.PayDate()


def GetCFProj(cashflow, confirmation):
    try:
        trd = confirmation.Trade()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        return cashflow.Calculation().Projected(calcSpace, trd).Number()
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return 0


def GetCFProjConverted(cashflow, confirmation):
    absCF = abs(GetCFProj(cashflow, confirmation))
    if absCF >= 0.01:
        return round(absCF, 2)
    else:
        return 0


def GetCFPayOrReceive(cashflow, confirmation):
    if GetCFProj(cashflow, confirmation) < 0:
        return "Pay"
    return "Receive"


def GetCFBuyOrSell(cashflow, confirmation):
    if GetCFProj(cashflow, confirmation) > 0:
        return "BUY"
    return "SELL"


def GetCFCurr(cashflow, confirmation):
    del confirmation
    return cashflow.Leg().Currency().Name()


def GetCFType(cashflow, confirmation):
    del confirmation
    return cashflow.CashFlowType()


def GetCFTypeConverted(cashflow, confirmation):
    cashflow_type = GetCFType(cashflow, confirmation)
    if cashflow_type == 'Fixed Rate':
        return 'Interest'
    elif cashflow_type == 'Fixed Amount':
        return 'Principal Repayment'
    return cashflow_type


# Leg functions
# --------------------------------------------------------------------------------------------------

def GetResetPeriod(leg, confirmation):
    del confirmation
    return str(leg.ResetPeriodCount()) + ' ' + leg.ResetPeriodUnit()


def GetLegRollingFormatted(leg, confirmation):
    del confirmation
    rolling = str(leg.RollingPeriodCount()) + ' ' + leg.RollingPeriodUnit()
    return GetFormatted(rolling)


def GetAmortRollingFormatted(leg, confirmation):
    del confirmation
    rolling = str(leg.AmortPeriodCount()) + ' ' + leg.AmortPeriodUnit()
    return GetFormatted(rolling)


def GetCashFlows(leg, confirmation):
    del confirmation
    if leg.CashFlows():
        return leg.CashFlows().SortByProperty('PayDate', True)


def GetLegSpread(leg, confirmation):
    """ Gets the spread to display - varies per Instrument type """
    del confirmation

    spread = leg.Spread()
    if leg.Instrument().InsType() == 'FRN':
        spread = leg.Spread() * 100

    return spread


def GetFixingValue(leg, confirmation):
    """ Gets the fixing value """
    del leg

    reset = confirmation.Reset()
    if reset:
        return reset.FixingValue()
    return 0


def GetRate(leg, confirmation):
    """ Gets the rate to display """

    rate = leg.FixedRate()
    if GetLegTypeFixOrFloat(leg, confirmation) == 'Float' and leg.FloatPriceReference():
        floatReferenceName = leg.FloatPriceReference().Name()
        eventType = confirmation.EventType()
        if eventType in 'Rate Reset':
            return GetFixingValue(leg, confirmation)
        else:
            variance = GetLegSpread(leg, confirmation)

        if variance > 0:
            variance = '+{0}'.format(variance)

        return '{0} {1}'.format(floatReferenceName, variance)
    else:
        return rate


def GetDayCount(leg, confirmation):
    del confirmation

    return leg.DayCountMethod()


def GetLegPayOrReceive(leg, confirmation):
    del confirmation

    if leg.PayLeg():
        return 'Pay'
    else:
        return 'Receive'


def Get_First_Or_Last_CF(leg, acm_date_field, flag, confirmation):
    cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
    cashFlowType = cashFlowQuery.AddOpNode('OR')
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Float Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Floorlet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Floorlet'))

    cashFlows = cashFlowQuery.Select().SortByProperty(acm_date_field, flag)  # The last argument is "ascending"
    if cashFlows:
        return cashFlows[0]
    return None


def Is_Initial_Rate(leg, confirmation):
    first_cf = Get_First_Or_Last_CF(leg, 'PayDate', True, confirmation)
    retVal = None
    if first_cf:
        if ael.date(first_cf.StartDate()) == ael.date(leg.Instrument().StartDate()) and (
                ael.date(first_cf.EndDate()) >= ael.date_today()):
            if first_cf.Resets():
                resetQuery = acm.CreateFASQLQuery(acm.FReset, 'AND')
                resetQuery.AddAttrNode('CashFlow.Oid', 'EQUAL', first_cf.Oid())
                resetQuery.AddAttrNode('ResetType', 'NOT_EQUAL', Utils.GetEnum('ResetType', 'Nominal Scaling'))
                resetQuery.AddAttrNode('FixingValue', 'NOT_EQUAL', 0)
                reset = resetQuery.Select().SortByProperty('EndDate', True)
                if reset:
                    retVal = reset[0]
    return retVal


def GetLegTypeFixOrFloat(leg, confirmation):
    del confirmation

    if leg.LegType() in ('Call Fixed Adjustable', 'Fixed', 'Call Fixed'):
        return 'Fixed'
    elif leg.LegType() in ('Float', 'Call Float'):
        return 'Float'
    else:
        return leg.LegType()


def DayCountMethod(leg, confirmation):
    del confirmation

    method = leg.DayCountMethod()
    try:
        return str(str(method).replace('Act', 'Actual')).replace('Bus', 'Business')
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return method


def PayDayMethod(leg, confirmation):
    del confirmation

    method = leg.PayDayMethod()
    try:
        if method == 'Following':
            return 'Adjusted to first following business day.'
        elif method == 'Mod. Following':
            return 'Modified Following'
        elif method == 'Preceding':
            return 'Adjusted to most recent previous business day.'
        elif method == 'Mod. Preceding':
            return 'Modified Preceding'
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return method

    return method


# Trade functions
# --------------------------------------------------------------------------------------------------

def GetCurrencyQuote(trade, confirmation):
    del confirmation
    return trade.Instrument().Currency().Name() + '/' + trade.Currency().Name()


def GetExternalID(trade, confirmation):
    del confirmation
    optional_key = trade.OptionalKey()
    if optional_key.startswith('BARXMM'):
        return 'BARXMM'
    return ''


def GetBARXTradeNumber(trade, confirmation):
    del confirmation
    optional_key = str(trade.OptionalKey())
    if optional_key.startswith('BARXMM'):
        barx_trade_id = optional_key.split('-').pop()
        return barx_trade_id
    return ''


def GetTradeReferenceNumber(trade, confirmation):
    del confirmation
    tradeReferenceNumber = trade.StringKey()
    if trade.Instrument().IsCallAccount():
        tradeReferenceNumber = trade.Instrument().Name()

    return tradeReferenceNumber


def GetTradeReferenceNumberLabel(trade, confirmation):
    del confirmation
    tradeReferenceNumberLabel = 'Trade Reference Number:'
    if trade.Instrument().IsCallAccount():
        tradeReferenceNumberLabel = 'Account number:'

    return tradeReferenceNumberLabel


def GetTraderBPID(trade, confirmation):
    del confirmation
    trader_BPID = trade.AdditionalInfo().Demat_Acq_BPID()

    return trader_BPID and trader_BPID or ''


def GetInterestRate(trade, confirmation):
    del confirmation
    ins = trade and trade.Instrument()

    legs = [leg for leg in ins.Legs()]
    if len(legs) == 1:
        leg = legs[0]
        if leg.IsFixedLeg():
            return '%2.4f %s' % (leg.FixedRate(), '%')
        elif leg.IsFloatLeg():
            sign = (abs(leg.Spread()) < 0) and '-' or '+'
            return '%s %s %2.4f %s' % (leg.FloatRateReference().Name(), sign, abs(leg.Spread()), '%')


def GetInterestAmount(trade, confirmation):
    del confirmation
    ins = trade and trade.Instrument()
    quantity = trade and trade.Quantity() or 0.0
    value_day = acm_date(trade.ValueDay())
    cashflowAmount = 0.0
    roundingSpec = ins.RoundingSpecification()

    legs = [leg for leg in ins.Legs()]
    if len(legs) == 1:
        leg = legs[0]
        if leg.IsFixedLeg():
            nominal = ins.NominalAmount()
            staticLegInfo = leg.StaticLegInformation(ins, trade.ValueDay(), None)
            for cf in leg.CashFlows():
                if value_day >= cf.StartDate() and value_day < cf.EndDate():
                    cfInfo = cf.CashFlowInformation(staticLegInfo)
                    cfAmount = cfInfo.SimpleProjectedCashFlow(acm.Time().DateToday(), (
                                roundingSpec and roundingSpec.RoundingInformation())).Number()
                    cashflowAmount = nominal * cfAmount

        elif leg.IsFloatLeg():
            staticLegInfo = leg.StaticLegInformation(ins, trade.ValueDay(), None)
            legInfo = leg.LegInformation(trade.ValueDay())
            for cf in leg.CashFlows():
                if value_day >= cf.StartDate() and value_day < cf.EndDate():
                    cfInfo = cf.CashFlowInformation(staticLegInfo)
                    cashflowAmount = cfInfo.Rate(legInfo) * cfInfo.CashFlowBase(legInfo, acm.Time().DateToday(),
                                                                                True).Number()

    cashflowAmount = cashflowAmount * quantity

    return '%15.2f %s' % (cashflowAmount, ins.Currency().Name())


def get_Ceded_CreateTime(trade, Confirmation):
    del trade
    if 'Account Ceded' in Confirmation.EventType():
        return acm_date(Confirmation.CreateTime())

    return ''


def GetCededAmount(trade, confirmation):
    del confirmation
    ceded = trade.AdditionalInfo().MM_Ceded_Amount()
    if ceded:
        if ceded not in (0, ''):
            return ceded

    return ''


''' Not used'''


def is_valid_status(trade):
    if trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        return True
    return False


def GetFxSwapTrades(trade, confirmation):
    del confirmation
    trades = acm.FArray()
    trades.Add(trade)
    if 'Swap Near Leg' in trade.TradeProcessesToString():
        confTrdNbr = trade.Oid()
        for trd in acm.FTrade.Select('connectedTrdnbr = %d' % confTrdNbr):
            if trd.Instrument().InsType() == 'Curr':
                if confTrdNbr == trd.ConnectedTrdnbr():
                    if trd not in trades:
                        trades.Add(trd)
    return trades


def CloseTrade(trade, confirmation):  # Follow same rules as in TradeCustomEOD
    del confirmation
    if trade.Instrument().InsType() == 'Deposit':
        if trade.Type() == 'Closing':
            if trade.ContractTrdnbr() != trade.Oid():
                if acm.FTrade[trade.ContractTrdnbr()]:
                    return trade.ContractTrdnbr()

        elif trade.Type() == 'Novated Assigned':
            if trade.BusinessEvents():
                for link in trade.BusinessEvents().At(0).TradeLinks():
                    if link.Trade().Type() == 'Normal':
                        return link.Trade().Oid()
    return ''


def GetTradeCorrection(trade, confirmation):
    if trade.CorrectionTrade():
        if trade.CorrectionTrade().Oid() == trade.Oid():
            return '(TRADE CORRECTION)'
        else:
            if trade.Status() != 'Void':
                return '(CORRECTION OF TRADE ' + str(trade.CorrectionTrade().Oid()) + ')'
    else:
        ClsTrd = CloseTrade(trade, confirmation)
        if ClsTrd != '':
            return 'OF TRADE ' + str(ClsTrd)
    return ''


def GetPaymentSum(trade, confirmation):
    del confirmation
    payment_sum = 0.00
    for p in trade.Payments():
        payment_sum = payment_sum + p.Amount()
    return float(abs(payment_sum))


def GetClosingPayments(trade, confirmation):
    del confirmation
    closing_payments = acm.FArray()
    for p in trade.Payments():
        closing_payments.Add(p)
    return closing_payments


def GetTerminatedAmount(trade, confirmation):
    terminatedAmount = 0.00
    if CloseTrade(trade, confirmation):
        terminatedAmount = abs(trade.Nominal())
    return terminatedAmount


def GetTerminationRemainingAmount(trade, confirmation):
    terminationRemainingAmount = 0.00
    if trade.ConnectedTrade() and CloseTrade(trade, confirmation):
        terminationRemainingAmount = abs(trade.ConnectedTrade().RemainingNominal())
    return terminationRemainingAmount


def GetCashTrdPoints(trade, confirmation):
    del confirmation
    try:
        return abs(10000 * (trade.Price() - trade.ReferencePrice()))
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return 0


def GetTrdNominal(trade, confirmation):
    if CloseTrade(trade, confirmation) == '':
        return abs(trade.Nominal())
    else:
        return GetPaymentSum(trade, confirmation)


def GetTrdNominalFormat(trade, confirmation):
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%.2f" % (float(GetTrdNominal(trade, confirmation))))


def GetTermAvailableBalance(trade, confirmation):
    del confirmation

    if trade.AdditionalInfo().MM_Ceded_Amount():
        ceded_amount = trade.AdditionalInfo().MM_Ceded_Amount()
        return abs(trade.Nominal()) - ceded_amount
    return abs(trade.Nominal())


def GetTrdInterest(trade, confirmation):
    return GetTrdEndCash(trade, confirmation) - GetTrdNominal(trade, confirmation)


def GetTrdBuyOrSell(trade, confirmation):
    del confirmation
    if trade.Instrument().IsCallAccount():
        if trade.Quantity() > 0:
            return 'Sell'
        return 'Buy'

    elif trade.Type() == 'Closing':
        if trade.Quantity() < 0:
            return 'Buy'
        return 'Sell'
    else:
        if trade.Quantity() < 0:
            return 'Sell'
        return 'Buy'


def GetTrdSalePurchaseIndicator(trade, confirmation):
    del confirmation
    if trade.Quantity() < 0:
        return 'SELL'
    else:
        return 'PURCHASE'


def GetTrdQuantity(trade, confirmation):
    del confirmation
    return abs(trade.Quantity())


def GetTrdPos(trade, confirmation):
    return GetTrdNominal(trade, confirmation) * GetTrdQuantity(trade, confirmation)


def GetPremiumBuyOrSell(trade, confirmation):
    del confirmation
    if trade.Premium() < 0:
        return 'Sell'
    return 'Buy'


def GetTrdPremium(trade, confirmation):
    del confirmation
    return abs(trade.Premium())


def GetTrdPremiumFormat(trade, confirmation):
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%.2f" % (float(GetTrdPremium(trade, confirmation))))


def GetTrdPremiumPayDate(trade, confirmation):
    del confirmation
    if trade.Premium() != 0:
        return trade.ValueDay()
    else:
        return None


def GetTrdEndCash(trade, confirmation):
    del confirmation
    try:
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        Calc = calc_space.CalculateValue(trade, 'End Cash')
        return abs(round(Calc, 2))
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return '0'


def GetTrdValueDay(trade, confirmation):
    if isCall(trade) and confirmation and confirmation.CashFlow():
        return confirmation.CashFlow().PayDate()

    return acm_date(trade.ValueDay())


def GetTrdTradeDay(trade, confirmation):
    del confirmation
    return trade.TradeTime()[:10]


def GetHandlingFee(trade, confirmation):
    del confirmation
    return GetAdditionalPaymentAmount(trade, 'HandlngFee', 'HandlngFee2')


def GetCommission(trade, confirmation):
    del confirmation
    return GetAdditionalPaymentAmount(trade, 'Comm1', 'Comm2')


def GetAdditionalPaymentAmount(trade, text, text2):
    amount = 0
    if trade.Payments():
        for p in trade.Payments():
            if p.Text().startswith(text) or p.Text().startswith(text2):
                amount = amount + abs(p.Amount())
    if amount != 0:
        return amount
    else:
        return ''


def GetOptBuyer(trade, confirmation):
    if GetTrdBuyOrSell(trade, confirmation) == 'Buy':
        return ABSA_CIB
    else:
        return trade.Counterparty().Fullname()


def GetOptSeller(trade, confirmation):
    if GetTrdBuyOrSell(trade, confirmation) == 'Sell':
        return ABSA_CIB
    else:
        return trade.Counterparty().Fullname()


def GetFXSwapMargin(trade, confirmation):
    del confirmation
    return FxSwapFunctions(str(trade.Oid()), 0, 0, 1)


def GetFXSwapCFs(trade, confirmation):
    del confirmation
    return FxSwapFunctions(str(trade.Oid()), 0, 1, 0)


def GetFXSwapCost(trade, confirmation):
    LegCost = 0
    Cost = 0
    for l in trade.Instrument().Legs():
        for cashflow in l.CashFlows():
            LegCost = abs(GetCFProj(cashflow, confirmation)) - LegCost
        Cost = Cost + abs(LegCost)
        LegCost = 0
    return str(Cost)


def GetFXSwapCostCurr(trade, confirmation):
    del confirmation

    for l in trade.Instrument().Legs():
        if l.PayLeg():
            return l.Currency().Name()
    return ''


def GetBondDirtyPrice(trade, confirmation):
    del confirmation

    i = ael.Instrument[trade.Instrument().Oid()]
    return i.dirty_from_yield(i.start_day, None, None, trade.Price()) * trade.Nominal() / 100


def GetBondCleanPrice(trade, confirmation):
    del confirmation

    i = ael.Instrument[trade.Instrument().Oid()]
    return i.clean_from_yield(i.start_day, None, None, trade.Price()) * trade.Nominal() / 100


def isCall(trade):
    ins = trade.Instrument()

    if ins.InsType() == 'Deposit' and ins.IsCallAccount():
        return True

    return False


def GetCallTradeBalance(trade, confirmation):
    del confirmation

    bal = 0
    if isCall(trade):
        for money_flow in trade.MoneyFlows():
            if money_flow.Type() == 'Redemption Amount':
                bal = -money_flow_value(money_flow, acm_date('today'), 'Cash Analysis Projected')
                if trade.AdditionalInfo().MM_Ceded_Amount():
                    return bal - trade.AdditionalInfo().MM_Ceded_Amount()

    return bal


def GetCallInterestAmount(trade, confirmation):
    del confirmation

    interest_amount = []

    if isCall(trade):
        for money_flow in trade.MoneyFlows():
            if money_flow.Type() == 'Call Fixed Rate Adjustable':
                interest_amount.append(money_flow_value(money_flow, acm_date('today'), 'Cash Analysis Projected'))

    return interest_amount[-1]


def GetDepositBalance(trade, confirmation):
    del confirmation

    if trade.Instrument().InsType() == 'Deposit':
        if isCall(trade):
            for money_flow in trade.MoneyFlows():
                if money_flow.Type() == 'Redemption Amount':
                    balance = abs(money_flow_value(money_flow, acm_date('today'), 'Cash Analysis Projected'))
                    if trade.AdditionalInfo().MM_Ceded_Amount():
                        return balance - trade.AdditionalInfo().MM_Ceded_Amount()
                    return balance

            raise ValueError('Redemption Cash Flow could not be found for Trade {trade}'.format(trade=trade.Oid()))

        else:
            ceded_amount = 0
            if trade.AdditionalInfo().MM_Ceded_Amount():
                ceded_amount = trade.AdditionalInfo().MM_Ceded_Amount()
            bal = abs(trade.Nominal()) - ceded_amount
            return bal

    error_message = 'Instrument type {instrument} not supported for Deposit Balance Calculation'
    raise ValueError(error_message.format(instrument=trade.Instrument().InsType()))


def funding_instype(trade, confirmation):
    del confirmation
    if trade.Instrument().InsType() == 'Deposit':
        return trade.AdditionalInfo().Funding_Instype()
    return ''


# Party functions
# --------------------------------------------------------------------------------------------------

def GetAcquirerEmail(party, confirmation):
    del party
    try:
        acquirer = confirmation.Trade().Acquirer()
        acquirer_name = acquirer.Name()
        email_group = ACQUIRER_EMAIL_GROUP[acquirer_name]
        return email_group
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return DEFAULT_EMAIL_ADDR


def GetContact(party, confirmation):
    for c in party.Contacts():
        if c.Fullname() == confirmation.CounterpartyContact():
            return c


def GetCounterpartyShortname(party, confirmation):
    del confirmation

    if party.Name() != 'SAFEX':
        return party.Name()
    return ''


def GetCounterpartyAlias(party, confirmation):
    del confirmation

    if 'ShortCode' in dir(party):
        if party.ShortCode():
            return party.ShortCode()
        return ''
    else:
        acm.Log('[ERROR] ShortCode custom method not available on party object. party.ShortCode()')


def GetCounterpartyFullname(party, confirmation):
    del confirmation

    if party.Fullname():
        return party.Fullname()
    return ''


def GetAcquirerContact(party, confirmation):
    for c in party.Contacts():
        if c.Fullname() == confirmation.AcquirerContact():
            return c


def GetCptyAcc(party, confirmation):
    del party
    accountWrapperList = acm.FArray()
    try:
        if confirmation.EventChlItem().Name() == 'Adjust Deposit':
            cf = confirmation.CashFlow()
            cf_CP__Acc_Ref = cf.AdditionalInfo().CP_Account_Ref()
            if cf_CP__Acc_Ref:
                account = acm.FAccount[cf_CP__Acc_Ref]
                accountWrapperList.Add(FAccountWrapper(account, 'Fixed Amount'))
                return accountWrapperList
            else:
                for money_flow in confirmation.Trade().MoneyFlows().AsArray():
                    if money_flow.SourceObject() != cf:
                        continue
                    accountWrapperList.Add(FAccountWrapper(money_flow.CounterpartyAccount(), money_flow.Type()))
                    return accountWrapperList

        allowedCashflowTypes = GetAllowedCashflowTypes(confirmation)
        for mf in confirmation.Trade().MoneyFlows(ael.date_today().add_days(-maxBankingDaysBack), None):
            if mf.Type() in allowedCashflowTypes:
                account = mf.CounterpartyAccount()
                if account and account not in [accountWrapper.account for accountWrapper in accountWrapperList]:
                    accountWrapperList.Add(FAccountWrapper(account, mf.Type()))

        return accountWrapperList

    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return []


def GetAcqrAcc(party, confirmation):
    del party
    accountWrapperList = acm.FArray()
    allowedCashflowTypes = GetAllowedCashflowTypes(confirmation)
    for mf in confirmation.Trade().MoneyFlows(ael.date_today().add_days(-maxBankingDaysBack), None):
        if mf.Type() in allowedCashflowTypes:
            account = mf.AcquirerAccount()
            if account and account not in [accountWrapper.account for accountWrapper in accountWrapperList]:
                accountWrapperList.Add(FAccountWrapper(account, mf.Type()))

    return accountWrapperList


def GetAllowedCashflowTypes(confirmation):
    """ Gets the list of allowed cashflow types for whose accounts should be displayed """

    trade = confirmation.Trade()
    allowedCashflowTypes = []
    if isCall(trade):
        allowedCashflowTypes.extend([
            'Fixed Amount',
            'Fixed Rate Adjustable'
        ])
    else:
        if SelectCorrectTemplateFields(confirmation) == EVENT_TYPE_NEW_TRADE:
            allowedCashflowTypes.extend([
                'Premium'
            ])
        else:
            allowedCashflowTypes.extend([
                'Fixed Amount',
                'Fixed Rate'
            ])
    return allowedCashflowTypes


def GetOurRef(party, confirmation):
    del confirmation
    if party.Fullname() and party.Fullname() == 'Barclays Bank of Botswana':
        return 'TREASURY OPS'
    else:
        return ''


def GetFormattedTelephone(contact, confirmation):
    del confirmation

    telephone = contact.Telephone()
    try:
        regex = re.compile('\+\d{0,2}')
        countryCode = regex.match(telephone).group(0)
        splitTelNo = re.sub(r"\B(?=(?:\d{4})+)", " ", re.split('\+\d{0,2}', telephone)[1]).split(' ')
        return '{0} (0){1} {2} {3}'.format(countryCode, splitTelNo[0] + splitTelNo[1],
                                           splitTelNo[2] + splitTelNo[3] + splitTelNo[4], splitTelNo[5])
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return telephone


# Account functions
# --------------------------------------------------------------------------------------------------

def GetAccCurr(accountWrapper, confirmation):
    del confirmation

    try:
        if accountWrapper.account.Currency():
            return accountWrapper.account.Currency().Name()
        else:
            return 'All'
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return None


def GetCorrBank(accountWrapper, confirmation):
    del confirmation

    try:
        return accountWrapper.account.CorrespondentBank().Name()
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return None


def GetAccNumber(accountWrapper, confirmation):
    del confirmation

    try:
        return accountWrapper.account.Account()
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return None


def GetAccCashflowType(accountWrapper, confirmation):
    del confirmation
    return accountWrapper.moneyflowType


# Instrument functions
# --------------------------------------------------------------------------------------------------

def DaysToMaturity(ins, confirmation):
    del confirmation

    days_to_maturity = to_date(ins.ExpiryDateOnly()) - to_date(acm_date('Today'))

    return days_to_maturity.days


def GetPayLeg(ins, confirmation):
    del confirmation

    for leg in ins.Legs():
        if leg.PayLeg():
            legs = acm.FArray()
            legs.Add(leg)
            return legs


def GetReceiveLeg(ins, confirmation):
    del confirmation

    for leg in ins.Legs():
        if not leg.PayLeg():
            legs = acm.FArray()
            legs.Add(leg)
            return legs


def GetCallMovement(ins, confirmation):
    del ins

    try:
        event = confirmation.EventChlItem().Name()
        if event == 'Adjust Deposit':
            return confirmation.CashFlow().FixedAmount()
        else:
            return 0
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return 0


def GetCallMovementAmt(ins, confirmation):
    return abs(GetCallMovement(ins, confirmation))


def GetCallMovementSgn(ins, confirmation):
    callMovement = GetCallMovement(ins, confirmation)
    if ins.IsCallAccount():
        callMovement = confirmation.Trade().Quantity() * callMovement

    if callMovement > 0:
        return ' (Payment)'
    else:
        return ' (Receipt)'


def GetDaysBetween(ins, confirmation):
    try:
        return ael.date(GetTrdValueDay(confirmation.Trade(), confirmation)).days_between(
            ael.date(GetInsExpiration(ins, confirmation)))
    except Exception as error:
        Utils.LogAlways('Exception occurred: %s' % error)
        traceback.print_stack()
        return None


def GetInsType(ins, confirmation):  # Adaptiv keywords
    instype = ins.InsType()
    trade = confirmation.Trade()
    if instype == 'Deposit':
        if ins.IsCallAccount():
            funding_ins_type = trade.AdditionalInfo().Funding_Instype()
            if funding_ins_type in CALL_DEP_FUND_INS_TYPE_DEFAULT:
                return funding_ins_type.upper()
            elif funding_ins_type in list(CALL_DEP_FUND_INS_TYPE_MAPPING.keys()):
                return CALL_DEP_FUND_INS_TYPE_MAPPING[funding_ins_type].upper()
            else:
                if GetTrdBuyOrSell(trade, confirmation) == 'Buy':
                    return 'CALL LOAN'
                else:
                    return 'CALL DEPOSIT'
        else:

            if GetTrdBuyOrSell(trade, confirmation) == 'Buy':
                return 'FIXED LOAN'
            else:
                return 'FIXED DEPOSIT'
    elif instype == 'Curr':
        trade = confirmation.Trade()
        if len(GetFxSwapTrades(trade, confirmation)) > 1:
            return 'FX SWAP'
        else:
            if GetCashTrdPoints(trade, confirmation) == 0:
                return 'FX SPOT'
            else:
                return 'FX FORWARD'
    elif instype == 'Bond':
        return 'GOVERNMENT BOND SALE AND PURCHASE'
    elif instype == 'FRN':
        return 'FRN'
    elif instype == 'Bill':
        return 'BILL SALE AND PURCHASE'
    elif instype == 'Option':
        return 'FX OPTION'
    elif instype == 'CurrSwap':
        return 'Currency Swap'
    elif instype == 'Combination':
        return 'FX Chooser Option'
    else:
        return instype


def GetInsExpiration(ins, confirmation):
    del confirmation
    return ins.ExpiryDate()[:10]


def GetInsDeliveryDate(ins, confirmation):
    return ael.date(GetInsExpiration(ins, confirmation)).add_days(ins.PayDayOffset())


def GetAllCFPayDays(ins, confirmation):
    del confirmation
    flows = ''
    for l in ins.Legs():
        for cf in l.CashFlows():
            if cf.CashFlowType() == 'Float Rate':
                flows = flows + str(ael.date(cf.PayDate()).to_ymd()[2]) + ' ' + GetMonth(
                    ael.date(cf.PayDate()).to_ymd()[1]) + ' ' + str(ael.date(cf.PayDate()).to_ymd()[0]) + '/ '
    return flows[0:len(flows) - 2]


def GetOptCallOrPut(ins, confirmation):
    del confirmation
    if ins.IsCallOption():
        return 'Call'
    else:
        return 'Put'


def GetOptCallAmnt(ins, confirmation):
    if ins.IsCallOption():
        return confirmation.Trade().Quantity()
    else:
        return confirmation.Trade().Quantity() * ins.StrikePrice()


def GetOptCallCurr(ins, confirmation):
    del confirmation
    if ins.IsCallOption():
        return ins.Underlying().Name()
    else:
        return ins.StrikeCurrency().Name()


def GetOptPutAmnt(ins, confirmation):
    if not ins.IsCallOption():
        return confirmation.Trade().Quantity()
    else:
        return confirmation.Trade().Quantity() * ins.StrikePrice()


def GetOptPutCurr(ins, confirmation):
    del confirmation
    if not ins.IsCallOption():
        return ins.Underlying().Name()
    else:
        return ins.StrikeCurrency().Name()


def GetOptType(ins, confirmation):
    return GetOptCallCurr(ins, confirmation) + ' Call / ' + GetOptPutCurr(ins, confirmation) + ' Put'


def GetResets(ins, confirmation):
    del confirmation
    Resets = acm.FList()
    for l in ins.Legs():
        if l.CashFlows():
            for cf in l.CashFlows().SortByProperty("StartDate", True):
                if cf.Resets():
                    for r in cf.Resets().SortByProperty("Day", True):
                        Resets.Add(r)

    return Resets


def GetCoupons(ins, confirmation):
    del confirmation

    Coupons = acm.FList()
    if ins.InsType() in ['FRN', 'CLN']:
        fleg = [leg for leg in ins.Legs() if leg.IsFloatLeg() is True]
        if fleg:
            for cf in fleg[0].CashFlows().SortByProperty("PayDate", True):
                Coupons.Add(cf)

    elif ins.InsType() in ['CD']:
        fleg = [leg for leg in ins.Legs() if leg.IsFixedLeg() is True]
        if fleg:
            cfs = fleg[0].CashFlows()
            if cfs:
                for cf in fleg[0].CashFlows().SortByProperty("PayDate", True):
                    Coupons.Add(cf)

    return Coupons


# Reset functions
# --------------------------------------------------------------------------------------------------

def Convert_Reset_Rate(reset, confirmation):
    del confirmation
    rate = reset.FixingValue() / 100
    return rate


def GetResetDay(reset, confirmation):
    del confirmation
    return reset.Day()[0:10]


def GetCashFlowPayDate(cf, confirmation):
    del confirmation
    return cf.PayDate()[0:10]


def GetCashFlowDate(reset, confirmation):
    del confirmation
    return reset.CashFlow().PayDate()[0:10]


def GetCashFlowAmount(reset, confirmation):
    return GetCFProjConverted(reset.CashFlow(), confirmation)


def GetForwardRate(reset, confirmation):
    Spread = 0
    ResetRate = reset.FixingValue()
    for l in confirmation.Trade().Instrument().Legs():
        Spread = l.Spread()
    return ResetRate + Spread


# Confirmation functions
# --------------------------------------------------------------------------------------------------

def GetTrdAcquirer(confirmation):
    trd = confirmation.Trade()
    return trd.Acquirer().Name()


def GetConfCreateData(confirmation):
    return acm.Time.DateFromTime(confirmation.CreateTime())


def GetEmailSubjectHeader(confirmation):
    space = " "
    trade_no = str(confirmation.Trade().Oid())
    counterparty = str(confirmation.Receiver().Fullname())
    event_name = confirmation.EventType()
    seq = (trade_no, counterparty, event_name)
    return space.join(seq)


def getCashPaymentId(confirmation):
    if 'Adjust Deposit' in confirmation.EventType():
        return confirmation.CashFlow().Oid()
    return ''


def getAmendmentFixed(confirmation):
    confirmation_type = confirmation.Type()
    event = confirmation.EventType()

    if confirmation_type == 'Amendment' and event == 'New Trade':
        return 'AMENDMENT_FIXED'


def getAmendmentAdjustDeposit(confirmation):
    confirmation_type = confirmation.Type()
    event = confirmation.EventType()

    if confirmation_type == 'Amendment' and event == 'Adjust Deposit':
        return 'AMENDMENT_ADJUSTDEPOSIT'


def GetTemplateToUse(confirmation):
    template = ''
    event_type = confirmation.EventType()

    if 'Call' in event_type or 'Novation' in event_type or 'Rate' in event_type or 'Ceded' in event_type:
        template = 'ABSA_Deposit_Ceding_Opening_RateChange'
    elif 'New Trade' in event_type:
        template = 'ABSA_Fixed_Term'
    elif 'Maturity Notice' in event_type or 'Close' in event_type:
        template = 'ABSA_Call_Txn_Maturity_Termination'
    elif 'Adjust Deposit' in event_type:
        template = 'ABSA_Notice_tranaction'
    elif 'Prolong Deposit' in event_type:
        template = 'ABSA_Prolong_Deposit'

    return template


def SelectCorrectTemplateFields(confirmation):
    event_name = confirmation.EventChlItem().Name()
    if event_name == 'New Trade':
        return EVENT_TYPE_NEW_TRADE
    elif event_name == 'New Trade Call':
        return EVENT_TYPE_NEW_TRADE_CALL
    elif event_name == 'Account Ceded':
        return EVENT_TYPE_ACCOUNT_CEDED
    elif event_name in ['Rate Fixing', 'Weighted Rate Fixing', 'Rate Fixing Call']:
        return EVENT_TYPE_RATE_FIXING
    elif event_name == 'Partial Close':
        return EVENT_TYPE_PARTIAL_CLOSE
    elif event_name == 'Maturity Notice':
        return EVENT_TYPE_MATURITY_NOTICE
    elif event_name == 'Novation':
        return EVENT_TYPE_NOVATION
    elif event_name == 'Close':
        return EVENT_TYPE_CLOSE
    elif event_name == 'Prolong Deposit':
        return EVENT_TYPE_PROLONG_DEPOSIT
    elif event_name == 'Rate Reset':
        return EVENT_TYPE_RATE_RESET
    return ''


def GetEventType(confirmation):
    return confirmation.EventType()


def GetConfType(confirmation):
    confirmation_type = confirmation.Type()
    event = confirmation.EventType()

    if confirmation_type == 'Cancellation':
        return 'CANCELLATION OF THE'
    elif confirmation_type == 'Amendment':
        return 'AMENDMENT OF THE'
    elif event == 'Adjust Deposit':
        return 'ADJUSTMENT TO THE'
    elif event == 'Account Ceded':
        return 'CEDING OF THE'
    elif event == 'New Trade':
        return ''
    elif event == 'New Trade Call':
        return 'OPENING OF'
    elif event == 'Prolong Deposit':
        return 'ROLLING OF THE'
    elif event == 'Maturity Notice':
        return 'MATURITY OF THE'
    elif event == 'Novation':
        return 'NOVATION OF YOUR'
    elif event == 'Close':
        return 'TERMINATION OF THE'
    elif event == 'Partial Close':
        return 'PARTIAL TERMINATION OF THE'
    elif event in ('Weighted Rate Fixing', 'Rate Fixing Call', 'Rate Fixing Call Amendment'):
        return 'RATE CHANGE OF THE'
    elif event == 'Rate Reset':
        return 'RATE RESET OF THE'
    else:
        return ''  # Requested by Legal


def GetNovatedCP(confirmation):
    old_cp = ''

    trade = confirmation.Trade()
    if trade.Type() == 'Novated Assigned':
        if trade.BusinessEvents():
            for link in trade.BusinessEvents().At(0).TradeLinks():
                if link.Trade().Type() == 'Normal':
                    return link.Trade().Counterparty().Name()
    return old_cp


def GetFileName(confirmation):
    del confirmation
    return 'Absa_Confirmation'


def GetAcquirerContactEmail(confirmation):
    party = confirmation.Acquirer()
    for i in party.Contacts():
        if i.Name() == confirmation.AcquirerContact():
            return i.Email()
    return None


def GetSpecialInstruction(confirmation):  # Adaptiv keywords
    SI = []
    trade = confirmation.Trade()
    # instrument = trade.Instrument()
    party = trade.Counterparty()
    acquire = trade.Acquirer()

    # Used to hide counterparty address.
    if acquire.Name() == 'Mauritius':
        if confirmation.Transport() == 'Email':
            try:
                from AddConfirmationInstructions import internalConfEmails
                if confirmation.CounterpartyAddress() != internalConfEmails['Mauritius IBD']:
                    if party.BusinessStatus().Name() in ['Barclays Staff', 'Personal Customer']:
                        SI.append('HideCptyAddr')
            except Exception as error:
                Utils.LogAlways('Exception occurred: %s' % error)
                traceback.print_stack()
                Utils.LogAlways('Adaptiv_XML_Functions GetSpecialInstruction - Import failed.')

    return SI


def GetLegalNotice(confirmation):
    """ Gets the Legal Notice based on the Confirmation Event type  """

    DEFAULT_LEGAL_NOTICE = 'The Commercial Terms detailed on this confirmation are subject to Terms and Conditions ' \
                           'of the Product Agreement.'
    CEDED_LEGAL_NOTICE = (
        'It is hereby confirmed that the Depositor has pledged and ceded in securitatem debiti all its rights, title '
        'and interest to the Pledged and Ceded Deposit Amount specified below to the Deposit Taker as continuing '
        'covering security, which is subject to the terms and conditions of the Product Agreement.'
    )

    if SelectCorrectTemplateFields(confirmation) == EVENT_TYPE_ACCOUNT_CEDED:
        return CEDED_LEGAL_NOTICE

    return DEFAULT_LEGAL_NOTICE


def IsShowSSI(confirmation):
    """ Returns TRUE if SSI info should be displayed, otherwise returns FALSE  """

    isShowSSI = 'TRUE'

    if (SelectCorrectTemplateFields(confirmation) in (
            EVENT_TYPE_ACCOUNT_CEDED,
            EVENT_TYPE_RATE_FIXING,
            EVENT_TYPE_RATE_RESET,
            EVENT_TYPE_NEW_TRADE_CALL
    )):
        isShowSSI = 'FALSE'

    return isShowSSI


def getCounterpartyAddress(confirmation):
    """Return the conterparty address according to the standard function in
    production environment, or a development email address if it is non prod
    environment.
    """

    prod_env = acm.FInstallationData.Select('').At(0).Name() == 'Production'
    if prod_env:
        return confirmation.CounterpartyAddress()
    else:
        return DEV_CONF_EMAIL


# Payment functions
# --------------------------------------------------------------------------------------------------

def GetPaymentPayOrReceive(payment, confirmation):
    del confirmation
    if payment.Amount() < 0:
        return "Pay"
    else:
        return "Receive"


def GetAbsoluteRoundPayment(payment, confirmation):
    del confirmation
    return abs(round(payment.Amount(), 2))


# Contact functions
# --------------------------------------------------------------------------------------------------

def GetContactAttention(contact, confirmation):
    del confirmation
    partyFullName = RemoveSpecialChar(contact.Party().Fullname())
    contactAttention = RemoveSpecialChar(contact.Attention())
    if partyFullName == contactAttention:
        return ""
    else:
        return contact.Attention()


# General functions
# --------------------------------------------------------------------------------------------------

def getCashFlowReset(cashFlow):
    thisCashFlowNumber = cashFlow.Oid()
    for reset in cashFlow.Resets():
        if thisCashFlowNumber == reset.CashFlow().Oid():
            return reset
    return None


def getCashFlowPaymentDate(cashFlow):
    today = str(datetime.datetime.today())[0:10]
    if ael.date(cashFlow.PayDate()) >= ael.date(today):
        return cashFlow
    return None


def Return_Trade(object, confirmation):
    del object
    return confirmation.Trade()


def RemoveSpecialChar(text):
    charList = ["'", "/", "\\", "_", "-", ",", "#", "`", " "]
    for i in charList:
        text = text.replace(i, "")
    return text


def GetMonth(month):
    if month == 1:
        return 'January'
    elif month == 2:
        return 'February'
    elif month == 3:
        return 'March'
    elif month == 4:
        return 'April'
    elif month == 5:
        return 'May'
    elif month == 6:
        return 'June'
    elif month == 7:
        return 'July'
    elif month == 8:
        return 'August'
    elif month == 9:
        return 'September'
    elif month == 10:
        return 'October'
    elif month == 11:
        return 'November'
    elif month == 12:
        return 'December'


def GetIsin(ins, confirmation):
    del ins
    trd = confirmation.Trade()
    ins = trd.Instrument()

    return ins.Isin()


def FxSwapFunctions(trdnbr, stringOut=0, rateOut=0, marginOut=0):
    selectASQL = '''
    select
        t.trdnbr,
        cf.pay_day,
        projected_cf(cf)    'Proj',
        l.payleg,
        curr.insid  'Curr'
    into PayLeg
    from
        trade t,
        leg l,
        cashflow cf,
        instrument curr
    where
            t.trdnbr = @TRDNBR
        and t.insaddr = l.insaddr
        and cf.legnbr = l.legnbr
        and curr.insaddr = l.curr
        and l.payleg = 'Yes'

    select
        t.trdnbr,
        cf.pay_day,
        projected_cf(cf)    'Proj',
        l.payleg,
        curr.insid  'Curr'
    into RecLeg
    from
        trade t,
        leg l,
        cashflow cf,
        instrument curr
    where
            t.trdnbr = @TRDNBR
        and t.insaddr = l.insaddr
        and cf.legnbr = l.legnbr
        and curr.insaddr = l.curr
        and l.payleg = 'No'

    select
        RL.pay_day  'Date',
        RL.Proj < 0 ? 'SELL' : 'BUY' 'Leg1',
        abs(RL.Proj) 'Leg1',
        RL.Curr,
        PL.Proj < 0 ? 'SELL' : 'BUY' 'Leg2',
        abs(PL.Proj) 'Leg2',
        PL.Curr,
        abs(PL.Proj)/abs(RL.Proj)   'Rate'
    from
        PayLeg PL,
        RecLeg RL
    where
        PL.pay_day = RL.pay_day
    '''

    out = ael.asql(selectASQL, 0, ['@TRDNBR'], ["'" + trdnbr + "'"])[1][0]

    rate = acm.FArray()
    ArrayOut = acm.FArray()
    for lineout in out:
        finalOut = str(lineout[0]) + ' We '
        rate.Add([lineout[0], lineout[7]])
        for i in lineout[1:4]:
            finalOut = finalOut + str(i) + ' '
        finalOut = finalOut + 'for '
        for i in lineout[5:7]:
            finalOut = finalOut + str(i) + ' '

        ArrayOut.Add(finalOut)

    if stringOut == 1:
        return ArrayOut
    if rateOut == 1:
        return rate
    if marginOut == 1:
        return abs(rate[0][1] - rate[1][1])  # Margin


def GetFXSwapCFsRate(object, confirmation):
    del confirmation
    return object[1]


def GetFXSwapCFsRateDate(object, confirmation):
    del confirmation
    return object[0]


def GetFormatted(rolling):
    if rolling == '1 Months':
        return 'Monthly'
    elif rolling == '1 Weeks':
        return 'Weekly'
    elif rolling == '6 Months':
        return 'Semi-annually'
    elif rolling == '3 Months':
        return 'Quarterly'
    elif rolling == '12 Months' or rolling == '1 Years':
        return 'Annually'
    elif rolling[0] == '0':
        return 'Maturity'  # Adaptiv keyword
    return rolling


def GetDematPaymentFlag(trade, confirmation):
    del confirmation
    mm_mminstype = mm_instype(trade)

    return mm_mminstype in ['NCC', 'FRN', 'LNCD']


def GetDematResetFlag(trade, confirmation):
    del confirmation
    mm_mminstype = mm_instype(trade)

    return mm_mminstype in ['FRN', 'LNCD']


class FAccountWrapper(object):
    """ FAccountWrapper - A wrapper for the FAccount class to allow stuffing in additional attributes"""

    def __init__(self, account, moneyflowType):
        """ FAccountWrapper Constructor

            [account] - The FAccount object
            [moneyflowType] - The moneyflow type containing this account - Either as Conuterparty or Acquirer account

        """

        self.account = account
        self.moneyflowType = 'Interest' if 'Rate' in moneyflowType else moneyflowType
