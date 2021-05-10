""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSOCustomMappingsFacility.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOCustomMappingsFacility - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    User defined custom mappings for uploading facilities using the instrument upload tool in Front Arena. 
    
-------------------------------------------------------------------------------------------------------"""

#pylint: disable-msg=E0102


'''Custom defined functions used by custom defined methods.'''

import acm

def FA_CategoryChlItem(evDict):
    categoryChl = acm.FChoiceList.Select01("name = 'Category'", None)
    return str(categoryChl.Choices().First().Name()) if categoryChl else ''

def FA_Name(evDict):
    # Mandatory mapping
    from FWSOUtils import WSOUtils as utils
    facilityName = evDict.get('Facility_Name')
    return utils.RemoveUTFCharacters(facilityName)

def FA_CategoryChlItem(evDict):
    return ''

def FA_Issuer(evDict):
    return ''
    
'''Custom defined methods responsible for retrieving custom mapped data.'''

class WSOCustomMappingsFacility(object):
    ''' Retrieves mapped data (from a custom defined dictionary) between a WSO XML attribute (key) and a Front Arena object name (value). 
        The custom methods are defined by their method name, used by the external values hook.
    '''
    
    def __init__(self, evDict):
        self.evDict = evDict
    
    # Mandatory mappings (for facility upload)
    def FA_Name(self):             return FA_Name(self.evDict)
    def FA_CategoryChlItem(self):  return FA_CategoryChlItem(self.evDict)
    def FA_Issuer(self):           return FA_Issuer(self.evDict)