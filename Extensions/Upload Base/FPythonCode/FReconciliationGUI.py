""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationGUI.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationGUI -

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import itertools

import acm
import FBusinessProcessUtils
from FOperationsManagerWorkbench import BusinessProcessWorkbenchPanel, WorkbenchControl
from FReconciliationValueMapping import GetSheetInsertableACMObject
import FPositionCreator
import FReconciliationColumnCreator
import FReconciliationDataTypeHandler
import FReconciliationSpecification
import FWorkbenchControls


def _IsNumericDataType(reconSpec, columnid):
    dataTypeMapping = reconSpec.DataTypeMapping()
    nameSpace = ' '.join((reconSpec.Name(), 'External '))
    datatype = dataTypeMapping.GetString(columnid.replace(nameSpace, ''))
    if not datatype or datatype == '':
        raise TypeError("Column '%s' has not been mapped to a data type" % columnid.replace(nameSpace, ''))
    dataHandler = FReconciliationDataTypeHandler.FDataTypeHandler(datatype)
    return dataHandler.IsNumericDataType()

def _ColumnName(reconSpec, columnid, title):
    params = {
        'Absolute':['Absolute'],
        'Relative':['Relative'],
        'Both':['Absolute', 'Relative']
        }
    if _IsNumericDataType(reconSpec, columnid):
        suffix = FReconciliationColumnCreator.ColumnCreator.SUFFIX
        return [
            ' '.join((columnid.replace('External ', ''), suffix, title))
            for title in params[title]
            ]
    return [None for title in params[title]]

def _GetComparisonColumnNames(reconSpec, columns):
    comparisonType = reconSpec.ComparisonType()
    if not comparisonType or comparisonType.lower() not in ('absolute', 'relative', 'both'):
        return []
    title = comparisonType.capitalize()
    return [_ColumnName(reconSpec, name, title) for name in columns]

def _GetExternalColumns(columns):
    try:
        return columns[1]
    except IndexError:
        return []

def GetComparisonColumnIds(reconSpec):
    columns = list()
    columnMap = reconSpec.ValueMapping()
    columnNameSpace = reconSpec.Name()
    if columnMap and columnNameSpace:
        columns = [
            [FReconciliationColumnCreator.MakeColumnId(
            column,
            ' '.join((columnNameSpace, i)))
            for column in columnMap.Keys()]
            for i in ('Internal', 'External')
            ]
        for columnList in columns:
            columnList.sort()
        comparisonMatrix = _GetComparisonColumnNames(reconSpec,
                _GetExternalColumns(columns))
        # Interleave internal and external columns for side-by-side comparison
        for cmpcolumns in zip(*comparisonMatrix):
            columns.append(list(cmpcolumns))
        columns = [column for column in list(itertools.chain(*list(zip(*columns)))) if column]
    return columns

def GetStoredReconciliationData(reconciliationItem):
    dataValues = reconciliationItem.ExternalValues()
    if dataValues.IsEmpty():
        dataValues = reconciliationItem.InternalValues()
    return {key: value for key, value in zip(dataValues.Keys(), dataValues.Values())}

def TransformDataValues(dataValues, dataAttributeMap):
    return {dataAttributeMap.get(key) if key in dataAttributeMap else key: value for
            key, value in zip(dataValues.keys(), dataValues.values())}


class ReconciliationPositionRetriever(object):
    '''
        This class is used to retrieve a dynamic position
        based on a recon item and a specification.
    '''

    def __init__(self, reconItem, reconSpec, allowIncompletePositions = False):
        assert reconItem and reconSpec
        self.reconciliationItem = reconItem
        self.reconciliationSpecification = reconSpec
        self._allowIncompletePositions = allowIncompletePositions

    def ReconciliationItem(self):
        return self.reconciliationItem

    def ReconciliationSpecification(self):
        return self.reconciliationSpecification

    def RetrieveDynamicStoredPositionQuery(self):
        position = None
        if self.ReconciliationItem().ReconciliationDocument().ObjectType() == 'Position':
            reconItemAttributesDict = GetStoredReconciliationData(self.ReconciliationItem())
            dataAttributeMap = self.ReconciliationSpecification().ExternalAttributeMap()
            reconItemAttributesDict = TransformDataValues(reconItemAttributesDict, dataAttributeMap)
            if reconItemAttributesDict:
                position = self.ReconciliationSpecification().IdentificationRules().FindPosition(
                    attributeValueDict=reconItemAttributesDict,
                    relaxValidation=True,
                    allowIncompletePositions=self._allowIncompletePositions)
        return position.InfantPositionStoredQuery() if position else None

class ReconcilationWorkbenchPanel(BusinessProcessWorkbenchPanel):
    """A WorkbenchPanel with reconcilation specific behaviour."""

    SUBJECT_TYPE = acm.FReconciliationItem

    def __init__(self):
        BusinessProcessWorkbenchPanel.__init__(self)
        self._reconciliationItem = None
        self._reconSpecification = None
        self._allowIncompletePositions = True

    def ReconciliationItem(self, reconItem = None):
        """Return the currently selected FReconciliationItem."""
        # pylint: disable-msg=W0221
        if reconItem is None:
            return self._reconciliationItem
        self._reconciliationItem = reconItem
        self._SetReconItemSubject()

    def ReconciliationDocument(self):
        """Return the currently selected FReconciliationDocument."""
        if self.ReconciliationItem():
            return self.ReconciliationItem().ReconciliationDocument()
        return None

    def ReconciliationSpecification(self, reconSpec = None):
        """Return the currently selected FReconciliationSpecification."""
        if reconSpec is None:
            return self._reconSpecification
        self._reconSpecification = reconSpec

    def _SetReconItemSubject(self):
        if self.ReconciliationItem() and self.ReconciliationItem().ReconciliationDocument().ObjectType() == 'Position':
            ''' Since no position query is stored as the subject of the recon item anymore,
                we know that we have to dynamically set the subject for these recon item types.
            '''
            positionRetriever = ReconciliationPositionRetriever(self.ReconciliationItem(),
                                                                self.ReconciliationSpecification(),
                                                                allowIncompletePositions = self._allowIncompletePositions)
            infantStoredPositionQuery = positionRetriever.RetrieveDynamicStoredPositionQuery()
            self.ReconciliationItem().Subject(infantStoredPositionQuery)

    def _SetBusinessProcess(self, bp):
        BusinessProcessWorkbenchPanel._SetBusinessProcess(self, bp)
        reconciliationItem = bp.Subject() if bp else None
        if bp and reconciliationItem and reconciliationItem.IsKindOf(self.SubjectType()):
            # It does not matter whether it is an upload or not at this stage. Validation is relaxed.
            self.ReconciliationSpecification(FReconciliationSpecification.GetReconciliationSpecification(reconciliationItem,
                                                                                                         upload=False,
                                                                                                         relaxValidation=True)
                                             )
            self.ReconciliationItem(reconciliationItem)
        else:
            setattr(self, '_reconSpecification', None)
            setattr(self, '_reconciliationItem', None)


class ReconciliationWorkflowPanel(ReconcilationWorkbenchPanel):
    """A workbench panel to support reconciliation workflow.

    Consists of controls to:
        - Manage business process workflow for reconciliation items.
        - Assist in identifying unlocated external items in the system.
        - Display position definition attributes.
        - Display reconcilation statistics.

    """
    def __init__(self):
        ReconcilationWorkbenchPanel.__init__(self)
        self._businessProcessCtrl = self.AddControl(FWorkbenchControls.WorkbenchBusinessProcessControl(self))
        self._unidentifiedReconciliationItemCtrl = self.AddControl(ReconciliationUnidentifiedItemControl(self))
        self._positionDefinitionCtrl = self.AddControl(ReconciliationPositionDefinitionControl(self))
        self._statisticsCtrl = self.AddControl(ReconciliationDocumentStatisticsControl(self))

    def OnSelectedItemChanged(self):
        # pylint: disable-msg=E1101
        reconciliationItem = self.ReconciliationItem()
        if reconciliationItem and self.ReconciliationSpecification():
            objectType = reconciliationItem.ReconciliationDocument().ObjectType()
            isIdentified = bool(reconciliationItem.Subject() != None)
            self._businessProcessCtrl.Enabled(True)
            self._unidentifiedReconciliationItemCtrl.Enabled(not isIdentified)
            self._positionDefinitionCtrl.Enabled(bool(isIdentified and objectType == 'Position'))
            self._statisticsCtrl.Enabled(True)
        else:
            self.Enabled(False)
        ReconcilationWorkbenchPanel.OnSelectedItemChanged(self)


class ReconciliationItemPanel(ReconcilationWorkbenchPanel):
    """A workbench panel to display reconciliation item details.

    Displays details of a reconciliation item, including sheets to:
        - Compare the front arena and external reconciliation item objects.
        - Display details of the located front arena item in its native sheet.

    """
    def __init__(self):
        ReconcilationWorkbenchPanel.__init__(self)
        self._positionComparisonCtrl = self.AddControl(ReconciliationValueComparisonControl(self, 'FPortfolioSheet'))
        self._tradeComparisonCtrl = self.AddControl(ReconciliationValueComparisonControl(self, 'FTradeSheet'))
        self._instrumentComparisonCtrl = self.AddControl(ReconciliationValueComparisonControl(self, 'FDealSheet'))
        self._settlementComparisonCtrl = self.AddControl(ReconciliationValueComparisonControl(self, 'FSettlementSheet'))
        self._journalComparisonCtrl = self.AddControl(ReconciliationValueComparisonControl(self, 'FJournalSheet'))
        self._tradeSheetCtrl = self.AddControl(ReconciliationTradingSheetControl(self, 'FTradeSheet', 150))
        self._settlementSheetCtrl = self.AddControl(ReconciliationTradingSheetControl(self, 'FSettlementSheet', 120))
        self._dealSheetCtrl = self.AddControl(ReconciliationTradingSheetControl(self, 'FDealSheet', 120))
        self._journalSheetCtrl = self.AddControl(ReconciliationTradingSheetControl(self, 'FJournalSheet', 120))

    def OnSelectedItemChanged(self):
        # pylint: disable-msg=E1101,
        reconciliationItem = self.ReconciliationItem()
        if reconciliationItem and self.ReconciliationSpecification():
            objectType = reconciliationItem.ReconciliationDocument().ObjectType()
            isIdentified = bool(reconciliationItem.Subject() != None)
            self._positionComparisonCtrl.Enabled(bool(isIdentified and objectType == 'Position'))
            self._tradeComparisonCtrl.Enabled(bool(isIdentified and objectType == 'Trade'))
            self._instrumentComparisonCtrl.Enabled(bool(isIdentified and objectType == 'Instrument'))
            self._settlementComparisonCtrl.Enabled(bool(isIdentified and objectType == 'Settlement'))
            self._journalComparisonCtrl.Enabled(bool(isIdentified and objectType == 'Journal'))
            self._tradeSheetCtrl.Enabled(bool(isIdentified and objectType in ('Trade', 'Position')))
            self._settlementSheetCtrl.Enabled(bool(isIdentified and objectType == 'Settlement'))
            self._dealSheetCtrl.Enabled(bool(isIdentified and objectType == 'Instrument'))
            self._journalSheetCtrl.Enabled(bool(isIdentified and objectType == 'Journal'))
        else:
            self.Enabled(False)
        ReconcilationWorkbenchPanel.OnSelectedItemChanged(self)


class ReconciliationUnidentifiedItemControl(WorkbenchControl):
    """ A control for assisting in the identification of unidentified reconciliation items.
        This control is also used for recon items missing in document
    """

    ICON_ATTRIBUTE = 'BlueBall'

    def __init__(self, panel):
        super(ReconciliationUnidentifiedItemControl, self).__init__(panel)
        self._currentReconSpecName = None
        self._ruleSelectionCtrl = None
        self._rulesListCtrl = None
        self._searchButton = None

    def CreateLayout(self, builder):
        builder.BeginHorzBox('EtchedIn', 'Identification Rules')
        builder.  BeginVertBox('None')
        builder.    BeginHorzBox('None')
        builder.      AddOption('ruleSelection', 'Rule')
        builder.    EndBox()
        builder.    BeginHorzBox('None')
        builder.      AddList('rulesList', 10, -1, -1)
        builder.    EndBox()
        builder.    BeginHorzBox('None')
        builder.      AddFill()
        builder.      AddButton('search', 'Search', True, False)
        builder.    EndBox()
        builder.  EndBox()
        builder.EndBox()

    def HandleCreate(self, layout):
        self._currentReconSpecName = None
        self._ruleSelectionCtrl = self.RegisterFUxControl(layout.GetControl('ruleSelection'))
        self._rulesListCtrl = self.RegisterFUxControl(layout.GetControl('rulesList'))
        self._searchButton = self.RegisterFUxControl(layout.GetControl('search'))

        self._ruleSelectionCtrl.AddCallback('Changed', self.OnRuleSelectionChanged, None)
        self._searchButton.AddCallback('Activate', self.OnSearchClicked, None)

        ctrl = self._rulesListCtrl
        ctrl.ShowGridLines()
        ctrl.ShowColumnHeaders()
        ctrl.AddColumn('Name', -1, "Name of the rule")
        ctrl.AddColumn('Value', -1, "Value of the rule")

    def OnSelectedItemChanged(self):
        if self.Panel().ReconciliationSpecification().Name() != self._currentReconSpecName:
            # Rules are dependent on the reconciliation specification. Only update them when
            # this changes, such that user selection persists across recon item selections.
            self._currentReconSpecName = self.Panel().ReconciliationSpecification().Name()
            self._SetRuleSelectionCtrl()
        self._SetRulesListCtrl()

    def OnRuleSelectionChanged(self, params, _cd):
        self._SetRulesListCtrl()

    def OnSearchClicked(self, _params, _cd):
        query = self._GetSelectedPositionQuery()
        if query:
            acm.StartFASQLEditor(None, None, None, query, None, '', True)

    def _SetRuleSelectionCtrl(self):
        self._ruleSelectionCtrl.Clear()
        reconSpec = self.Panel().ReconciliationSpecification()
        rules = reconSpec.IdentificationRules()
        for i, rule in enumerate(rules):
            ruleName = '%i - %s' % (i+1, rule.QueryName())
            self._ruleSelectionCtrl.AddItem(ruleName)
            if i == 0:
                self._ruleSelectionCtrl.SetData(ruleName)

    def _SetRulesListCtrl(self):
        self._rulesListCtrl.Clear()
        root = self._rulesListCtrl.GetRootItem()
        ruleValues = self._GetUnidentifiedRuleValues()
        if ruleValues:
            for attribute, value in sorted(ruleValues.items()):
                child = root.AddChild()
                child.Label(attribute)
                child.Icon(self.ICON_ATTRIBUTE)
                child.Label(value, 1)
            self._rulesListCtrl.AdjustColumnWidthToFitItems(0)
            self._rulesListCtrl.AdjustColumnWidthToFitItems(1)

    def _GetUnidentifiedRuleValues(self):
        query = self._GetSelectedPositionQuery()
        if query:
            return FWorkbenchControls.WorkbenchPositionControl.GetDisplayableQueryNodes(query)
        return None

    def _GetSelectedStoredPositionQuery(self):
        idRule = self._GetSelectedIdentificationRule()
        if not idRule:
            return None

        storedDataValues = GetStoredReconciliationData(self.Panel().ReconciliationItem())
        dataAttributeMap = self.Panel().ReconciliationSpecification().ExternalAttributeMap()
        storedDataValues = TransformDataValues(storedDataValues, dataAttributeMap)

        positionSpec = FPositionCreator.FPositionSpecification(idRule.StoredQuery(), allowIncompletePositions=True)
        position = positionSpec.GetInfantPositionFromDict(storedDataValues, allowIncompletePositions=True)
        return position.InfantPositionStoredQuery()

    def _GetSelectedPositionQuery(self):
        return self._GetSelectedStoredPositionQuery().Query()

    def _GetSelectedIdentificationRule(self):
        reconSpec = self.Panel().ReconciliationSpecification()
        try:
            ruleIndex = int(str(self._ruleSelectionCtrl.GetData()).split(' ')[0]) - 1
            return reconSpec.IdentificationRules()[ruleIndex]
        except ValueError:
            pass    # No rules have been setup
        return None

    def Enabled(self, enabled=None):
        return WorkbenchControl.Enabled(self, enabled)

    def HandleDestroy(self):
        WorkbenchControl.HandleDestroy(self)


class ReconciliationPositionDefinitionControl(FWorkbenchControls.WorkbenchPositionControl):
    """A control for displaying the attributes of a position reconciliation item."""

    PADDING = '_' * 50

    def __init__(self, panel):
        super(ReconciliationPositionDefinitionControl, self).__init__(panel)
        self._reconPeriodCtrl = None

    def CreateLayout(self, builder):
        builder.BeginHorzBox('EtchedIn', 'Position')
        builder.  BeginVertBox('None')
        builder.    BeginHorzBox('None')
        builder.      BeginHorzBox('None')
        builder.        AddLabel('reconPeriod', self.PADDING)
        builder.      EndBox()
        builder.    EndBox()
        builder.    BeginHorzBox('None')
        builder.      AddList('attributesList', 7, -1, -1)
        builder.    EndBox()
        builder.    BeginHorzBox('None')
        builder.      AddFill()
        builder.      AddButton('viewPosition', 'View Position', False, False)
        builder.      AddButton('viewTrades', 'View Trades', True, False)
        builder.    EndBox()
        builder.  EndBox()
        builder.EndBox()

    def HandleCreate(self, layout):
        # Super class handles attribute list and view trade controls
        super(ReconciliationPositionDefinitionControl, self).HandleCreate(layout)
        self._reconPeriodCtrl = self.RegisterFUxControl(layout.GetControl('reconPeriod'))

    def OnSelectedItemChanged(self):
        self._SetReconciliationPeriodCtrl()
        self._SetAttributesListCtrl()

    def _SetReconciliationPeriodCtrl(self):
        doc = self.Panel().ReconciliationDocument()
        self._reconPeriodCtrl.Label('Period: ' + \
            (doc.CustomStartDate() if doc.StartDate() == 'Custom Date' else doc.StartDate()) + \
            ' to ' + \
            (doc.CustomEndDate() if doc.EndDate() == 'Custom Date' else doc.EndDate()))

    @staticmethod
    def _ACMDictToDict(acmDict):
        return {key: value for key, value in zip(acmDict.Keys(), acmDict.Values())}

    def _GetPosition(self):
        ''' This method is backwards compatible '''
        reconItem = self.Panel().ReconciliationItem()
        storedWildcardedQuery = self.Panel().StoredWildcardedQuery()
        positionStoredQuery = storedWildcardedQuery.Clone()
        query = positionStoredQuery.Query()
        reconItemAttributes = self._ACMDictToDict(reconItem.ExternalValues())
        query = FPositionCreator.FPositionSpecification.PositionQueryFromWildcardedQuery(
                query, reconItemAttributes, allowIncompletePositions=True)
        positionStoredQuery.Query(query)
        return positionStoredQuery

class ReconciliationDocumentStatisticsControl(FWorkbenchControls.WorkbenchStatisticsListControl):
    """A control for displaying statistics on the completion progress of
    handling of a reconciliation document.

    """

    def __init__(self, panel):
        super(ReconciliationDocumentStatisticsControl, self).__init__(panel)

    def _GetReconciliationItemCurrentStates(self):
        reconciliationItems = self.Panel().ReconciliationDocument().ReconciliationItems()
        stateChartName = self.Panel().ReconciliationSpecification().StateChartName()

        self._RemoveBusinessProcessesDependencies()
        stateCounts = {}
        for bi in reconciliationItems:
            bp = FBusinessProcessUtils.GetBusinessProcessWithCache(bi, stateChartName)
            if bp:
                self._AddDependentBusinessProcess(bp)
                state = bp.CurrentStep().State().Name()
                stateCounts[state] = stateCounts.get(state, 0) + 1
        return stateCounts


class ReconciliationTradingSheetControl(FWorkbenchControls.WorkbenchTradingSheetControl):
    """A control to display a generic trading sheet."""

    def __init__(self, panel, sheetType, height=100):
        super(ReconciliationTradingSheetControl, self).__init__(panel, sheetType, height)
        self._currentReconSpecName = None

    def HandleCreate(self, layout):
        super(ReconciliationTradingSheetControl, self).HandleCreate(layout)
        self._currentReconSpecName = None

    def OnSelectedItemChanged(self):
        if self.Panel().ReconciliationSpecification().Name() != self._currentReconSpecName:
            # Column configuration is dependent on the reconciliation specification.
            # Only set the columns when this changes, such that user applied columns
            # are not lost between reconcilation item selections.
            self._currentReconSpecName = self.Panel().ReconciliationSpecification().Name()
            self._SetSheetColumns()
        self._SetTradingSheetCtrl()

    def _GetSheetColumnNames(self):
        sheetTemplate = self.Panel().ReconciliationSpecification().SheetTemplate()
        if not sheetTemplate or str(sheetTemplate.SheetClass()) != str(self._sheetType):
            return []
        return [c.ColumnId() for c in sheetTemplate.TradingSheet().ColumnCollection(None)]

    def _GetSheetInsertableItem(self):
        reconItem = self.Panel().ReconciliationItem()
        insertableObjectOrObjects = reconItem.Subject()
        if insertableObjectOrObjects.IsKindOf(acm.FStoredASQLQuery):
            insertableObjectOrObjects = insertableObjectOrObjects.Query().Select()
        return insertableObjectOrObjects

class ReconciliationValueComparisonControl(ReconciliationTradingSheetControl):
    """A control to display a comparison between front arena and external
       reconciliation item objects.
    """

    def OnSelectedItemChanged(self):
        super(ReconciliationValueComparisonControl, self).OnSelectedItemChanged()
        self._SetSimulation()
        self._SetTreeVisibilityOptions()

    def _GetSheetColumnNames(self):
        reconSpec = self.Panel().ReconciliationSpecification()
        return GetComparisonColumnIds(reconSpec)

    def _GetSheetInsertableItem(self):
        reconItem = self.Panel().ReconciliationItem()
        subject = reconItem.Subject()
        acmObject = subject.Clone() if subject else subject
        isFXReconciliation = self.Panel().ReconciliationSpecification().IsFXReconciliation()
        insertableObject = GetSheetInsertableACMObject(acmObject, isFXReconciliation, reconItem)
        return insertableObject

    def _SetSimulation(self):
        reconDocument = self.Panel().ReconciliationDocument()
        try:
            startDateTypeNode, startDateValueNode = self._GetSimulationColumns(
                'profitAndLossStartDate', 'showWhatStartDate', 'customPLStartDate')
            startDateTypeNode.Simulate(self._GetEnumerationValue('EnumPLStartDate', reconDocument.StartDate()), 0)
            startDateValueNode.Simulate(reconDocument.CustomStartDate(), 0)
        except ValueError as _err:
            pass    # Ignore problems with simulation
        try:
            endDateTypeNode, endDateValueNode = self._GetSimulationColumns(
                'profitAndLossEndDate', 'showWhatEndDate', 'customPLEndDate')
            endDateTypeNode.Simulate(self._GetEnumerationValue('EnumPLEndDate', reconDocument.EndDate()), 0)
            endDateValueNode.Simulate(reconDocument.CustomEndDate(), 0)
        except ValueError as _err:
            pass    # Ignore problems with simulation

    def _SetTreeVisibilityOptions(self):
        try:
            tree = self._tradingSheet.RowTreeIterator(False).FirstChild().Tree()
            visibility = tree.VisibilityController()
            if visibility.IsShowExpiredPositionsSupported():
                visibility.ShowExpiredPositions(True)
            if visibility.IsShowInstrumentRowsSupported():
                visibility.ShowInstrumentRows(True)
            if visibility.IsShowZeroPositionsSupported():
                visibility.ShowZeroPositions(True)
        except AttributeError:
            pass    # Ignore if no tree is available

    def _GetSimulationColumns(self, attributeName, dateTypeNodeName, dateValueNodeName):
        sheetEvaluator = self._GetSheetEvaluator()
        if not sheetEvaluator:
            raise ValueError('Unable to get evaluator for sheet')
        attribute = acm.GetCalculatedValueFromString(
                acm.FUndefinedObject(),
                acm.GetDefaultContext().Name(),
                attributeName,
                sheetEvaluator.Tag())
        dateTypeNode = attribute.FindAdHoc(dateTypeNodeName, acm.FEvaluator).At(0)
        dateValueNode = attribute.FindAdHoc(dateValueNodeName, acm.FEvaluator).At(0)
        return dateTypeNode, dateValueNode

    def _GetSheetEvaluator(self):
        sheet = self._tradingSheet
        rowIterator = sheet.RowTreeIterator(False)
        citer = sheet.GridColumnIterator()
        if (sheet.SheetClass() in (acm.FPortfolioSheet, acm.FTradeSheet, acm.FDealSheet, acm.FSettlementSheet, acm.FJournalSheet)
            and rowIterator and citer):
            riter = rowIterator.NextUsingDepthFirst()
            while riter:
                column = citer.First()
                while column:
                    citer = sheet.GridColumnIterator()
                    evaluator = sheet.GetCell(riter, column).Evaluator()
                    if evaluator:
                        return evaluator
                    column = column.Next()
                riter = riter.NextUsingDepthFirst()

    @staticmethod
    def _GetEnumerationValue(enumerationName, valueName):
        try:
            context = acm.GetDefaultContext()
            enum = context.GetExtension('FEnumFormatter', 'FObject', enumerationName).Value().Enumeration()
            return enum.Enumeration(valueName)
        except RuntimeError:
            raise ValueError('Unknown enumeration value: ' + str(valueName))