'''
P A C K A G E   I N S T A L L E R   P A R A M E T E R S   M A N A G E R

Copyright (c) 2015 by SunGard Front Arena AB
Author: Michael Gogins

This module stores, saves, and restores configurable parameters for the 
Package Installer system. Some of these parameters are global for the ADS, 
and some parameters are per user.

All parameters are stored in an FParameters object. Per-user parameters 
are stored in the Windows registry, and override default FParameters values. 

'''
import acm

import traceback
import _winreg

from string import Template
import os

debug = False
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
    
    def getVerboseValue(self, attr):
        attr = int(attr)
        for each_val in self.lookup:
            if self.lookup[each_val] == attr:
                return each_val

enumNames = ["INFO", "DEBUG", "WARNING", "ERROR"]
enum = Enumeration_Dict(enumNames)
                
class ParametersManager(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParametersManager, cls).__new__(cls)
            cls._instance.config_parameters = cls._instance.read_config_parameters()
        return cls._instance
    
    def read_config_parameters(self):
        """read config parameters"""
        key_list = []
        val_list = []
        try:
            import acm
            context = acm.GetDefaultContext()
            extension_list = ['PackageInstallerParameters']
            for extn in extension_list:
                config_extension = context.GetExtension("FParameters", "FObject", extn)
                if config_extension:
                    for key in config_extension.Value().Keys():
                        key_list.append(str(key))
                    for vals in config_extension.Value().Values():
                        vals = str(vals).split('#')[0]
                        vals = vals.replace("'", "")
                        vals = vals.replace('"', "")
                        val_list.append(str(vals))
                        if vals.lower() in ["'true'", "true"]:
                            vals = 'True'
                        if vals.lower() in ["'false'", "false"]:
                            vals = 'False'
            params_dict = dict(list(zip(key_list, val_list)))
            
            default_config_values = {   'Verbosity' : 'INFO', 'DefaultFolder' : 'C:\ProgramData\Front\Packages', 'DefaultFolderLocal' : 'C:\ProgramData\Front\Packages', \
                                        'AmbaMessageDatetimeFormat' : '%Y-%m-%d %H:%M:%S UTC', 'Category' : 'Demo;Tool;Application', 'Status' : 'Development;Beta;Internal;Production', \
                                        'AlwaysIgnoreObjectTypes' : "['FUserLog', 'FCashFlow', 'FReset', 'FLeg', \
                         'FInstrumentRegulatoryInfo', 'FTradeRegulatoryInfo', \
                         'FAel','FExtensionContext', 'FExtensionModule', \
                         'FPersistentText', 'FAdditionalInfo', \
                         'FBusinessProcessStep', 'FBusinessProcessDiary', \
                         'FPartyAlias', 'FStateChartTransition']"}
            default_bool_values = {     'ConfigurationVisible' : 'False', 'NoOverWriteExistingEntities' : 'False', 'NoOverWriteNewerEntities' : 'False', \
                                        'ShowDependencyTree' : 'True', 'ShowExcludedInDependencyTree' : 'True', 'TestMode' : 'False'}
            for each_config in default_config_values:
                if not params_dict.get(each_config):
                    print "Defaulting <%s> to <%s>, since it is either not mentioned in the FParameters or has an invalid value."%(each_config, default_config_values[each_config])
                    params_dict[each_config] = default_config_values[each_config]
            for each_config in default_bool_values:
                try:
                    if (not params_dict[each_config]) or (str(params_dict[each_config]).upper() not in ['TRUE', 'FALSE']):
                        print "Defaulting <%s> to <%s>, since it is either not mentioned in the FParameters or have an invalid value."%(each_config, default_bool_values[each_config])
                        params_dict[each_config] = default_bool_values[each_config]
                except Exception, e:
                    print str(e)
            params_dict['message_verbosity'] = enum.getAttributeValue(params_dict['Verbosity'])
            default_folder = params_dict['DefaultFolder']
            if default_folder:
                try:
                    os.stat(default_folder)
                except:
                    os.makedirs(default_folder)
        except Exception, e:
            params_dict = {}
        return params_dict

    #def set_paramvalue(self, key, value):
    def write(self, key, value):
        """sets the value of the given config parameter"""
        self.config_parameters[key] = value

    #def get_paramvalue(self, key):
    def read(self, key):
        """gets the value of the given config parameter"""
        retval = ''
        try:
            retval = self.config_parameters[key]
            if isinstance(retval, str):
                retval = retval.strip()
        except:
            pass
        return retval

