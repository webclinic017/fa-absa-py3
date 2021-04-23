""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPGui.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
Module
    FBDPGui - Module with code used by the parameter GUI.

DESCRIPTION
    This module is the only module that can be reloaded at the top of the
    start script, since it is needed before ael_main. All other modules shall
    be reloaded in the beginning of ael_main.
----------------------------------------------------------------------------"""
import collections
import itertools
import os
import tempfile

import acm
import ael

def defaultLogDir():
    path = FBDPParameters().Logdir
    getLogDir = acm.GetFunction('getLogDir', 0)
    if not path and getLogDir:
        path = getLogDir()

    if os.path.isdir(path):
        return path
    return tempfile.gettempdir()


class Parameters:
    def getData(self, *names):
        for FParameter in names:
            p = acm.GetDefaultContext().GetExtension('FParameters',
                    'FObject', FParameter)
            try:
                template = p.Value()
            except AttributeError:
                continue
            for k in template.Keys():
                k = str(k)
                setattr(self, k, str(template.At(k)))

    def __init__(self, *names):
        #self.mainParameter = names[-1]
        self.getData(*names)

    def __str__(self):
        return str(self.__dict__)

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise Exception('Variable {0} was not found. Please check the '
                    'FParameters tab in the Extension Manager.'.format(attr))


def FBDPParameters():
    return Parameters('FBDPParameters')

defaultFileFilter = (
    'XML Files (*.xml)|*.xml|'
    'CSV Files (*.csv)|*.csv|'
    'DAT Files (*.dat)|*.dat|'
    'Text Files (*.txt)|*.txt|'
    'All Files (*.*)|*.*||'
)

def inputFileSelection(fileFilter=defaultFileFilter):
    # Prepare selection for retrieving an existing file
    input_file_selection = acm.FFileSelection()
    input_file_selection.FileFilter = fileFilter
    input_file_selection.PickExistingFile(True)
    return input_file_selection


def outputFileSelection(fileFilter=defaultFileFilter):
    # Prepare selection for getting filename to save to
    output_file_selection = acm.FFileSelection()
    output_file_selection.FileFilter = fileFilter
    output_file_selection.PickExistingFile(False)
    return output_file_selection


def directorySelection():
    # Prepare selection for retrieving a directory
    dir_selection = acm.FFileSelection()
    dir_selection.PickDirectory(True)
    return dir_selection


def instrumentQuery(instype=()):
    # Create empty question or get default question for certain class
    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    # enum
    op = q.AddOpNode('OR')
    if instype:
        for i in instype:
            op.AddAttrNode('InsType', 'EQUAL',
                    ael.enum_from_string('InsType', i))
    else:
        op.AddAttrNode('InsType', 'EQUAL', None)
    # integer field
    op = q.AddOpNode('AND')
    op.AddAttrNode('Trades.Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Trades.Oid', 'LESS_EQUAL', None)
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Trades.Portfolio.Name', 'EQUAL', None)
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('OrderBooks.MarketPlace.Name', 'EQUAL', None)
    return q


def insertInstruments(expiryEnd=None, expiryStart=None, generic=0, instype=(),
        showStrike=False):
    q = instrumentQuery(instype=instype)
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('Underlying.InsType', 'EQUAL', None)
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Underlying.Name', 'RE_LIKE_NOCASE', None)
    # bool
    op = q.AddOpNode('OR')
    op.AddAttrNode('Otc', 'EQUAL', None)
    # date field
    op = q.AddOpNode('AND')
    op.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', expiryStart)
    op.AddAttrNode('ExpiryDate', 'LESS_EQUAL', expiryEnd)
    if showStrike:
        op = q.AddOpNode('AND')
        op.AddAttrNode('StrikePrice', 'GREATER_EQUAL', 0)
        op.AddAttrNode('StrikePrice', 'LESS_EQUAL', 100)
    # bool
    op = q.AddOpNode('OR')
    op.AddAttrNode('Generic', 'EQUAL', generic)
    return q


def insertStock():
    q = instrumentQuery(instype=('Stock',))
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('derivatives.trades.oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('derivatives.trades.oid', 'LESS_EQUAL', None)
    return q


def insertNewInstrument():
    return insertInstruments(instype=('Stock', 'Option', 'Warrant'))


def insertCombinations():
    return insertInstruments(instype=('Combination', 'EquityIndex'))


def insertDividend(instruments=None):
    q = acm.CreateFASQLQuery(acm.FDividend, 'AND')
    if instruments:
        op = q.AddOpNode('OR')
        for i in instruments:
            op.AddAttrNode('Instrument.Name', 'EQUAL', i)

    return q


def insertRollback():
    q = acm.CreateFASQLQuery(acm.FRollbackSpec, 'AND')
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('CreateUser.Name', 'RE_LIKE_NOCASE', None)
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('CreateTime', 'GREATER_EQUAL', '0d')
    op.AddAttrNode('CreateTime', 'LESS_EQUAL', '')
    return q


def insertReconciliationDoc(greater_equal='0d', less_equal=''):
    q = acm.CreateFASQLQuery(acm.FReconciliationDocument, 'AND')
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('ReconciliationName', 'RE_LIKE_NOCASE', None)
    # integer
    op = q.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Oid', 'LESS_EQUAL', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('ObjectType', 'RE_LIKE_NOCASE', None)
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('StartDate', 'EQUAL', None)
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('CreateTime', 'GREATER_EQUAL', greater_equal)
    op.AddAttrNode('CreateTime', 'LESS_EQUAL', less_equal)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('CreateUser.Name', 'RE_LIKE_NOCASE', None)
    return q


def insertLimits(greater_equal='0d', less_equal=''):

    q = acm.CreateFASQLQuery(acm.FLimit, 'AND')
    # integer
    op = q.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Oid', 'LESS_EQUAL', None)
    #
    q.AddOpNode('AND').AddAttrNode('LimitSpecification.Name', 'RE_LIKE_NOCASE', None)
    #
    q.AddOpNode('AND').AddAttrNode('LimitSpecification.LimitType.Name', 'EQUAL', None)
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('CreateTime', 'GREATER_EQUAL', greater_equal)
    op.AddAttrNode('CreateTime', 'LESS_EQUAL', less_equal)
    #
    q.AddOpNode('AND').AddAttrNode('LimitSpecification.RealtimeMonitored', 'EQUAL', True)
    return q


def insertTrades(expiryEnd=None, expiryStart=None):

    q = acm.CreateFASQLQuery(acm.FTrade, 'AND')  # empty query
    #q = CreateDefaultFASQLQuery(FTrade) # trade default query
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.Name', 'RE_LIKE_NOCASE', None)
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', None)
    # integer
    op = q.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Oid', 'LESS_EQUAL', None)
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Portfolio.Name', 'EQUAL', None)
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.OrderBooks.MarketPlace.Name', 'EQUAL', None)
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.Underlying.InsType', 'EQUAL', None)
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.Underlying.Name', 'RE_LIKE_NOCASE', None)
    # bool
    op = q.AddOpNode('OR')
    op.AddAttrNode('Instrument.Otc', 'EQUAL', None)
    # date field
    op = q.AddOpNode('AND')
    op.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', expiryStart)
    op.AddAttrNode('Instrument.ExpiryDate', 'LESS_EQUAL', expiryEnd)
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Acquirer.Name', 'EQUAL', None)
    # Text
    op = q.AddOpNode('OR')
    op.AddAttrNode('Counterparty.Name', 'EQUAL', None)
    return q


def insertOpenEndIns():
    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')  # empty query
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('InsType', 'EQUAL', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('Legs.LegType', 'EQUAL', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('OpenEnd', 'EQUAL',
            ael.enum_from_string('OpenEndStatus', 'Open End'))
    return q


def insertResets():
    q = acm.CreateFASQLQuery(acm.FReset, 'AND')  # empty query
    # date field
    op = q.AddOpNode('AND')
    op.AddAttrNode('Day', 'GREATER_EQUAL', None)
    op.AddAttrNode('Day', 'LESS_EQUAL', '0d')
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('FixingValue', 'GREATER_EQUAL', '0.0')
    op.AddAttrNode('FixingValue', 'LESS_EQUAL', '0.0')
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('CashFlow.leg.instrument.insType', 'EQUAL', None)
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('CashFlow.leg.instrument.trades.status', 'EQUAL', None)
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('ReadTime', 'GREATER_EQUAL', None)
    op.AddAttrNode('ReadTime', 'LESS_EQUAL', '1970-01-01')
    return q


def insertPhysicalPortfolio():
    q = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('AND')
    op.AddAttrNode('Currency.Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('AND')
    op.AddAttrNode('Compound', 'EQUAL', 0)
    return q


def insertAcquirer():
    q = acm.CreateFASQLQuery(acm.FParty, 'AND')  # empty query
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    #
    op = q.AddOpNode('OR')
    op.AddAttrNode('Type', 'EQUAL',
            ael.enum_from_string('PartyType', 'Intern Dept'))
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    return q


def insertCounterparty():

    q = acm.CreateFASQLQuery(acm.FParty, 'AND')  # empty query
    op = q.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('OR')
    op.AddAttrNode('Type', 'EQUAL', ael.enum_from_string('PartyType',
            'CounterParty'))
    op = q.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    return q


def insertStoredFolder():
    q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('AND')
    op.AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FTrade')
    return q


def insertInstrumentStoredFolder():
    q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('AND')
    op.AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FInstrument')
    return q


def insertStoredFolderDialog(shell, params):

    import FBDPCustomPairDlg
    customDlg = FBDPCustomPairDlg.SelectACMQueriesCustomDialog(shell,
            params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def insertYieldCurves(includeYcTypes=()):

    q = acm.CreateFASQLQuery(acm.FYieldCurve, 'AND')  # empty query
    #
    op = q.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    # integer
    op = q.AddOpNode('AND')
    val = None
    if ael.historical_mode():
        op.Not(True)
        val = 0
    op.AddAttrNode('Oid', 'GREATER_EQUAL', val)
    op.AddAttrNode('Oid', 'LESS_EQUAL', val)
    #
    op = q.AddOpNode('AND')
    for ycType in includeYcTypes:
        op.AddAttrNode('Type', 'EQUAL', ael.enum_from_string('IrType', ycType))
    return q


def insertVolatilities():
    q = acm.CreateFASQLQuery(acm.FVolatilityStructure, 'AND')  # empty query

    op = q.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)

    # integer
    op = q.AddOpNode('AND')
    val = None
    if ael.historical_mode():
        op.Not(True)
        val = 0
    op.AddAttrNode('Oid', 'GREATER_EQUAL', val)
    op.AddAttrNode('Oid', 'LESS_EQUAL', val)

    return q

def insertCorpAction():
    q = acm.CreateFASQLQuery(acm.FCorporateAction, 'AND')  # empty query

    op = q.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)

    op = q.AddOpNode('AND')
    op.AddAttrNode('businessEvent.Oid', 'NOT_EQUAL', 0)

    return q

def insertInstrumentPackage(def_name=None):
    q = acm.CreateFASQLQuery(acm.FInstrumentPackage, 'AND')  # empty query
    q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    q.AddOpNode('AND').AddAttrNode('DefinitionName', 'EQUAL', def_name)
    return q

def insertDealPackage(def_name=None):
    q = acm.CreateFASQLQuery(acm.FDealPackage, 'AND')  # empty query
    q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    q.AddOpNode('AND').AddAttrNode('InstrumentPackage.Name', 'EQUAL', None)
    q.AddOpNode('AND').AddAttrNode(
        'InstrumentPackage.DefinitionName', 'EQUAL', def_name
    )
    return q

def insertPortfolioSwap():
    q = acm.CreateFASQLQuery(acm.FPortfolioSwap, 'AND')  # empty query
    q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

def insertTradeFilter():
    q = acm.CreateFASQLQuery(acm.FTradeSelection, 'AND')  # empty query
    q.AddOpNode('AND').AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q

class AelVariables(list):
    _BooleanAttributes = ('mandatory', 'multiple', 'enabled')
    _VariableAttributes = collections.namedtuple('VariableAttributes',
            'index cstor default_value')
    _VariableAttributesMap = collections.OrderedDict([
        ('varName', _VariableAttributes(0, str, None)),
        ('displayName', _VariableAttributes(1, str, None)),
        ('type', _VariableAttributes(2, None, None)),
        ('candidate_values', _VariableAttributes(3, None, None)),
        ('default_value', _VariableAttributes(4, None, None)),
        ('mandatory', _VariableAttributes(5, bool, False)),
        ('multiple', _VariableAttributes(6, bool, False)),
        ('tooltip', _VariableAttributes(7, str, None)),
        ('call_back', _VariableAttributes(8, None, None)),
        ('enabled', _VariableAttributes(9, bool, True)),
        ('selectionDialog', _VariableAttributes(10, None, None)),
    ])
    _OtherAttributes = ('oldTooltip', 'sequenceNumber')

    class Variable(list):
        """
        Wrapper class for an ael variable.
        TODO: deprecate isEnabled and hasCallback since all
        list elements can now be referenced by name.
        """
        def __init__(self, r, i):
            attr_names = AelVariables._VariableAttributesMap.keys()
            for value, attr_name in itertools.zip_longest(r, attr_names):
                if attr_name:
                    value, _ = self._getValueAndIndex(attr_name, value)
                    self.append(value)
                else:
                    self.append(value)

            self.oldTooltip = '' if len(self) < 7 else self.tooltip
            self.sequenceNumber = i

        def __str__(self):
            lst = []
            attr_names = AelVariables._VariableAttributesMap.keys()
            for value, attr_name in itertools.zip_longest(self, attr_names):
                if attr_name:
                    value, _ = self._getValueAndIndex(attr_name, value)
                    if attr_name in AelVariables._BooleanAttributes:
                        value = bool(value)

                lst.append(value)

            return str(lst)

        def __setattr__(self, name, value):
            val, idx = self._getValueAndIndex(name, value)
            if idx is None:
                list.__setattr__(self, name, value)
            else:
                self[idx] = val

            return

        def __getattr__(self, name):
            attr = AelVariables._VariableAttributesMap[name]
            return self[attr.index]

        def isEnabled(self):
            return bool(self.enabled)

        def hasCallback(self):
            return bool(self.call_back)

        def enable(self, enabled, disabledTooltip=None):
            enabled = self._parseBool(enabled)
            was_enabled = self.enabled
            self.enabled = enabled
            self.mandatory = self.mandatory and self.enabled
            if self.enabled:
                self.tooltip = self.oldTooltip
            else:
                if was_enabled:
                    self.oldTooltip = self.tooltip

                self.tooltip = disabledTooltip or ''

        def set(self, fieldValues, value):
            fieldValues[self.sequenceNumber] = value
            return fieldValues

        def callback(self, fieldValues):
            return self.call_back(self.sequenceNumber, fieldValues)

        def callbackIfEnabled(self, fieldValues):
            if self.enabled and self.call_back:
                return self.callback(fieldValues)

            return fieldValues

        def _getValueAndIndex(self, name, value):
            if name not in AelVariables._VariableAttributesMap:
                return None, None

            attr = AelVariables._VariableAttributesMap[name]
            value = attr.default_value if value is None else value
            if (value is not None) and attr.cstor:
                if attr.cstor == bool:
                    value = int(self._parseBool(value))
                else:
                    value = attr.cstor(value)

            return value, attr.index

        def _parseBool(self, bool_var):
            if isinstance(bool_var, str):
                bool_var = bool_var.strip()
                try:
                    return bool(int(bool_var)) if len(bool_var) else True
                except:
                    return True

            return bool(bool_var)

    def createVariable(self, row):
        """
        Factory of Variables.
        """
        row = AelVariables.Variable(row, len(self))
        setattr(self, row.varName, row)
        self.append(row)
        return row

    def __init__(self, *ael_variables):
        for i in ael_variables:
            self.createVariable(i)

def ael_gui_parameters(**extraGuiParameters):
    guiParameters = {'runButtonLabel': '&&Save',
                     'hideExtraControls': True}
    guiParameters.update(extraGuiParameters)
    return guiParameters


class DefaultVariables(AelVariables):
    """
    Default variables can be taken from a class.
    """
    defaults = Parameters('FBDPParameters')
    fileType = type(acm.FFileSelection())

    def createVariable(self, row):
        """
        Factory of Variables.
        """
        row = super(DefaultVariables, self).createVariable(row)
        if (hasattr(self, 'defaults') and hasattr(
            self.defaults, row.varName) and not row.default_value):
            row.default_value = getattr(self.defaults, row.varName)

        if type(row.type) == self.fileType:
            row.multiple = True
            if row.call_back:
                cb = row.call_back
                row.call_back = lambda idx, fv: self.fileSelection_cb(
                    idx, cb(idx, fv)
                )
            else:
                row.call_back = self.fileSelection_cb

        return row

    def setVariables(self, d, fieldValues):
        temp = fieldValues[getattr(self, 'Template').sequenceNumber]
        toolT = 'This field is not enabled for the template'
        toolTip = toolT + ' ' + temp + '.'
        for var in self:
            if (var.tooltip != toolTip and toolT in var.tooltip and
                    var.varName not in ('CashCurrency', 'ProtectedMarkets',
                    'SavePriceChanges')):
                var.enable(True)

        for key, value in d.items():
            if value == None:
                value = ''

            if hasattr(self, key):
                fieldValues = getattr(self, key).set(fieldValues, value)
            else:
                k = key.split('.')
                var = []
                values = []
                if len(k) > 1 and hasattr(self, k[0]):
                    var.append(getattr(self, k[0]))
                    values.append(value)
                    if k[0] == 'NewInstrument':
                        var.extend([getattr(self, 'NewPrice'),
                                getattr(self, 'SpinoffCostFraction'),
                                getattr(self, 'WhatToDoWithNewInstrument')])
                        values.extend([value, value, value])
                    elif k[0] == 'CashAmount':
                        var.append(getattr(self, 'CashCurrency'))
                        values.append(value)
                    elif k[0] == 'ChangeHistoricalPrices':
                        var.extend([getattr(self, 'ProtectedMarkets'),
                                getattr(self, 'SavePriceChanges')])
                        values.extend([value, value])
                    elif k[0] == 'ChangeQuantity':
                        var.extend([getattr(self, 'ChangeWeights'),
                                getattr(self, 'ProtectedComb')])
                        values.extend([value, value])

                    for i in range(len(var)):
                        var[i].enable(values[i], toolTip)

        return fieldValues

    def fileSelection_cb(self, index, fieldValues):
        """
        Set the internal Selected[Directory|File] in the
        FFileSelection object, this way the [...] button
        stays in sync with the textfield
        """
        row = self[index]
        try:
            value = str(fieldValues[index])
            if row.type.PickDirectory():
                row.type.SelectedDirectory = value
            else:
                if value.endswith(('\\', ':')) or '/' in value:
                    row.type.SelectedFile = ''
                else:
                    row.type.SelectedFile = value
        except AttributeError:
            pass

        return fieldValues


class OperationsEODVariables(DefaultVariables):
    def logfile_cb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To '
                'File to be able to select a Logfile.')
        return fieldValues

    def __init__(self, *ael_variables):

        DefaultVariables.__init__(self, *ael_variables)
        ttLogToCon = ('Whether logging should be done in the Log Console or '
                'not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, '
                r'c:\log\...')

        self.createVariable(
                ['LogToConsole',
                        'Log to console_Logging',
                        'int', [1, 0], None,
                        True, False, ttLogToCon])
        self.createVariable(
                ['LogToFile',
                        'Log to file_Logging',
                        'int', [1, 0], 0,
                        True, False, ttLogToFile, self.logfile_cb])
        self.createVariable(
                ['Logfile',
                        'Log file_Logging',
                        'string', None, 'AccountingEOD.log',
                        False, False, ttLogFile, None, None])


class LogVariables(DefaultVariables):
    def logfile_cb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To '
                'File to be able to select a Logfile.')
        return fieldValues

    def sendReportByMail_cb(self, index, fieldValues):
        tt = ('This field is only applicable if Send Report By Mail is '
                'selected.')
        self.MailList.enable(fieldValues[index], tt)
        self.ReportMessageType.enable(fieldValues[index], tt)
        return fieldValues

    def reportMessageType_cb(self, index, fieldValues):
        if 'Full Log' in fieldValues[index]:
            fieldValues[index] = 'Full Log'
        return fieldValues

    def __init__(self, *ael_variables):
        DefaultVariables.__init__(self, *ael_variables)
        ttLogMode = 'Defines the amount of logging produced.'
        ttLogToCon = ('Whether logging should be done in the Log Console or '
                'not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, '
                r'c:\log\...')
        ttSendReportByMail = ('Send reports by email when procedure is '
                'finished.')
        ttMailList = ('Specify mail recipients. Specify them in the form: '
                'user1@address.com, user2@address.com.')
        ttReportMessageType = ('Whether the report should be the full log, or '
                'if it should be only the selected messagetypes. If the '
                'selected messagetypes does not occur, no mail will be sent.')

        messageTypes = ['Full Log', 'START', 'FINISH', 'ABORT', 'ERROR',
                'WARNING', 'NOTIME', 'INFO', 'DEBUG']
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['Logmode',
                        'Logmode_Logging',
                        'int', [0, 1, 2], None,
                        True, False, ttLogMode])
        self.createVariable(
                ['LogToConsole',
                        'Log To Console_Logging',
                        'int', [1, 0], None,
                        True, False, ttLogToCon])
        self.createVariable(
                ['LogToFile',
                        'Log To File_Logging',
                        'int', [1, 0], 0,
                        True, False, ttLogToFile, self.logfile_cb])
        self.createVariable(
                ['Logfile',
                        'Logfile_Logging',
                        'string', None, None,
                        False, False, ttLogFile, None, None])
        self.createVariable(
                ['SendReportByMail',
                        'Send Report By Mail_Logging',
                        'int', [1, 0], None,
                        False, False, ttSendReportByMail,
                        self.sendReportByMail_cb])
        self.createVariable(
                ['MailList',
                        'MailList_Logging',
                        'string', None, None,
                        False, False, ttMailList])
        self.createVariable(
                ['ReportMessageType',
                        'ReportMessageType_Logging',
                        'string', messageTypes, 'Full Log',
                        True, True, ttReportMessageType,
                        self.reportMessageType_cb])


class TestVariables(LogVariables):
    def __init__(self, *ael_variables):
        ttTestMode = 'No changes will be committed to the database.'
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['Testmode',
                        'Testmode',
                        'int', ['0', '1'], None,
                        False, False, ttTestMode])
        LogVariables.__init__(self, *ael_variables)


class FxPositionVariablesBase(TestVariables):

    def object_cb(self, index, fieldValues):

        tt = 'You can only select one type of object.'
        for field in (self.TradeQuery, self.TradeFilter,
                self.TradingPortfolios):
            if self[index] != field:
                field.enable(not fieldValues[index], tt)
        return fieldValues

    def grouper_cb(self, index, fieldValues):

        return fieldValues


class FxPositionVariablesBaseNoTest(LogVariables):

    def object_cb(self, index, fieldValues):

        tt = 'You can only select one type of object.'
        for field in (self.TradeQuery, self.TradeFilter,
                self.TradingPortfolios):
            if self[index] != field:
                field.enable(not fieldValues[index], tt)
        return fieldValues

    def grouper_cb(self, index, fieldValues):

        return fieldValues


class FxPositionVariables(FxPositionVariablesBase):

    def __init__(self, *ael_variables):

        onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
                'Filters or Portfolios - should be used.')
        ttStoredFolder = ('Select positions using Stored Folders. '
                '{0}'.format(onlyOne))
        ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
        ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
        ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'the default behaviour is to group by portfolio.')
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradeQuery',
                        'Stored Folder_Positions',
                        'FStoredASQLQuery', None, insertStoredFolder(),
                        False, True, ttStoredFolder, self.object_cb])
        self.createVariable(
                ['TradeFilter',
                        'Trade Filter_Positions',
                        'FTradeSelection', None, None,
                        False, True, ttTradeFilter, self.object_cb])
        self.createVariable(
                ['TradingPortfolios',
                        'Portfolio_Positions',
                        'FPhysicalPortfolio', None, None,
                        False, True, ttPortfolio, self.object_cb])
        self.createVariable(
                ['PortfolioGrouper',
                        'Portfolio Grouper_Positions',
                        'FStoredPortfolioGrouper', None, None,
                        False, True, ttGrouper, self.grouper_cb])
        FxPositionVariablesBase.__init__(self, *ael_variables)


class FxPositionVariablesNoTestMode(FxPositionVariablesBaseNoTest):

    def __init__(self, *ael_variables):

        onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
                'Filters or Portfolios - should be used.')
        ttStoredFolder = ('Select positions using Stored Folders. '
                '{0}'.format(onlyOne))
        ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
        ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
        ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'the default behaviour is to group by portfolio.')
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradeQuery',
                        'Stored Folder_Positions',
                        'FStoredASQLQuery', None, insertStoredFolder(),
                        False, True, ttStoredFolder, self.object_cb])
        self.createVariable(
                ['TradeFilter',
                        'Trade Filter_Positions',
                        'FTradeSelection', None, None,
                        False, True, ttTradeFilter, self.object_cb])
        self.createVariable(
                ['TradingPortfolios',
                        'Portfolio_Positions',
                        'FPhysicalPortfolio', None, None,
                        False, True, ttPortfolio, self.object_cb])
        self.createVariable(
                ['PortfolioGrouper',
                        'Portfolio Grouper_Positions',
                        'FStoredPortfolioGrouper', None, None,
                        False, True, ttGrouper, self.grouper_cb])
        FxPositionVariablesBaseNoTest.__init__(self, *ael_variables)


class FxAggregationVariables(FxPositionVariables):
    ttPnLTest = ("Compare Profit and Loss Values for the aggregated positions "
            "before and after aggregation.")
    ttRepPath = ("Log the result of Profit and Loss Comparison Test to this "
            "directory.")
    ttInactiveSheet = "A workbook has to be selected to use this field. "
    ttNoDiffTest = ("Run Profit and Loss Comparison Test must be selected to "
            "use this field.")
    ttbypassTradeValidation = 'Bypass internal validation of trade updates.'

    defaultReportPath = os.path.join(defaultLogDir(), "FXAggregation")

    def diffPL(self, index, fieldValues):
        enable = fieldValues[index] != '0'
        self.report_path.enable(enable, FxAggregationVariables.ttNoDiffTest)
        return fieldValues

    def __init__(self, *ael_variables):
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        variables = [
            ['diff_test',
                'Run Profit and Loss Comparison Test_Validation',
                'int', [1, 0], 0,
                True, False, FxAggregationVariables.ttPnLTest, self.diffPL],
            ['report_path',
                'Output File Path_Validation',
                'string', [], FxAggregationVariables.defaultReportPath,
                False, False, FxAggregationVariables.ttRepPath, None, 1],
        ]

        variables.extend(ael_variables)
        FxPositionVariables.__init__(self, *variables)


class FxPositionVariablesBuySide(FxPositionVariablesBase):

    def __init__(self, *ael_variables):

        onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
                'Filters or Portfolios - should be used.')
        ttStoredFolder = ('Select positions using Stored Folders. '
                '{0}'.format(onlyOne))
        ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
        ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
        ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'the default behaviour is to group by portfolio.')
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradeQuery',
                        'Stored Folder_Positions',
                        'string', [], None,
                        False, True, ttStoredFolder, self.object_cb, 1,
                                insertStoredFolderDialog])
        self.createVariable(
                ['TradeFilter',
                        'Trade Filter_Positions',
                        'FTradeSelection', None, None,
                        False, True, ttTradeFilter, self.object_cb])
        self.createVariable(
                ['TradingPortfolios',
                        'Portfolio_Positions',
                        'FPhysicalPortfolio', None, None,
                        False, True, ttPortfolio, self.object_cb])
        self.createVariable(
                ['PortfolioGrouper',
                        'Portfolio Grouper_Positions',
                        'FStoredPortfolioGrouper', None, None,
                        False, True, ttGrouper])
        FxPositionVariablesBase.__init__(self, *ael_variables)


class FxVariables(FxPositionVariables):

    def __init__(self, *ael_variables, **additional_kwargs):

        ttTradingCalendar = ('Trading location\'s calendar. Default is '
                'calendar of accounting currency.')
        ttNextTradingDate = ('Next trading session date to be used. '
                'This can also be specified in date format.')
        ttUseMtM = ('Use mark-to-market rates rather than spot funding rates')
        ttMtM = ('Rates will be retrieved from the selected MtM market')
        tradingDates = ['Spot next', 'Tom next'] + additional_kwargs.get(
            'additional_trading_dates', [])
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradingCalendar',
                        'Trading location calendar',
                        'FCalendar', None, None,
                        False, True, ttTradingCalendar],
                ['NextTradingDate',
                        'Next trading date',
                        'string', tradingDates, None,
                        True, False, ttNextTradingDate],
                ['UseMtM',
                    'Use MtM Rates_Rates',
                    'int', ['0', '1'], None,
                    False, False, ttUseMtM, self.enableMtM],
                ['MtMMarket',
                    'MtM Market_Rates',
                    'FMTMMarket', None, None,
                    False, True, ttMtM],
                ]

        variables.extend(ael_variables)
        FxPositionVariables.__init__(self, *variables)

    def enableMtM(self, index, fieldValues):
        self.MtMMarket.enable(fieldValues[index], 'MtM Market will be enabled '
                'only if "Use MtM Rates" is selected.')
        return fieldValues


class RollbackVariables(LogVariables):
    def __init__(self, *ael_variables):
        tt = 'These Rollback Specifications will be deleted.'
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['rollbackSpec',
                        'Rollback Specification',
                        'FRollbackSpec', None, insertRollback(),
                        True, True, tt])
        LogVariables.__init__(self, *ael_variables)


def setPortfolioGrouper(dictionary, key='PortfolioGrouper'):
    if key in dictionary and dictionary[key]:
        grouper = dictionary[key][0]
        if type(grouper) == type(acm.FChainedGrouper()):
            dictionary[key] = grouper
        elif type(grouper) == type(''):
            pg = acm.FStoredPortfolioGrouper.Select('name={0}'.format(grouper))
            pg = pg[0] if pg else None
            dictionary[key] = pg.PortfolioGrouper() if pg else None
        else:
            dictionary[key] = grouper.PortfolioGrouper()


def getMtMMarket():
    """
    Returns MtM Market defined in Accounting Parameters
    """
    mtm_market = acm.GetFunction('mappedGlobalAccountingParameters',
            0)().Parameter().MtmMarket()
    if mtm_market:
        return mtm_market
    else:
        raise Exception('ERROR! Could not find MtM-Market. Aborting...')


def getCorporateActionNames():

    return [acmCA.Name() for acmCA in acm.FCorporateAction.Select('')]


def _getAllFParametersList():

    acmFParamsList = [acmFParams for acmFParams in
            acm.GetDefaultContext().GetAllExtensions(
                    'FParameters',    # FClass type
                    'FObject',        # FClass optClass
                    True,             # bool inherited
                    True)             # bool global
            ]
    return acmFParamsList


def _isAcmFParameters(obj):

    return (obj and hasattr(obj, 'IsKindOf') and
            obj.IsKindOf(acm.FParameters))


def _isAcmFParamsForCorpActTemplate(acmFParams):

    if not _isAcmFParameters(acmFParams):
        return False
    for key in acmFParams.Keys():
        if key.Text() != 'TemplateType':
            continue
        return acmFParams[key].Text() == 'CorporateAction'
    return False


def getCorpActTemplateNames():

    return [acmFParams.Name() for acmFParams in _getAllFParametersList()
            if _isAcmFParamsForCorpActTemplate(acmFParams)]


def getAdditionalInfoDataTypeString(infoSpec):
    RecordRef_ACMObject_Mapping = {'Position': 'FCalculationRow',
                                   'Instrument': 'FInstrument'}

    dataTypeGroup = infoSpec.DataTypeGroup()
    dataType = infoSpec.DataTypeType()
    dataTypeStr = ''
    if dataTypeGroup == 'Standard':
        data_type_enums = acm.FEnumeration['enum(B92StandardType)']
        dataTypeStr = data_type_enums.Enumerator(dataType).lower()
        if dataTypeStr in ('integer', 'integer64'):
            dataTypeStr = 'int'
    elif dataTypeGroup == 'RecordRef':
        data_type_enums = acm.FEnumeration['enum(B92RecordType)']
        dataTypeStr = data_type_enums.Enumerator(dataType)
        dataTypeStr = RecordRef_ACMObject_Mapping[dataTypeStr]
    return dataTypeStr

def createAdditionalInfoVariables(variables, recType, fieldsToDisable=[]):

    query = "recType={}".format(recType)
    infoSpecs = acm.FAdditionalInfoSpec.Select(query)
    data_type_enums = acm.FEnumeration['enum(B92StandardType)']
    for info in infoSpecs:
        fieldName = info.FieldName()
        dataTypeStr = getAdditionalInfoDataTypeString(info)
        defaultValue = info.DefaultValue()
        mandatory = info.Mandatory()
        enabled = 1
        if fieldName in fieldsToDisable:
            enabled = 0
        variables.createVariable([fieldName,
            fieldName + '_Add Info',
            dataTypeStr, None, defaultValue,
            mandatory, None, info.Description(),
            None, enabled],)


def makeGuiParameters(**extraGuiParameters):
    guiParameters = {'runButtonLabel': '&&Save',
                     'hideExtraControls': True}
    guiParameters.update(extraGuiParameters)
    return guiParameters
