"""
-------------------------------------------------------------------------------
MODULE
    LoanNoticeGeneral


DESCRIPTION
    Date                : 2018-06-14
    Purpose             :
    Requester           : Kgomotso Gumbo
    Developer           : Stuart Wilson


HISTORY
===============================================================================
2018-09-20    Stuart Wilson      FAOPS-97  Refactor additional module
2018-02-28    Stuart Wilson      Refactor to make task based
2019-04-30    Tawanda Mukhalela  Changed Cashflow lookup to include Previous Cashflow
-------------------------------------------------------------------------------"""

from datetime import datetime
import re

import acm

from at_logging import getLogger
import DocumentGeneral


LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def get_conf_date(confirmation):
    """
    This Function returns the Confirmation create time
    """
    if confirmation.IsInfant():
        date = acm.Time.DateToday()
    else:
        date = acm.Time.DateFromTime(confirmation.CreateTime())

    return datetime(*acm.Time.DateToYMD(date)).strftime('%d %B %Y')


def _get_counterparty_loan_trades(counterparty, acquirer, date=acm.Time.DateToday()):
    """
    Function to get counterparty trades
    """
    query_name = loan_notice_get_documentation_parameter('loan_notice_query_name')
    query_nodes = acm.FStoredASQLQuery[query_name].Query().AsqlNodes()
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AsqlNodes(query_nodes)
    asql_query.AddAttrNode('Counterparty.Oid', 'EQUAL', counterparty.Oid())
    asql_query.AddAttrNode('Acquirer.Oid', 'EQUAL', acquirer.Oid())
    asql_query.AddAttrNode('Instrument.Legs.Resets.Day', 'EQUAL', date)

    return asql_query.Select()


def convert_xml_to_dict(element):
    """
    Function to convert xml elements to dictionary
    """
    xml_dict = {}
    for temp in element[0]:
        xml_dict[temp.tag] = temp.text

    return xml_dict


def trade_filter(trade, date=acm.Time.DateToday()):
    """
    Function to filter trades through query folder and return trades that match counterparty
    """
    return _get_counterparty_loan_trades(trade.Counterparty(), trade.Acquirer(), date)


def check_valid_reset(trade, date=acm.Time.DateToday()):
    """
    Function to check with reset is valid
    """
    reset = _get_current_reset(trade, date)
    previous_reset = _get_prev_reset(reset)
    if reset is not None:
        if abs(reset.FixingValue()) > 0.0:
            if match_primelinked_trades(trade):
                if previous_reset:
                    if previous_reset.FixingValue() == reset.FixingValue():
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return True

    return False


def match_primelinked_trades(entry):
    """
    Function to match prime linked trades
    """
    pattern = re.compile('ZAR-PRIME', re.IGNORECASE)
    if get_instrument_leg_float_ref(entry.Instrument()):
        match = pattern.search(get_instrument_leg_float_ref(entry.Instrument()).Name())
        if match:
            return True

    return False


def get_instrument_leg_float_ref(ins_object):
    """
    Function to get the instrument leg float ref
    """
    return ins_object.MainLeg().FloatRateReference()


def get_current_cashflow(trade, date=acm.Time.DateToday()):
    """
    This Function gets the  instrument current cashflow.
    It checks if the cashflow is within the current date today,
    then returns the cashflow object
    """
    return _get_current_reset(trade, date).CashFlow()


def loan_notice_get_documentation_parameter(parameter_name):
    """
    Get a documentation FParameter value.
    """
    return str(DocumentGeneral.get_fparameter('ABSALoanNoticeParameters', parameter_name))


def sum_nominal_before_payday_repayment_notice(trade, date=acm.Time.DateToday()):
    """
    Function to sum all  nominal nominal before cashflow current pay day
    """
    nominal = 0
    leg = trade.Instrument().MainLeg()
    for cashflow in leg.CashFlows():
        if cashflow.PayDate() < date and cashflow.CashFlowType() == 'Fixed Amount':
            nominal += cashflow.Calculation().Nominal(CALC_SPACE, trade).Number()

    return nominal


def sum_nominal_before_payday(trade, date=acm.Time.DateToday()):
    """
    Function to sum all  nominal nominal before cashflow current pay day
    """
    nominal = 0
    leg = trade.Instrument().MainLeg()
    for cashflow in leg.CashFlows():
        if cashflow.PayDate() <= date and cashflow.CashFlowType() == 'Fixed Amount':
            nominal += cashflow.Calculation().Nominal(CALC_SPACE, trade).Number()

    return nominal


def is_prime_facility_present_in_element(element):
    """
    Checks for prime facility in element
    """
    pattern = re.compile('ZAR-PRIME', re.IGNORECASE)
    xml_list = list()
    for main in element:
        for temp in main:
            xml_list.append(temp.text)

    for val in xml_list:
        match = pattern.search(str(val))
        if match:
            return True
        else:
            return False


def conf_rate_notice_event(trade):
    """
    Function to check if event criteria for rate notice has been met
    """
    if trade in trade_filter(trade):
        if check_valid_reset(trade):
            return True

    return False


def have_all_trades_reset(trade):
    """
    Function to evaluate if all trades that need to be reset have been for today
    """
    trades = trade_filter(trade)

    for _trade in trades:
        if has_been_fixed_today(_trade):
            continue
        else:
            return False
    return True


def has_facility(trade):
    """
    Evaluates if trade has facility ID
    """
    facility = trade.AdditionalInfo().PM_FacilityID()
    return facility != '' and facility is not None


def _get_current_reset(trade, date=acm.Time.DateToday()):
    """
    Returns reset on leg with day value equal to date passed in
    """
    main_leg = trade.Instrument().MainLeg()
    sorted_resets = _get_all_resets_from_leg_sorted_by_day(main_leg)
    for reset in sorted_resets:
        if reset.Day() == date:
            return reset

    return None


def _get_all_resets_from_leg_sorted_by_day(leg):
    """
    Returns FArray of resets sorted by day for a specific instrument leg
    """
    cashflows = leg.CashFlows().AsArray()
    all_leg_resets = acm.FArray()
    for cashflow in cashflows:
        for reset in cashflow.Resets().AsArray():
            all_leg_resets.Add(reset)

    return all_leg_resets.SortByProperty('Day')


def _get_prev_reset(current_reset):
    """
    Returns the previous reset by day from a given reset
    """
    reset_leg = current_reset.CashFlow().Leg()
    sorted_resets = _get_all_resets_from_leg_sorted_by_day(reset_leg)

    return sorted_resets[sorted_resets.IndexOf(current_reset) - 1]


def has_been_fixed_today(trade):
    """
    Evaluates if trade was reset today
    """
    reset = _get_current_reset(trade)
    if reset:
        if reset.IsFixed():
            return True

    return False


def get_previous_cashflow(cashflow):
    """
    Returns previous cashflow based on paydate order with floating type
    """
    cashf_legnbr = cashflow.Leg().Oid()
    previous_cashflows = acm.FCashFlow.Select("leg={legnbr} and payDate<='{paydate}' and "
                                              "cashFlowType in ('Call Float Rate', 'Float Rate')"
                                              .format(legnbr=cashf_legnbr, paydate=cashflow.PayDate()))

    sorted_cashf = previous_cashflows.SortByProperty('PayDate', False)

    return sorted_cashf[0]
