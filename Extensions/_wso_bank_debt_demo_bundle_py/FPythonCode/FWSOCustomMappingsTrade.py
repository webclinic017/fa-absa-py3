""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSOCustomMappingsTrade.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOCustomMappingsTrade - 

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    User defined custom mappings in Front Arena. Define methods using custom written functions that return 
    values from unique WSO attribute ID:s (e.g. Trade_ID).
    
    Each of the methods in class WSOCustomMappings define additional key-value pairs that should be included
    in the dictionary. The FWSOCustomMappings is used by the external values hook.
    
    The dictionary evDict represents a trade from the WSO XML, where each key value pair is an attribute
    and its value.
    
    Example:
    evDict = {
        'Trade_ID': '16799',
        'Trade_TradeDate': '2014-07-22T00:00:00+01:00',
        'TradeTypeDescription': 'Purchase',
        [...]
    }
    
    # Example of mapping function
    def FA_Counterparty(evDict):
        # Mapping from WSO XML Trade_CounterCompany_ID to FCounterParty instance in ADS.
        mappings = {
            '500': 'European Investment Bank',
            '501': 'Investments Inc.',
            '502': 'Goldman Sachs',
            '503': 'Deutsche Bank',
            '504': 'Barclays Bank',
        }
        counterpartyId = evDict.get('Trade_CounterCompany_ID')
        counterparty = mappings.get(counterpartyId)
        return counterparty

    # Example of retrieving portfolio name from WSO XML for a trade
    def FA_Portfolio(evDict):
        mappings = {
            'ALPHA EUR': 'FA ALPHA EUR', # Portfolio "ALPHA EUR" maps to "FA ALPHA EUR" in the ADS
            [...]
        }
        portfolioId = evDict.get('Trade_Portfolio_ID')
        wsoPortfoliosDict = WSODictAccessor.Portfolio()
        wsoPortfolioDict = wsoPortfoliosDict.get(portfolioId)
        portfolioName = wsoPortfolioDict.get('Portfolio_Name')
        FA_portfolioName = mappings.get(portfolioName)
        return FA_portfolioName
    
-------------------------------------------------------------------------------------------------------"""

'''Custom defined functions used by custom defined methods.'''

def FA_Acquirer(evDict):
    # Mandatory mapping
    return 'Demo_Acquirer'

def FA_Portfolio(evDict):
    # Mandatory mapping
    return 'Wall Street Structure Arbitrage SP USD'

def FA_Counterparty(evDict):
    # Mandatory mapping
    return 'Demo_Counterparty'

def FA_Trader(evDict):
    # Mandatory mapping
    import acm
    return acm.UserName()
    
    
'''Custom defined methods responsible for retrieving custom mapped data.'''

class WSOCustomMappings(object):
    ''' Retrieves mapped data (from a custom defined dictionary) between a WSO XML attribute (key) and a Front Arena object name (value). 
        The custom methods are defined by their method name, used by the external values hook.
    '''
    
    def __init__(self, evDict):
        self.evDict = evDict
    
    # Mandatory mappings (for trade upload)
    def FA_Acquirer(self):      return FA_Acquirer(self.evDict)
    def FA_Counterparty(self):  return FA_Counterparty(self.evDict)
    def FA_Portfolio(self):     return FA_Portfolio(self.evDict)
    def FA_Trader(self):        return FA_Trader(self.evDict)    