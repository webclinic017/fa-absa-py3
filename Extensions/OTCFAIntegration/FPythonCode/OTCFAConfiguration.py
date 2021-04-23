from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FAOTCConfiguration - Manage all AEL task parameters and default values for 
    all modules in the OTC-FA integration scripts.
    
    Copyright (c) 2006 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module is imported by OTCFAMarketServer, OTCFATradeServer, 
    OTCFAMarketServerController, OTCFATradeServerController, and OTCFASetup 
    for the purpose of managing all internal and external configuration, 
    including AEL task parameters.

ENDDESCRIPTION
"""
import acm
import cStringIO

class AelVariable:
    def __init__(self, name, label, tipe='string', choices=None, defaults=None, mandatory=1, multiple=1, tooltip='', inputhook=None, enabled=True):
        self.name = name
        self.label = label
        self.tipe = tipe
        self.choices = choices
        self.defaults = defaults
        self.mandatory = mandatory
        self.multiple = multiple
        self.tooltip = tooltip
        self.inputhook = inputhook
        self.enabled = enabled
    def getAsTuple(self):
        return (self.name, self.label, self.tipe, self.choices, self.defaults, self.mandatory, self.multiple, self.tooltip, self.inputhook, self.enabled)
        
class AelVariableModuleInfo:
    def __init__(self, aelVariable, module, page=None):
        self.aelVariable = aelVariable
        self.module = module
        self.page = page
    def getAsTuple(self):
        if self.page:
            label = self.aelVariable.label + '_' + self.page
        else:
            label = self.aelVariable.label
        v = list(self.aelVariable.getAsTuple())
        v[1] = label
        return tuple(v)
    def __str__(self):
        output = cStringIO.StringIO()
        output.write('Module:      %s\n' % self.module)
        output.write('  page:      %s\n' % self.page)
        output.write('  name:      %s\n' % self.aelVariable.name)
        output.write('  label:     %s\n' % self.aelVariable.label)
        output.write('  type:      %s\n' % self.aelVariable.tipe)
        output.write('  choices:   %s\n' % self.aelVariable.choices)
        output.write('  defaults:  %s\n' % self.aelVariable.defaults)
        output.write('  mandatory: %s\n' % self.aelVariable.mandatory)
        output.write('  tooltip:   %s\n' % self.aelVariable.tooltip)
        output.write('  enabled:   %s\n' % self.aelVariable.enabled)
        return output.getvalue()
        
class OTCFAConfiguration:
    def __init__(self):
        self.aelVariablesForNames = {}
        self.aelVariableModuleInfosForNamesForModules = {}
        self.aelVariableNamesInOrder = []
    def addAelVariable(self, name, label, tipe, choices, defaults, mandatory, multiple, tooltip):
        aelVariable = AelVariable(name, label, tipe, choices, defaults, mandatory, multiple, tooltip)
        if name in self.aelVariablesForNames:
            raise ValueError('AEL variable "%s" is already defined.' % name) 
        self.aelVariablesForNames[name] = aelVariable
        self.aelVariableNamesInOrder.append(name)
    def assignToModule(self, name, module, page=None):
        aelVariable = self.aelVariablesForNames[name]
        aelVariableModuleInfo = AelVariableModuleInfo(aelVariable, module, page)
        if not module in self.aelVariableModuleInfosForNamesForModules:
            self.aelVariableModuleInfosForNamesForModules[module] = {}
        if name in self.aelVariableModuleInfosForNamesForModules[module]:
            raise ValueError('AEL variable "%s" is already assigned to "%s".' % (name, module))
        self.aelVariableModuleInfosForNamesForModules[module][name] = aelVariableModuleInfo
    def getAelVariablesForModule(self, module):
        aelVariables = []
        moduleInfosForNames = self.aelVariableModuleInfosForNamesForModules[module]
        for name in self.aelVariableNamesInOrder:
            if name in moduleInfosForNames:
                moduleInfo = moduleInfosForNames[name]
                aelVariables.append(moduleInfo.getAsTuple())
        return aelVariables
    def getParametersForModule(self, module):
        parameters = {}
        moduleInfosForNames = self.aelVariableModuleInfosForNamesForModules[module]
        for name, moduleInfo in moduleInfosForNames.items():
            parameters[name] = moduleInfo.aelVariable.defaults
        return parameters
    def dump(self):
        for module, moduleInfosForNames in self.aelVariableModuleInfosForNamesForModules.items():
            for name, moduleInfo in moduleInfosForNames.items():
                print (moduleInfo)
     
'''
This is the global cache of configuration parameters
and default values used by all the modules and tasks.
'''
configuration = OTCFAConfiguration()

def allTaskKeys():
    result = []
    instances = acm.FAelTask.Instances()
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result

def allCurrencyPairKeys():
    result = []
    instances = acm.FCurrencyPair.Instances()
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result
    
def allUserKeys():
    result = []
    instances = acm.FUser.Instances()
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result

def allPortfolioKeys():
    result = []
    instances = acm.FPhysicalPortfolio.Instances()
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result
    
def allAcquirerKeys():
    result = []
    instances = acm.FParty.Select('type=%s' % acm.EnumFromString('PartyType', 'PARTY_INTERN_DEPT'))
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result

def allCounterpartyKeys():
    result = []
    instances = acm.FParty.Select('type=%s' % acm.EnumFromString('PartyType', 'PARTY_COUNTERPARTY'))
    for instance in instances:
        result.append(str(instance.Name()))
    result.sort()
    return result

configuration.addAelVariable('ats_task',
    'Name of ATS task',
    'string',
    allTaskKeys(),
    None,
    1,
    0,
    "Name of the task for ATS to run"
    )
configuration.assignToModule('ats_task', 'OTCFAMarketServerController')
configuration.assignToModule('ats_task', 'OTCFATradeServerController')

configuration.addAelVariable('action',
    'Action to perform',
    'string',
    ['Start', 'Report', 'Stop'],
    'Start',
    1,
    0,
    "Action to perform on 'Run'"
    )
configuration.assignToModule('action', 'OTCFAMarketServerController')
configuration.assignToModule('action', 'OTCFATradeServerController')

configuration.addAelVariable('ms_controller_port',
    'Remote controller port',
    'int',
    [9091],
    None,
    1,
    0,
    'Network port on localhost for remote control task (e.g. scheduled shutdown)')
configuration.assignToModule('ms_controller_port', 'OTCFAMarketServer', 'Server')
configuration.assignToModule('ms_controller_port', 'OTCFASetup', 'Market Server')
configuration.assignToModule('ms_controller_port', 'OTCFAMarketServerController', 'Server')

configuration.addAelVariable('ts_controller_port',
    'Remote controller port',
    'int',
    [9092],
    None,
    1,
    0,
    'Network port on localhost for remote control task (e.g. scheduled shutdown)')
configuration.assignToModule('ts_controller_port', 'OTCFATradeServer', 'Server')
configuration.assignToModule('ts_controller_port', 'OTCFASetup', 'Trade Server')
configuration.assignToModule('ts_controller_port', 'OTCFATradeServerController', 'Server')

configuration.addAelVariable('run_mode',
    'Run mode',
    'string',
    ['Static data only', 'Market data only', 'Static data and market data'],
    'Static data and market data',
    1,
    0,
    '''Static: Update static and market data, then exit.
Market: Update market data, then monitor real-time market data.
Both: Update static data and market data, then monitor real-time market data.''')
configuration.assignToModule('run_mode', 'OTCFAMarketServer')
configuration.assignToModule('run_mode', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('test_mode',
    'Test mode',
    'string',
    ['1', '0'],
    str(0),
    1,
    0,
    "Run without actually committing deals"
    )
configuration.assignToModule('test_mode', 'OTCFATradeServer')
configuration.assignToModule('test_mode', 'OTCFASetup', 'Trade Server')
    
configuration.addAelVariable('mds_ior_path', 
    'Pathname to Market Data Server IOR', 
    'string', 
    [r'C:/FCS/FAFXOpt/MDS'], 
    r'C:/FCS/FAFXOpt/MDS', 
    1, 
    0, 
    'Path to directory containing Interoperable Object Reference for Market Data Server (e.g. the Market Data Server log file directory)')
configuration.assignToModule('mds_ior_path', 'OTCFAMarketServer')
configuration.assignToModule('mds_ior_path', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('mds_username', 
    'Market Data Server username', 
    'string', 
    ['mdowner'], 
    '', 
    1, 
    0, 
    'Username for Market Data Server login')
configuration.assignToModule('mds_username', 'OTCFAMarketServer')
configuration.assignToModule('mds_username', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('mds_password', 
    'Market Data Server password', 
    'string', 
    ['mdowner'], 
    '', 
    1, 
    0, 
    'Password for Market Data Server login')
configuration.assignToModule('mds_password', 'OTCFAMarketServer')
configuration.assignToModule('mds_password', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('mds_dataset', 
    'Data set for Market Data Server', 
    'string', 
    ['IntraDay'], 
    'IntraDay', 
    1, 
    0, 
    'Data set for Market Data Server')
configuration.assignToModule('mds_dataset', 'OTCFAMarketServer')
configuration.assignToModule('mds_dataset', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('currency_pairs', 
    'Currency pairs', 
    'string', 
    allCurrencyPairKeys(), 
    None, 
    1, 
    1, 
    'Currency pairs (context mapping determines volatility structures, spot rates, and deposit rates)')
configuration.assignToModule('currency_pairs', 'OTCFAMarketServer')
configuration.assignToModule('currency_pairs', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('failover_retries',
    'Failover retries',
    'int',
    [3],
    3,
    1,
    0,
    'Number of attempts to start or restart before exit')
configuration.assignToModule('failover_retries', 'OTCFAMarketServer', 'Server')
configuration.assignToModule('failover_retries', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('failover_interval',
    'Retry interval (seconds)',
    'int',
    [120],
    120,
    1,
    0,
    'Seconds to wait before attempting to restart')
configuration.assignToModule('failover_interval', 'OTCFAMarketServer', 'Server')
configuration.assignToModule('failover_interval', 'OTCFASetup', 'Market Server')
    
configuration.addAelVariable('logmode',
    'Log mode',
    'string',
    ['0', '1', '2'],
    1,
    1,
    0,
    '0 for none, 1 for normal, 2 for debug')
configuration.assignToModule('logmode', 'OTCFAMarketServer', 'Logging')
configuration.assignToModule('logmode', 'OTCFATradeServer', 'Logging')
configuration.assignToModule('logmode', 'OTCFAMarketServerController', 'Logging')
configuration.assignToModule('logmode', 'OTCFATradeServerController', 'Logging')
configuration.assignToModule('logmode', 'OTCFASetup', 'Logging')

configuration.addAelVariable('log_to_console',
    'Log to console',
    'string',
    ['1', '0'],
    1,
    1,
    0,
    '1 to log to console, 0 not to log to console')
configuration.assignToModule('log_to_console', 'OTCFAMarketServer', 'Logging')
configuration.assignToModule('log_to_console', 'OTCFATradeServer', 'Logging')
configuration.assignToModule('log_to_console', 'OTCFAMarketServerController', 'Logging')
configuration.assignToModule('log_to_console', 'OTCFATradeServerController', 'Logging')
configuration.assignToModule('log_to_console', 'OTCFASetup', 'Logging')

configuration.addAelVariable('log_to_file',
    'Log to file',
    'string',
    ['1', '0'],
    1,
    1,
    0,
    '1 to log to file, 0 not to log to file')
configuration.assignToModule('log_to_file', 'OTCFAMarketServer', 'Logging')
configuration.assignToModule('log_to_file', 'OTCFATradeServer', 'Logging')
configuration.assignToModule('log_to_file', 'OTCFAMarketServerController', 'Logging')
configuration.assignToModule('log_to_file', 'OTCFATradeServerController', 'Logging')
configuration.assignToModule('log_to_file', 'OTCFASetup', 'Logging')

configuration.addAelVariable('ads_url',
    'Hostname:port for ADS',
    'string',
    ['localhost:9000'],
    '',
    1,
    0,
    "ADS hostname and network port for task"
    )
configuration.assignToModule('ads_url', 'OTCFAMarketServerController')
configuration.assignToModule('ads_url', 'OTCFATradeServerController')
configuration.assignToModule('ads_url', 'OTCFASetup')

configuration.addAelVariable('ads_username',
    'Username for ADS',
    'string',
    ['ARENASYS'],
    '',
    1,
    0,
    "ADS username for task"
    )
configuration.assignToModule('ads_username', 'OTCFAMarketServerController')
configuration.assignToModule('ads_username', 'OTCFATradeServerController')
configuration.assignToModule('ads_username', 'OTCFASetup')
        
configuration.addAelVariable('ads_password',
    'Password for ADS',
    'string',
    ['Holistic1'],
    '',
    1,
    0,
    "ADS password for task"
    )
configuration.assignToModule('ads_password', 'OTCFAMarketServerController')
configuration.assignToModule('ads_password', 'OTCFATradeServerController')
configuration.assignToModule('ads_password', 'OTCFASetup')

configuration.addAelVariable('ats_path',
    'Pathname to Arena Task Server',
    'string',
    [r'C:/Program Files/FRONT/Front Arena/ATS/ATS.exe'],
    '',
    1,
    0,
    "Complete pathname to the instance of the Arena Task Server to be used for running this task"
    )
configuration.assignToModule('ats_path', 'OTCFAMarketServerController')
configuration.assignToModule('ats_path', 'OTCFATradeServerController')
configuration.assignToModule('ats_path', 'OTCFASetup')

configuration.addAelVariable('otc_xml_output_path',
    'OTC XML output path',
    'string',
    [r'C:/FCS/FAFXOpt/OTC/xmlOutput'],
    r'C:/FCS/FAFXOpt/OTC/xmlOutput',
    1,
    0,
    "Full pathname for directory where OTC captures trades as XML files (e.g. " + r"'C:\FCS\FAFXOpt\OTC\xmlOutput'" + ")"
    )
configuration.assignToModule('otc_xml_output_path', 'OTCFATradeServer')
configuration.assignToModule('otc_xml_output_path', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('trader', 
    'Trader', 
    'string', 
    allUserKeys(), 
    'ARENASYS',
    1, 
    0, 
    "Default trader for all deals"
    )
configuration.assignToModule('trader', 'OTCFATradeServer')
configuration.assignToModule('trader', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('acquirer', 
    'Acquirer', 
    'string', 
    allAcquirerKeys(), 
    None, 
    1, 
    0, 
    "Default acquirer for all deals"
    )
configuration.assignToModule('acquirer', 'OTCFATradeServer')
configuration.assignToModule('acquirer', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('counterparty', 
    'Counterparty', 
    'string', 
    allCounterpartyKeys(), 
    None, 
    1, 
    0, 
    "Default counterparty for all deals"
    )
configuration.assignToModule('counterparty', 'OTCFATradeServer')
configuration.assignToModule('counterparty', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('portfolio', 
    'Portfolio', 
    'string', 
    allPortfolioKeys(), 
    None, 
    1, 
    0, 
    "Default portfolio for all deals"
    )
configuration.assignToModule('portfolio', 'OTCFATradeServer')
configuration.assignToModule('portfolio', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('instrument_val_group',
    'Instrument ValGroup',
    'string',
    ['FX'],
    'FX',
    1,
    0,
    "Instrument valuation group"
    )
configuration.assignToModule('instrument_val_group', 'OTCFATradeServer')
configuration.assignToModule('instrument_val_group', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('markets_for_locations',
    'FA Markets for OTC Locations',
    'string',
    ['{"NY":("New York 10 AM", 10.0)}'],
    '{"NY":("New York 10 AM", 10.0)}',
    1,
    0,
    '''Map FA cut time markets to OTC locations,
as a Python map from OTC location name to tuple(FA market name, cut time), 
e.g.: '("NY":("New York 10 AM", 10.00)' '''
    )
configuration.assignToModule('markets_for_locations', 'OTCFATradeServer')
configuration.assignToModule('markets_for_locations', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('settlement_type',
    'Default settlement type',
    'string',
    ['Cash', 'Physical Delivery'],
    'Cash',
    1,
    0,
    "Default type of delivery for final settlement"
    )
configuration.assignToModule('settlement_type', 'OTCFATradeServer', 'Settlement Types')
configuration.assignToModule('settlement_type', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('settlement_type_vanilla',
    'Default settlement type (Vanilla)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Physical Delivery',
    0,
    0,
    "Default type of delivery for final settlement (Vanilla)"
    )
configuration.assignToModule('settlement_type_vanilla', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_barrier',
    'Default settlement  type (Barrier)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Physical Delivery',
    0,
    0,
    "Default type of delivery for final settlement (Barrier)"
    )
configuration.assignToModule('settlement_type_barrier', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_digital_underlying',
    'Default settlement  type (Digital, payout in underlying)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Physical Delivery',
    0,
    0,
    "Default type of delivery for final settlement (Digital, payout in underlying currency"
    )
configuration.assignToModule('settlement_type_digital_underlying', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_digital_strike',
    'Default settlement  type (Digital, payout in strike)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Cash',
    0,
    0,
    "Default type of delivery for final settlement (Digital, payout in strike currency"
    )
configuration.assignToModule('settlement_type_digital_strike', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_asian',
    'Default settlement  type (Asian)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Cash',
    0,
    0,
    "Default type of delivery for final settlement (Asian)"
    )
configuration.assignToModule('settlement_type_asian', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_lookback',
    'Default settlement  type (Lookback)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Cash',
    0,
    0,
    "Default type of delivery for final settlement (Lookback)"
    )
configuration.assignToModule('settlement_type_lookback', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('settlement_type_barrier_forward',
    'Default settlement  type (Barrier Forward)',
    'string',
    ['Cash', 'Physical Delivery'],
    'Physical Delivery',
    0,
    0,
    "Default type of delivery for final settlement (Barrier Forward)"
    )
configuration.assignToModule('settlement_type_barrier_forward', 'OTCFATradeServer', 'Settlement Types')

configuration.addAelVariable('polling_interval',
    'Polling interval',
    'double',
    [.5],
    .5,
    1,
    0,
    "Seconds to wait before re-polling output directory"
    )
configuration.assignToModule('polling_interval', 'OTCFATradeServer', 'Server')
configuration.assignToModule('polling_interval', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('ms_logfile',
    'Logfile',
    'string',
    ['DT_FAOTCMarketServer.log'],
    'DT_FAOTCMarketServer.log',
    0,
    0,
    'Name of the log file')
configuration.assignToModule('ms_logfile', 'OTCFAMarketServer', 'Logging')
configuration.assignToModule('ms_logfile', 'OTCFASetup', 'Market Server')

configuration.addAelVariable('ts_logfile',
    'Logfile',
    'string',
    ['DT_FAOTCTradeServer.log'],
    'DT_FAOTCTradeServer.log',
    0,
    0,
    'Name of the log file')
configuration.assignToModule('ts_logfile', 'OTCFATradeServer', 'Logging')
configuration.assignToModule('ts_logfile', 'OTCFASetup', 'Trade Server')

configuration.addAelVariable('sc_logfile',
    'Logfile',
    'string',
    ['DT_FAOTCServerController.log'],
    'DT_FAOTCServerController.log',
    0,
    0,
    'Name of the log file')
configuration.assignToModule('sc_logfile', 'OTCFAMarketServerController', 'Logging')
configuration.assignToModule('sc_logfile', 'OTCFATradeServerController', 'Logging')

configuration.addAelVariable('setup_logfile',
    'Logfile',
    'string',
    ['DT_FAOTCSetup.log'],
    'DT_FAOTCSetup.log',
    0,
    0,
    'Name of the log file')
configuration.assignToModule('setup_logfile', 'OTCFASetup', 'Logging')
