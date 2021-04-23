""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerApplication.py"
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerApplication

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    An appication used to view portfolios or clients and depots, and the
    conditions that apply to these items.

-----------------------------------------------------------------------------"""

import FUxCore
import acm
import PortfolioViewerDialogs
import PortfolioViewerFunctions as functions
import PortfolioViewerConditionsDlg as ConditionalFunctions
from PortfolioViewerMenuItems import MenuItems
from PortfolioViewerMenuItems import TypeMenuItems
from PortfolioViewerDockedPane import FilterPanel

""" ---------------------- Start-up functions ---------------------- """
def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0)

def ReallyStartApplication(shell, count):
    """ Start the application in the session manager. """
    acm.UX().SessionManager().StartApplication('Portfolio Viewer', None)

def CreateApplicationInstance():
    return portfolioViewerApplication()

#Default settings for the Portfolio Viewer
def CreateDefaultSettings():
    dictionary = acm.FDictionary()
    dictionary.AtPut('defDataType', 'Portfolio')
    dictionary.AtPut('saveColumnSelections', True)
    dictionary.AtPut('prfViewCol', ['Name', 'Currency', 'Update Time'])
    dictionary.AtPut('depViewCol', ['Name', 'UpdateTime', 'Parent', 'Alias'])
    dictionary.AtPut('clntViewCol', ['Name', 'UpdateTime', 'Alias', 'FIX'])
    dictionary.AtPut('ptyTreeCol', ['Name', 'UpdateTime', 'Alias'])
    dictionary.AtPut('conditionColumnsPrf', ['Type', 'Value', 'Currency', '#Portfolios', 'Priority', 'Portfolio', 'Portfolio Filter', 'Instrument', 'Instrument Filter'])
    dictionary.AtPut('conditionColumnsDepClnt', ['Type', 'Value', 'Currency', '#Depots', 'Priority', 'Depot', 'Client', 'Client Group'])
    dictionary.AtPut('useConditionColumns', 'conditionColumnsPrf') #Which type of condition columns to use.
    dictionary.AtPut('modelCategories', ['AMS Limits', 'Collateral', 'Margin'])
    dictionary.AtPut('loadRange', 250)
    dictionary.AtPut('showListGridlines', False)
    dictionary.AtPut('showDepotTreeExpanded', True)
    dictionary.AtPut('depWithoutParentTree', False)
    dictionary.AtPut('useSlopeInSearch', False)
    dictionary.AtPut('showCurrentConditions', True)
    dictionary.AtPut('fillConditionsAutomatically', True)
    return dictionary

""" ------------------------------------- The Portfolio Viewer application class -------------------------------------"""
class portfolioViewerApplication(FUxCore.LayoutApplication):
    """ The application class for the Portfolio Viewer. """
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.filterPanel = None #Panel with portfolio or depot filters
        self.matchedItems = None
        self.numberOfMatchedItems = 0
        self.nextItem = 0
        self.matchedClients = None
        self.numberOfMatchedClients = 0
        self.nextClient = 0
        self.skippedDepots = 0
        self.filteredConditions = None
        self.partiesSelected = None
        self.insSelected = None
        self.addInfoNode = None
        self.condition_array = acm.FArray()
        self.currentPtyType = 'Depot'
        self.userSettings = CreateDefaultSettings()
        self.defaultSettings = CreateDefaultSettings()
        self.panelInstantiated = False
    
    def CreateCommandCB(self):
        """ Create a command item of class MenuItems. """
        mItems = MenuItems()
        mItems.SetApplication(self)
        return mItems

    def CreatePortfolioTypeCommand(self):
        """ Create a command item of class TypeMenuItems and mark as 
            checked if Portfolio is current type. """
        mItem = TypeMenuItems()
        mItem.SetApplication(self)
        if self.userSettings.At('defDataType') == 'Portfolio':
            mItem.checked = True
        return mItem

    def CreateDepotTypeCommand(self):
        """ Create a command item of class TypeMenuItems and mark as 
            checked if Depot is current type. """
        mItem = TypeMenuItems()
        mItem.SetApplication(self)
        if self.userSettings.At('defDataType') == 'Depot':
            mItem.checked = True
        return mItem

    def DoChangeCreateParameters(self, createParams):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(True)
        createParams.LimitMinSize(False)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)

    def HandleCanStoreLayout(self):
        return True

    def GetApplicationIcon(self):
        return "AdminConsole"

    def GetActiveItem(self):
        if self.userSettings.At('defDataType') == 'Portfolio' and self.prfView.GetSelectedItem():
            return self.prfView.GetSelectedItem().GetData()
        elif self.userSettings.At('defDataType') == 'Depot':
            if self.tabs.GetActivePage() == 0 and self.depView.GetSelectedItem():
                return self.depView.GetSelectedItem().GetData()
            elif self.tabs.GetActivePage() == 1 and self.clntView.GetSelectedItem():
                return self.clntView.GetSelectedItem().GetData()
            elif self.tabs.GetActivePage() == 2 and self.depTree.GetSelectedItem():
                return self.depTree.GetSelectedItem().GetData()
        return None #Nothing selected

    def GetActiveDataType(self):
        if self.userSettings.At('defDataType') == 'Portfolio':
            return 'Portfolio'
        elif self.userSettings.At('defDataType') == 'Depot':
            if self.tabs.GetActivePage() == 0:
                return 'Depot'
            elif self.tabs.GetActivePage() == 1:
                return 'Client'
            elif self.tabs.GetActivePage() == 2:
                if self.depTree.GetSelectedItem() and self.depTree.GetSelectedItem().GetData():
                    return self.depTree.GetSelectedItem().GetData().Type()

    """ Right click context menu for the portfolio, depot and client lists. """
    @FUxCore.aux_cb
    def ListContextMenuCB(self, ud, cd): 
        menuBuilder = cd.At("menuBuilder")
        items = cd.At("items")
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        if self.userSettings.At("defDataType") == "Portfolio":
            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, True, self.AddContextItemsPortfolio, None)
        elif self.userSettings.At("defDataType") == "Depot":
            acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, True, self.AddCustomContextItemsParty, None)
            
    def AddContextItemsPortfolio(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        selItem = self.prfView.GetSelectedItem()
        if selItem == None:
            return
        prf = selItem.GetData()
        commands = acm.FArray()
        commands.Add(['openPortfolio', '', 'Open Portfolio', '', '', '', self.CreateCommandCB, True])
        commands.Add(['copyConditions', '', 'Copy conditions to...', '', '', '', self.CreateCommandCB, False])
        if prf.Compound():
            commands.Add(['setCompoundNode', '', 'Set as Compound Portfolio', '', '', '', self.CreateCommandCB, False])
        if not self.userSettings.At("fillConditionsAutomatically"):
            commands.Add(['showConditions', '', 'Show conditions for portfolio', '', '', '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def AddCustomContextItemsParty(self, ud, cd):
        if self.tabs.GetActivePage() == 0:
            selItem = self.depView.GetSelectedItem()
        elif self.tabs.GetActivePage() == 1:
            selItem = self.clntView.GetSelectedItem()
        if selItem == None:
            return
        item = selItem.GetData()

        menuBuilder = cd.At('menuBuilder')
        commands = acm.FArray()
        if self.tabs.GetActivePage() == 0 and not self.userSettings.At("fillConditionsAutomatically"):
            commands.Add(['showConditions', '', 'Show conditions for depot', '', '', '', self.CreateCommandCB, False])
        elif self.tabs.GetActivePage() == 1:
            commands.Add(['newDepotWParent', '', 'Create new depot', '', '', '', self.CreateCommandCB, False])
            qry = acm.CreateFASQLQuery(acm.FPartyGroupLink, 'AND')
            qry.AddAttrNode('PartyGroup.GroupType', 'EQUAL', 'Client Group')
            qry.AddAttrNode('Party.Id', 'EQUAL', item.Id())
            if qry.Select().Size()>0:
                clientGroups = acm.FArray()
                for link in qry.Select():
                    clientGroups.Add(['ClientGroups', '', 'Client Groups/%s'%link.PartyGroup().Name(), link.PartyGroup().Name(), '', '', self.CreateCommandCB, False])
                commands.AddAll(clientGroups)
        commands.Add(['copyConditions', '', 'Copy conditions to...', '', '', '', self.CreateCommandCB, False])
        
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    """ Right click context menu for Condition and Condition Models tree"""
    @FUxCore.aux_cb
    def TreeContextMenuCB(self, ud, cd):
        useDelete = False
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            if not item.GetData(): #Categories have no data - don't show context menu.
                return  None
            if item.GetData().RecordType() == 'Condition':
                useDelete = True
            objects.Add(item.GetData())
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, useDelete, self.AddTreeCustomContextItemsCB, None)

    def AddTreeCustomContextItemsCB(self, ud, cd):
        selectedItem = self.treeView.GetSelectedItem()
        if selectedItem == None or selectedItem.GetData() == None:
            return
        
        menuBuilder = cd.At('menuBuilder')
        commands = acm.FArray()
        if selectedItem.GetData().RecordType() == "ConditionalValueModel":
            commands.Add(['openInAdminConsole', '', 'Open in Admin Console', '', '', '', self.CreateCommandCB, True])
            if functions.IsBrokerageRiskModel(selectedItem.GetData()): #Supports creation of Brokerage Risk conditional model conditions.
                name = selectedItem.GetData().Name()
                if self.userSettings.At('defDataType') == 'Portfolio':
                    commands.Add(['newPrfCondition', '', 'Create new %s condition for the selected portfolio'%name, '', '', '', self.CreateCommandCB, False])
                elif self.userSettings.At('defDataType') == 'Depot':
                    commands.Add(['newDepCondition', '', 'Create new %s condition for the selected party'%(name), '', '', '', self.CreateCommandCB, False])
                commands.Add(['newCondforModel', '', 'Create new %s condition'%name, '', '', '', self.CreateCommandCB, False])
        elif selectedItem.GetData().RecordType() == 'Condition':
            commands.Add(['openSelCondition', '', 'Edit condition', '', '', '', self.CreateCommandCB, True])
            commands.Add(['openInAdminConsole', '', 'Open in Admin Console', '', '', '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    """ Right click context menu for condition overview tree """
    @FUxCore.aux_cb
    def ConditionOverviewContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, None, True, self.CustomConditionOverviewContextMenu, None)

    def CustomConditionOverviewContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        selItem = self.conditionOverviewTree.GetSelectedItem()
        if selItem and selItem.GetData():
            item = selItem.GetData()
            commands = acm.FArray()
            q = acm.CreateFASQLQuery('FConditionalValueModel', 'AND')
            q.AddAttrNode('ModelCategory', 'EQUAL', 'AMS Limits')
            for model in q.Select():
                conditionFound = False 
                params = acm.FConditionParameters()
                if item.RecordType() == 'Portfolio':
                    params.Portfolio(item)
                elif item.Type() == 'Client':
                    params.Client(item)
                elif item.Type() == 'Depot':
                    params.Depot(item)
                #Instrument options?
                for condition in model.Conditions().SortByProperty('Priority'):
                    if functions.MatchesCondition(condition, params, self.userSettings.At('showCurrentConditions')):
                        conditionFound = True 
                        break
                if conditionFound:       
                    commands.Add(['overviewModelsUpdateCondition', '', 'Update Matched Condition for/%s'%model.Name(), model.Name(), '', '', self.CreateCommandCB, False])
                commands.Add(['overviewModelsSpecialCondition', '', 'New %s Condition for/%s'%(item.Name(), model.Name()), model.Name(), '', '', self.CreateCommandCB, False])
                commands.Add(['overviewModelsDefaultCondition', '', 'New Condition for/%s'%(model.Name()), model.Name(), '', '', self.CreateCommandCB, False])

            menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    """ Right click context menu for client/depot tree """
    @FUxCore.aux_cb
    def DepotTreeContextMenu(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, True, self.AddDepotTreeContextItems, None)

    def AddDepotTreeContextItems(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        selectedItem = self.depTree.GetSelectedItem()
        if selectedItem == None or selectedItem.GetData() == None:
            return
        pty = selectedItem.GetData()
        commands = acm.FArray()
        if pty.Type() == 'Depot':
            if not self.userSettings.At('fillConditionsAutomatically'):
                commands.Add(['showConditions', '', 'Show conditions for depot', '', '', '', self.CreateCommandCB, False])
        elif pty.Type() == 'Client': #Display and open party groups for client
            commands.Add(['newDepotWParent', '', 'Create new depot', '', '', '', self.CreateCommandCB, False])
            qry = acm.CreateFASQLQuery(acm.FPartyGroupLink, 'AND')
            qry.AddAttrNode('PartyGroup.GroupType', 'EQUAL', 'Client Group')
            qry.AddAttrNode('Party.Id', 'EQUAL', pty.Id())
            if qry.Select().Size()>0:
                clientGroups = acm.FArray()
                for link in qry.Select():
                    clientGroups.Add(['ClientGroups', '', 'Client Groups/%s'%link.PartyGroup().Name(), link.PartyGroup().Name(), '', '', self.CreateCommandCB, False])
                commands.AddAll(clientGroups)
        
        commands.Add(['copyConditions', '', 'Copy conditions to...', '', '', '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    """ Ribbon commands """
    def HandleRegisterCommands(self, builder):
        commands = [
            ['ClearFields', 'View', 'Clear Fields',      '', '', '', self.CreateCommandCB, False],\
            ['DoSearch',    'View', 'Search',            '', '', '', self.CreateCommandCB, False],\
            ['CondModels',  'View', 'Conditional Models', '', '', '', self.CreateCommandCB, False],\
            ['NewPortfolio', 'View', 'Create new',        '', '', '', self.CreateCommandCB, False],\
            ['Columns',     'View', 'Column Selection',  '', '', '', self.CreateCommandCB, False],\
            ['ViewSettings', 'View', 'View Settings',     '', '', '', self.CreateCommandCB, False],\
            ['DataType',    'View', 'Type Shown',        '', '', '', self.CreateCommandCB, False]]
        fileCommands = acm.FSet()
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)
        builder.RegisterDynamicCommand('Columns', False, True, self.DynamicMenuCB, self)
        builder.RegisterDynamicCommand('NewPortfolio', False, True, self.DynamicMenuCreateNewCB, self)
        builder.RegisterDynamicCommand('DataType', False, False, self.DynamicTypeSwitch, self)

    def DynamicMenuCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        label = self.userSettings.At('defDataType') + ' columns'
        commands = acm.FArray()
        commands.Add(['columnSelection_list', '', label, '', '', '', self.CreateCommandCB, False])
        if self.userSettings.At('defDataType') == "Depot":
            commands.Add(['columnsSelection_clnt', '', 'Client columns', '', '', '', self.CreateCommandCB, False])
        commands.Add(['columnSelection_cond', '', 'Condition columns', '', '', '', self.CreateCommandCB, False])
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands)) 

    def DynamicMenuCreateNewCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        label = self.userSettings.At('defDataType')
        if self.userSettings.At('defDataType') == 'Depot':
            label = 'Party (with Party Definition)'
        commands = [
            ['new_prfOrDepot', '', label, '', '', '', self.CreateCommandCB, False],
            ['new_condition', '', 'Condition', '', '', '', self.CreateCommandCB, False]
        ]
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def DynamicTypeSwitch(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = [
            ['use_Portfolio', '', 'Portfolio', '', '', '', self.CreatePortfolioTypeCommand, False],
            ['use_Depot', '', 'Depot', '', '', '', self.CreateDepotTypeCommand, False]
        ]
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
    
    def HandleCreate(self, creationContext):
        #Adds the filter panel to the application
        self.filterPanel = FilterPanel()
        self.filterPanel.SetParent(self)
        self.Frame().CreateCustomDockWindow(self.filterPanel, 'filters', 'Search Fields', 'Left')
        
        #TabControl (possible to remove and add pages to)
        self.tabs = creationContext.AddTabControlPane('Pane')
        
        #Build and control portfolio list
        functions.AddPortfolioTabs(self)

        """ Conditions """
        self.conditionTabs = creationContext.AddTabControlPane('ConditionsPane')

        """ Normal conditions view """
        layout = self.conditionTabs.AddLayoutPage(functions.buildConditionLayout(), "Detailed View")
        # Instrument filter on commissions
        self.insFilter = layout.GetControl('Instrument')
        self.insFilter.AddCallback('Activate', functions.UpdateConditionalModels, self)
        self.insFilter.Editable(False)
        self.openInsertIns = layout.GetControl('OpenInsertInstrument')
        self.clearIns = layout.GetControl('ClearInstrument')
        self.openInsertIns.AddCallback('Activate', functions.StartInsertInstrument, self)
        self.clearIns.AddCallback('Activate', functions.ClearInstrument, self)

        # Tree view for conditional models
        self.treeView = layout.GetControl('TreeView')
        self.treeView.ShowColumnHeaders()
        self.treeView.AddCallback("ContextMenu", self.TreeContextMenuCB, None)
        self.treeView.AddCallback("DefaultAction", functions.OpenConditionCustom, self)
        self.treeView.ColumnLabel(0, 'Name')
        self.treeView.ColumnWidth(0, 220)

        for col in range(0, 30):
            self.treeView.AddColumn(str(col), 0)
        
        for i in range(0, len(self.userSettings.At('conditionColumnsPrf'))): #Redraw selected columns
            self.treeView.ColumnLabel((i+1), self.userSettings.At('conditionColumnsPrf')[i])
            self.treeView.ColumnWidth((i+1), 50)

        """ Condition overview"""
        layout = self.conditionTabs.AddLayoutPage(functions.buildConditionOverviewLayout(), "Overview")
        self.overviewInsFilter = layout.GetControl('Instrument')
        self.overviewInsFilter.AddCallback('Activate', functions.UpdateConditionalModels, self)
        self.overviewInsFilter.Editable(False)
        self.overviewInsertIns = layout.GetControl('OpenInsertInstrument')
        self.overviewInsertIns.AddCallback('Activate', functions.StartInsertInstrument, self)
        self.overviewClearIns = layout.GetControl('ClearInstrument')
        self.overviewClearIns.AddCallback('Activate', functions.ClearInstrument, self)

        self.conditionOverviewTree = layout.GetControl('TreeView')
        self.conditionOverviewTree.ShowColumnHeaders()
        self.conditionOverviewTree.AddCallback("ContextMenu", self.ConditionOverviewContextMenu, None)
        self.conditionOverviewTree.AddCallback("DefaultAction", functions.ShowDetailsForItem, self)
        self.conditionOverviewTree.ColumnLabel(0, 'Name')
        self.conditionOverviewTree.ColumnWidth(0, 150)

        qry = acm.CreateFASQLQuery('FConditionalValueModel', 'AND')
        qry.AddAttrNode('ModelCategory', 'EQUAL', 'AMS Limits')
        for model in qry.Select():
            self.conditionOverviewTree.AddColumn(model.Name(), 100)

        """ End of condition view initialisation. """
        self.matchedItems = acm.FArray()
        qry = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND') 
        self.matchedItems.AddAll(qry.Select()) 
        self.numberOfMatchedItems = self.matchedItems.Size()

        #Make sure correct fields are visible (if panel has been created)
        functions.ShowFields(self, False, self.panelInstantiated)
        """ Fill with data """
        functions.LoadFilteredPortfolios(self, None)
        for col in range(0, len(self.userSettings.At('prfViewCol'))):
            self.prfView.AdjustColumnWidthToFitItems(col)

    def HandleSaveLayout(self, contents):
        contents.AtPut('defaultType', self.userSettings.At('defDataType'))
        contents.AtPut('loadRange', self.userSettings.At('loadRange'))
        contents.AtPut('modelCategories', self.userSettings.At('modelCategories'))
        contents.AtPut('currentConditionsOnly', self.userSettings.At('showCurrentConditions'))
        contents.AtPut('fillConditionsAutomatically', self.userSettings.At('fillConditionsAutomatically'))
        contents.AtPut('showListGridlines', self.userSettings.At('showListGridlines'))
        contents.AtPut('depTreeExpanded', self.userSettings.At('showDepotTreeExpanded'))
        contents.AtPut('depWithoutParentTree', self.userSettings.At('depWithoutParentTree'))
        contents.AtPut('useSlopeInSearch', self.userSettings.At('useSlopeInSearch'))
        if self.userSettings.At('saveColumnSelections'):
            if contents.At('defaultType') == 'Portfolio':
                contents.AtPut('prfColSelection', self.userSettings.At('prfViewCol'))
            elif contents.At('defaultType') == 'Depot':
                contents.AtPut('depotColSelection', self.userSettings.At('depViewCol'))
                contents.AtPut('clntViewCol', self.userSettings.At('clntViewCol'))
            contents.AtPut('treeColumns', [self.userSettings.At('conditionColumnsPrf'), self.userSettings.At('conditionColumnsDepClnt')])

    def HandleLoadLayout(self, contents):
        if not contents or not contents.IsKindOf('FDictionary'):
            return
        if contents.At('loadRange'):
            self.userSettings.AtPut('loadRange', contents.At('loadRange'))
        if contents.At('modelCategories'):
            self.userSettings.AtPut('modelCategories', contents.At('modelCategories'))
        if contents.At('currentConditionsOnly'):
            self.userSettings.AtPut('showCurrentConditions', contents.At('currentConditionsOnly'))
        if contents.At('fillConditionsAutomatically'):
            self.userSettings.AtPut('fillConditionsAutomatically', contents.At('fillConditionsAutomatically'))
        if contents.At('treeColumns'):
            self.userSettings.AtPut('conditionColumnsPrf', contents.At('treeColumns')[0])
            self.userSettings.AtPut('conditionColumnsDepClnt', contents.At('treeColumns')[1])
            functions.UpdateConditionColumns(self)
        if contents.At('showListGridlines'):
            self.userSettings.AtPut('showListGridlines', contents.At('showListGridlines'))
        if contents.At('depTreeExpanded'):
            self.userSettings.AtPut('showDepotTreeExpanded', contents.At('depTreeExpanded'))
        if contents.At('depWithoutParentTree'):
            self.userSettings.AtPut('depWithoutParentTree', contents.At('depWithoutParentTree'))
        if contents.At('useSlopeInSearch'):
            self.userSettings.AtPut('useSlopeInSearch', contents.At('useSlopeInSearch'))

        if contents.At('prfColSelection'): 
            self.userSettings.AtPut('prfViewCol', contents.At('prfColSelection'))
        elif contents.At('depotColSelection'):
            self.userSettings.AtPut('depViewCol', contents.At('depotColSelection'))
            if contents.At('clntViewCol'):
                self.userSettings.AtPut('clntViewCol', contents.At('clntViewCol'))
            ptyTreeColumns = self.userSettings.At('clntViewCol').Clone()
            for col in self.userSettings.At('depViewCol'):
                if col not in ptyTreeColumns:
                    ptyTreeColumns.Add(col)
            self.userSettings.AtPut('ptyTreeCol', ptyTreeColumns)
        else:
            self.userSettings.AtPut('saveColumnSelections', False)

        if contents.At('defaultType'):
            t = contents.At('defaultType')
            self.userSettings.AtPut('defDataType', t)
            if t == 'Portfolio':
                functions.ShowFields(self, False, True)
                functions.UpdatePortfolioColumns(self)
                self.nextItem = 0
                functions.LoadFilteredPortfolios(self, None)
                for i in range(0, self.prfView.ColumnCount()):
                    self.prfView.AdjustColumnWidthToFitItems(i)

                self.prfView.ShowGridLines(self.userSettings.At('showListGridlines'))
            elif t == 'Depot':
                functions.ChangeType(self, None, False)

""" End of file """
