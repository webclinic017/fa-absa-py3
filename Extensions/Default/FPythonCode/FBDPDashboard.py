""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboard.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""
The FBDP Dashboard is an AUX application that presents a graphical overview
of the database based on the configuration. The tool highlights the areas that
needs the user's attention, and from which the user can launch the BDP script
to perform the necessary data maintenance.
"""


import collections
import os.path


import acm


import FUxCore


import FBDPDashboardDefaultConfig
import FBDPDashboardDisplay
import FBDPDashboardSuggestTask
import FBDPDashboardViews


# Menu commands
FILE_OPEN = 'FileOpen'
FILE_SAVE = 'FileSave'
FILE_SAVE_AS = 'FileSaveAs'
FILE_TYPES = ("Json Files (*.json)|*.json|"
                "Text Files (*.txt)|*.txt|"
                "XML Files (*.xml)|*.xml|"
                "All Files (*.*)|*.*")


PORT_SHEET_PG_INDEX = 2
LIMIT_SHEET_PG_INDEX = 3

CONFIG_MODE = 0
SHEET_SELECTION_MODE = 1


MenuItemCommandSpec = collections.namedtuple('MenuItemCommandSpec',
        ['name', 'parent', 'path',
        'tooltip', 'shortcut', 'mnemonic', 'callback', 'default'])


MENU_ITEM_COMMAND_SPEC_LIST = [
        MenuItemCommandSpec(FBDPDashboardDefaultConfig.VIEW_TYPE_DATABASE,
                'View', 'Database', 'View DB Data',
                'Ctrl+D', '1', None, False),
        MenuItemCommandSpec(FBDPDashboardDefaultConfig.VIEW_TYPE_TRADES,
                'View', 'Trades', 'View Trade Data',
                'Ctrl+T', '1', None, False),
        MenuItemCommandSpec(FBDPDashboardDefaultConfig.VIEW_TYPE_INSTRUMENTS,
                'View', 'Instruments', 'View Instrument Data',
                'Ctrl+I', '2', None, False),
        MenuItemCommandSpec(FBDPDashboardDefaultConfig.VIEW_TYPE_PRICES,
                'View', 'Prices', 'View Price Data',
                'Ctrl+P', '3', None, False),
        #When support Yield Curves & Volatility Structures
        #MenuItemCommandSpec('yieldCurves',
        #        'View', 'Yield Curves', 'View Yield Curve Data',
        #        'Ctrl+Y', '4', None, False),
        #MenuItemCommandSpec('volStructures',
        #        'View', 'Volatility Structures',
        #        'View Vol Structure Data', '', '', None, False),
        MenuItemCommandSpec('insertItems',
                'View', 'Items', '',
                '', '', None, False),
        MenuItemCommandSpec('export',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('import',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('refresh',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('up',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('aggregation',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('expiration',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('fxAggregation',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('deletePrices',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('benchmarktest',
                'View', '', '',
                '', '', None, False),
        MenuItemCommandSpec('traderollout',
                'View', '', '',
                '', '', None, False)
]


def CreateApplicationInstance():
    return BDPDashboard()


def ReallyStartApplication(_shell, _count):
    acm.UX().SessionManager().StartApplication('BDP Dashboard', None)


def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0)


def _formatPath(fileSelection):
    dirname = fileSelection.SelectedDirectory().AsString()
    filename = fileSelection.SelectedFile().AsString()
    path = os.path.join(dirname, filename)
    return os.path.normcase(path)


class BDPDashboard(FUxCore.LayoutApplication):

    def __init__(self):

        FUxCore.LayoutApplication.__init__(self)

        self.chartPie = None
        self.chart2d = None
        self.resultTab = None
        self.configTab = None
        self.menuItems = None

        self.uiModel = FBDPDashboardViews.DefaultUIModel()
        self.m_tabControl = None
        self.m_portSheet = None
        self.m_limitSheet = None
        self.m_selectedItem = None
        self.m_mode = CONFIG_MODE
        self.m_doUpdateSelection = False

    def HandleOnIdle(self):
        if self.m_doUpdateSelection:
            self.m_doUpdateSelection = False
            self.uiModel.updateWithSheetSelection(self.m_selectedItem,
                self.display)

    def ActiveSheet(self):
        pgNum = self.m_tabControl.GetActivePage()
        if pgNum == PORT_SHEET_PG_INDEX:
            return self.m_portSheet

        if pgNum == LIMIT_SHEET_PG_INDEX:
            return self.m_limitSheet

        return None

    def HandleRegisterCommands(self, builder):

        # To be able to use the standard File commands(Open,Save,Save As etc)
        # create an FSet and add the enumerator values corresponding to the
        # commands desired. Look at the FUxStandardFileCommands enum for a list
        # of available commands.
        fileCommands = acm.FSet()
        fileCommands.Add(FILE_OPEN)
        fileCommands.Add(FILE_SAVE)
        fileCommands.Add(FILE_SAVE_AS)
        builder.RegisterCommands(FUxCore.ConvertCommands(
                self.menuItems.getCommands()), fileCommands)

    def HandleStandardFileCommandEnabled(self, commandName):
        if commandName == FILE_SAVE:
            return False
        return True

    # Always use @FUxCore.aux_cb when executing code in a .Net event handler to
    # handle exceptions.
    @FUxCore.aux_cb
    def HandleStandardFileCommandInvoke(self, commandName):
        # Handlers need to be class static. See e.g. PriceLinkSpecification.py.
        if commandName == FILE_OPEN:
            BDPDashboard.OnFileOpen(self)
        elif commandName == FILE_SAVE_AS:
            BDPDashboard.OnFileSave(self)
        return True

    @classmethod
    def OnFileOpen(cls, obj):
        selection = acm.UX().Dialogs().BrowseForFiles(obj.Shell(), FILE_TYPES,
                ".")
        if selection:
            obj.loadConfig(_formatPath(selection[0]))

    @classmethod
    def OnFileSave(cls, obj):
        selection = acm.FFileSelection()
        selection.PickExistingFile = False
        selection.FileFilter = FILE_TYPES
        res = acm.UX().Dialogs().BrowseForFile(obj.Shell(), selection)
        if res:
            obj.saveConfig(selection.AsString())

    def loadConfig(self, path):

        self.uiModel.loadConfig(path)

    def saveConfig(self, path):

        self.uiModel.saveConfig(path)

    @FUxCore.aux_cb
    def OnInsertItemClicked(self):  # ,source, args):

        pgNum = self.m_tabControl.GetActivePage()
        if pgNum == PORT_SHEET_PG_INDEX:
            item = acm.UX().Dialogs().SelectObjectsInsertItems(
                self.Shell(), acm.FPhysicalPortfolio, True)
            self.m_portSheet.InsertObject(item, 'IOAP_LAST')

        if pgNum == LIMIT_SHEET_PG_INDEX:
            item = acm.UX().Dialogs().SelectObjectsInsertItems(
                self.Shell(), acm.FLimit, True)
            self.m_limitSheet.InsertObject(item, 'IOAP_LAST')

    @FUxCore.aux_cb
    def OnExportClicked(self):  # ,source, args):
        selection = acm.FFileSelection()
        selection.PickExistingFile = False
        selection.FileFilter = FILE_TYPES
        res = acm.UX().Dialogs().BrowseForFile(self.Shell(), selection)
        if res:
            self.uiModel.exportToFile(selection.AsString())

    @FUxCore.aux_cb
    def OnImportClicked(self):  # ,source, args):
        selection = acm.UX().Dialogs().BrowseForFiles(self.Shell(), FILE_TYPES,
                ".")
        if selection:
            self.uiModel.loadFromFile(_formatPath(selection[0]))

    @FUxCore.aux_cb
    def OnRefreshClicked(self):
        pgNum = self.m_tabControl.GetActivePage()
        if pgNum == PORT_SHEET_PG_INDEX and self.m_selectedItem:
            self.m_mode = SHEET_SELECTION_MODE
            self.uiModel.switchViewOnPortSheet(self.uiModel.getViewType(),
                self.m_selectedItem, self.display)
        else:
            self.uiModel.refreshCurrentView(self.display)

    @FUxCore.aux_cb
    def OnUpClicked(self):

        if (self.uiModel.getViewType() !=
                FBDPDashboardDefaultConfig.VIEW_TYPE_DATABASE and
                self.uiModel.getViewLevel() != 0):
            self.uiModel.goBack(self.display)
        else:
            self.SetView(FBDPDashboardDefaultConfig.VIEW_TYPE_DATABASE)

    @FUxCore.aux_cb
    def OnAggregationClicked(self):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.AGGREGATION_MODULE_NAME)

    @FUxCore.aux_cb
    def OnFXAggregationClicked(self,):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.FXAGGREGATION_MODULE_NAME)

    @FUxCore.aux_cb
    def OnExpirationClicked(self):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.EXPIRATION_MODULE_NAME)

    @FUxCore.aux_cb
    def OnDeletePricesClicked(self):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.DELETEPRICES_MODULE_NAME)

    @FUxCore.aux_cb
    def OnBenchmarkTestClicked(self):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.BENCHMARKTEST_MODULE_NAME)

    @FUxCore.aux_cb
    def OnTradeRolloutClicked(self):
        FBDPDashboardSuggestTask.startSuggestTask(
                FBDPDashboardSuggestTask.TRADEROLLOUT_MODULE_NAME)

    def OnResultDoubleClick(self, _cd, _arg):

        if self.m_mode != CONFIG_MODE:
            return

        key = self.resultTab.getSelectedItemData()
        if (self.uiModel.getViewType() ==
                FBDPDashboardDefaultConfig.VIEW_TYPE_DATABASE and
                self.uiModel.getViewLevel() == 1):
            viewType = FBDPDashboardViews.convertDbTableNameToViewType(key)
            if viewType:
                self.SetView(viewType)
        else:
            self.uiModel.drillDown(key, self.display)

    def ServerUpdate(self, _sender, _aspectSymbol, _parameter):

        pgNum = self.m_tabControl.GetActivePage()
        selection = None
        if pgNum == PORT_SHEET_PG_INDEX:
            selection = self.m_portSheet.Selection().SelectedRowObjects()

        if not selection:
            return

        self.m_mode = SHEET_SELECTION_MODE
        self.m_selectedItem = selection[0]
        self.m_doUpdateSelection = True

    def HandleApply(self):
        return 1

    def HandleCreate(self, creationInfo):

        builder = self.CreateLayout()

        self.m_tabControl = creationInfo.AddTabControlPane("tabPanel")
        self.SetupTabControl()

        layout = creationInfo.AddPane(builder, "mainPane")

        self.chartPie = FBDPDashboardDisplay.DisplayPieChart(
                layout.GetControl('chartPie'))
        self.chartPie.setup()

        self.chart2d = FBDPDashboardDisplay.Display2DChart(
                layout.GetControl('chart2d'))
        self.chart2d.setup()

        self.menuItems = FBDPDashboardDisplay.DisplayMenuItems(
                MENU_ITEM_COMMAND_SPEC_LIST, self)
        self.menuItems.setup()

        self.SetView('database')
        self.EnableOnIdleCallback(True)

    def DoChangeCreateParameters(self, createParams):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(True)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)

    def SetupTabControl(self):

        #self.SetupViewDetailsControl()
        b1 = acm.FUxLayoutBuilder()
        b1.BeginHorzBox('EtchedIn')
        b1.  AddList('configList', -1, -1, 30, -1)
        b1.EndBox()

        b2 = acm.FUxLayoutBuilder()
        b2.BeginHorzBox('EtchedIn')
        b2.  AddList('resultList', -1, -1, 30, -1)
        b2.EndBox()

        #Setup list
        resultPg = self.m_tabControl.AddLayoutPage(b2, 'Results')
        resultPgCtrl = resultPg.GetControl('resultList')
        self.resultTab = FBDPDashboardDisplay.DisplayResultTab(self,
                resultPgCtrl)
        self.resultTab.setup()

        # config list
        configPg = self.m_tabControl.AddLayoutPage(b1, 'Configuration')
        configPgCtrl = configPg.GetControl('configList')
        self.configTab = FBDPDashboardDisplay.DisplayConfigTab(self,
                configPgCtrl)
        self.configTab.setup()

        b3 = acm.FUxLayoutBuilder()
        b3.BeginVertBox('None')
        b3.AddCustom('sheet', 'sheet.FPortfolioSheet', 500, 500)
        b3.EndBox()

        # portfolio sheet tab
        portSheetPg = self.m_tabControl.AddLayoutPage(b3, 'Portfolio Sheet')
        self.m_portSheet = portSheetPg.GetControl('sheet').GetCustomControl()
        self.m_portSheet.AddDependent(self)
        self.SetupPortSheetColumns()

        b4 = acm.FUxLayoutBuilder()
        b4.BeginVertBox('None')
        b4.AddCustom('sheet', 'sheet.FLimitSheet', 500, 500)
        b4.EndBox()

        # limit sheet tab
        limitSheetPg = self.m_tabControl.AddLayoutPage(b4, 'Limit Sheet')
        self.m_limitSheet = limitSheetPg.GetControl('sheet').GetCustomControl()
        self.m_limitSheet.AddDependent(self)

        b5 = acm.FUxLayoutBuilder()
        b5.BeginVertBox('None')
        b5.AddCustom('sheet', 'sheet.FMoneyFlowSheet', 500, 500)
        b5.EndBox()

        return

    def SetupPortSheetColumns(self):

        colCreators = self.m_portSheet.ColumnCreators()
        colCreators.Clear()
        ccPosExpCount = acm.Sheet.Column().GetCreatorTemplate(
                'Position Expired Count', 'Standard').CreateCreator()
        colCreators.Add(ccPosExpCount)
        ccPosLiveCount = acm.Sheet.Column().GetCreatorTemplate(
                'Position Live Count', 'Standard').CreateCreator()
        colCreators.Add(ccPosLiveCount)
        ccPosTotCount = acm.Sheet.Column().GetCreatorTemplate(
                'Position Total Count', 'Standard').CreateCreator()
        colCreators.Add(ccPosTotCount)
        ccTrdCount = acm.Sheet.Column().GetCreatorTemplate(
                'Trade Count', 'Standard').CreateCreator()
        colCreators.Add(ccTrdCount)
        histPriceCount = acm.Sheet.Column().GetCreatorTemplate(
                'Position Historical Price Count', 'Standard').CreateCreator()
        colCreators.Add(histPriceCount)
        livePriceCount = acm.Sheet.Column().GetCreatorTemplate(
                'Position Live Price Count', 'Standard').CreateCreator()
        colCreators.Add(livePriceCount)

    def display(self, uiData):

        self.configTab.display(uiData)
        self.resultTab.display(uiData)
        self.chartPie.display(uiData)
        self.chart2d.display(uiData)
        self.menuItems.display(uiData)

    def SetView(self, viewType):

        pgNum = self.m_tabControl.GetActivePage()
        if pgNum == PORT_SHEET_PG_INDEX and self.m_selectedItem:
            self.m_mode = SHEET_SELECTION_MODE
            self.uiModel.switchViewOnPortSheet(viewType, self.m_selectedItem,
                    self.display)
        else:
            self.m_mode = CONFIG_MODE
            self.uiModel.switchViewOnConfig(viewType, self.display)

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.AddPieChart('chartPie', 400, 300)
        b.Add2DChart('chart2d', 400, 300)
        b.EndBox()
        return b
