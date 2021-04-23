""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FExportUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of helper classes and functions for export base.
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FStateChartUtils
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")

def StandardExportEventId():
    return 'Export Executed'

def CreateStateChart(name, definition, layout=None, limit='Unlimited'):
    """Creates a state chart with the given name, if required.

    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).

    """
    sc = acm.FStateChart[name]
    if sc:
        return sc

    sc = acm.FStateChart(name=name)
    sc.BusinessProcessesPerSubject(limit)

    # Create all states, including those referenced in transitions
    state_names = definition.keys()
    for all_transitions in definition.values():
        state_names.extend([s for s in all_transitions.values() if s not in state_names])

    for state_name in (s for s in state_names if s not in ('Ready', 'Error')):
        sc.CreateState(state_name)
    sc.Commit()
    states = sc.StatesByName()

    # Link states based on transitions, creating events as required
    for state_name, transitions in definition.items():
        state = states.At(state_name)
        for event_name, to_state_name in transitions.items():
            event = acm.FStateChartEvent(event_name)
            to_state = states.At(to_state_name)
            state.CreateTransition(event, to_state)
    sc.Commit()

    if layout:
        sc.Layout().Text(layout)
        sc.Commit()
        logger.info('Successfully created state chart "{0}"'.format(sc.Name()))
    return sc	
	
def CreateStandardExportStateChart(name):
    exportEventId = StandardExportEventId()
    limit = 'Single'
    layout = 'Awaiting Confirmation,280,-76;Cancel,469,133;Corrected,280,59;Ready,91,-71;Cancel Sent,466,-70;Sent,92,139;'
    definition = {
        'Ready':                 {exportEventId:     'Sent'},
        'Sent':                  {'Void Trade':      'Cancel',
                                  'Correct Trade':   'Awaiting Confirmation'},
        'Awaiting Confirmation': {'Correction Confirmed': 'Corrected',
                                  'Void Trade':      'Cancel'},
        'Corrected':             {exportEventId:     'Sent',
                                 'Void Trade':      'Cancel'},
        'Cancel':                {exportEventId:     'Cancel Sent'},
    }
    return CreateStateChart(name, definition, layout, limit)

def CreateInstrumentExportStateChart_adv(name):
    exportEventId = StandardExportEventId()
    limit = 'Single'
    layout = 'Amended,280,-76;Cancel,469,133;Ready,91,-71;Cancel Sent,466,-70;Sent,92,139;'
    definition = {
        'Ready':                 {exportEventId:     'Sent'},
        'Sent':                  {'Void Instrument':      'Cancel',
                                  'Inst. Amended':   'Amended'},
        'Amended':               {exportEventId: 'Sent'},
        'Cancel':                {exportEventId:     'Cancel Sent'},
    }
    return CreateStateChart(name, definition, layout, limit)	
	
def CreateInstrumentExportStateChart(name):
    exportEventId = StandardExportEventId()
    limit = 'Single'
    layout = 'Awaiting Confirmation,280,-76;Cancel,469,133;Corrected,280,59;Ready,91,-71;Cancel Sent,466,-70;Sent,92,139;'
    definition = {
        'Ready':                 {exportEventId:     'Sent'},
    }
    return CreateStateChart(name, definition, layout, limit)

def TradeFilterQueriesForIntegration(tradeQueryPrefix):
    integrationQueries = list()
    allQueries = acm.FStoredASQLQuery.Select("")
    for storedQuery in allQueries:
        if storedQuery.Name().startswith(tradeQueryPrefix) and storedQuery.User() == None and storedQuery.Query().QueryClass() == acm.FTrade:
            integrationQueries.append(storedQuery)
    return integrationQueries

def FindMatchingQueryId(subject, ACMQueryIdList):
    """
    first query satisfying the subject type is picked
    Need to see if and for which query (often represents product type) the subject fits
    """
    if ACMQueryIdList:
        if type(ACMQueryIdList) == type(''):
            ACMQueryId = ACMQueryIdList
        else:
            ACMQueryId = ACMQueryIdList[0]
    #for ACMQueryId in ACMQueryIdList:
        ACMQuery = acm.FStoredASQLQuery[str(ACMQueryId)]
        assert ACMQuery, "No ACM query with name %s" % ACMQueryId
        qClass = ACMQuery.Query().QueryClass()
        #assert subject.IsKindOf(qClass), "Query '%s' is for %s, but the subject is %s" % (ACMQuery.Name(), qClass.Name(), subject.Class().Name())
        if ACMQuery.Query().IsSatisfiedBy(subject):
            return ACMQueryId
    return None

def RevertBusinessProcessesInErrorState(stateChartId):
    for bp in acm.BusinessProcess.FindByStateChart(acm.FStateChart[stateChartId]):
        if bp.CurrentStep().State().Name() == 'Error':
            try:
                bp.HandleEvent('Revert', notes=['Retry failed export'])
                bp.Commit()
            except RuntimeError as err:
                pass


class ExportTestMode(object):

    MODES = ('Disabled',
             'Disabled - Do NOT transfer export file(s)',
             'Enabled - Transfer export file(s)',
             'Enabled - Do NOT transfer export file(s)')
    DEFAULT_MODE = 'Disabled'

    def __init__(self, mode=DEFAULT_MODE):
        if mode not in self.MODES:
            raise ValueError('Invalid export test mode "' + str(mode) + '"')
        self._mode = mode

    def __str__(self):
        return self.Mode()

    def IsEnabled(self):
        return (self.Mode() == 'Enabled - Transfer export file(s)' or self.Mode() == 'Enabled - Do NOT transfer export file(s)')

    def IsFileTransferEnabled(self):
        return (self.Mode() == 'Enabled - Transfer export file(s)' or self.Mode() == 'Disabled')

    def Mode(self):
        return self._mode


class ExportParty(object):
    broker = 'Broker'
    acquirer = 'Acquirer'
    counterparty = 'Counterparty'

    exts = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition', 'trade_Broker')
    if len(exts) != 0:
        if exts[0].Value().GetString('ColumnName') != '':
            broker = exts[0].Value().GetString('ColumnName')
        if exts[0].Value().GetString('LabelList') != '':
            broker = exts[0].Value().GetString('LabelList').split(';')[0]
    exts = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition', 'trade_acquirer_ptynbr')
    if len(exts) != 0:
        if exts[0].Value().GetString('ColumnName') != '':
            acquirer = exts[0].Value().GetString('ColumnName')
        if exts[0].Value().GetString('LabelList') != '':
            acquirer = exts[0].Value().GetString('LabelList').split(';')[0]
    exts = acm.GetDefaultContext().GetAllExtensions('FColumnDefinition', 'trade_counterparty_ptynbr')
    if len(exts) != 0:
        if exts[0].Value().GetString('ColumnName') != '':
            counterparty = exts[0].Value().GetString('ColumnName')
        if exts[0].Value().GetString('LabelList') != '':
            counterparty = exts[0].Value().GetString('LabelList').split(';')[0]

    MODES = (broker,
             acquirer,
             counterparty)
    DEFAULT_MODE = broker

    def __init__(self, mode=DEFAULT_MODE):
        if mode not in self.MODES:
            raise ValueError('Invalid party "' + str(mode) + '"')
        self._mode = mode

    def __str__(self):
        return self.Mode()

    def Mode(self):
        return self._mode

    def GetPartyObj(self, trade):
        if self._mode in self.MODES:
            if self._mode == self.MODES[0]:
                return trade.Broker()
            elif self._mode == self.MODES[1]:
                return trade.Acquirer()
            elif self._mode == self.MODES[2]:
                return trade.Counterparty()
    
    
    
def ExportBusinessProcess(trade, stateChart):
    collection = acm.BusinessProcess().FindBySubjectAndStateChart(trade, stateChart)
    if collection:
        return collection[0]

def ExportBusinessProcessStates(businessProcess):
    if businessProcess:
        currentStep = businessProcess.CurrentStep()
        currentStepName = str(currentStep.State().Name())
        previousStep = currentStep.PreviousStep()
        previousStepName = 'None'
        if previousStep:
            previousStepName = str(previousStep.State().Name())
        return (previousStepName, currentStepName)
    return ('None', 'None')


def import_custom_integration_module(prepack_name):
    if not prepack_name:
        return None

    import importlib
    module_suffix = 'CustomIntegration'
    try:
        prepack_module = acm.GetDefaultContext().GetModule(prepack_name)
        python_files = prepack_module.GetAllExtensions('FPythonCode')
        custom_integration_files = [python_file for python_file in python_files
                                    if module_suffix in python_file.Name().Text()]
        if custom_integration_files:
            if len(custom_integration_files) > 1:
                logger.error("More than one Custom Integration Python module found.")
                return None

            return importlib.import_module(custom_integration_files[0].Name().Text())

        else:
            logger.error("Couldn't find Custom Integration Python module")
            return None

    except Exception as e:
        logger.error('Error while importing Custom Integration Python module. ' + str(e.message))
        return None


def create_add_info_spec(type, add_info_list):
    DATA_TYPE_ENUM = list(acm.FEnumeration['enum(B92StandardType)'].Values())
    for i in add_info_list:
        add_info_spec = acm.FAdditionalInfoSpec[i]
        if not add_info_spec:
            add_info_spec = acm.FAdditionalInfoSpec()
            add_info_spec.RecType(type)
            add_info_spec.DataTypeType(DATA_TYPE_ENUM.index('String'))
            add_info_spec.Name(i)
            add_info_spec.Description(i)
            add_info_spec.Commit()


def create_add_info(type, i):
    DATA_TYPE_ENUM = list(acm.FEnumeration['enum(B92StandardType)'].Values())
    add_info_spec = acm.FAdditionalInfoSpec[i]
    if not add_info_spec:
        add_info_spec = acm.FAdditionalInfoSpec()
        add_info_spec.RecType(type)
        add_info_spec.DataTypeType(DATA_TYPE_ENUM.index('String'))
        add_info_spec.Name(i)
        add_info_spec.Description(i)
        add_info_spec.Commit()
        logger.info('Additional Info Specification {} for record type {} created successfully.'.format(i, type))
    else:
        logger.warn('Additional Info Specification {} for record type {} already exists.'.format(i, type))


def check_parameter(param):
    aliases_types = [alias.Name() for alias in acm.FInstrAliasType.Select('')]
    addinfos_types = [addinfo.Name() for addinfo in acm.FAdditionalInfoSpec.Select("recType='Instrument'")]
    if param.Text() in aliases_types:
        return 'Alias'
    elif param.Text() in addinfos_types:
        return 'AdditionalInfo'
    elif isAttribute(acm.FInstrument, param):
        return 'Attribute'
    else:
        return None


def isAttribute(acmObj, attributes):
    if ":" not in attributes:#not alias and not addinfo
        attr = attributes.Text().split(".", 1)
        if len(attr) == 2:
            try:
                return isAttribute(acmObj.GetMethod(attr[0], 0).ValueDomain(), attr[1])
            except Exception as e:
                return False
        else:
            return acmObj.GetMethod(attr[0], 0) is not None      


def get_parameters(parameters_file):
    settings = acm.FDictionary()
    parameters = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', parameters_file)
    if parameters:
        settings.AddAll(parameters.Value())
    return settings


def InitialiseParameters():
    parameters = get_parameters("InstIdentifiers")
 
    paramTypes = acm.FDictionary()

    for p in parameters:
        parType = check_parameter(parameters[p])
        if parType:
            paramTypes[p] = acm.FDictionary()
            paramTypes[p][parameters[p]] = parType
    
    return paramTypes
    
def FindInsIdentifiers(ins, paramTypes):
    dict = acm.FOrderedDictionary()
    for iden in paramTypes:
        for value in paramTypes[iden]:
            idenValue = FindID(ins, value.Text(), paramTypes[iden][value])
            if idenValue:
                    dict[iden]= idenValue
    return dict

def FindID(inst, IdName, IdType):
    if IdType == 'Alias':
        ident = inst.Alias(IdName)
    elif IdType == 'AdditionalInfo':
        ident = inst.add_info(IdName) 
    elif IdType == 'Attribute':
        ident = getattr(inst, IdName)()
    else:
        ident = None
    return ident