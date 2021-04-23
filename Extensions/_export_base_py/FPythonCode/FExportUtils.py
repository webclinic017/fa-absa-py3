""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FExportUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportUtils

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of helper classes and functions for export base.
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FStateChartUtils

logger = FAssetManagementUtils.GetLogger()


def StandardExportEventId():
    return 'Export Executed'

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
    return FStateChartUtils.CreateStateChart(name, definition, layout, limit)

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
    for ACMQueryId in ACMQueryIdList:
        ACMQuery = acm.FStoredASQLQuery[ACMQueryId]
        assert ACMQuery, "No ACM query with name %s" % ACMQueryId
        qClass = ACMQuery.Query().QueryClass()
        assert subject.IsKindOf(qClass), "Query '%s' is for %s, but the subject is %s" % (ACMQuery.Name(), qClass.Name(), subject.Class().Name())
        if ACMQuery.Query().IsSatisfiedBy(subject):
            return ACMQueryId
    return None

def RevertBusinessProcessesInErrorState(stateChartId):
    for bp in acm.BusinessProcess.FindByStateChart(acm.FStateChart[stateChartId]):
        if bp.CurrentStep().State().Name() == 'Error':
            bp.HandleEvent('Revert', notes=['Retry failed export'])
            bp.Commit()


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


class FileTransferAddInfoSpecCreator(object):
    """Class to create AdditionalInfoSpec for file transfer methods.
       Params: tuple with 3 elements:
           string addInfoSpecName
	       string addInfoSpecTable='Contact'
		   string addInfoSpecDataType='String'
       Example:
       add_info_specs = [('FTP Server', None, None), ('FTP Password', 'Contact', 'String')]
       for add_info_spec in add_info_specs:
           add_info_spec_creator = FileTransferAddInfoSpecCreator(add_info_spec)
           add_info_spec_creator.Create()"""

    DATA_TYPE_ENUM = list(acm.FEnumeration['enum(B92StandardType)'].Values())

    def __init__(self, addInfoSpec):
        self._aiSpecName = None
        self._aiSpecTable = None
        self._aiSpecDataType = None
        self.__class__.ValidateInput(addInfoSpec)
        self._PopulateData(addInfoSpec)
        self._ValidateData()

    @classmethod
    def ValidateInput(cls, addInfoSpec):
        if not isinstance(addInfoSpec, type(tuple())):
            if not 1 < len(addInfoSpec) < 3:
                raise Exception('Input must be a tuple with 3 elements')
            raise Exception('Input must be a tuple')

    def _PopulateData(self, addInfoSpec):
        self._aiSpecName = addInfoSpec[0]
        self._aiSpecTable = addInfoSpec[1]
        if self._aiSpecTable is None:
            self._aiSpecTable = 'Contact'
            logger.info('Add Info Spec table missing, defaulting to Contact')
        self._aiSpecDataType = addInfoSpec[2]
        if self._aiSpecDataType is None:
            self._aiSpecDataType = 'String'
            logger.info('Add Info Spec data type missing, defaulting to string')

    def _ValidateName(self):
        if not isinstance(self._aiSpecName, type(str())):
            raise Exception('Add Info Spec name must be a string')

    def _ValidateTable(self):
        tableName = 'ADM.%s' % self._aiSpecTable
        if not acm.FTable[tableName]:
            raise Exception('Add Info Spec table %s not found' % tableName)

    def _ValidateDataType(self):
        dataTypeEnum = self.__class__.DATA_TYPE_ENUM
        if self._aiSpecDataType not in dataTypeEnum:
            raise Exception('Add Info Spec data type %s is not valid. Please select one of the following %s' % (self._aiSpecDataType, str(dataTypeEnum)))

    def _GetIntFromDataType(self):
        return self.__class__.DATA_TYPE_ENUM.index(self._aiSpecDataType)

    def _ValidateData(self):
        self._ValidateName()
        self._ValidateTable()
        self._ValidateDataType()

    def _GetAddInfoSpec(self):
        return acm.FAdditionalInfoSpec[self._aiSpecName]

    def _CreateAddInfoSpecObject(self):
        try:
            ais = acm.FAdditionalInfoSpec()
            ais.Name(self._aiSpecName)
            ais.FieldName(self._aiSpecName)
            ais.DataTypeGroup('Standard')
            ais.DataTypeType(self._GetIntFromDataType())
            ais.RecType(self._aiSpecTable)
            ais.Commit()
        except RuntimeError as err:
            raise err

    def _CreateAddInfoSpec(self):
        add_info_spec = self._GetAddInfoSpec()
        if not add_info_spec:
            self._CreateAddInfoSpecObject()

    def Create(self):
        self._CreateAddInfoSpec()
