
import acm

def get_TradeReportTransType_string_from_value(val):
    '''
    Accepts value for TradeReportTransType, in FIX message and returns mapped value, which needs to be displayed in tradesheet for particular column.
    '''
    switcher = { 
        "0": "New", 
        "1": "Cancel", 
        "2": "Replace",
        "3": "Release",
        "4": "Reverse"
    } 
  
    ret = switcher.get(val, val)
    return ret

def get_TradeReportType_string_from_value(val):
    '''
    Accepts value for TradeReportType, in FIX message and returns mapped value, which needs to be displayed in tradesheet for particular column.
    '''
    switcher = { 
        "0": "Submit",
        "1": "Alleged",
        "2": "Accept",
        "3": "Decline",
        "4": "Addendum",
        "5": "No/Was",
        "6": "Trade Report Cancel",
        "7": "Locked In Trade Break"
    } 
  
    ret = switcher.get(val, val)
    return ret

def get_PartyRole_string_from_value(val):
    '''
    Accepts value for PartyRole, in FIX message and returns mapped value, which needs to be displayed in tradesheet for particular column.
    '''
    switcher = { 
        "1": "Executing Firm",
        "7": "Entering Firm",
        "14": "Giveup Firm",
        "17": "Contra Firm",
        "83": "Clearing Account"
    } 
  
    ret = switcher.get(val, val)
    return ret
