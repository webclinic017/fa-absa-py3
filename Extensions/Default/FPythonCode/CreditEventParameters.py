
import acm

# the following trade statuses will be excluded from the "Create Closing" drop down list
TRADE_STATUSES_CLOSING_EXCLUDE = ["Exchange", "Void", "Terminated", "Reserved", "Confirmed Void" ]

# the following trade statuses will be excluded from the "Modify Closing" drop down list
TRADE_STATUSES_MODIFY_CLOSING_EXCLUDE = ["Exchange", "Void", "Terminated", "Reserved", "Confirmed Void" ]

# the following trade statuses will be excluded from the "Modify Other" drop down list
TRADE_STATUSES_MODIFY_OTHER_EXCLUDE = ["Exchange", "Void", "Terminated", "Reserved", "Confirmed Void" ]

# the following instruments are supported by the Credit Event Processing application 
SUPPORTED_TYPES = ['Singlename CDS', 'Index CDS', 'Tranche CDS', 'Nth-To-Default CDS']

# Default Columns in the instrument table
INSTRUMENT_COLUMNS = ['Credit Event Process', 'Credit Event Instrument Type', 'SettlementType', 'Credit Event Expiry', 'Credit Event Position', 'Seniority', 'Credit Event Currency', 'Credit Event Reference Currency', 'Credit Event Restructuring']
# Default Columns in the trade table
TRADE_COLUMNS = ['Credit Event Instrument Name', 'Credit Event Contract', 'Credit Event Portfolio', 'Credit Event Trade Type', 'Credit Event Face Value', 'Credit Event Remaining Nominal', 'Counterparty', 'Credit Event Acquire Day']

INSTYPES = ['Credit Default Swap']
CLASSES  = [acm.FCreditDefaultSwap]

def TradeStatusClosingDefault():
    defaultValue = "FO Confirmed"
    return acm.EnumFromString("TradeStatus", defaultValue)
    
def TradeStatusModifyClosingDefault():
    defaultValue = "No Change"
    if defaultValue == "No Change":
        return 0
    else:
        return acm.EnumFromString("TradeStatus", defaultValue)
    
def TradeStatusModifyOtherDefault():
    defaultValue = "No Change"
    if defaultValue == "No Change":
        return 0
    else:
        return acm.EnumFromString("TradeStatus", defaultValue)
    
def InsTypeToClass():
    typeToClass = acm.FDictionary()
    [typeToClass.AtPut(INSTYPES[index], CLASSES[index]) for index in range(len(INSTYPES))]
    
    return typeToClass

def ClassToInsType():
    classToType = acm.FDictionary()
    [classToType.AtPut(CLASSES[index], INSTYPES[index]) for index in range(len(INSTYPES))]
    
    return classToType
