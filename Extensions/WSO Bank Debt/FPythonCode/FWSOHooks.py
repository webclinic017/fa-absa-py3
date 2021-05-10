""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOHooks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOHooks - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Global provider of hook methods for the Front Arena adapted dictionaries.
    
-------------------------------------------------------------------------------------------------------"""

import acm
from FWSOUtils import WSOUtils as utils
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class DefaultHooks(object):
    ''' Methods that define the default logic in case there is no hook function present.
    '''
    
    @classmethod
    def CombinationIssuerName(cls, assetBaseDict, facilityDict):
        return None
        
    @classmethod
    def CombinationName(cls, assetBaseDict):
        return utils.RemoveUTFCharacters(assetBaseDict.get('Asset_Name'))

    @classmethod
    def FrnIssuerName(cls, contractDict):
        return None

    @classmethod
    def RateIndexName(cls, contractDict):
        ''' Default logic for contract rate index names.
            Rate index name is defined as currency/rateRef/frequency, 
            e.g. USD/LIBOR/3M.
        '''
        def AsRollingPeriod(frequency):
            return str(12/int(frequency)) + 'm'
            
        logger.info('Default RateIndexName hook called.')
        currencyName = contractDict.get('Contract_CurrencyType_Identifier')
        rateRef = contractDict.get('Contract_FacilityOption_Name')
        frequency = contractDict.get('Contract_Frequency')
        rateIndexName = currencyName + '/' + rateRef + '/' + AsRollingPeriod(frequency).upper()
        rateIndexInADS = acm.FRateIndex[rateIndexName]
        if not rateIndexInADS:
            logger.error('No rate index with name %s has been created in the ADS.' % rateIndexName)
        return rateIndexInADS.Name() if rateIndexInADS else None


class HookOrDefault(object):
    ''' Tries to call a hook function. If it has not been defined, default
        logic (in DefaultHooks) will be called instead.
    '''
        
    @classmethod
    def RateIndexName(cls, contractDict):
        rateIndexName = None
        try:
            import FWSOCustomHooks
            rateIndexName = FWSOCustomHooks.RateIndexName(contractDict)
            logger.debug('A rate index hook was found. It will be used.')
        except ImportError:
            #logger.debug('The Rate Index Name hook function has not been defined (FWSOCustomHooks does not exist). Using built-in logic.')
            rateIndexName = DefaultHooks.RateIndexName(contractDict)
        except AttributeError:
            logger.debug('The Rate Index Name hook function has not been defined. Using built-in logic.')
            rateIndexName = DefaultHooks.RateIndexName(contractDict)
        except Exception as e:
            logger.error('There was an error when calling the RateIndexName hook function: %s' % e)
        logger.debug('Returned value from RateIndexName-function: %s' % rateIndexName)
        return rateIndexName
    
    @classmethod
    def CombinationIssuerName(cls, assetBaseDict, facilityDict):
        issuerName = None
        try:
            import FWSOCustomHooks
            issuerName = FWSOCustomHooks.CombinationIssuerName(assetBaseDict, facilityDict)
            logger.debug('A combination Issuer Name hook was found. Its value will be used.')
        except ImportError:
            issuerName = DefaultHooks.CombinationIssuerName(assetBaseDict, facilityDict)
        except AttributeError:
            logger.debug('A combination Issuer Name hook function has not been defined (function does not exist).')
            issuerName = DefaultHooks.CombinationIssuerName(assetBaseDict, facilityDict)
        except Exception as e:
            logger.error('There was an error when calling the combination Issuer Name hook function: %s' % e)
        logger.debug('Returned value from CombinationIssuerName-function: %s' % str(issuerName))
        return issuerName

    @classmethod
    def FrnIssuerName(cls, contractDict):
        issuerName = None
        try:
            import FWSOCustomHooks
            issuerName = FWSOCustomHooks.FrnIssuerName(contractDict)
            logger.debug('A FRN Issuer Name hook was found. Its value will be used.')
        except ImportError:
            issuerName = DefaultHooks.FrnIssuerName(contractDict)
        except AttributeError:
            logger.debug('A FRN Issuer Name hook function has not been defined (function does not exist).')
            issuerName = DefaultHooks.FrnIssuerName(contractDict)
        except Exception as e:
            logger.error('There was an error when calling the FRN Issuer Name hook function: %s' % e)
        logger.debug('Returned value from FrnIssuerName-function: %s' % str(issuerName))
        return issuerName
        
    @classmethod
    def CombinationCategoryName(cls, assetBaseDict):
        categoryName = None
        try:
            import FWSOCustomHooks
            categoryName = FWSOCustomHooks.CombinationCategoryName(assetBaseDict)
        except ImportError:
            pass
        except AttributeError:
            logger.debug('The combination category hook function has not been defined (function does not exist).')
        return categoryName
        
    @classmethod
    def CombinationName(cls, assetBaseDict):
        combinationName = None
        try:
            import FWSOCustomHooks
            combinationName = FWSOCustomHooks.CombinationName(assetBaseDict)
        except ImportError:
            logger.debug('Import of module %s failed.' % FWSOCustomHooks.__name__)
            combinationName = DefaultHooks.CombinationName(assetBaseDict)
        except AttributeError:
            logger.debug('The combination name hook function has not been defined (function does not exist). Using default logic.')
            combinationName = DefaultHooks.CombinationName(assetBaseDict)
        logger.debug('The name of instrument is %s.' % str(combinationName))
        return combinationName 
        
    @classmethod
    def FrnCategoryName(cls, contractDict):
        categoryName = None
        try:
            import FWSOCustomHooks
            categoryName = FWSOCustomHooks.FrnCategoryName(contractDict)
        except ImportError:
            pass
        except AttributeError:
            logger.debug('The FRN category hook function has not been defined (function does not exist).')
        return categoryName
