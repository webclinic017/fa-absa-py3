import acm

def get_instrument_alias_name(trade):
    '''
    Return instrument alias name to be used to report a trade to TRACE.
    This Alias should be available in instrument
    Return value should be either 
    1) FINRA_SYMBOL : when Exchange symbol is used.
    2) CUSIP : When CUSIP is used .
    '''

    return 'FINRA_SYMBOL'


def should_be_cancelled(trade):
    '''
    Return True if trade should be cancelled or False otherwise.
    It is up to the customer to decide when a trade should be cancelled.
    '''

    return False

def add_constraint_on_instrument_type():
    '''
    Returns tuple (action, instrument_list)
    - action is either True if constraint to be added or False as default (means no constraints are added and TRADS will listen to all instrument types)
    - instrument_list is list of instrument types on which constraints are added if action is set to TRUE

    TRADS will listen to only instrument types listed in below list. It is up to customer to decide for which instrument type constraint to be added.

    - Ex : instrument_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                            33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59. 60, 61,
                            62, 63, 64, 65, 66, 67, 68, 69]
    '''
    instrument_list = []
    addConstraint = False

    return addConstraint, instrument_list

def should_be_reported(trade):
    '''
    Return tuple (action, reportTo) where:
    - action is either True if trade is to be reported or False otherwise
    - reportTo is name of exchange service ('TRACE', ...) or '' if trade should not be reported.
    It is up to the customer to decide when a trade should be reported.
    '''

    return False, ''

def report_result(trade, result, errText = None):
    '''
    Modify the trade after a reporting is done (result indcates if success or not) so
    it does not report again if a trade is modified. errText contains any error text.
    '''
    pass


def cancel_result(trade, result, errText = None):
    '''
    Modify the trade after a cancel is done (result indcates if success or not) so
    it does not cancel again if a trade is modified. errText contains any error text.
    '''
    pass

    
def calc_trade_checksum(trade):
    '''
    Calculate a "checksum" for the trade do decide if trade is a candidate for 'should_be_reported'-analysis.
    Returns tuple (Replace, checksum) where Replce is True if returned checksum should replace TRADS built in checksum or False 
    if returned checksum should be appended to TRADS builtin checksum.
    If returned checksum is None, empty string or exception is raised, the TRADS built in checksum is used.
    Below is an example (same as TRADS uses) of "checksum" functionality where the checksum should replace TRADS builtin.

    def getRegName(r):    
        return r.Name() if r else ''
        
    ri = trade.RegulatoryInfo()
    for s in [trade.Instrument().Name(), trade.TradeTime(), trade.Currency().Name(), trade.Premium(), trade.Price(), trade.Quantity(), \
         getRegName(ri.OurOrganisation()), getRegName(ri.TheirOrganisation()), getRegName(ri.ReportingEntity())]:
        checkSum += str(s) + '/'
    return True, checkSum

    '''

    return ''

def enable_debug_log():
    '''
    Return True to enable debug logging
    Return False to disable debug logging
    '''
    return False

def get_lastQty(trade):
    '''
    Returns LastQty
    It should return value for LastQty, if customized lastQty value to be used, else returns None
    '''
    return None

def get_lastPx(trade):
    '''
    Returns LastPx
    It should return value for LastPx, if customized lastPx value to be used, else returns None.
    '''
    return None

def use_custom_party_mapping(trade):
    '''
        returns True, if custom party mapping to be used, and party mapping is implemented in FFIXCustom
        return False, if custom party mapping is not used, and default party mapping is used,
        If this returns True, repeating group of tag 552, should be implemented in FFIXCustom
    '''
    return False
