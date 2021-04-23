""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FSheetUtils.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FSheetUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of utility functions used by the sheet panels.
-------------------------------------------------------------------------------------------------"""

__all__ = [
    'ApplyGrouperToSheet',
    'ApplyGrouperInstanceToSheet',
    'GetGrouperFromSheet',
    'GetGrouper',
    'TopRow',
    'ExpandTree',
    'SheetObserver',
    'SingleInstrumentAndTrades',
    'Trade',
    'Trades',
    'TreeConfiguration',
    'TreeConfigurations',
    'SelectedInstruments',
    'SelectedTrades',
    'SelectedOrders',
    'OrderBook',
    'OrderBooks',
    'QueryBy',
    'AsFolder',
    'AsFolders',
    'GetObjectsAsFolder',
    'GetTradesAsFolder',
    'CreateSheetSetup',
    'ColumnIds',
    'ColumnsConfiguration',
    'ColumnCretor',
    'ColumnCreatorInSheet',
    'ColumnCreators',
    'ColumnIsInSheet',
    'AddColumn',
    'Contents',
    'RemoveRows',
    'SaveSheetTemplate',
    'GetSheetTemplate',
    'ApplySheetToTemplate',
    'SaveSheetAsTemplate',
    'GetWorkbook',
    'SimulateCell',
    'UnsimulateCell',
    'GetEvaluator',
    'GetCell',
    'SheetSettings',
    'SheetContents',
    'Sheet'
    ]

import itertools
import acm
from FParameterSettings import ParameterSettingsCreator
from FAssetManagementUtils import logger, MethodNameFromDomain

def ApplyGrouperToSheet(sheet, grname):
    """ Get named grouper and apply to the sheet. """
    grouper = acm.Risk().GetGrouperFromName(grname)
    ApplyGrouperInstanceToSheet(sheet, grouper)

def ApplyGrouperInstanceToSheet(sheet, grouper):
    """ Apply grouper to sheet. """
    if not grouper:
        logger.debug('ApplyGrouperInstanceToSheet() Grouper object is None')
        return
    iterator = sheet.RowTreeIterator(True)
    while iterator.NextUsingDepthFirst():             
        if iterator.Tree():
            logger.debug("ApplyGrouperInstanceToSheet() Applying grouper '%s' (%s) to node: '%s' root: '%s' " %
            (grouper.DisplayName(), grouper, iterator.Tree().StringKey(), sheet.RowTreeIterator(True).Tree().StringKey()))
            try:
                iterator.Tree().ApplyGrouper(grouper)
            except Exception as stderr:
                logger.debug("ApplyGrouperInstanceToSheet() Unable to apply grouper '%s' to sheet '%s' : %s" % (grouper.DisplayName(), sheet.Name(), stderr))
    sheet.GridBuilder().Refresh()

def GetGrouperFromSheet(sheet):
    """ Get the first grouper used in the sheet. """
    grouper = None
    rowIter = sheet.RowTreeIterator(True).FirstChild()
    columnIter = sheet.GridColumnIterator().First()
    cell = sheet.GetCell(rowIter, columnIter)
    if cell:
        treeSpec = cell.TreeSpecification()
        if treeSpec and treeSpec.Grouper():
            grouper = treeSpec.Grouper()
    return grouper

def GetGrouper(row):
    try:
        return row.Grouping().Grouper()
    except AttributeError:
        return None

def TopRow(row):
    while row.Parent():
        row = row.Parent()
    return row

def ExpandTree(sheet, level=1000):
    """ Expand the nodes of a sheet to specified level. """
    sheet.RowTreeIterator(0).Tree().Expand(True, level)

class SheetObserver(object):
    """ Helper class for listening to ServerUpdates from a sheet control. """
    def __init__(self, parent):
        self._parent = parent

    def ServerUpdate(self, sender, aspect, param=None):
        # pylint: disable-msg=R0903
        try:
            logger.debug("SheetObserver.ServerUpdate() event: %s %s" % (aspect, param))
            if str(aspect) == 'OnDestroy':
                self._parent.HandleDestroy()
            elif str(aspect) == 'SelectionChanged':
                # pylint: disable-msg=W0212
                self._parent._SendSheetChanged(sender)
            else:
                logger.error("SheetObserver.ServerUpdate() Unhandled event with aspect: %s" % (aspect))
        except Exception as exc:
            logger.error("SheetObserver.ServerUpdate() Exception:")
            logger.error(exc, exc_info=True)

def SingleInstrumentAndTrades(instrument):
    portfolio = acm.FSingleDealPortfolio(instrument)
    return acm.Risk().CreateSingleInstrumentAndTradesBuilder(
        portfolio, instrument).GetTargetInstrumentAndTrades()

def Trade(instrument):
    try:
        return acm.FSingleDealPortfolio(instrument).Trades().First()
    except RuntimeError:
        return None

def Trades(instruments):
    trade = Trade
    return [trade(i) for i in instruments]

def TreeConfiguration(instrument):
    siat = SingleInstrumentAndTrades(instrument)
    return siat.Builder().TreeConfiguration()

def TreeConfigurations(instruments):
    treeConfig = TreeConfiguration
    return [treeConfig(ins) for ins in instruments]

def SelectedInstruments(selection):
    rowObjects = selection.SelectedRowObjects()
    if rowObjects and rowObjects[0].IsKindOf(acm.FDistributedRow):
        try:
            return [rowObj.SingleInstrumentOrSingleTrade()
                    for rowObj in rowObjects]
        except RuntimeError:
            return []
    return selection.SelectedInstruments() or []

def SelectedTrades(selection):
    try:
        return list(set(itertools.chain(*[row.Trades() for row in selection])))
    except (AttributeError, TypeError):
        return list()

def SelectedOrders(selection):
    orders = list()
    if selection and selection.SelectedOrders():
        for order in selection.SelectedOrders():
            orders.append(order)
            orders.extend(AllChildOrders(order))
    return [order for order in set(orders) if not order.IsKindOf(acm.FGroupingOrder)]

def AllChildOrders(order):
    orders = list()
    if order.IsKindOf(acm.FMultiOrder):
        for childOrder in order.OwnOrders():
            orders.append(childOrder)
            orders.extend(AllChildOrders(childOrder))
    return orders

# def OrderBook(instrument):
#     try:
#         return instrument.OrderBooks().First()
#     except RuntimeError:
#         return None
# 
# def OrderBooks(instruments):
#     orderBook = OrderBook
#     return [orderBook(i) for i in instruments]

def QueryBy(record, cls):
    """ Query cls by record. """
    methodName = MethodNameFromDomain(cls, record.Domain())
    if methodName is None:
        logger.info('Can\'t query {0} with {1} = {2}.'.format(
            cls.StringKey(), record.ClassName(), record.StringKey()))
        return None
    query = acm.CreateFASQLQuery(cls, 'AND')
    query.AddAttrNode('{0}.Name'.format(methodName),
                      'EQUAL', record.Name())
    return query

def AsFolder(record, cls):
    query = QueryBy(record, cls)
    if query:
        folder = acm.FASQLQueryFolder()
        folder.Name(record.StringKey())
        folder.AsqlQuery(query)
        return folder
    return None

def AsFolders(records, clsName='FSalesActivity'):
    asFolder = AsFolder
    cls = acm.GetDomain(clsName)
    return [asFolder(r, cls) for r in records]

def GetTradesAsFolder(trades, label=None):
    folder = acm.FAdhocPortfolio()
    folder.Name(label)
    for trade in trades:
        folder.Add(trade)
    return folder

def GetObjectsAsFolder(objects, label=None):
    if objects:
        folder = acm.FASQLQueryFolder()
        folder.Name(label)
        objectType = objects[0].Class().Name()
        query = acm.CreateFASQLQuery(objectType, 'OR')
        for obj in objects:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', obj.Oid())
        folder.AsqlQuery(query)
        return folder
    return None

def CreateSheetSetup(cls='FPortfolioSheet'):
    definition = acm.Sheet.GetSheetDefinition(cls)
    return definition.CreateSheetSetup()

def ColumnsConfiguration(extensionName, cls='FObject'):
    try:
        config = acm.GetCalculatedValue(
            acm.FClass[cls].BasicNew(None),
            acm.GetDefaultContext(),
            extensionName
            ).Value()
        return acm.GetFunction('createDictionary', 2)(
            acm.GetFunction('symbol', 1)(config.Keys()),
            config.Values())
    except AttributeError:
        return None

def ColumnIds(extensionName, cls='FObject'):
    try:
        return acm.GetCalculatedValue(
            acm.FClass[cls].BasicNew(None),
            acm.GetDefaultContext(),
            extensionName
            ).Value().split('.')
    except AttributeError:
        return None

def ColumnCreators(columnIds=None, context=None, additionalData=None):
    if columnIds is None:
        columnIds = str()
    if context is None:
        context = acm.GetDefaultContext()
    return acm.GetColumnCreators(columnIds, context, additionalData)

def ColumnCreator(columnId, context=None, additionalData=None):
    try:
        return ColumnCreators([columnId], context, additionalData).At(0)
    except RuntimeError:
        return None

def ColumnCreatorInSheet(sheet, columnId):
    columnCreators = sheet.ColumnCreators()
    for index in range(columnCreators.Size()):
        if str(columnCreators.At(index).ColumnId()) == columnId:
            return columnCreators.At(index)

def ColumnIsInSheet(sheet, columnId):
    columnCreators = sheet.ColumnCreators()
    for index in range(columnCreators.Size()):
        if str(columnCreators.At(index).ColumnId()) == columnId:
            return True
    return False

def AddColumn(sheet, columnId):
    if not ColumnIsInSheet(sheet, columnId):
        columnCreator = ColumnCreators([columnId]).At(0)
        sheet.ColumnCreators().Add(columnCreator)

def SelectedColumns(sheet):
    return set(cell.Column() for cell in sheet.Selection().SelectedCells())

def GetColumnIfOneSelected(sheet):
    columns = SelectedColumns(sheet)
    if len(columns) == 1:
        return columns.pop()
    else:
        return None
        
def ColumnParameters(column):
    try:
        return column.Creator().Configuration().ParamDict().At('columnParameters')  
    except AttributeError:
        return None

def Contents(setup):
    d = acm.FDictionary()
    d.AtPut(acm.FSymbol('SheetSetup'), setup)
    return d

def RemoveRows(template):
    try:
        tradingSheet = template.TradingSheet()
        tradingSheet.RemoveAllRows()
        tradingSheet.Commit()
    except Exception as e:
        logger.error('Failed to remove rows. Reason: {0}'.format(e))

def SaveSheetTemplate(template, isShared=True):
    try:
        template.AutoUser(not isShared)
        template.Commit()
        logger.info('Saved {0} sheet template for user '
                    '{1}.'.format(template.Name(),
                                  acm.UserName() if isShared is False else 'None'))
    except Exception as e:
        raise Exception('Failed to save sheet template {0}. '
                            'Reason: {1}'.format(template.Name(), e))

def GetSheetTemplate(name, isShared=False):
    query = 'name = "{0}" and user = {1}'.format(name,
        acm.UserName() if isShared is False else 0)
    return acm.FTradingSheetTemplate.Select01(query, None)

def ApplySheetToTemplate(uxSheet, template, caption=''):
    if not uxSheet.Name():
        uxSheet.Name(caption)
    uxSheet.ApplyToTemplate(template)

def SaveSheetAsTemplate(uxSheet, paramName):
    contents = SheetContents(ParameterSettingsCreator.FromRootParameter(paramName))
    template = GetSheetTemplate(contents.Name(), contents.IsShared())
    if template is None:
        template = acm.FTradingSheetTemplate()
        template.Name(contents.Name())
    ApplySheetToTemplate(uxSheet, template, contents.Caption())
    if contents.IncludeRows() is False:
        RemoveRows(template)
    SaveSheetTemplate(template, contents.IsShared())

def GetWorkbook(name, isShared=False):
    query = 'name = "{0}" and user = {1}'.format(name,
        acm.UserName() if isShared is False else 0)
    return acm.FWorkbook.Select01(query, None)

def FindAppWithWorkbook(workbook):
    if acm.ObjectServer().IsKindOf('FTmServer'):
        for app in acm.ApplicationList():
            if app.IsKindOf(acm.FManagerBaseFrame):
                if app.ActiveWorkbook().StoredWorkbook() is workbook:
                    return app

def SimulateCell(sheet, row, columnId, value):
    try:
        evaluator = GetEvaluator(sheet, row, columnId)
        if evaluator:
            if value is not None:
                evaluator.Simulate(value, False)
            else:
                evaluator.RemoveSimulation()
    except Exception as err:
        logger.error("An error in SimulateCell occurred:{0}".format(err))

def UnsimulateCell(sheet, row, columnId):
    try:
        evaluator = GetEvaluator(sheet, row, columnId)
        if evaluator:
            evaluator.RemoveSimulation()
    except Exception as err:
        logger.error("An error in UnsimulateCell occurred:{0}".format(err))

def GetEvaluator(sheet, row, columnId):
    cell = GetCell(sheet, row, columnId)
    return cell.Evaluator() if cell else None

def GetCell(sheet, row, columnId):
    columnIter = sheet.GridColumnIterator()
    while columnIter:
        columnName = str(columnIter.GridColumn().ColumnId()) if \
                columnIter.GridColumn() else None
        if columnName == columnId:
            break
        columnIter = columnIter.Next()
    if columnIter:
        rowIter = sheet.RowTreeIterator(False)
        rowIter = rowIter.Find(row) if rowIter else None
        if rowIter:
            return sheet.GetCell(rowIter, columnIter)
    return None

class SheetSettings(object):

    def __init__(self):
        self._showGroupLabels = True
        self._showRowHeaders = True

    def ShowGroupLabels(self, show=None):
        if show is None:
            return self._showGroupLabels
        self._showGroupLabels = show

    def ShowRowHeaders(self, show=None):
        if show is None:
            return self._showRowHeaders
        self._showRowHeaders = show

    def ApplyTo(self, sheet):
        sheet.ShowGroupLabels(self.ShowGroupLabels())
        sheet.ShowRowHeaders(self.ShowRowHeaders())

class SheetParser(object):

    KEY = 'sname'
    START = '<string type ="AcmDomain">'
    END = '</string>'

    def __init__(self, text):
        self._text = text

    def Name(self):
        text = self._text[self._text.find(self.KEY):]
        start = text.find(self.START)+len(self.START)
        end = start + text[start:].find(self.END)
        return text[start:end]


class SheetContents(object):

    def __init__(self, settings):
        self._settings = settings
        self._isTemplate = False

    def GetSetting(self, name):
        try:
            return getattr(self._settings, name)()
        except AttributeError:
            pass

    def GetSettingAsFObject(self, name, type_):
        value = self.GetSetting(name)
        if value:
            obj = acm.GetDomain(type_)[value]
            if not obj:
                logger.debug(
                    "Couldn't find {2} named {0}. Check settings in FParameter for {1}."
                    "Using default columns for now.".format(value, name, type_)
                    )
                return None
            return obj

    def Name(self):
        return self.GetSetting('SheetTemplate')

    def Distributed(self):
        return self.GetSetting('Distributed')
        
    def SheetType(self):
        return self.GetSetting('SheetType')

    def Caption(self):
        return self.GetSetting('Caption')

    def IncludeRows(self):
        return self.GetSetting('IncludeRows')

    def IsShared(self):
        return self.GetSetting('IsShared')

    def Disposition(self):
        return self.GetSetting('Disposition')        

    def SheetTemplate(self):
        template = self.GetSettingAsFObject('SheetTemplate',
                                            'FTradingSheetTemplate')
        if template:
            self._isTemplate = True
        return template

    def Context(self):
        context = self.GetSettingAsFObject('Context',
                                           'FExtensionContext')
        return context or acm.GetDefaultContext()

    def ColumnCreators(self):
        columnsExtension = self.GetSetting('Columns')
        if columnsExtension:
            columnIds = ColumnIds(columnsExtension, self.SheetType())
            columnsConfiguration = self.GetSetting('ColumnsConfiguration')
            columnData = ColumnsConfiguration(columnsConfiguration, self.SheetType())
            return ColumnCreators(columnIds, self.Context(), columnData)

    def SetColumnCreators(self, setup):
        creators = self.ColumnCreators()
        setup.ColumnCreators(creators)

    def SetSheetTitle(self, setup):
        caption = self.GetSetting('Caption')
        if caption: setup.SheetTitle(caption)

    def SetDistributed(self, setup):
        distributed = self.Distributed()
        setup.DistributedMode(distributed or False)
        
    def SetDisposition(self, setup):
        disposition = self.Disposition()
        setup.DispositionName(disposition)

    def SheetSetup(self):
        setup = CreateSheetSetup(self._settings.SheetType())
        self.SetColumnCreators(setup)
        self.SetSheetTitle(setup)
        self.SetDistributed(setup)
        self.SetDisposition(setup)
        return setup

    def ForApplication(self):
        template = self.SheetTemplate()
        if template is None:
            return self.SheetSetup()
        return template

    def ForControl(self):
        d = acm.FDictionary()
        contents = self.ForApplication()
        if self._isTemplate:
            d.AtPut(acm.FSymbol('Sheet'),
                    contents.TradingSheet())
        else:
            d.AtPut(acm.FSymbol('SheetSetup'),
                    contents)
        return d


class Sheet(object):

    def __init__(self, uxSheet):
        self._uxSheet = uxSheet
        self._lastGrouper = None

    def Sheet(self, uxSheet=None):
        if uxSheet is None:
            return self._uxSheet
        self._uxSheet = uxSheet

    def LastGrouper(self, lastGrouper=None):
        if lastGrouper is None:
            return self._lastGrouper
        self._lastGrouper = lastGrouper

    def SelectedRows(self):
        """ Return the selected rows in the current sheet. """
        return self.Sheet().Selection()

    def InsertObject(self, obj, pos=None):
        grouper = GetGrouperFromSheet(self.Sheet())
        if grouper:
            self.LastGrouper(grouper)
        if pos in ('IOAP_REPLACE', 'IOAP_SORTED'):
            self.Sheet().InsertObject(obj, pos)
        else:
            self.Sheet().RemoveAllRows()
            for o in self.AsIterable(obj):
                if pos is None:
                    pos = 'IOAP_LAST'
                self.Sheet().InsertObject(o, pos)
        if self.LastGrouper():
            ApplyGrouperInstanceToSheet(self.Sheet(), self.LastGrouper())

    def ApplyGrouper(self, grname):
        ApplyGrouperToSheet(self.Sheet(), grname)

    def ExpandTree(self, level=1000):
        ExpandTree(self.Sheet(), level)

    def OnSaveSheetAsTemplate(self, event):
        if self.Sheet() is event.Sheet():
            SaveSheetAsTemplate(self.Sheet(), self.Name())

    @staticmethod
    def AsIterable(selection):
        try:
            iter(selection)
            return selection
        except TypeError:
            return [selection]

    def __getattr__(self, attr):
        """ Pass calls to actual ACM Sheet object. """
        try:
            return getattr(self.Sheet(), attr)
        except AttributeError:
            pass