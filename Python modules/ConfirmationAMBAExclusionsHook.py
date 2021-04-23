"""
------------------------------------------------------------------------------------------------------------------------
MODULE                  :       ConfirmationAMBAExclusionsHook
PURPOSE                 :       Contains hook functions to exclude certain messages from being submitted to the AMB for
                                ATS consumption e.g. Generic instrument exclusions

------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date            Change no       Developer               Description
------------------------------------------------------------------------------------------------------------------------
2016-06-02      Prod Fix        Anwar Banoo             Initial Implementation.
2016-08-08      ABITFA-4401     Willie van der Bank     Added user ATS_ECONTRD_AMD_PRD for exclusion.
                                                        Added additional check to prevent messages for
                                                        instruments with no trades and for instruments
                                                        with no trades in a valid status.
                                                        Added additional check to prevent CFD and Stock
                                                        instruments on trade level.
                                                        Added additional check to exclude trades
                                                        based on statusses.
                                                        Modified to import functions from
                                                        SettlementAMBAExclusionsHook.
2016-11-03      CHNG0004066826  Willie van der Bank     Modified value fields to cater for nice_enum_names
                                                        on the AMBA = 0 or 1
                                                        Modified is_invalid_trades to include acquirer check
2016-12-06                      Willie van der Bank     added modify_instrument_message to remove unwanted
                                                        cash flows from instrument amba message to enhance
                                                        call account processing
                                                        Added check to is_invalid_reset to remove reset
                                                        messages on call accounts without a float ref link
                                                        since these will never rerate overnight
2018-05-11      CHG1000406751   Willie van der Bank     Modified the trade and instrument hooks to read
                                                        trade filter queries from the parameters module
2020-12-10      FAOPS-821       Tawanda Mukhalela       Added check for Bulk Static Updates to be excluded.
2021-02-23      FAOPS-1101      Tawanda Mukhalela       Added IMPRINT_PROD to users to exclude
------------------------------------------------------------------------------------------------------------------------
"""

import ael, acm
from SettlementAMBAExclusionsHook import (
    objects_by_name, object_by_name, is_invalid_instrument_user,
    is_generic_instrument, is_invalid_instrument_trades, is_invalid_trade,
    modify_instrument_message
)
from FConfirmationParameters import tradeFilterQueries


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

    if event_type_as_string == 'INSERT_INSTRUMENT' or event_type_as_string == 'UPDATE_INSTRUMENT':
        users_to_exclude = ('SDF_WRITE_PRD', 'ATS_ECONTRD_AMD_PRD', 'BULK_UPDATE', 'IMPRINT_PROD')
        if is_invalid_instrument_user(amba_message, users_to_exclude):
            result_tuple = None
        elif is_generic_instrument(amba_message):
            result_tuple = None
        elif is_invalid_instrument_trades(amba_message, tradeFilterQueries):
            result_tuple = None
        elif is_invalid_reset(amba_message):
            result_tuple = None
        else:
            modify_instrument_message(amba_message)

    elif event_type_as_string in ('INSERT_TRADE', 'UPDATE_TRADE'):
        if is_invalid_trade(amba_message, tradeFilterQueries):
            result_tuple = None
        if is_invalid_update_user(amba_message, 'TRADE'):
            result_tuple = None
    elif event_type_as_string == 'UPDATE_PARTY':
        if is_invalid_update_user(amba_message, 'PARTY'):
            result_tuple = None
    return result_tuple


def is_invalid_reset(instrument_message):
    """
    DESCRIPTION: If the instrument update is for a rerate process and there has been
                 no rate change then ignore.
    INPUT:       instrument_message: instrument event in the message broker format
    OUTPUT:      True or False
    """

    USERS_TO_EXCLUDE = ['ATS_FRERATE_PRD']

    _is_invalid_reset = False
    hasRef = False
    instrument_obj = object_by_name(instrument_message, ['', '+', '!'], 'INSTRUMENT')
    _user = instrument_obj.mbf_find_object('UPDAT_USRNBR.USERID')
    user = _user.mbf_get_value()
    if user in USERS_TO_EXCLUDE:
        for addinfo_obj in objects_by_name(instrument_obj, ['', '+', '!'], 'ADDITIONALINFO'):
            _field = addinfo_obj.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME')
            field = _field.mbf_get_value()
            if field == 'CallFloatRef':
                hasRef = True
                _fieldVal = addinfo_obj.mbf_find_object('VALUE')
                fieldVal = _fieldVal.mbf_get_value()
                today = acm.Time.DateToday()
                ZAR_calendar = acm.FCalendar['ZAR Johannesburg']
                prevBusDay = ZAR_calendar.AdjustBankingDays(today, -1)
                ytd = 1
                tdyPrice = 0
                try:
                    tdyPrice = acm.FInstrument[fieldVal].UsedPrice(today, 'ZAR', 'SPOT_SOB')
                    ytd = acm.FInstrument[fieldVal].UsedPrice(prevBusDay, 'ZAR', 'SPOT')
                except Exception, e:
                    print('Price entry failure lookup!')
                    print(e)
                if ytd == tdyPrice:
                    _is_invalid_reset = True
                    ael.log(user + " amba instrument message filtered out")

        if not hasRef:
            _is_invalid_reset = True
            ael.log(user + " amba instrument message filtered out")

    return _is_invalid_reset


def is_invalid_update_user(amba_message, table_name):
    trade_message = object_by_name(amba_message, ['', '+', '!'], table_name)
    update_user = trade_message.mbf_find_object('UPDAT_USRNBR.USERID')
    update_user_name = update_user.mbf_get_value()
    if update_user_name in ('BULK_UPDATE', 'IMPRINT_PROD'):
        return True
    return False
