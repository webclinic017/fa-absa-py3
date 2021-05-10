""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSOCustomMappingsContract.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOCustomMappingsContract - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    
-------------------------------------------------------------------------------------------------------"""

'''Custom defined functions used by custom defined methods.'''

import acm

def FA_CategoryChlItem(evDict):
    categoryChl = acm.FChoiceList.Select01("name = 'Category'", None)
    return str(categoryChl.Choices().First().Name()) if categoryChl else ''

def FA_Issuer(evDict):
    return '' 
    
'''Custom defined methods responsible for retrieving custom mapped data.'''

class WSOCustomMappingsContract(object):
    ''' Retrieves mapped data (from a custom defined dictionary) between a WSO XML attribute (key) and a Front Arena object name (value). 
        The custom methods are defined by their method name, used by the external values hook.
    '''
    
    def __init__(self, evDict):
        self.evDict = evDict
            
    # Mappings
    def FA_CategoryChlItem(self):       return FA_CategoryChlItem(self.evDict)
    def FA_Issuer(self):                return FA_Issuer(self.evDict)