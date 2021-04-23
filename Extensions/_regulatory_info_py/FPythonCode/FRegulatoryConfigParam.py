""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/FRegulatoryConfigParam.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryConfigParam -
DESCRIPTION:
    This file is used to read all the FParameters that are required by the component to function as expected
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import acm
class Enumeration_Dict:

    def __init__(self, enumList):
        lookup = { }
        i = 1
        for x in enumList:
            lookup[x] = i
            i = i + 1
        self.lookup = lookup

    def getAttributeValue(self, attr):
        attr = attr.strip()
        return self.lookup[attr]
        
class FRegulatoryConfigParam(object):
    _instance = None    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FRegulatoryConfigParam, cls).__new__(cls)
            cls._instance.config_parameters = cls._instance.read_config_parameters()
        else:
            cls._instance.set_parameters(cls._instance.config_parameters)
        return cls._instance
    
    def set_paramvalue(self, key, value):
        """sets the value of the given config parameter"""
        self.config_parameters[key] = value        

    def get_paramvalue(self, key):
        """gets the value of the given config parameter"""
        retval = ''
        try:
            retval = self.config_parameters[key]
            if isinstance(retval, str):
                retval = retval.strip()
        except:
            pass
        return retval
    
    def read_config_parameters(self):
        """reads the config parameters from FParameters within extension manager """
        key_list = []
        val_list = []
        context = acm.GetDefaultContext()
        extension_lst = {}
        extension_lst['RegulatoryInfoApp'] = ['FRegulatoryLogConfig', 'FRegulatoryNotificationConfig', 'FRegulatoryDefaultConfig', 'FIntegrationUtilsOverride', 'FRegulatoryRepLogConfig']
        for extn in  extension_lst['RegulatoryInfoApp']:
            config_extension = context.GetExtension("FParameters", "FObject", extn)                 
            if config_extension:
                for key in config_extension.Value().Keys():
                    key_list.append(str(key))
                for vals in config_extension.Value().Values():
                    vals = str(vals).split('#')[0]
                    if 0 == vals.count('{'):
                        vals = vals.replace("'", "")
                    val_list.append(str(vals))                      
        params_dict = dict(list(zip(key_list, val_list)))
        self.set_parameters(params_dict)
        return params_dict
        
    def set_parameters(self, params_dict):
        """set the RegulatoryInfo component specific FParameteres to common parameters to be used in code"""
        enumNames = ["INFO", "DEBUG", "WARNING", "ERROR"]
        enum = Enumeration_Dict(enumNames)
        if 'FREGULATORY_MESSAGE_VERBOSE' in params_dict:
            FParameterVerbosityLevel = params_dict['FREGULATORY_MESSAGE_VERBOSE'].strip()
        else:
            FParameterVerbosityLevel = 'WARNING'
        params_dict['FREGULATORY_VERBOSITY_LEVEL'] = enum.getAttributeValue(FParameterVerbosityLevel)