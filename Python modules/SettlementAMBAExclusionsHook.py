'''----------------------------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementAMBAExclusionsHook
PURPOSE                 :       Contains hook functions to exclude certain messages from being submitted to the AMB for ATS
                                consumption e.g. FRerate exclusions

-------------------------------------------------------------------------------------------------------------------------------

HISTORY
===============================================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------------------------
2016-04-11      CHNG0003564575  Lawrence Mucheka        Initial Implementation.
2016-06-01      Prod Issue      Anwar Banoo             Filter out generic instruments.
2016-08-04      ABITFA-4401     Willie van der Bank     Added user ATS_ECONTRD_AMD_PRD for exclusion.
                                                        Added additional check to prevent messages for
                                                        instruments with no trades and for instruments
                                                        with no trades in a valid status.
                                                        Added additional check to prevent CFD and Stock
                                                        instruments on trade level.
                                                        Added additional check to exclude trades
                                                        based on statusses.
2016-08-19      Demat go-live   Willie van der Bank     Added error handling to is_invalid_trades
2016-09-20                      Mighty Mkansi           Added Void status on valid trades filter in order 
                                                        to remove settlements once a trade is voided
2016-11-03      CHNG0004066826  Willie van der Bank     Modified value fields to cater for nice_enum_names
                                                        on the AMBA = 0 or 1
                                                        Modified is_invalid_trades to include acquirer check
2016-11-28                      Willie van der Bank     added modify_instrument_message to remove unwanted
                                                        cash flows from instrument amba message to enhance
                                                        call account processing
2018-05-11      CHG1000406751   Willie van der Bank     Modified the trade and instrument hooks to read
                                                        trade filter queries from the parameters module
2020-04-20      SBL             Jaysen Naicker          Filter out Adaptiv settlement messages going to
                                                        Swift Solutions
2020-12-10      FAOPS-821       Tawanda MUkhalela       Added check for Bulk Static Updates to be excluded.
-------------------------------------------------------------------------------------------------------------------------------
'''

import ael, acm
from FSettlementParameters import maximumDaysForward, maximumDaysBack, tradeFilterQueries
from FSwiftServiceSelector import bypass_Swift_Solutions
import FSwiftMLUtils


def modify_outgoing_amba_message(amba_message, subject):
    """
    DESCRIPTION: Function called by AMBA before sending message to AMB.
                 To enable modification of outgoing AMBA messages, set
                 parameter ael_sender_modify in AMBA ini-file to reference
                 this function (also state the name of this module as a part of
                 parameter ael_module_name).

    INPUT:       amba_message: event in the message broker format.
                 subject: subject string in the format <instance name>/<table>
    OUTPUT:      Either None (no message will be sent to AMB), or the tuple pair
                 (amba_message, subject)
    """
    result_tuple = (amba_message, subject)
    event_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type_as_string = event_type.mbf_get_value()
    if event_type_as_string in ('INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT'):
        users_to_exclude = ['ATS_FRERATE_PRD', 'SDF_WRITE_PRD', 'ATS_ECONTRD_AMD_PRD', 'AGGREGATION', 'BULK_UPDATE']
        if is_invalid_instrument_user(amba_message, users_to_exclude):
            result_tuple = None
        elif is_generic_instrument(amba_message):
            result_tuple = None
        elif is_invalid_instrument_trades(amba_message, tradeFilterQueries):
            result_tuple = None
        else:
            modify_instrument_message(amba_message)
            
    elif event_type_as_string in ('INSERT_TRADE', 'UPDATE_TRADE'):
        if is_invalid_trade(amba_message, tradeFilterQueries):
            result_tuple = None
        if is_invalid_update_user(amba_message, 'TRADE'):
            result_tuple = None

    elif event_type_as_string in ('INSERT_SETTLEMENT', 'UPDATE_SETTLEMENT'):
        source_config = FSwiftMLUtils.Parameters('FSwiftSolutionConfig')
        source_param = getattr(source_config, 'AMBASenderSource', '')
        if subject == '%s/SETTLEMENT' % source_param:
            settlement_obj = object_by_name(amba_message, ['', '+', '!'], 'SETTLEMENT')
            _settlement_number = settlement_obj.mbf_find_object('SEQNBR')
            settlement_number = _settlement_number.mbf_get_value()
            settlement = acm.FSettlement[settlement_number]
            try:
                if bypass_Swift_Solutions(settlement):
                    ael.log("Adaptiv settlement amba message filtered out %s" % str(settlement_number))
                    result_tuple = None
            except Exception as e:
                ael.log('Error: %s' % (str(e.message)))
        if is_invalid_update_user(amba_message, 'SETTLEMENT'):
            result_tuple = None
    elif event_type_as_string == 'UPDATE_PARTY':
        if is_invalid_update_user(amba_message, 'PARTY'):
            result_tuple = None
    return result_tuple
    

def trade_match_all_filters(acmTrd, trade_filters):
    """
    Local function
    """
    for filter in trade_filters:
        if not acm.FStoredASQLQuery[filter].Query().IsSatisfiedBy(acmTrd):
            return False
    return True
    
    
def is_invalid_trade(trade_message, trade_filters):
    """
    DESCRIPTION: Excludes invalid trade messages.
    INPUT:       trade_message: trade event in the message broker format
    OUTPUT:      True or False
    """
    _is_invalid_trade = False
    trade_obj = object_by_name(trade_message, ['', '+', '!'], 'TRADE')
    _trdnbr = trade_obj.mbf_find_object('TRDNBR')
    trdnbr = _trdnbr.mbf_get_value()
    acmTrd = acm.FTrade[trdnbr]
    if acmTrd:
        if not trade_match_all_filters(acmTrd, trade_filters):
            ael.log("Invalid trade amba message filtered out %s" % str(acmTrd.Oid()))
            _is_invalid_trade = True
            return _is_invalid_trade
    else:
        ael.log("Invalid trade number:" + trdnbr)
    return _is_invalid_trade


def is_invalid_instrument_trades(instrument_message, trade_filters):
    """
    DESCRIPTION: Excludes instrument messages based on invalid trades.
    INPUT:       instrument_message: instrument event in the message broker
                 format
    OUTPUT:      True or False
    """

    _is_invalid_trades = False
    instrument_obj = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    _insid = instrument_obj.mbf_find_object('INSID')
    ins = _insid.mbf_get_value()
    acmIns = acm.FInstrument[ins]
    if acmIns:
        _is_invalid_trades = True
        for acmTrd in acmIns.Trades(): #Instrument with no trades will also be excluded
            if trade_match_all_filters(acmTrd, trade_filters):
                _is_invalid_trades = False
                return _is_invalid_trades
        ael.log("Invalid amba instrument message filtered out")
    else:
        ael.log("Invalid instrument ID:" + ins)
    return _is_invalid_trades
    

def is_invalid_instrument_user(instrument_message, USERS_TO_EXCLUDE):
    """
    DESCRIPTION: Excludes instrument messages based on the update user
    INPUT:       instrument_message: instrument event in the message broker format
    OUTPUT:      True or False
    """
    
    _is_invalid_instrument_user = False
    instrument_obj = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    _user = instrument_obj.mbf_find_object('UPDAT_USRNBR.USERID')
    user = _user.mbf_get_value()

    if user in USERS_TO_EXCLUDE:
        ael.log(user + " amba instrument message filtered out")
        _is_invalid_instrument_user = True

    return _is_invalid_instrument_user
    
    
def is_generic_instrument(instrument_message):
    """
    DESCRIPTION: If the instrument update is for market data purposes then ignore.
    INPUT:       instrument_message: instrument event in the message broker format
    OUTPUT:      True or False
    """

    _is_generic_instrument = False
    instrument_obj = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    _generic = instrument_obj.mbf_find_object('GENERIC')
    isGeneric = _generic.mbf_get_value()

    if isGeneric == 'Yes':
        ael.log("Generic instrument amba message filtered out")
        _is_generic_instrument = True

    return _is_generic_instrument
    

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
            cfwnbr = 0
            cfwnbr_obj = cash_flow_object.mbf_find_object('CFWNBR')
            if cfwnbr_obj:
                cfwnbr = cfwnbr_obj.mbf_get_value()
            ael.log("Cashflow filtered out, pay day is out of time window")

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
    end_day = ael.date_today().add_banking_day(ael.Instrument[currency], maximumDaysForward)
    start_day = ael.date_today().add_banking_day(ael.Instrument[currency], -maximumDaysBack)
    return start_day <= pay_day <= end_day


def objects_by_name(parent_obj, name_prefixes, name):
    """Get objects from AMBA message e.g. instruments """

    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()
        
        
def object_by_name(parent_obj, name_prefixes, name):
    """Get single object from AMBA message e.g. instrument """

    for obj in objects_by_name(parent_obj, name_prefixes, name):
        return obj
    return None


def is_invalid_update_user(amba_message, table_name):
    trade_message = object_by_name(amba_message, ['', '+', '!'], table_name)
    update_user = trade_message.mbf_find_object('UPDAT_USRNBR.USERID')
    update_user_name = update_user.mbf_get_value()
    if update_user_name == 'BULK_UPDATE':
        return True
    return False
