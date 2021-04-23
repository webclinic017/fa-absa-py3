
import acm
import FUxCore
import IndexSearchCreator
import IndexSearchMultiDialog

from IndexSearchConsumer import ScopeTaskConsumer
from IndexSearchConsumer import QueryTaskConsumer

from IndexSearchUtils import unicode_encode
from IndexSearchUtils import unicode_decode

s_colCount = 2

def V(info, key) :
    value = info.get(key, '')

    return unicode_encode(value)

def ClearUserDialogConfiguration(frameClass) :
    context = acm.GetDefaultContext()

    editModule = context.EditModule()
    ret = False
    if editModule and not editModule.IsBuiltIn() :
        try :
            editModule.RemoveExtension('FExtensionValue', frameClass, 'IndexSearchDialogDefinitions')
            editModule.Commit()
            ret = True
        except Exception as e:
            print (e)

    return ret

def GetDialogConfigurations(frameClass) :
    context = acm.GetDefaultContext()
    
    dialogConfigurations = context.GetExtension('FExtensionValue', frameClass, 'IndexSearchDialogDefinitions')
    if dialogConfigurations :
        dialogConfigurations = dialogConfigurations.Value()
        dialogConfigurations = dialogConfigurations.split(';')
    else:
        dialogConfigurations = []



    return dialogConfigurations

def SetDialogConfigurations(dialogConfiguration, frameClass) :
    context = acm.GetDefaultContext()
    dialogConfiguration = ';'.join(dialogConfiguration)
    dialogConfiguration = frameClass.StringKey() + ':IndexSearchDialogDefinitions\n' + dialogConfiguration
    context.EditImport('FExtensionValue', dialogConfiguration, False, None)
    editModule = context.EditModule()
    if editModule and not editModule.IsBuiltIn() :
        try :
            editModule.Commit()
        except Exception as e:
            print (e)


def FilterConfigurations(configurations, frameClass) :
    filterConfigurations = []

    dialogConfigurations = GetDialogConfigurations(frameClass)
    if dialogConfigurations :
        for dialogConfiguration in dialogConfigurations :
            for configuration in configurations :
                if dialogConfiguration == configuration.Identifier() :
                    filterConfigurations.append(configuration)
                    break
    else:
        filterConfigurations = configurations

    return filterConfigurations

class CellType :
    Header = 0
    Main = 1
    Sub = 2

class ProgressHelper(object):
    def __init__(self, progressControl, n) :
        self.m_n = n
        self.m_step = 100.0 / n
        self.m_current = 0
        self.m_progressControl = progressControl

    def SetSize(self, n) :
        self.m_n = n        
        self.m_step = 100.0 / n


    def Step(self):
        self.m_current += self.m_step
        self.m_progressControl.SetData(int(self.m_current)) 

    def Reset(self):
        self.m_current = 0
        self.m_progressControl.SetData(int(self.m_current)) 


class GridRowData(object) :
    def __init__(self, cellType, resultItem) :
        self.m_cellType = cellType
        self.m_resultItem = resultItem

class ResultItem(object) :
    def __init__(self, name, matchedTerms, icon, moniker) :
        self.m_name = name
        self.m_matchedTerms = matchedTerms
        self.m_icon = icon
        self.m_moniker = moniker


class ResultInfo(object) :
    def __init__(self):
        self.m_results = []
        self.m_page = 0
        self.m_pageCount = 0
        self.m_offset = 0
        self.m_foundCount = 0
        self.m_pageLength = 0
        self.m_suggestion = 0

class State :
    WAITING = 0
    ATTACHED = 1
    CONNECTED = 2

class IndexSearchGridNode(object) :
    def __init__(self, configuration, rootGridNode, populateGridCB, stateCB, connectedCB) :
        self.m_configuration = configuration
        self.m_columnKeys = configuration.IndexAttributes()
        self.m_indexName = configuration.Identifier()
        self.m_resultPageSize = 5
        self.m_populateGridCB = populateGridCB
        self.m_stateCB = stateCB
        self.m_connectedCB = connectedCB

        self.m_scopePaceConsumer = ScopeTaskConsumer.Create(self.IndexName(), self.OnScopeTaskConsumerResult, self.OnScopeTaskConsumerProgress, self.OnScopeState, self.OnScopeInitialPopulateDone)
        self.m_queryPaceConsumer = QueryTaskConsumer(self.OnQueryTaskConsumerResult)
        self.m_rootGridNode = rootGridNode

    def OnScopeState(self, status, statusText):
        if self.m_stateCB:
            self.m_stateCB(self.m_indexName, status, statusText)

    def OnScopeInitialPopulateDone(self) :
        if self.m_connectedCB :
            self.m_connectedCB(self.m_indexName)

    def OnScopeTaskConsumerResult(self, result):
        pass

    def OnScopeTaskConsumerProgress(self, percent, progressText):
        pass

    def OnQueryTaskConsumerResult(self, consumerResults):
        resultInfo = ResultInfo()
        resultInfo.m_foundCount = consumerResults.foundCount
        resultInfo.m_page = consumerResults.page
        resultInfo.m_pageCount = consumerResults.pageCount
        resultInfo.m_offset = consumerResults.offset
        resultInfo.m_pageLength = consumerResults.pageLength
        resultInfo.m_total = consumerResults.total

        for searchResult in consumerResults.searchResults :
            di = searchResult.displayInformation
            info = {}
            for keyValue in searchResult.keyValues :
                info[keyValue.key] = keyValue.value
            termsMatched = unicode_encode(info['terms'])
            termsMatched = termsMatched.replace('\n', ' ')
            resultItem = ResultItem(unicode_encode(di.label.formatString), termsMatched, unicode_encode(di.icon), searchResult.moniker)
            resultInfo.m_results.append(resultItem)

        headerText = unicode_encode(self.m_indexName + ' (' + str(resultInfo.m_pageLength) + '/' + str(resultInfo.m_total) + ')')
        self.m_populateGridCB(self.m_rootGridNode, resultInfo, headerText)

    def HandleDestroy(self) :
        self.m_queryPaceConsumer.Destroy()

    def IndexName(self) :
        return self.m_indexName

    def GetNameColumnKey(self) :
        return unicode_encode(self.m_columnKeys[0])

    def DoSearch(self, query) :
        
        self.m_queryPaceConsumer.DoSearch(query, 1, self.m_resultPageSize, self.m_scopePaceConsumer.PaceConsumer(), self.m_scopePaceConsumer.Scope())


class IndexSearchGridDialog(FUxCore.LayoutDialog):
    def __init__(self, configurations, parentApplication):
        self.m_configurations = configurations
        self.m_parentApplication = parentApplication
        self.m_searchInput = None
        self.m_information = None
        self.m_settingsButton = None
        self.m_indexSearchGridNodes = []
        self.m_rowDataByGridRow = {}
        self.m_currentState = State.WAITING
        self.m_connectedCount = 0
        self.m_progressHelper = None

        self.m_frameClass = self.m_parentApplication.Class()

    def HandleApply( self ):
        return self.Open()

    def Caption(self) :
        return 'Index Search'

    def HandleDestroy(self):
        for indexSearchGridNode in  self.m_indexSearchGridNodes :
            indexSearchGridNode.HandleDestroy()

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.Caption())

        okButton = layout.GetControl('ok')
        okButton.Visible(False)

        self.m_searchInput = layout.GetControl('searchInput')
        self.m_searchInput.AddCallback( 'Changed', self.OnSearchChanged, self )
        self.m_searchInput.AddCallback( 'LooseFocus', self.OnLooseFocus, self )
        self.m_searchInput.Enabled(self.m_currentState == State.CONNECTED)
        self.m_grid = layout.GetControl('resultGrid')

        self.m_information = layout.GetControl('information')
        self.m_information.SetData('Waiting for index service...')
        #self.m_information.Enabled(False)

        self.m_grid.ShowRowHeaders(False)
        self.m_grid.ShowColumnHeaders(False)
        self.m_grid.SetEnterKeyMove(True, 'Down')
        self.m_grid.SetCellBorderStyle('None')

        self.m_grid.AddCallback('CellCreate', self.OnCellCreate, self.m_grid)
        self.m_grid.AddCallback('ContextMenu', self.OnContextMenu, self.m_grid)
        self.m_grid.AddCallback('SelectionChanged', self.OnSelectionChanged, self.m_grid)

        self.m_column = self.m_grid.AddColumn('Result', 1600)
        self.m_grid.SelectColumn(self.m_column)

        self.m_settingsButton = layout.GetControl('settingsButton')
        self.m_settingsButton.AddCallback('Activate', self.OnSettings, None)
        self.m_settingsButton.TabStop(False)
        #settingsButton.SetIcon('Settings', False)
        self.m_progressHelper = ProgressHelper(layout.GetControl('searchProgress'), len(self.m_configurations))
        self.SetupGridFromConfiguration()

    def Reinitialize(self) :
        configurations = IndexSearchCreator.get_configurations()

        self.m_configurations = FilterConfigurations(configurations, self.m_frameClass)
        self.m_indexSearchGridNodes = []
        self.m_grid.RemoveAllItems()
        self.m_progressHelper.SetSize(len(self.m_configurations))
        self.SetupGridFromConfiguration()
        self.DoSearch()


    def ChangeSettings(self) :
        configurations = IndexSearchCreator.get_configurations()
        configurationNames = []

        for configuration in configurations :
            configurationNames.append(str(configuration.Identifier()))            

        configurationNames.sort()
        selection = GetDialogConfigurations(self.m_frameClass)
        selection = acm.UX().Dialogs().SelectSubset(self.m_fuxDlg.Shell(), configurationNames, 'Index Search Settings', True, selection, False, 'FreezePane') 

        if selection :
            SetDialogConfigurations(selection, self.m_frameClass)
            self.Reinitialize()

    def OnChangeSettings(self, ud) :
        self.ChangeSettings()

    def OnClearSettings(self, ud):
        if ClearUserDialogConfiguration(self.m_frameClass) :
            self.Reinitialize()

    def OnSettings(self, ud, cd) :
        menu = acm.FUxMenu()

        menu.AddItem( self.OnChangeSettings, None, 'Settings...', '', True)

        menu.AddSeparator()
        menu.AddItem( self.OnClearSettings, None, 'Revert to Default', '', True)
        menu.Track( self.m_settingsButton)


    def SetupGridFromConfiguration(self) :
        for configuration in self.m_configurations :
            rootGridNode = self.AddHeaderRow(self.m_grid, self.m_grid.GetRootItem(), configuration.Identifier(), configuration.IndexClass())
            rootGridNode.Visible(False)

            indexSearchGridNode = IndexSearchGridNode(configuration, rootGridNode, self.PopulateSearchResult, self.OnState, self.OnConnected)
            self.m_indexSearchGridNodes.append(indexSearchGridNode)

    def RebuildIndexSearchGridNodes(self) :
        for indexSearchGridNode in  self.m_indexSearchGridNodes :
            configuration = indexSearchGridNode.m_configuration
            rootGridNode = self.AddHeaderRow(self.m_grid, self.m_grid.GetRootItem(), configuration.Identifier(), configuration.IndexClass())
            rootGridNode.Visible(False)
            indexSearchGridNode.m_rootGridNode = rootGridNode

    def PopulateSearchResult(self, gridRootNode, resultInfo, headerText) :
        self.m_progressHelper.Step()

        if resultInfo.m_results:
            gridRootNode.Visible(True)
        
        gridRootNode.Expand(True)
        for resultItem in resultInfo.m_results :
            self.AddRow(self.m_grid, gridRootNode, resultItem)

        gridRootNode.GetCell(self.m_column).SetData(headerText)

    def OnState(self, indexName, state, stateText):
        message = 'Working... ' + str(self.m_connectedCount) + '/' + str(len(self.m_indexSearchGridNodes)) + ' indexes built'
        self.m_information.SetData(message)
        self.m_currentState = State.ATTACHED

    def OnConnected(self, indexName):
        self.m_connectedCount += 1
        if not self.m_searchInput.Enabled() :
            self.m_searchInput.Enabled(True)
            self.m_searchInput.SetFocus()

        self.m_currentState = State.CONNECTED

        message = 'Working... ' + str(self.m_connectedCount) + '/' + str(len(self.m_indexSearchGridNodes)) + ' indexes built'
        self.m_information.SetData(message)


        if self.m_connectedCount == len(self.m_indexSearchGridNodes) :
            self.m_information.Visible(False)

    def AddHeaderRow(self, grid, parent, label, icon) :
        label = unicode_encode(label)
        icon = unicode_encode(icon)

        row = parent.AddChild()
        row.Height(30)
        resultItem = ResultItem(label, '', icon, '')
        self.m_rowDataByGridRow[row] = GridRowData(CellType.Header, resultItem)
        row.GetCell(self.m_column)

        return row

    def AddRow(self, grid, parent, resultItem) :
        row = parent.AddChild()
        row.Height(20)
        row.Icon(resultItem.m_icon)

        self.m_rowDataByGridRow[row] = GridRowData(CellType.Main, resultItem)
        row.GetCell(self.m_column)

        row = parent.AddChild()
        
        self.m_rowDataByGridRow[row] = GridRowData(CellType.Sub, resultItem)
        row.GetCell(self.m_column)

    def OnSelectionChanged(self, control, cd):
        pass

    def GetSelectedRowData(self) :
        rowData = None
        selectedRow = self.m_grid.GetSelectedItem()

        if not selectedRow :
            treeIterator = self.m_grid.RowTreeIterator(True)
            if treeIterator :
                firstIterator = treeIterator.FirstChild()
                if firstIterator :
                    firstIterator = firstIterator.FirstChild()
                    if firstIterator :
                        selectedRow = firstIterator.Tree()

        if selectedRow:
            rowData = self.m_rowDataByGridRow[selectedRow]

        return rowData

    def GetSelectedObject(self, rowData = None) :
        obj = None
        rowData = rowData if rowData else self.GetSelectedRowData()

        if rowData :
            resultItem = rowData.m_resultItem
            if resultItem.m_moniker :
                obj = acm.Hgc().ResolveMoniker(resultItem.m_moniker.SerializeToString(), 'any')

        return obj

    def Open(self) :
        rowData = self.GetSelectedRowData()
        ok = None
        if rowData :
            if rowData.m_cellType == CellType.Header :
                IndexSearchMultiDialog.ShowIndexSearcMultiDialog(self.m_parentApplication, rowData.m_resultItem.m_name, self.m_searchInput.GetData())
                ok = True
            else :
                obj = self.GetSelectedObject(rowData)

                if obj :
                    applicationName = acm.UX().SessionManager().GetDefaultApplicationForDocument(obj.Class())
                    acm.UX().SessionManager().StartApplication(applicationName, obj)
                    ok = True

        return ok


    def OnContextMenu(self, control, cd):
        menuBuilder = cd.At('menuBuilder')

        obj = self.GetSelectedObject()

        if obj :
            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, None, None)

    def CreateCellEventData(self, row, cell) :
        return {'row':row, 'cell':cell}

    def OnCellEvent(self, event, eventData, cellData):
        cell = cellData['cell']
        row = cellData['row']

        if event == 'DefaultAction':
            self.m_fuxDlg.CloseDialogOK()            

    def GetFirstCell(self) :
        firstCell = None
        treeIterator = self.m_grid.RowTreeIterator(True)

        if treeIterator :
            firstIterator = treeIterator.FirstChild()
            if firstIterator :
                firstIterator = firstIterator.FirstChild()
                if firstIterator :
                    selectedRow = firstIterator.Tree()
                    firstCell = selectedRow.GetCell(self.m_column)

        return firstCell


    def OnCellCreate(self, control, cd):
        row = cd.At('row')
        column = cd.At('column')
        cell = cd.At('cell')


        if cell.HeaderType() == 'None':
            rowData = self.m_rowDataByGridRow[row]
            resultItem = rowData.m_resultItem

            cell.BorderStyle('None')
            if rowData.m_cellType == CellType.Main :
                cell.SetData(resultItem.m_name)
                cell.Icon(resultItem.m_icon)
                cell.SetFont(None, 11)
                cell.AddCallback(self.OnCellEvent, self.CreateCellEventData(row, cell))

            elif  rowData.m_cellType == CellType.Sub :
                cell.SetData('      ' + resultItem.m_matchedTerms)
                cell.SetColor('Text', acm.UXColors.Create(60, 60, 60))
                cell.TabStop(False)      
            elif  rowData.m_cellType == CellType.Header :
                cell.SetData(resultItem.m_name)
                cell.Bold(True)
                cell.SetColor('Background', acm.UXColors.Create(235, 235, 235))
                cell.TabStop(False)      
                cell.AddCallback(self.OnCellEvent, self.CreateCellEventData(row, cell))

    def OnLooseFocus(self, ud, cd) :
        firstCell = self.GetFirstCell()

        if firstCell :
            self.m_grid.SelectCell(firstCell)

    def DoSearch(self) :
        self.m_grid.RemoveAllItems()
        self.m_rowDataByGridRow = {}
        self.RebuildIndexSearchGridNodes()

        query = unicode_decode(self.m_searchInput.GetData())
        self.m_progressHelper.Reset()


        for indexSearchGridNode in  self.m_indexSearchGridNodes :
            indexSearchGridNode.DoSearch(query)

    def OnSearchChanged(self, ud, cd) :
        self.DoSearch()

    def CreateLayout(self) :
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.  BeginHorzBox()
        builder.      AddInput('searchInput', '')
        builder.      AddButton('settingsButton', '>', False, True)
        builder.  EndBox()
        builder.AddGrid('resultGrid',  350, 600)
        builder.AddLabel('information', '                                                   ')
        builder.AddProgress('searchProgress', 1, 8, -1, 8)
        builder.AddButton('ok', 'OK')
        builder.EndBox()

        return builder


def ReallyStartDialog(basicApp):
    configurations = IndexSearchCreator.get_configurations()

    configurations = FilterConfigurations(configurations, basicApp.Class())

    if configurations :
        indexSearchDialog = IndexSearchGridDialog(configurations, basicApp)
        builder = indexSearchDialog.CreateLayout()
        acm.UX().Dialogs().ShowCustomDialog(basicApp.Shell(), builder, indexSearchDialog)

def ShowDialog(eii) :
    basicApp = eii.ExtensionObject()
    ReallyStartDialog(basicApp)
