""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementAMBAHookTemp.py"
"""
FSettlementAMBAHookTemp

This is a template of amba hook that can be used for filtering out
AMBA messages that are irrelevant to receiving Settlement ATS. 
Note that this template imports FSettlementParameters but not other
parameters (python modules) that belong to Operations solution. It
is up to the customer to adopt the hook to own needs but note that
filtering on AMBA side can effect other ATS instances in case you
use same AMBA.

Adding or changing any of these hooks require a restart of the AMBA
for it to take affect.
"""
import ael, acm

# State instrument types valid for settlement processing.
# Here is an example where Deposit and Stock events are only sent:
# valid_instrument_types = ['Deposit', 'Stock']
# Note that valid_instrument_types should always be in synch with
# Insert Item filter configured i FSettlementParameters. The same goes
# for include_constraints AMBA setting.

valid_instrument_types = []

# State explicit insids as strings here.
# Here is an example where specific instrument name is not sent:
# exclude_instruments    = ['EUR/DEP/100614-110614/4.00']
# Note: this instrument must be valid instrument type from valid_instrument_types
exclude_instruments    = []

# State if portfolios are to be considered for filtering.
# By default trade portfolios are not checked (portfolio_filtering_mode = 0).
# If portfolio_filtering_mode = 1 then variables portfolios and
# exclude_portfolios will be considered and filtering will be based on those.
# Note: filtering on portfolios means not sending AMBA trade messages, however
# an instrument update can on Settlement ATS side trigger Settlement inserts/updates
portfolio_filtering_mode = 0

# State explicit portfolio names here.
# Here is an example where 2 portfolios are to be considered:
# portfolios       = ['myPortfolio']
# Note: variable portfolio_filtering_mode is considered to be 1
portfolios       = []

# State if configured portfolios are to be excluded (default) or included.
# Here is one example where ONLY portfolio myPortfolio2 is included:
# portfolio_filtering_mode = 1 AND portfolios = ['myPortfolio2'] AND exclude_portfolios = False
exclude_portfolios = True

# State if amba log should include information about filtered records
# By default nothing will be printed.
ambaLog = False


def modify_outgoing_amba_message(amba_message, subject):
    """
    DESCRIPTION: Function called by AMBA before sending message to AMB.
                 To enable modification of outgoing AMBA messages, set
                 parameter ael_sender_modify in AMBA ini-file to reference
                 this function (also state the name of this module as a part of
                 parameter ael_module_name).

                 In the first if-clause below, no message will
                 be sent to the AMB if the message is a trade, made in an
                 instrument of an instrument type, that is not found in the
                 list valid_instrument_types. In addition trade portfolio is
                 checked. AMB message for the trade that has portfolio
                 represented in the portfolio exclude list will not be sent.
                 On the other hand if the flag exclude_portfolios = False
                 then only trade AMB message with stated portfolios
                 will be sent.

                 If the message is an instrument event, of type INSERT or
                 UPDATE, no message will be sent to the AMB if the instrument
                 type is not found in the list valid_instrument_types. If the
                 instrument message contains cash flows with pay days beyond
                 the time frame of settlement processing, those cash flows will
                 be removed from the message before being sent to the AMB.
                 Time frame is based on number of days stated in maximumDaysForward
                 and maximumDaysBackfrom (see FSettlementParameters module).

                 Note that filtering on AMBA side might have effect on
                 corresponding ATS instances that might need that message. For
                 example do not stop voided trades since it can effect
                 cancellations or ammendments. In addition always reconcile
                 settings in Insert items queries that maybe are used as a part
                 of tradeFilterQueries in FAccountingParamsTemplate,
                 FConfirmationParametersTemplate or FSettlementParametersTemplate.

    INPUT:       amba_message: event in the message broker format.
                 subject: subject string in the format <instance name>/<table>
    OUTPUT:      Either None (no message will be sent to AMB), or the tuple pair
                 (amba_message, subject)
    """
    result_tuple = (amba_message, subject)
    event_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type_as_string = event_type.mbf_get_value()

    if (event_type_as_string == 'INSERT_TRADE' or event_type_as_string == 'UPDATE_TRADE'):
        if is_invalid_trade(amba_message):
            result_tuple = None
    elif (event_type_as_string == 'INSERT_INSTRUMENT' or event_type_as_string == 'UPDATE_INSTRUMENT'):
        if is_invalid_instrument(amba_message):
            result_tuple = None
        else:
            modify_instrument_message(amba_message)

    return result_tuple


def is_invalid_instrument(instrument_message):
    """
    DESCRIPTION: If the instrument type of input instrument_message cannot
                 be found in the list valid_instrument_types, the instrument
                 is considered to be invalid.
    INPUT:       instrument_message: instrument event in the message broker
                 format.
    OUTPUT:      True or False
    """
    _is_invalid_instrument = False
    instrument_obj = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    _type = instrument_obj.mbf_find_object('INSTYPE')
    type_value_string = _type.mbf_get_value()
    _insid = instrument_obj.mbf_find_object('INSID')
    insid = _insid.mbf_get_value()

    if type_value_string not in valid_instrument_types:
        if ambaLog:
            ael.log(type_value_string + " invalid instype, amba instrument message filtered out")
        return True

    if insid in exclude_instruments:
        if ambaLog:
            ael.log(insid + " invalid insid, amba instrument message filtered out")
        return True

    return _is_invalid_instrument

def is_invalid_trade(trade_message):
    """
    DESCRIPTION: If a trade, made in an instrument of an instrument type that is
                 not found in the list valid_instrument_types, the trade is
                 considered to be invalid.
    INPUT:       trade_message: trade event in the message broker
                 format.
    OUTPUT:      True or False
    """
    _is_invalid_trade = False
    trade_object =  object_by_name(trade_message, ['', '+', '!'], 'TRADE')
    insaddr_object = trade_object.mbf_find_object('INSADDR')

    if insaddr_object:
        insaddr_as_string = insaddr_object.mbf_get_value()
        if insaddr_as_string:
            instrument = ael.Instrument[int(insaddr_as_string)]
            if instrument:
                if instrument.instype not in valid_instrument_types:
                    if ambaLog:
                        ael.log(instrument.instype + " invalid instype, amba trade message filtered out")
                    return True
                if instrument.insid in exclude_instruments:
                    if ambaLog:
                        ael.log(instrument.insid + " invalid insid, amba trade message filtered out")
                    return True

    if trade_object:
        _is_invalid_trade = is_invalid_portfolio(trade_object)

    return _is_invalid_trade


def is_invalid_portfolio(trade_message):
    """
    DESCRIPTION: Returns True if portfolio is found in the portfolio list and
                 should be excluded or portfolio is not found in the list among
                 portfolios to be included. If portfolio_filtering_mode is 0
                 then this function will not be used.
                 This function handles Compound portfolios so if the portfolio
                 on the trade is part of compound portfolio then compound portfolio
                 is checked towards portfolio list.

                 Please note that as for all tables filtering on portfolios
                 can include risk because some AMBA messages might (not) be
                 sent when they should (not) and thereby receiver side (for
                 example Settlement ATS) might create unwanted results. Hence
                 this function is template and customers can implement as per
                 own wish.

    INPUT:       trade_message: trade event in the message broker format.
    OUTPUT:      True or False
    """
    if not portfolio_filtering_mode:
        return False

    portf_obj = trade_message.mbf_find_object('PRFNBR')
    if portf_obj:
        portf = ael.Portfolio[int(portf_obj.mbf_get_value())]
        if portf:
            for comp_portf in get_fcompoundportfolios(portf):
                ptype = "portfolio, trade filtered out"
                if comp_portf.IsKindOf(acm.FCompoundPortfolio):
                    ptype = "compound portfolio, trade filtered out"

                if comp_portf.Name() in portfolios:
                    if ambaLog and exclude_portfolios:
                        ael.log(portf.prfid + " found in portfolio list via " + ptype)
                    return exclude_portfolios
                else:
                    if ambaLog and not exclude_portfolios:
                        ael.log(portf.prfid + " not found in portfolio list via " + ptype)
    elif ambaLog:
        ael.log("portfolio not found in AMBA trade message, exclude_portfolios = " + exclude_portfolios)

    return not exclude_portfolios


def is_compound_portfolio(prf):
    return prf.compound == 'Yes'

def get_fcompoundportfolios(prf):
    compound_portfolios = []
    if not is_compound_portfolio(prf):
        for acmCompoundPortfolio in acm.FCompoundPortfolio.Select(''):
            physicalPortfolios = acmCompoundPortfolio.AllPhysicalPortfolios()
            for physicalPortfolio in physicalPortfolios:
                if physicalPortfolio.Oid() == prf.prfnbr:
                    compound_portfolios.append(acmCompoundPortfolio)
        if not compound_portfolios:
            compound_portfolios.append(acm.FPhysicalPortfolio[prf.prfid])
    return compound_portfolios

def modify_instrument_message(instrument_message):
    """
    DESCRIPTION: This function modifies an outgoing instrument message. If the
                 instrument contains cash flows with pay days beyond the time
                 frame of settlement processing, those cash flows will be
                 removed from the message
    INPUT:       instrument_message: instrument event in the message broker
                 format.
    OUTPUT:      Void
    """
    instrument_object = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    for leg_object in objects_by_name(instrument_object, ['', '+', '!'], 'LEG'):
        currency_object = leg_object.mbf_find_object('CURR.INSID')
        if currency_object:
            currency = currency_object.mbf_get_value()
            for cash_flow_object in objects_by_name(leg_object, ['', '+', '!'], 'CASHFLOW'):
                if cash_flow_can_be_removed_from_message(cash_flow_object, currency):
                    leg_object.mbf_remove_object()

def cash_flow_can_be_removed_from_message(cash_flow_object, currency):
    """
    DESCRIPTION: If the pay day of cash_flow_object is beyond the time frame
                 of settlement processing, this function will return True.

                 Please note that as for all tables filtering on cash flows
                 can include risk because some AMBA messages might (not) be
                 sent when they should (not) and thereby receiver side (for
                 example Settlement ATS) might create unwanted results. Hence
                 this function is template and customers can implement as per
                 own wish.

    INPUT:       cash_flow_object: cash flow in the message broker format.
                 currency: A string representing a currency
    OUTPUT:      True or False
    """
    is_removable = False
    pay_day_object = cash_flow_object.mbf_find_object('PAY_DAY')
    if pay_day_object:
        pay_day = pay_day_object.mbf_get_value()
        try:
            cf_date = ael.date(pay_day)
        except Exception as e:
            cf_date = ael.date('1900-01-01')
            cfwnbr_obj = cash_flow_object.mbf_find_object('CFWNBR')
            cfwnbr = 'No cfwnbr in amba message'
            if cfwnbr_obj:
                cfwnbr = cfwnbr_obj.mbf_get_value()
            ael.log('Cashflow paydate is invalid for cashflow: %s with error: %s' % (str(cfwnbr), str(e.message)))

        if not is_within_time_window(cf_date, currency):
            is_removable = True
            if ambaLog:
                cfwnbr = 0
                cfwnbr_obj = cash_flow_object.mbf_find_object('CFWNBR')
                if cfwnbr_obj:
                    cfwnbr = cfwnbr_obj.mbf_get_value()
                ael.log("Cashflow " + str(cfwnbr) + " is filtered out, pay day " + str(cf_date) + " is out of time window")

    return is_removable

def is_within_time_window(pay_day, currency):
    """
    DESCRIPTION: Function determining whether pay_day is within a calculated
                 time span. The time span is calculated from current date and
                 maximumDaysForward and maximumDaysBack in
                 FSettlementParameters.
    INPUT:       pay_day: date when cash flow is paid.
                 currency: A string representing a currency
    OUTPUT:      True or False
    """
    from FSettlementParameters import maximumDaysForward, maximumDaysBack

    end_day = ael.date_today().add_banking_day(ael.Instrument[currency], maximumDaysForward)
    start_day = ael.date_today().add_banking_day(ael.Instrument[currency], -maximumDaysBack)
    return (start_day <= pay_day <= end_day)

def objects_by_name(parent_obj, name_prefixes, name):
    """
    DESCRIPTION: Function for finding objects specified by input
                 parameter name. For example if name = CASHFLOW,
                 cash flow objects in message broker format will be returned.
    INPUT:       parent_obj: object in message broker format.
                 name_prefixes: string representing an event
                 name: a table name
    OUTPUT:      Iterator with objects in message broker format
    """
    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()

def object_by_name(parent_obj, name_prefixes, name):
    """
    DESCRIPTION: Function for finding object specified by input
                 parameter name.
    INPUT:       parent_obj: object in message broker format.
                 name_prefixes: string representing an event
                 name: a table name
    OUTPUT:      object in message broker format
    """
    for obj in objects_by_name(parent_obj, name_prefixes, name):
        return obj
    return None
