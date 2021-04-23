'''---------------------------------------------------------------------
CashManagementHooksDefault module contains functions called by CashManagment. 
It should never be edited. All functions in CashManagementHooksDefault can be 
overridden in a CashManagementHooks module. To do so, create a module called CashManagementHooks 
(or rename the CashManagementHooksDefault to CashManagementHooks) and copy the function 
declaration of the function you want to override into it. 
---------------------------------------------------------------------'''

def AdjustmentInitialAttributeValues(row):
    '''
    Used to set initial values in the Cash Transfer Instrument Definition when
    opened using "Adjust Cash" from the Portfolio sheet
    
    row: A acm.FSingleInstrumentAndTrades object
    return value: A dictionary where the Key is the FCashEntry attribute, and the value
    is the value to initially set on the source trade.
    '''
    return DefaultInitialAttrubuteValues(row)

def FXRateFixingInitialSourceAttributeValues(row):
    '''
    Used to set initial values in the Cash Transfer Instrument Definition when
    opened using "Fix RPL Fx Rate" from the Portfolio sheet
    
    row: A acm.FSingleInstrumentAndTrades object
    return value: A dictionary where the Key is the FCashDualCurrencyEntry attribute, and the value
    is the value to initially set on the source trade.
    '''
    return DefaultInitialAttrubuteValues(row)

def FXRateFixingInitialDestinationAttributeValues(row):
    '''
    Used to set initial values in the Cash Transfer Instrument Definition when
    opened using "Fix RPL Fx Rate" from the Portfolio sheet
    
    row: A acm.FSingleInstrumentAndTrades object
    return value: A dictionary where the Key is the FCashDualCurrencyEntry attribute, and the value
    is the value to initially set on the destination trade.
    '''
    return DefaultInitialAttrubuteValues(row)

def TransferInitialSourceAttributeValues(row):
    '''
    Used to set initial values in the Cash Transfer Instrument Definition when
    opened using "Transfer RPL" from the Portfolio sheet
    
    row: A acm.FSingleInstrumentAndTrades object
    return value: A dictionary where the Key is the FCashEntry attribute, and the value
    is the value to initially set on the source trade.
    '''
    return DefaultInitialAttrubuteValues(row)

def TransferInitialDestinationAttributeValues(row):
    '''
    Used to set initial values in the Cash Transfer Instrument Definition when
    opened using "Transfer RPL" from the Portfolio sheet
    
    row: A acm.FSingleInstrumentAndTrades object
    return value: A dictionary where the Key is the FCashEntry attribute, and the value
    is the value to initially set on the destination trade.
    '''
    return DefaultInitialAttrubuteValues(row)

def DefaultInitialAttrubuteValues(row):
    attributes = ['Counterparty',
                  'Portfolio',
                  'Acquirer',
                  'OptKey1',
                  'OptKey2',
                  'OptKey3',
                  'OptKey4']
                  
    d = GetSharedTradeAttributesFromRow(row, attributes)
    
    return {'Counterparty'    : d['Counterparty'],
            'Trade.Portfolio' : d['Portfolio'],
            'Trade.Acquirer'  : d['Acquirer'],
            'Trade.OptKey1'   : d['OptKey1'],
            'Trade.OptKey2'   : d['OptKey2'],
            'Trade.OptKey3'   : d['OptKey3'],
            'Trade.OptKey4'   : d['OptKey4']}
    
def GetSharedTradeAttributesFromRow(row, attributes):
    '''
    attributes: A list of trade attributes
    return: A dictionary with the attributes as key, and value is the value of the trades attribute
    if all the trades on the row have the same value, otherwise None
    '''
    trades = row.Trades().AsArray()
    firstTrade = trades.First()
    
    d = dict()
    for att in attributes:
        d[att] = firstTrade.GetProperty(att)
    
    for t in trades:
        found = False
        for att, val in list(d.items()):
            if val and (t.GetProperty(att) == val):
                found = True
            else:
                d[att] = None
        
        if not found:
            break
    
    return d
