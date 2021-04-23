import ast
import acm
from FBDPCurrentContext import Logme
from FX_AUTOROLL_UTILS import AUTOROLL_UTILS

class AUTOROLL_PARAMETERS():
    def __init__(self, queryFolderName):
        self.__queryFolderName = queryFolderName
        self.__FParameterName = 'FxAutoRollCurrencySpecification'
        self.__currencyDictionaryName = 'currencyDictionary'
        self.__targetPortfolioName = 'targetPortfolio'
        self.__currencyDictionary = None
        self.__targetPortfolioDictionary = None
        self.__status = 'FO Confirmed'
        self.__getCurrencyDictionary()
        self.__getTargetPortfolioDictionary()
        
    def __get_parameter_dict(self, name):
        """get values from FParameter by name"""
        values = {}
        p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', name)

        try:
            template = p.Value()
        except AttributeError, e:
            Logme()('ERROR: Could not get the parameters ( %s ): %s' %(name, str(e)), 'ERROR')

        for k in template.Keys():
            k = str(k)
            value = str( template.At(k) )
            value = None if value == "" else value
            values[ str(k) ] = value
        return values
    
    def __getCurrencyDictionary(self):
        Logme()('DEBUG: Retrieving parameters for %s' %self.__currencyDictionaryName, 'DEBUG')
        try:
            self.__currencyDictionary = ast.literal_eval((self.__get_parameter_dict(self.__FParameterName))[self.__currencyDictionaryName])
        except Exception, e:
            Logme()('ERROR: Could not retrieve the currency config that contains the flags for O/N and T/N rolls as well as the destination portfolio.', 'ERROR')
            Logme()('ERROR: The missing config is in FParameters with name %s and attribute name %s' %(self.__FParameterName, self.__currencyDictionaryName), 'ERROR')
            Lofme()('ERROR: The error message: %s' %str(e), 'ERROR')

    def __getTargetPortfolioDictionary(self):
        Logme()('DEBUG: Retrieving parameters for %s' %self.__targetPortfolioName, 'DEBUG')
        try:
            self.__targetPortfolioDictionary = ast.literal_eval((self.__get_parameter_dict(self.__FParameterName))[self.__targetPortfolioName])
        except Exception, e:
            Logme()('ERROR: Could not retrieve the target portfolio config that contains the portfolio into which the initial trade should be booked per Query Folder.', 'ERROR')
            Logme()('ERROR: The missing config is in FParameters with name %s and attribute name %s' %(self.__FParameterName, self.__targetPortfolioName), 'ERROR')
            Lofme()('ERROR: The error message: %s' %str(e), 'ERROR')
    
    @property
    def currencyDictionary(self):
        return self.__currencyDictionary
    
    @property
    def targetPortfolioDictionary(self):
        return self.__targetPortfolioDictionary

    @property
    def status(self):
        return self.__status
