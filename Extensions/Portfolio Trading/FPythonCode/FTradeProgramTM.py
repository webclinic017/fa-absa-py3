""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramTM.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramTM

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    FTradeProgramTM is the base class for interfaces between the
    TradingManager and the various portfolio based actions.
-----------------------------------------------------------------------------"""

import acm
import math
import FIntegratedWorkbench
import FAssetManagementUtils

from FParameterSettings import ParameterSettingsCreator
from FTradeProgramEvents import OnCandidateTradesCreated, OnPlaceholderTradesCreated
from FCandidateTrades import CandidateTrades, PlaceholderTrades
from FEvent import OnError
from FTradeProgramUtils import Logger


class FTradeProgramTM(object):

    CONTEXT = acm.GetDefaultContext()
    SETTINGS = ParameterSettingsCreator.FromRootParameter('TradeProgramSettings')

    def __init__(self, eii, action=None, inputColumn=None, name=None, selectAll=False):
        self.frame = eii.ExtensionObject()
        self.sheet = self.frame.ActiveSheet()
        self.action = action
        self.inputColumn = inputColumn
        self.targetColumnId = None
        self.selectAll = selectAll
        self.name = name

    @staticmethod
    def CallTradeCreationHook(action, trades):
        functionPath = FTradeProgramTM.Settings().CandidateTradesHook()
        FAssetManagementUtils.CallFunction(functionPath, action, trades)

    @staticmethod
    def SetPremium(trades):
        for trade in trades:
            decorator = acm.FBusinessLogicDecorator.WrapObject(trade)
            decorator.Quantity(trade.Quantity())

    def Execute(self, trades): #All trade program actions converge here
        self.CallTradeCreationHook(self.action.Name(), trades)
        self.SetPremium(trades)
        
        if self.ValidateTrades(trades):
            self.SendEvent(OnCandidateTradesCreated(self, trades, self.action))       
    
    def ExecutePlaceholder(self, trades):
        if self.ValidateTrades(trades):
            self.SendEvent(OnPlaceholderTradesCreated(self, trades, self.action))      
    
    def RowsInputsAndCurrency(self, asString=False):
        inputColumnIter = self._ColumnIter(self.inputColumn)

        for tree in self._InstrumentRowTrees():
            inputValue = self._GetInput(tree.Iterator(), inputColumnIter, asString)
            if inputValue is not None:
                row = RowProxy(tree.Item()).Row()
                currency = self._GetRowCurrency(tree.Iterator())
                yield row, inputValue, currency

    def InstrumentRows(self):
        for tree in self._InstrumentRowTrees():
            row = RowProxy(tree.Item()).Row()
            yield row
    
    def ValidateTrades(self, trades):
        try:
            for trade in trades:
                assert not trade.Instrument().IsExpired(), '{0} has expired and can\'t be traded'.format(trade.Instrument().Name())
                if trade.Portfolio():
                    assert not trade.Portfolio().Compound(), 'Can\'t create candidate trades on compound portfolios. Please use Subportfolio grouper.'
        except AssertionError as e:
            self.SendEvent(OnError(self, 'Information', e.message))
            return False
        else:
            return True
    
    def SendEvent(self, event):
        dispatcher = FIntegratedWorkbench.GetView(self.frame).Dispatcher()
        dispatcher.Update(event)
    
    @classmethod
    def Settings(cls):
        return cls.SETTINGS

    def _GetInput(self, rowIter, columnIter, asString=False):
        try:
            if not columnIter:
                raise Exception
            cell = self.sheet.GetCell(rowIter, columnIter)

            if asString:
                val = cell.FormattedValue()
            else:
                val = cell.Value()
                try:
                    val = float(val)
                    if math.isnan(val):
                        val = None
                except ValueError:
                    Logger().debug('Failed to cast {0} to float'.format(val))
                    val = None
            return val
        except Exception:
            Logger().info('Error reading input from row {0}'.format(
                rowIter.Tree().Item().StringKey()))

    def _GetRowCurrency(self, rowIter):
        columnIter = self.sheet.GridColumnIterator()
        if columnIter is None:
            Logger().info('Error reading target column currency from row {0}'.format(
                rowIter.Tree().Item().StringKey()))

        while columnIter:
            cell = self.sheet.GetCell(rowIter, columnIter)
            if cell.Tag():
                return acm.GetCalculatedValueFromString(rowIter.Tree().Item(),
                                                        acm.GetDefaultContext(),
                                                        'displayCurrency',
                                                        cell.Tag()
                                                       ).Value()
            columnIter = columnIter.Next()
    
    def _ColumnIter(self, column):
        def SameColumn(gridColumn, gridColumnOrColumnId):
            if isinstance(gridColumnOrColumnId, str):
                return gridColumn and str(gridColumn.ColumnId()) == gridColumnOrColumnId
            else:
                return gridColumn == gridColumnOrColumnId
                
        columnIter = self.sheet.GridColumnIterator()
        while columnIter:
            gridColumn = columnIter.GridColumn()
            if SameColumn(gridColumn, column):
                return columnIter
            columnIter = columnIter.Next()

    def _InstrumentRowTrees(self):
        if self.selectAll:
            return self._AllRowTrees()
        else:
            return self._SelectedRowTrees()

    def _AllRowTrees(self):
        instrumentRowTrees = dict()
        rowIter = self.sheet.RowTreeIterator(0)
        while rowIter.NextUsingDepthFirst():
            tree = rowIter.Tree()
            row = tree.Item()
            if RowProxy.IsInstrument(row):
                instrumentRowTrees[row] = tree
        return instrumentRowTrees.values()

    def _SelectedRowTrees(self, instrumentRowTrees=None, selectedRowTrees=None):
        if instrumentRowTrees is None:
            instrumentRowTrees = dict()
        if selectedRowTrees is None:
            selectedRowTrees = (cell.Tree() for cell in
                                self.sheet.Selection().SelectedRowCells())
        for tree in selectedRowTrees:
            rowObject = tree.Item()
            if RowProxy.IsInstrument(rowObject):
                instrumentRowTrees[rowObject] = tree
            self._SelectedRowTrees(instrumentRowTrees,
                                   self._ChildrenTrees(tree))
        return instrumentRowTrees.values()

    @staticmethod
    def _ChildrenTrees(tree):
        child = tree.Iterator().FirstChild()
        while child:
            yield child.Tree()
            child = child.NextSibling()

class FTradeProgramExport(object):

    def __init__(self, items, grouper=None, creators=None, sheetTemplate=None,
                 xsltTemplate='FCSVTemplateFormatedDataWithHeader'):
        self.items = items
        self.creators = creators
        self.sheetTemplate = sheetTemplate
        self.grouper = grouper
        self.xsltTemplate = xsltTemplate
        self.output = acm.FXmlReportOutput('')
        self.builder = None
        self._InitSettings()

    def ToFile(self, path):
        self._GenerateXML()
        self._TransformXml()
        self._Write(path)

    def _Write(self, path):
        with open(path, 'w') as aFile:
            aFile.write(str(self.output))

    def _InitSettings(self):
        self.output.IncludeRawData(True)
        self.output.IncludeFullData(True)
        self.output.IncludeFormattedData(True)

    def _GenerateXML(self):
        config = acm.Report.CreateGridConfiguration(False, True)
        grid = acm.Report.CreateReport('', self.output)
        sheet = self.sheetTemplate.TradingSheet() if self.sheetTemplate else acm.FTradeSheet()
        grid.OpenSheet(sheet, config)
        self.builder = grid.GridBuilder()
        self._InsertContents()
        if self.creators:
            self._InsertColumns()
        grid.Generate()

    def _TransformXml(self):
        try:
            template = acm.GetDefaultContext().GetExtension(
                'FXSLTemplate', 'FObject', self.xsltTemplate)
            xsl = template.Value()
            transformer = acm.CreateWithParameter('FXSLTTransform', xsl)
            self.output = transformer.Transform(self.output.AsString())
        except AttributeError:
            raise AttributeError(
                "Failed to load XSLT xsltTemplate %s" % template)
        except Exception as e:
            raise Exception(
                "Failed to transform XML: %s" % str(e))

    def _InsertColumns(self):
        self.builder.ColumnCreators().Clear()
        for index in range(self.creators.Size()):
            self.builder.ColumnCreators().Add(self.creators.At(index))

    def _InsertContents(self):
        for item in self.items:
            node = self.builder.InsertItem(item)
            node.ApplyGrouper(self.grouper)


class RowProxy(object):

    __slots__ = ['row']

    def __init__(self, row):
        self.row = row

    @classmethod
    def Rows(cls, rows):
        for row in rows:
            yield cls(row).Row()

    @staticmethod
    def IsInstrument(item):
        if item.IsKindOf(acm.FSingleInstrumentAndTrades):
            return not item.Instrument().IsExpired()
        elif item.IsKindOf(acm.FDistributedRow):
            instrument = item.Instrument()
            return bool(instrument) and not instrument.IsExpired()
        return False

    def _SingleRow(self, instrument):
        return acm.Risk.CreateSingleInstrumentAndTradesBuilder(
            self.row.Portfolio(),
            instrument).GetTargetInstrumentAndTrades()

    def _PortfolioRow(self):
        return acm.Risk.CreatePortfolioInstrumentAndTrades(
            self.row.Portfolio())

    def _MultiRow(self, grouper):
        return acm.Risk.CreateMultiIntrumentAndTrades(
            self.row.Portfolio(), grouper, [self.row.AsSymbol()])

    def _ClassicRow(self):
        instrument = self.row.Instrument()
        if instrument:
            return self._SingleRow(instrument)
        grouper = self.row.GrouperOnLevel()
        if grouper.IsKindOf(acm.FPortfolioGrouper):
            return self._PortfolioRow()
        return self._MultiRow(grouper)

    def Row(self):
        if self.row.IsKindOf(acm.FDistributedRow):
            return self._ClassicRow()
        return self.row
