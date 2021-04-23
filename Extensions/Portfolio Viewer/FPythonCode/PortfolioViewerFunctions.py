""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerFunctions.py"
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerFunctions

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
	The functions used by the Portfolio Viewer application.
-----------------------------------------------------------------------------"""

import FUxCore
import acm
import PortfolioViewerDialogs
import PortfolioViewerSettings
import PortfolioViewerConditionsDlg as ConditionalFunctions

""" --------------------------------------------------------------------- """
""" ---------------------- MISCELLANEOUS FUNCTIONS ---------------------- """
""" --------------------------------------------------------------------- """
def clearAllFields(application):
    """ A function that clears all fields to enable a new search. """
    for f in application.commonFields:
        f.SetData('')
    for f in application.portfolioInputFields:
        f.SetData('')
    for f in application.depotInputFields:
        f.SetData('')

    application.insFilter.SetData('')
    application.overviewInsFilter.SetData('')
    if application.userSettings.At('defDataType') == 'Depot':
        application.depOrClntCtrl.SetData('Depot')
        ClientDepotSwitch(application, None)
    application.aliasNameCtrl.Enabled(False)
    application.comSlopeCtrl.Enabled(False)
    application.comShrSlopeCtrl.Enabled(False)

    application.partiesSelected = None
    application.insSelected = None
    application.addInfoNode = None

def CommonSearch(application, cd):
    if application.userSettings.At('defDataType') == 'Portfolio':
        PortfolioSearch(application, None)
    elif application.userSettings.At('defDataType') == 'Depot':
        PartySearch(application, None)

def EnableAliasField(application, _):
    aType = application.aliasTypeCtrl.GetData()
    if aType == '':
        application.aliasNameCtrl.Enabled(False)
    else:
        application.aliasNameCtrl.Enabled(True)

def DepotParentOptionSwitch(application, _):
    opt = application.depParentOptionCtrl.GetData()
    showFlds = False
    if opt == '' or opt == "With parent":
        showFlds = True
    application.depParentCtrl.Enabled(showFlds)
    application.openInsClientBtn.Enabled(showFlds)
    application.clearClientBtn.Enabled(showFlds)

def CommissionSearchFieldsSwitch((application, chargesType), _):
    if chargesType == "Commission":
        if application.comCtrl.GetData() == "Commission condition for depot exists. Curve slope:":
            application.comSlopeCtrl.Enabled(True)
        else:
            application.comSlopeCtrl.Enabled(False)
    elif chargesType == "Commission Sharing":
        if application.comShrCtrl.GetData() == "Commission sharing condition for depot exists. Curve slope:":
            application.comShrSlopeCtrl.Enabled(True)
        else:
            application.comShrSlopeCtrl.Enabled(False)

def IsBrokerageRiskModel(model):
    """ Returns true if the model's category belongs to the Brokerage Risk top category. """
    if model.ModelCategory() == 'AMS Limits' or model.ModelCategory() == 'Collateral' or model.ModelCategory() == 'Margin':
        return True
    return False

def FixFormat(numberInput):
    """ Enter an integer, and it will be returned with spaces inserted at every three digits """
    if type(numberInput) == 'String':
        return numberInput
    s = str(numberInput)
    res = ''
    if "." in s:
        subs = s.split('.')
        s = subs[0]
        res = '.'+ subs[1]
    if len(s) < 3:
        return s+res
    elif len(s) % 3 == 0:
        return ' '.join([s[i:i+3] for i in range(0, len(s), 3)])+ res
    elif len(s) % 3 == 1:
        return s[:1]+' '+ ' '.join([s[i:i+3] for i in range(1, len(s), 3)])+ res
    #len(s) % 3 == 2
    return s[:2]+' '+ ' '.join([s[i:i+3] for i in range(2, len(s), 3)])+ res

def ParameterFromName(name):
	""" Get the FParameter extension with a given name. """
	return acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, name) 

def ColumnSelection(application, dataType):
    """ Open the Portfolio Viewer dialog for column selection and update GUI """
    columns = []
    usedColumns = []
    if dataType == "Portfolio":
        settingsName = "prfViewCol"
        allColumns = ['Assignment Info', 'Currency', 'Type', 'Position Pair', 'Owner', 'Update Time']
        #Additional Info columns
        for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
            allColumns.append(addInfo.Name())
        for column in allColumns: #Add column to available columns if not current
            if not column in application.userSettings.At('prfViewCol'):
                columns.append(column)
    elif dataType == "Depot":
        settingsName = "depViewCol"
        allColumns = ["UpdateTime", "Alias", "Parent", "AimsEntity", "Profit/Loss", "Shaping", "Warehouse", "Default depot"]
        for addInfo in acm.FDepot().AddInfoSpecs():
            allColumns.append(addInfo.Name())
        for aliasType in acm.FPartyAliasType.Select(''):
            allColumns.append(aliasType.Name())
        for column in allColumns: #Add column to available columns if not current
            if not column in application.userSettings.At('depViewCol'): #Use two types? depotCol and portfolioCol? 
                columns.append(column)
    elif dataType == "Client":
        settingsName = 'clntViewCol'
        allColumns = ["UpdateTime", "Alias", "FIX"]
        for addInfo in acm.FClient().AddInfoSpecs():
            allColumns.append(addInfo.Name())
        for aliasType in acm.FPartyAliasType.Select(''):
            allColumns.append(aliasType.Name())
        for column in allColumns: #Add column to available columns if not current
            if not column in application.userSettings.At('clntViewCol'): #Use two types? depotCol and portfolioCol? 
                columns.append(column)
    elif dataType == 'Condition':
        settingsName = application.userSettings.At('useConditionColumns')
        allColumns = ['Currency', 'Value', 'Type', '#Portfolios', '#Depots', 'Priority', 'Mkt Group', 'Market', 'Market Segment',\
                      'Instrument', 'Client Group', 'Client', 'Counterparty Group', 'Counterparty', 'Broker Group',\
                      'Broker', 'Depot', 'Account', 'Portfolio', 'Exec type', 'Buy/Sell', 'Instrument Type', 'Paytype',\
                      'Underlying Instrument Type', 'Instrument Filter', 'Portfolio Filter', 'Curve Name',\
                      'Calculation Mode', 'Minimum Value', 'Curve Slope', 'Curve Type']
        for column in allColumns: #Add column to available columns if not current
            if not column in application.userSettings.At(application.userSettings.At('useConditionColumns')):
                columns.append(column)

    if PortfolioViewerSettings.StartColumnSelection(application, columns, settingsName, dataType): #Selection saved
        if dataType == 'Portfolio': #Portfolio
            UpdatePortfolioColumns(application)
            application.addMoreListItems.Editable(True)
            application.nextItem = 0
            LoadFilteredPortfolios(application, None) #Reload items in list. 
            for i in range(0, application.prfView.ColumnCount()):
                application.prfView.AdjustColumnWidthToFitItems(i)
        elif dataType == 'Depot' or dataType == 'Client':
            application.t_addMoreDep.Editable(True)
            ptyTreeColumns = application.userSettings.At('clntViewCol').Clone()
            for col in application.userSettings.At('depViewCol'):
                if col not in ptyTreeColumns:
                    ptyTreeColumns.Add(col)
            application.userSettings.AtPut('ptyTreeCol', ptyTreeColumns)
            if dataType == 'Depot':
                UpdateDepotColumns(application)
                application.addMoreDep.Editable(True)
                application.nextItem = 0
                LoadFilteredDepots(application, None)
                for i in range(0, application.depView.ColumnCount()):
                    application.depView.AdjustColumnWidthToFitItems(i)
            else: #Client
                UpdateClientColumns(application)
                application.addMoreClnt.Editable(True)
                application.nextClient = 0
                LoadFilteredClients(application, None)
                for i in range(0, application.clntView.ColumnCount()):
                    application.clntView.AdjustColumnWidthToFitItems(i)
        elif dataType == 'Condition': 
            UpdateConditionColumns(application)

def OpenSettings(application):
    dType = application.userSettings.At('defDataType')
    modTypes = application.userSettings.At('modelCategories')
    showCurrCon = application.userSettings.At('showCurrentConditions')
    showingAllInTree = application.userSettings.At('depWithoutParentTree')
    if PortfolioViewerSettings.StartViewSettingsDialog(application): #Returns true when saving
        if dType != application.userSettings.At('defDataType'): #Value changed
            ChangeType(application, None)
        elif dType == 'Portfolio': #Not changed - is still portfolio
            application.prfView.ShowGridLines(application.userSettings.At('showListGridlines'))
        elif dType == 'Depot': #Not changed - is still depot
            application.depView.ShowGridLines(application.userSettings.At('showListGridlines'))
            application.comCtrl.Visible(application.userSettings.At('useSlopeInSearch'))
            application.comSlopeCtrl.Visible(application.userSettings.At('useSlopeInSearch'))
            application.comShrCtrl.Visible(application.userSettings.At('useSlopeInSearch'))
            application.comShrSlopeCtrl.Visible(application.userSettings.At('useSlopeInSearch'))
            if (showingAllInTree != application.userSettings.At('depWithoutParentTree')):
                application.depTree.Clear()
                application.depView.Clear()
                application.nextItem = 0
                application.skippedDepots = 0
                LoadFilteredDepots(application, None)
        if set(modTypes) != set(application.userSettings.At('modelCategories')) or showCurrCon != application.userSettings.At('showCurrentConditions'): #Value changed
            UpdateConditionalModels(application, None) #Update tree with conditional models

""" ------------------------------------------------------------------------- """
""" ----------------------------- UPDATE COLUMNS ---------------------------- """
""" ------------------------------------------------------------------------- """
def UpdatePortfolioColumns(application):
    application.prfView.Clear()
    for i in range(application.prfView.ColumnCount()-1, -1, -1):
        application.prfView.RemoveColumn(i)
    for col in application.userSettings.At('prfViewCol'):
        application.prfView.AddColumn(col)

def UpdateDepotColumns(application):
    application.depView.Clear()
    for i in range(application.depView.ColumnCount()-1, -1, -1): #Remove backwards to avoid index changes
        application.depView.RemoveColumn(i)
    for col in application.userSettings.At('depViewCol'):
        application.depView.AddColumn(col)
    UpdatePartyTreeColumns(application)

def UpdateClientColumns(application):
    application.clntView.Clear()
    for i in range(application.clntView.ColumnCount()-1, -1, -1):
        application.clntView.RemoveColumn(i)
    for col in application.userSettings.At('clntViewCol'):
        application.clntView.AddColumn(col)
    UpdatePartyTreeColumns(application)

def UpdatePartyTreeColumns(application):
    application.depTree.Clear()
    for i in range (1, 29):
        application.depTree.ColumnWidth(i, 0)
    i = 0
    for col in application.userSettings.At('ptyTreeCol'):
        if col == 'Name':
            i += 1
            continue
        application.depTree.ColumnLabel(i, col)
        if col == 'Parent': #Do not display parent column in tree
            application.depTree.ColumnWidth(i, 0)
        else:
            application.depTree.ColumnWidth(i, 75)
        i+=1

def UpdateConditionColumns(application):
    for i in range(1, 29):
        application.treeView.ColumnWidth(i, 0) #Hide unused columns
    selCol = application.userSettings.At(application.userSettings.At('useConditionColumns'))
    for i in range(0, len(selCol)):
        application.treeView.ColumnLabel((i+1), selCol[i])
        if selCol[i] in ['Instrument', 'Portfolio']:
            application.treeView.ColumnWidth((i+1), 100)
        elif selCol[i] in ['Currency', 'Value', 'Priority']:
            application.treeView.ColumnWidth((i+1), 50)
        else: #Default width is 75
            application.treeView.ColumnWidth((i+1), 75)

    item = application.GetActiveItem() 
    if item:        
        application.treeView.Clear()
        FillTreeWithData(application, None)
        return

    #Fill with fake data to adjust columns (ForceRedraw works bad.)
    it = application.treeView.GetRootItem().AddChild()
    it.Label('updateList', 0)
    application.treeView.Clear()

""" ------------------------------------------------------------------------- """
""" ---------------------------LAYOUT BUILDERS ------------------------------ """
""" ------------------------------------------------------------------------- """
def buildPortfolioListLayout():
    builder = acm.FUxLayoutBuilder()
    builder.BeginVertBox('None')
    builder. BeginVertBox('Invisible')
    builder.  AddList('ListView', 13, -1, 50, -1)
    builder.  BeginHorzBox('None')
    builder.    AddButton('GetMorePortfolios', 'Show More Results', True, True)
    builder.    AddSpace(10)
    builder.    AddLabel('PortfoliosShown', 'Shows 1999999/1999999', -1, -1)
    builder.  EndBox()
    builder. EndBox()
    builder.EndBox()
    return builder

def buildDepotListLayout():
    builder = acm.FUxLayoutBuilder()
    builder. BeginVertBox('Invisible')
    builder.  AddList('DepotView', 13, -1, 50, -1)
    builder.  BeginHorzBox('None')
    builder.    AddButton('GetMoreDepots', 'Show More Results', True, True)
    builder.    AddSpace(10)
    builder.    AddLabel('DepotsShown', 'Shows 0/0 Depots. No search performed', -1, -1)
    builder.  EndBox()
    builder. EndBox()
    return builder

def buildClientListLayout():
    builder = acm.FUxLayoutBuilder()
    builder. BeginVertBox('Invisible')
    builder.  AddList('ClientView', 13, -1, 50, -1)
    builder.  BeginHorzBox('None')
    builder.    AddButton('GetMoreClients', 'Show More Results', True, True)
    builder.    AddSpace(10)
    builder.    AddLabel('ClientsShown', 'Shows 0/0 clients. No search performed', -1, -1)
    builder.  EndBox()
    builder. EndBox()
    return builder

def buildDepotTreeLayout():
    builder = acm.FUxLayoutBuilder()
    builder. BeginVertBox('Invisible')
    builder.  AddTree('DepotTree', 200, 75)
    builder.  BeginHorzBox('None')
    builder.    AddButton('GetMoreDepots', 'Show More Results', True, True)
    builder.    AddSpace(10)
    builder.    AddLabel('DepotsShown', 'Shows 1999999/1999999 depots', -1, -1)
    builder.  EndBox()
    builder. EndBox()
    return builder

def buildConditionLayout():
    builder = acm.FUxLayoutBuilder()
    builder.BeginVertBox('Invisible', 'Conditional Models')
    builder.  BeginHorzBox('None')
    builder.    AddInput('Instrument', 'Include Instrument')
    builder.    AddSpace(1)
    builder.    AddButton('OpenInsertInstrument', '...', 5, 5)
    builder.    AddButton('ClearInstrument', 'C', 5, 5)
    builder.  EndBox()
    """
    builder.  BeginHorzBox('None')
    builder.    AddInput('CurrencyCon','Include Currency')
    builder.    AddSpace(1)
    builder.    AddButton('OpenInsertCurr','...',5,5)
    builder.    AddButton('ClearCurr','C',5,5)
    builder.  EndBox()"""
    builder.  AddTree('TreeView', 200, 75)
    builder.EndBox()
    return builder

def buildConditionOverviewLayout():
    builder = acm.FUxLayoutBuilder()
    builder.BeginVertBox('Invisible', 'Conditional Models')
    builder.  BeginHorzBox('None')
    builder.    AddInput('Instrument', 'Include Instrument')
    builder.    AddSpace(1)
    builder.    AddButton('OpenInsertInstrument', '...', 5, 5)
    builder.    AddButton('ClearInstrument', 'C', 5, 5)
    builder.  EndBox()
    builder.  AddTree('TreeView', 200, 75)
    builder.EndBox()
    return builder

""" ------------------------------------------------------------------------- """
""" ------------------------- SWITCH TYPE FUNCTIONS ------------------------- """
""" ------------------------- (Portfolios / Depots) ------------------------- """
""" ----------------------------------- & ----------------------------------- """
""" --------------------------- (Clients / Depots) -------------------------- """
""" ------------------------------------------------------------------------- """
def ClientDepotSwitch(application, _):
    """ Class handling enabling and disabling of client/depot fields """
    opt = application.depOrClntCtrl.GetData()
    showDepotFlds = True
    if opt == "Client":
        showDepotFlds = False
        #application.tabs.SetPageLabel(0,"Clients")
        application.nameFld.Label('Client Name')
    elif opt == "Depot":
        showDepotFlds = True
        #application.tabs.SetPageLabel(0,"Depots")
        application.nameFld.Label('Depot Name')
    #Client fields
    application.clientHasDepotsCtrl.Visible(not showDepotFlds)
    application.fixClientCtrl.Visible(not showDepotFlds)
    #Depot fields
    for fld in [application.unknownDepotCtrl, application.pnlDepotCtrl, application.warehouseDepCtrl, application.shpDepotCtrl]:
        fld.Visible(showDepotFlds)
    application.depParentOptionCtrl.Visible(showDepotFlds)
    application.depParentCtrl.Visible(showDepotFlds)
    application.openInsClientBtn.Visible(showDepotFlds)
    application.clearClientBtn.Visible(showDepotFlds)
    if not application.userSettings.At('useSlopeInSearch'):
        showDepotFlds = False
    application.comCtrl.Visible(showDepotFlds)
    application.comSlopeCtrl.Visible(showDepotFlds)
    application.comShrCtrl.Visible(showDepotFlds)
    application.comShrSlopeCtrl.Visible(showDepotFlds)

def ChangeType(application,cd,clearFlds=True):
    if clearFlds:
        clearAllFields(application) #Since a new search is triggered all fields must be empty.
    if application.userSettings.At('defDataType') == 'Portfolio': #changed to portfolio
        #Reset client matched controls
        application.matchedClients = None
        application.numberOfMatchedClients = 0
        application.nextClient = 0

        AddPortfolioTabs(application)
        ShowFields(application, False)
        PortfolioSearch(application, cd)
        application.userSettings.AtPut('useConditionColumns', 'conditionColumnsPrf')
        UpdateConditionColumns(application)
    elif application.userSettings.At('defDataType') == 'Depot': #Changed to depot
        AddDepotTabs(application)
        ShowFields(application, True)
        ClientDepotSwitch(application, None) #Hide/Show Client/depot fields
        PartySearch(application, cd)
        application.userSettings.AtPut('useConditionColumns', 'conditionColumnsDepClnt')
        UpdateConditionColumns(application)
        if not clearFlds and application.depOrClntCtrl.GetData() == "Client": #Was set to client before
            application.addMoreDep.Editable(False)
        for i in range(0, application.depView.ColumnCount()):
            application.depView.AdjustColumnWidthToFitItems(i)

def AddDepotTabs(application):
    """ List View of Depots """
    application.tabs.RemoveAllPages()
    layout = application.tabs.AddLayoutPage(buildDepotListLayout(), "Depots")
    application.depView = layout.GetControl('DepotView')
    application.depView.EnableHeaderSorting()
    application.depView.AddCallback("SelectionChanged", LoadConditionalModels, application)
    application.depView.AddCallback("ContextMenu", application.ListContextMenuCB, None) 
    application.depView.AddCallback("DefaultAction", OpenParty, application)
    application.depView.ShowColumnHeaders()
    application.depView.ShowGridLines(application.userSettings.At('showListGridlines'))
    
    application.addMoreDep = layout.GetControl("GetMoreDepots")
    application.addMoreDep.AddCallback("Activate", LoadFilteredDepots, application)
    application.addedDepots = layout.GetControl("DepotsShown")
    
    """ CLIENT TAB """
    layout = application.tabs.AddLayoutPage(buildClientListLayout(), "Clients")
    application.clntView = layout.GetControl("ClientView")
    application.clntView.EnableHeaderSorting()
    application.clntView.AddCallback("SelectionChanged", LoadConditionalModels, application)
    application.clntView.AddCallback("ContextMenu", application.ListContextMenuCB, None)
    application.clntView.AddCallback("DefaultAction", OpenParty, application)
    application.clntView.ShowColumnHeaders()
    application.clntView.ShowGridLines(application.userSettings.At('showListGridlines'))

    application.addMoreClnt = layout.GetControl("GetMoreClients")
    application.addMoreClnt.AddCallback("Activate", LoadFilteredClients, application)
    application.addedClients = layout.GetControl("ClientsShown")

    """ TREE TAB """
    layout = application.tabs.AddLayoutPage(buildDepotTreeLayout(), "Tree View")
    application.depTree = layout.GetControl('DepotTree')
    application.depTree.ColumnLabel(0, 'Name')
    application.depTree.ColumnWidth(0, 125)
    application.depTree.AddCallback("SelectionChanged", LoadConditionalModels, application)
    application.depTree.AddCallback('ContextMenu', application.DepotTreeContextMenu, application)
    application.depTree.AddCallback("DefaultAction", OpenParty, application)
    application.depTree.ShowColumnHeaders()
    for col in range(0, 30): #All columns
        application.depTree.AddColumn(str(col), 0)

    application.t_addMoreDep = layout.GetControl("GetMoreDepots")
    application.t_addMoreDep.AddCallback("Activate", LoadFilteredParties, application)
    application.t_addedDepots = layout.GetControl("DepotsShown")

    UpdateDepotColumns(application)
    UpdateClientColumns(application)
    application.addMoreClnt.Editable(False)
    application.addedClients.Label('Shows 0/0. No Search Performed')

def AddPortfolioTabs(application):
    application.tabs.RemoveAllPages()
    layout = application.tabs.AddLayoutPage(buildPortfolioListLayout(), "Portfolios")
    application.prfView = layout.GetControl('ListView')
    application.prfView.EnableHeaderSorting()
    application.prfView.AddCallback("SelectionChanged", LoadConditionalModels, application)
    application.prfView.AddCallback("ContextMenu", application.ListContextMenuCB, None)
    application.prfView.AddCallback("DefaultAction", OpenPortfolio, application)
    application.prfView.ShowColumnHeaders()
    application.prfView.ShowGridLines(application.userSettings.At('showListGridlines'))
    UpdatePortfolioColumns(application)

    application.addMoreListItems = layout.GetControl('GetMorePortfolios')
    application.addMoreListItems.AddCallback("Activate", LoadFilteredPortfolios, application)
    application.addedPortfolios = layout.GetControl('PortfoliosShown')

def ShowFields(application,isDepot,instantiated=True):
    """ Makes the needed fields visible  (if they have been added to the 
        application yet (HandleLoadLayout 'bug') """
    if instantiated:
        for field in application.portfolioInputFields:
            field.Visible(not isDepot)
        application.openInsertParties.Visible(not isDepot)
        application.clearParties.Visible(not isDepot)
        application.openInsertCompoundPrtf.Visible(not isDepot)
        application.clearCompPrtf.Visible(not isDepot)

        if isDepot:
            application.nameFld.Label('Depot Name')
        else:
            application.nameFld.Label('Portfolio Name')

        for field in application.depotInputFields:
            field.Visible(isDepot)

""" ----------------------------------------------------------------------------- """
""" ------------------------ OPEN / CREATE NEW FUNCTIONS ------------------------ """
""" ----------------------------------------------------------------------------- """
def OpenPortfolio(application, cd):
    """ If a portfolio is double clicked, open it in the the custom portfolio dialog. """
    item = application.prfView.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    if PortfolioViewerDialogs.StartEditDialog(application, item.GetData()):
        AddItem(application, item.GetData(), item)

def OpenConditionCustom(application, cd):
    """ Open the condition in the custom dialog view or the admin console """
    item = application.treeView.GetSelectedItem()
    if not item or not item.GetData():
        return
    if cd or item.GetData().RecordType() != 'Condition': #Command = Open in Admin Console, or type is model
        acm.UX().SessionManager().StartApplication('Charges', item.GetData())
        return
    if ConditionalFunctions.OpenConditionDlg(application, item.GetData().Model(), item.GetData()):
        UpdateConditionalModels(application, None)

def OpenParty(application, cd):
    """ Open the Party Definition for double clicked entry. """
    item = application.GetActiveItem()
    if item == None or item.RecordType() != 'Party':
        return
    acm.UX().SessionManager().StartApplication('Party Definition', item)

def NewOverviewCondition(application, model):
    """ Create a new condition for item selected in the overview """
    if not application.conditionOverviewTree.GetSelectedItem():
        return

    item = application.conditionOverviewTree.GetSelectedItem().GetData()
    if not item: 
        return 
    if item.RecordType() == 'Portfolio':
        qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
        qry.AddAttrNode('Portfolio', 'EQUAL', True) #Should have portfolio selected!
        qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name()) #Correct model
        if qry.Select().Size() < 1: #No existing filter
            acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'Create new condition failed.\nThis model does not have a filter with portfolio enabled.')
            return
        return ConditionalFunctions.ShowNewPortfolioConditionDlg(application, model, item)
    elif item.RecordType() == 'Party' and item.Type() == 'Depot':
        qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
        qry.AddAttrNode('Depot', 'EQUAL', True) #Should have depot selected!
        qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name()) #Correct model
        if qry.Select().Size() < 1: #No existing filter
            acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'Create new condition failed.\nThis model does not have a filter with depot enabled.')
            return
        return ConditionalFunctions.ShowNewDepotConditionDlg(application, model, item)
    elif item.RecordType() == 'Party' and item.Type() == 'Client':
        qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
        qry.AddAttrNode('Client', 'EQUAL', True) #Should have client selected!
        qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name()) #Correct model
        if qry.Select().Size() < 1: #No existing filter
            acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'Create new condition failed.\nThis model does not have a filter with client enabled.')
            return
        return ConditionalFunctions.ShowNewClientConditionDlg(application, model, item)


def NewPortfolioCondition(application, cd):
	""" Create a new condition for the selected portfolio of the selected model type """
	model = application.treeView.GetSelectedItem().GetData()
	qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
	qry.AddAttrNode('Portfolio', 'EQUAL', True) #Should have portfolio selected!
	qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name()) #Correct model

	if qry.Select().Size() < 1: #Only open if filter exists.
		acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'This function requires the model to have a filter with portfolio enabled.')
		return

	if application.prfView.GetSelectedItem() == None: #No portfolio selected.
		acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'Please select a portfolio and try again.')
		return

	if ConditionalFunctions.StartNewPortfolioConditionDlg(application, cd): #Returns True when saving.
		UpdateConditionalModels(application, cd)

def NewPartyCondition(application, _):
    if ((application.tabs.GetActivePage() == 0 and application.depView.GetSelectedItem() == None) or
        (application.tabs.GetActivePage() == 1 and application.clntView.GetSelectedItem() == None) or
        (application.tabs.GetActivePage() == 2 and application.depTree.GetSelectedItem() == None)): #item must be selected on open page.
        acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'Please select a party in your active tab and try again.')
        return

    model = application.treeView.GetSelectedItem().GetData()

    qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
    qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name()) #Correct model

    ptyType = application.GetActiveDataType()
    if ptyType == 'Client' or ptyType == 'Depot':
        qry.AddAttrNode(ptyType, 'EQUAL', True) #Should have depot selected!

    if qry.Select().Size() < 1: #Only open if filter exists.
        acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'This function requires the model to have a filter with ' + ptyType + ' enabled.')
        return

    if ptyType == 'Depot':
        if ConditionalFunctions.StartNewDepotConditionDlg(application): #Returns True when saving.
            UpdateConditionalModels(application, _)
    elif ptyType == 'Client':
        if ConditionalFunctions.StartNewClientConditionDlg(application): #Returns True when saving.
            UpdateConditionalModels(application, _)

def NewCondition(application, cd):
    if ConditionalFunctions.StartNewConditionDlg(application): #If saved - reload
        UpdateConditionalModels(application, None)

def CopyConditionsFrom(application):
    selItem = application.GetActiveItem()

    if selItem:
        if ConditionalFunctions.StartCopyConditions(application, selItem):
            UpdateConditionalModels(application, None)

def ChangeConditionValue(application, model):
    selItem = application.conditionOverviewTree.GetSelectedItem()
    if not selItem and not selItem.GetData():
        return
    item = selItem.GetData()

    selCondition = None
    params = acm.FConditionParameters()
    dType = ''
    if item.RecordType() == 'Portfolio':
        dType = 'Portfolio'
        params.Portfolio(item)
    elif item.Type() == 'Client':
        dType = 'Client'
        params.Client(item)
    elif item.Type() == 'Depot':
        dType = 'Depot'
        params.Depot(item)

    #Add instrument args


    for condition in model.Conditions().SortByProperty('Priority'):
        if MatchesCondition(condition, params, application.userSettings.At('showCurrentConditions')):
            return ConditionalFunctions.OpenConditionDlg(application, model, condition)

""" --------------------------------------------------------------------- """
""" ------------------------- CALLBACKS --------------------------------- """
def ShowDetailsForItem(application, _):
    selItem = application.conditionOverviewTree.GetSelectedItem()
    if not selItem or not selItem.GetData():
        return

    item = selItem.GetData()
    application.treeView.Clear()
    FindConditions(application, item)
    application.conditionTabs.ActivatePage(0, True)

""" --------------------------------------------------------------------- """
""" ---------------------- ADDITIONAL INFOS ----------------------------- """
""" --------------------------------------------------------------------- """
def OpenAdditionalInfosDlg(application, _):
    PortfolioViewerDialogs.OpenAdditionalInfoDlg(application)

def ClearAdditionalInfos(application, _):
    application.addInfoNode = None
    application.addInfosCtrl.SetData('')

""" --------------------------------------------------------------------- """
""" ---------------------- PORTFOLIO FILTER FIELDS ---------------------- """
""" --------------------------------------------------------------------- """
def ClearParties(application, _):
    application.portfolioOwner.SetData('')
    application.partiesSelected = None

def StartInsertCompoundPortfolio(application, _):
    """ Opens Insert Item for parties. Supports one or zero elements and adds data to dialog field. """
    compPortfolio = acm.UX().Dialogs().SelectObjectsInsertItems(application.Shell(), acm.FCompoundPortfolio, False)
    if compPortfolio == None:
        return
    application.compParentFld.SetData(compPortfolio.Name())
    application.compFld.SetData('No')
    application.compFld.Editable(False)

def ClearCompound(application, _):
	""" Clear the Compound Portfolio (node) field """
	application.compParentFld.SetData('')
	application.compFld.Editable(True)

def SetCompoundNode(application, cd):
	""" Set the selected compound portfolio as compound portfolio (node) """
	listItem = application.prfView.GetSelectedItem()
	if listItem == None:
		return
	portfolio = listItem.GetData()
	if portfolio.Compound():
		application.compParentFld.SetData(portfolio.Name())
	PortfolioSearch(application, None)

""" ------------------------------------------------------------------------ """
""" ---------------------- PORTFOLIO SEARCH FUNCTIONS ---------------------- """
""" ------------------------------------------------------------------------ """
def PortfolioSearch(application, cd):
    """ When a search is triggered, filter results based on search input """
    application.prfView.RemoveAllItems()
    application.treeView.RemoveAllItems()
    application.conditionOverviewTree.RemoveAllItems()
    qry = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')

    if application.addInfoNode:
        qry.AsqlNodes([application.addInfoNode])

    """ Add common attributes """
    name = application.nameFld.GetData()
    date = application.dateFld.GetData()
    curr = application.currFld.GetData()
    prtfOwner = application.partiesSelected
    compParent = application.compParentFld.GetData()
    comp = application.compFld.GetData()
    if name != '':
    	qry.AddAttrNode('Name', 'RE_LIKE_NOCASE', '%s'%(name))
    if date != '':
    	qry.AddAttrNode('UpdateTime', 'GREATER', date)
    if curr != '':
    	qry.AddAttrNode('Currency.Name', 'EQUAL', curr)
    if prtfOwner != None:
    	node = qry.AddOpNode('OR')
    	for party in prtfOwner:
    		node.AddAttrNode('PortfolioOwner.Name', 'EQUAL', party.Name())
    if compParent != '': 
    	#Only shows physical portfolios.  
    	application.compFld.SetData('No')
    	application.compFld.Editable(False)
    	aCompNode = True #Set variable to go through if-statement and find intersection between collections.
    else:
    	aCompNode = False
    if comp != '':
    	if comp == 'Yes':
    		qry.AddAttrNode('Compound', 'EQUAL', True)
    	elif comp == 'No':
    		qry.AddAttrNode('Compound', 'EQUAL', False)

    res = qry.Select()
    matchedItems = res 
    if aCompNode:
    	cNode = acm.FCompoundPortfolio[compParent]
    	matchedItems = matchedItems.Intersection(cNode.AllPhysicalPortfolios())

    application.matchedItems = matchedItems.AsIndexedCollection()
    application.numberOfMatchedItems = application.matchedItems.Size()
    application.nextItem = 0
    if application.numberOfMatchedItems >= application.userSettings.At('loadRange'):
    	application.addMoreListItems.Editable(True)
    LoadFilteredPortfolios(application, None)

def LoadFilteredPortfolios(application, cd):
    """ Class used to only fill the application with a few portfolios at once. """
    listRoot = application.prfView.GetRootItem()
    for i in range(application.nextItem, (application.nextItem+application.userSettings.At('loadRange'))):
        if i >= application.numberOfMatchedItems:
            application.addMoreListItems.Editable(False)
            i = i-1
            break
        portfolio = application.matchedItems.At(i)
        listObj = listRoot.AddChild()
        AddItem(application, portfolio, listObj)
    application.nextItem = i+1
    application.addedPortfolios.Label("Shows %s/%s"%(FixFormat(application.nextItem), FixFormat(application.numberOfMatchedItems)))

def AddItem(application, portfolio, item):
    """ Add the item to the list and fill the columns with correct data."""
    item.Icon(portfolio.Icon(), portfolio.Icon())
    item.SetData(portfolio)
    i = 0
    addInfoCol = []
    for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs(): #Potential additional info columns
        addInfoCol.append(addInfo.Name())

    for col in application.userSettings.At('prfViewCol'):
        if col == 'Name':
            item.Label(portfolio.Name(), i)
        elif col == 'Assignment Info':
            item.Label(portfolio.AssignInfo(), i)
        elif col == 'Currency':
            item.Label(portfolio.Currency(), i)
        elif col == "Type":
            item.Label(portfolio.TypeChlItem(), i)
        elif col == 'Update Time':
            item.Label(acm.Time.DateFromTime(portfolio.UpdateTime()), i)
        elif col == 'Position Pair':
            item.Label(portfolio.CurrencyPair(), i)
        elif col == 'Owner':
            item.Label(portfolio.PortfolioOwner(), i)
        elif col in addInfoCol:
            item.Label(portfolio.add_info(col), i)
        i += 1

""" -------------------------------------------------------------------- """
""" ---------------------- PARTY SEARCH FUNCTIONS ---------------------- """
""" -------------------------------------------------------------------- """
def PartySearch(application, cd):
    opt = application.depOrClntCtrl.GetData()
    if opt == "Client":
        application.currentPtyType = "Client"
        application.clntView.RemoveAllItems()
        qry = acm.CreateFASQLQuery(acm.FClient, 'AND')
    elif opt == "Depot":
        application.currentPtyType = "Depot"
        application.depView.RemoveAllItems()
        qry = acm.CreateFASQLQuery(acm.FDepot, 'AND')

    application.depTree.RemoveAllItems()
    application.treeView.RemoveAllItems()
    application.conditionOverviewTree.RemoveAllItems()

    if application.addInfoNode:
        qry.AsqlNodes([application.addInfoNode])

    name = application.nameFld.GetData()
    date = application.dateFld.GetData()
    alias = application.ptyId2Ctrl.GetData()
    aliasType = application.aliasTypeCtrl.GetData()
    aliasName = application.aliasNameCtrl.GetData()
    aimsEntity = application.aimsEntCtrl.GetData()
    fixClnt = application.fixClientCtrl.GetData()
    pnlDepot = application.pnlDepotCtrl.GetData()
    shapingDepot = application.shpDepotCtrl.GetData()
    warehouseDepot = application.warehouseDepCtrl.GetData()
    unknownDepot = application.unknownDepotCtrl.GetData()
    parentOption = application.depParentOptionCtrl.GetData()
    clients = application.partiesSelected
    clntWDepots = application.clientHasDepotsCtrl.GetData()
    comm = application.comCtrl.GetData()
    commSlope = application.comSlopeCtrl.GetData()
    comShr = application.comShrCtrl.GetData()
    comShrSlope = application.comShrSlopeCtrl.GetData()

    if name != '':
        qry.AddAttrNode('Name', 're_like_nocase', name)
    if date != '':
        qry.AddAttrNode('UpdateTime', 'GREATER', date)
    if alias != '':
        qry.AddAttrNode('Id2', 're_like_nocase', alias)
    if aliasType != '': #Alias name only considered with alias type
        qry.AddAttrNode('Aliases.Type.AliasTypeName', 'EQUAL', aliasType)
        qry.AddAttrNode('Aliases.Name', 're_like_nocase', aliasName)
    if aimsEntity != '':
        b = False
        if aimsEntity == 'Yes':
            b = True
        qry.AddAttrNodeBool('AimsEntity', b)
    #Depot fields
    if application.currentPtyType == "Depot":
        if unknownDepot != '':
            b = False
            if unknownDepot == 'Yes':
                b = True
            qry.AddAttrNodeBool('DefaultDepot', b)
        if pnlDepot != '':
            b = False
            if pnlDepot == 'Yes':
                b = True
            qry.AddAttrNodeBool('PnlDepot', b)
        if shapingDepot != '':
            b = False
            if shapingDepot == 'Yes':
                b = True
            qry.AddAttrNodeBool('ShapingDepot', b)
        if warehouseDepot != '':
            b = False
            if warehouseDepot == 'Yes':
                b = True
            qry.AddAttrNodeBool('WarehouseDepot', b)
        if parentOption == '' or parentOption == 'With parent':
            if clients != None:
                node = qry.AddOpNode('OR')
                for party in clients:
                    node.AddAttrNode('Parent.Name', 'EQUAL', party.Name())
            elif parentOption == 'With parent':
                qry.AddAttrNode('Parent.Name', 're_like_nocase', '*')

    #Client fields
    elif application.currentPtyType == "Client":
        if fixClnt != '':
            b = False
            if fixClnt == 'Yes':
                b = True
            qry.AddAttrNodeBool('FixClient', b)
        if clntWDepots != '':
            if clntWDepots == 'Has depots':
                qry.AddAttrNode('Children.Name', 're_like_nocase', '*')
                
    res = qry.Select() #Select items

    if application.currentPtyType == "Depot":
        if parentOption == 'Without parent':
            qry.AddAttrNode('Parent.Name', 're_like_nocase', '*')
            res = res.RemoveAll(qry.Select())
        if application.userSettings.At('useSlopeInSearch'):
            if comm  != '':
                if comm == 'No commission condition for depot':
                    res = CommSearch('withoutDepot', '', 'Commission', res)
                elif comm == 'Commission condition for depot exists. Curve slope:':
                    res = CommSearch('withDepot', commSlope, 'Commission', res)
            if comShr != '':
                if comShr == 'No commission sharing condition for depot':
                    res = CommSearch('withoutDepot', '', 'Commission Sharing', res)
                elif comShr == 'Commission sharing condition for depot exists. Curve slope:':
                    res = CommSearch('withDepot', commSlope, 'Commission Sharing', res)

    elif application.currentPtyType == "Client":
        if clntWDepots == "Has no depots":
            qry.AddAttrNode('Children.Name', 're_like_nocase', '*')
            res = res.RemoveAll(qry.Select())

    matchedItems = res 

    if application.currentPtyType == "Depot": #depot search
        application.matchedItems = matchedItems.AsIndexedCollection()
        application.numberOfMatchedItems = application.matchedItems.Size()
        application.nextItem = 0
        application.skippedDepots = 0
        if application.numberOfMatchedItems >= application.userSettings.At('loadRange'):
            application.addMoreDep.Editable(True)
            application.t_addMoreDep.Editable(True)
        LoadFilteredDepots(application, None)
        if application.tabs.GetActivePage() == 1:
            application.tabs.ActivatePage(0, True)
    elif application.currentPtyType == "Client": #client search
        application.matchedClients = matchedItems.AsIndexedCollection()
        application.numberOfMatchedClients = application.matchedClients.Size()
        application.nextClient = 0
        if application.numberOfMatchedClients >= application.userSettings.At('loadRange'):
            application.addMoreClnt.Editable(True)
            application.t_addMoreDep.Editable(True)
        LoadFilteredClients(application, None)
        if application.tabs.GetActivePage() == 0:
            application.tabs.ActivatePage(1, True)
        for i in range(0, application.clntView.ColumnCount()):
            application.clntView.AdjustColumnWidthToFitItems(i)

def CommSearch(sType, slope, mType, res):
    """ Help function for Party Search. Handles commission/commission sharing alternatives.
        sType can be '','withDepot' or 'withoutDepot', slope is int in string, mType is 
        model type, and res is the collection of filtered depots """
    resCom = acm.FSet()
    comQry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    comQry.AddAttrNode('model.modelCategory', 'equal', mType)
    comQry.AddAttrNode('depot.Name', 're_like_nocase', '*')
    if slope == "":
        for cond in comQry.Select():
            resCom.Add(cond.Depot())
    else:
        for cond in comQry.Select():
            for curve in cond.Curve():
                for interval in curve.Intervals():
                    if str(interval.Slope()) == slope:
                        resCom.Add(cond.Depot())
    if sType == 'withoutDepot':
        return res.RemoveAll(resCom)
    elif sType == 'withDepot':
        return res.Intersection(resCom)
    return res

def LoadFilteredParties(application, cd):
    if application.currentPtyType == "Client":
        LoadFilteredClients(application, None)
    elif application.currentPtyType == "Depot":
        LoadFilteredDepots(application, None)

def LoadFilteredClients(application, cd):
    """ Class used to only fill the application with a few clients at once. """
    listRoot = application.clntView.GetRootItem()
    treeRoot = application.depTree.GetRootItem()
    for i in range(application.nextClient, (application.nextClient+application.userSettings.At('loadRange'))):
        if i >= application.numberOfMatchedClients:
            application.addMoreClnt.Editable(False)
            application.t_addMoreDep.Editable(False)
            i = i-1
            break
        client = application.matchedClients.At(i)
        listObj = listRoot.AddChild()
        ClientColumns(application, client, listObj)
        treeObj = treeRoot.AddChild()
        ClientColumns(application, client, treeObj, True)
        for chld in client.Children():
            chldNode = treeObj.AddChild()
            AddDepotItem(application, chld, chldNode, True)
    application.nextClient = i+1
    application.addedClients.Label("Shows %s/%s"%(FixFormat(application.nextClient), FixFormat(application.numberOfMatchedClients)))
    application.t_addedDepots.Label("Shows %s/%s Clients"%(FixFormat(application.nextClient), FixFormat(application.numberOfMatchedClients)))

def LoadFilteredDepots(application, cd):
    """ Class used to only fill the application with a few depots at once."""
    listRoot = application.depView.GetRootItem() 
    treeRoot = application.depTree.GetRootItem()
    for i in range(application.nextItem, (application.nextItem+application.userSettings.At('loadRange'))):
        if i >= application.numberOfMatchedItems:
            application.addMoreDep.Editable(False)
            application.t_addMoreDep.Editable(False)
            i = i-1
            break
        depot = application.matchedItems.At(i)
        listObj = listRoot.AddChild()
        AddDepotItem(application, depot, listObj)
        treeParentItem = ClientNode(application, depot)
        if treeParentItem:
            treeObj = treeParentItem.AddChild()
            AddDepotItem(application, depot, treeObj, True)
            if application.userSettings.At('showDepotTreeExpanded'):
                treeParentItem.Expand()
        else:
            application.skippedDepots += 1 #Will not be shown in tree - subtract.
    application.nextItem = i+1
    application.addedDepots.Label("Shows %s/%s"%(FixFormat(application.nextItem), FixFormat(application.numberOfMatchedItems)))
    application.t_addedDepots.Label("Shows %s/%s Depots"%(FixFormat(application.nextItem-application.skippedDepots), FixFormat(application.numberOfMatchedItems-application.skippedDepots)))

def AddDepotItem(application,depot,item,isTree=False):
    item.Icon(depot.Icon(), depot.Icon())
    item.SetData(depot)
    i = 0
    addInfoCol = []
    for addInfo in acm.FDepot().AddInfoSpecs():
        addInfoCol.append(addInfo.Name())
    aliasCol = []
    for aliasTypes in acm.FPartyAliasType.Select(''):
        aliasCol.append(aliasTypes.Name())
    columns = application.userSettings.At('depViewCol')
    if isTree:
        columns = application.userSettings.At('ptyTreeCol')
    for col in columns:
        if col == 'Name':
            item.Label(depot.Name(), i)
        elif col == 'UpdateTime':
            item.Label(acm.Time.DateFromTime(depot.UpdateTime()), i)
        elif col == 'Alias':
            item.Label(depot.Id2(), i)
        elif col == 'Parent':
            if depot.Parent():
                item.Label(depot.Parent().Name(), i)
        elif col == 'Default depot':
            if depot.DefaultDepot():
                item.Label('Yes', i)
        elif col == 'Profit/Loss':
            if depot.PnlDepot():
                item.Label('Yes', i)
        elif col == 'Shaping':
            if depot.ShapingDepot():
                item.Label('Yes', i)
        elif col == 'Warehouse':
            if depot.WarehouseDepot():
                item.Label('Yes', i)
        elif col == 'AimsEntity':
            if depot.AimsEntity():
                item.Label('Yes', i)
        elif col in addInfoCol:
            item.Label(depot.add_info(col), i)
        elif col in aliasCol:
            item.Label(depot.alias(col), i)
        i += 1

def ClientNode(application, depot):
    client = depot.Parent()
    node = application.depTree.GetRootItem().FirstChild()
    if client == None:
        if not application.userSettings.At('depWithoutParentTree'):
            return None
        if node and not node.GetData(): #Has node - node has no data
            return node
        item = application.depTree.GetRootItem().AddChild(False)
        item.Label('Depots without parent', 0)
        item.Icon('GreenBall', 'GreenBall')
        return item
    else:
        while node:
            if node.GetData() == client:
                return node
            node = node.Sibling()
        item = application.depTree.GetRootItem().AddChild()
        ClientColumns(application, client, item, True)
    return item

def ClientColumns(application,client,item,isTree=False):
    item.Icon(client.Icon(), client.Icon())
    item.SetData(client)
    addInfoCol = []
    for addInfo in acm.FClient().AddInfoSpecs():
        addInfoCol.append(addInfo.Name())
    aliasCol = []
    for aliasTypes in acm.FPartyAliasType.Select(''):
        aliasCol.append(aliasTypes.Name())
    i = 0
    columns = application.userSettings.At('clntViewCol')
    if isTree:
        columns = application.userSettings.At('ptyTreeCol')
    for col in columns:
        if col == 'Name':
            item.Label(client.Name(), i)
        elif col == 'UpdateTime':
            item.Label(acm.Time.DateFromTime(client.UpdateTime()), i)
        elif col == 'Alias':
            item.Label(client.Id2(), i)
        elif col == 'AimsEntity':
            if client.AimsEntity():
                item.Label('Yes')
        elif col == 'FIX':
            if client.FixClient()=='Yes':
                item.Label('Yes', i)
        elif col in addInfoCol:
            item.Label(client.add_info(col), i)
        elif col in aliasCol:
            item.Label(client.alias(col), i)
        i += 1

""" --------------------------------------------------------------------------- """
""" ---------------------- CONDITION FILTER INPUT FIELDS ---------------------- """
""" --------------------------------------------------------------------------- """
def StartInsertInstrument(application, cd):
    if PortfolioViewerDialogs.StartInsertInstrument(application, cd):
        UpdateConditionalModels(application, None)

def ClearInstrument(application, cd):
    """ Clear the instrument field. """
    application.insFilter.SetData('')
    application.overviewInsFilter.SetData('')
    application.insSelected = None
    UpdateConditionalModels(application, None)

""" ------------------------------------------------------------------------------------ """
""" ---------------------- FILL CONDITIONAL MODELS TREE FUNCTIONS ---------------------- """
""" ------------------------------------------------------------------------------------ """
def LoadConditionalModels(application, cd):
    if application.userSettings.At('fillConditionsAutomatically'):
        UpdateConditionalModels(application, cd)

def UpdateConditionalModels(application, cd):
    application.condition_array = acm.FArray()
    application.treeView.Clear()
    application.conditionOverviewTree.Clear()
    item = application.GetActiveItem()
    if item:
        FindConditions(application, item)
        FillConditionOverview(application, item)

def FindConditions(application, item):
    tree = application.treeView
    rootItem = tree.GetRootItem()
    
    conParams = acm.FConditionParameters() #Used to find matching conditions - set only once
    if item.RecordType() == 'Portfolio':
        conParams.Portfolio(item)
    elif item.RecordType() == 'Party':
        if item.Type() == 'Depot':
            conParams.Depot(item)
        elif item.Type() == 'Client':
            conParams.Client(item)
    if application.insSelected:
        conParams.Instrument(application.insSelected)
    for cat in reversed(application.userSettings.At('modelCategories')): #Loop backwards to not be thrown to bottom when expanding the node.
        treeNode = rootItem.AddChild(False)
        treeNode.Label(cat)
        AddModels(application, item, treeNode, cat, conParams, item)
        treeNode.Expand()

def AddModels(application, item, treeNode, modelType, conParams, selItem):
    """ Add models without conditions at end of tree. """
    getModels = acm.CreateFASQLQuery(acm.FConditionalValueModel, 'AND')
    getModels.AddAttrNode('ModelCategory', 'EQUAL', modelType)
    modelConditionArray = acm.FArray()
    for model in getModels.Select().SortByProperty('Name'):
        treeItem = treeNode.AddChild()
        treeItem.Label(model.StringKey())
        treeItem.Icon(model.Icon(), model.Icon())
        treeItem.SetData(model)
        conditions = FindMatchingConditions(application, model, conParams, treeItem)
        if conditions.Size() > 0:
            FillColumns(application, treeItem, conditions[0])
            modelConditionArray.Add((model, conditions))
        else:
            modelConditionArray.Add((model, None))
    application.condition_array.Add((modelType, modelConditionArray))


def FillConditionOverview(application, item):
    tree = application.conditionOverviewTree
    rootItem = tree.GetRootItem()
    
    qry = acm.CreateFASQLQuery('FConditionalValueModel', 'AND')
    qry.AddAttrNode('ModelCategory', 'EQUAL', 'AMS Limits')

    models = qry.Select()

    if item.RecordType() == 'Portfolio':
        owner = item.PortfolioOwner()
        if owner and owner.RecordType() == 'Party' and (owner.Type() == 'Depot' or owner.Type() == 'Client'):
            if owner.Type() == 'Depot':
                parent = owner.Parent()
                if parent and parent.Type() == 'Client': #Client, depot, portfolio structure
                    topNode = rootItem.AddChild()
                    nodeSetup(application, models, parent, topNode)
                    addDepots(application, models, parent, topNode)
                    addOwnedPortfolios(application, models, parent, topNode)
                else:
                    ownerNode = rootItem.AddChild()
                    nodeSetup(application, models, owner, ownerNode)
                    addOwnedPortfolios(application, models, owner, ownerNode)

            elif owner.Type() == 'Client': 
                parntNode = rootItem.AddChild()
                nodeSetup(application, models, owner, parntNode)
                addDepots(application, models, owner, parntNode)
                addOwnedPortfolios(application, models, owner, parntNode)
            return
        else:
            node = rootItem.AddChild()

    elif item.Type() == 'Client': #Party should be record type
        node = rootItem.AddChild()
        addDepots(application, models, item, node)
        addOwnedPortfolios(application, models, item, node)

    elif item.Type() == 'Depot': #Party should be record type
        parent = item.Parent()
        if parent and parent.Type() == 'Client':
            parntNode = rootItem.AddChild()
            nodeSetup(application, models, parent, parntNode)
            addDepots(application, models, parent, parntNode)
            addOwnedPortfolios(application, models, parent, parntNode)
            parntNode.Expand()
            return
        else:
            node = rootItem.AddChild()
            addOwnedPortfolios(application, models, item, node)
    else:
        return #incorrect type somehow
    nodeSetup(application, models, item, node)

def addOwnedPortfolios(application, models, item, node):
    """ Finds the owned portfolios for the selected item and adds 
        them as subnodes to the item. """
    for prf in item.OwnedPortfolios():
        prfNode = node.AddChild()
        nodeSetup(application, models, prf, prfNode)
    node.Expand()

def addDepots(application, models, client, node):
    """ Finds the depots that belong to a client and adds them as
        subnodes to the client node. Also adds all the depots' 
        owned portfolios as subnodes to the depot nodes. """
    for depot in client.Children():
        if depot.Type() == 'Depot':
            depotNode = node.AddChild()
            nodeSetup(application, models, depot, depotNode)
            addOwnedPortfolios(application, models, depot, depotNode)

def nodeSetup(application, models, item, node):
    """ Adds item data to all the node columns. """
    node.Label(item.Name())
    node.Icon(item.Icon(), item.Icon())
    node.SetData(item)
    i = 1
    for model in models:
        node.Label(FixFormat(FindValue(application, model, item)), i)
        i += 1

def FindValue(application, model, item):
    """ Finds the matched condition of a model type for the given item
        and returns the value of that condition. """
    selCondition = None
    params = acm.FConditionParameters()
    if item.RecordType() == 'Portfolio':
        params.Portfolio(item)
    elif item.Type() == 'Client':
        params.Client(item)
    elif item.Type() == 'Depot':
        params.Depot(item)

    #Add instrument and currency args.
    if application.insSelected:
        params.Instrument(application.insSelected)

    for condition in model.Conditions().SortByProperty('Priority'):
        if MatchesCondition(condition, params, application.userSettings.At('showCurrentConditions')):
            for curve in condition.Curve():
                return curve.MinValue()
    return ''

def FindMatchingConditions(application, model, params, treeNode):
    """ Finds all conditions that can match the given condition parameters. """
    conditionsList = acm.FArray() #Save all matched conditions in array for column updates
    for condition in model.Conditions().SortByProperty('Priority'):
        if MatchesCondition(condition, params, application.userSettings.At('showCurrentConditions')):
            child = treeNode.AddChild()
            conditionsList.Add(condition)
            child.Label(condition.StringKey())
            child.Icon(condition.Icon(), condition.Icon())
            child.SetData(condition)
            FillColumns(application, child, condition)
    return conditionsList

def MatchesCondition(condition, params, showCurr):
    ins = params.Instrument()
    currency = params.Currency()
    client = params.Client()
    depot = params.Depot()
    portfolio = params.Portfolio()
    startDay = condition.StartDay()
    endDay = condition.EndDay()
    today = acm.Time.DateNow()
    if (showCurr and ((startDay and (startDay > today)) or (endDay and (endDay < today)))):
        return False

    #Look for correct attributes
    if ((condition.Instrument() and ins and condition.Instrument() != ins) or
        (condition.Currency() and currency and condition.Currency() != currency) or
        (condition.ClientGroup() and not IsInGroup(condition.ClientGroup(), client)) or
        (condition.Client() and condition.Client() != client) or
        (condition.Depot() and condition.Depot() != depot) or
        (condition.Portfolio() and condition.Portfolio() != portfolio) or
        (condition.InsFilter() and ins and (not condition.InsFilter().Query().IsSatisfiedByUseAttributes(ins))) or
        (condition.PortfolioFilter() and (not condition.PortfolioFilter().Query().IsSatisfiedByUseAttributes(portfolio))) or
        (condition.Account()) or
        (condition.MarketGroup()) or (condition.Market()) or (condition.Segment()) or 
        (condition.ExecutionType()) or (condition.BuySell() != 'Undefined') or
        (condition.InsType() != 'None') or 
        (condition.PayType() != 'None') or 
        (condition.UndInsType() != 'None') or
        (condition.CounterpartyGroup()) or (condition.Counterparty()) or
        (condition.BrokerGroup()) or (condition.Broker())):
        return False
    else:
        return True

def IsInGroup(clientGrp, client):
    for links in clientGrp.Parties():
        if links.Party() == client:
            return True
    return False

def FillTreeWithData(application, _):
    treeRoot = application.treeView.GetRootItem()
    for modelCatTuple in application.condition_array:
        treeNode = treeRoot.AddChild()
        treeNode.Label(modelCatTuple[0])
        for modelCondTuple in modelCatTuple[1]:
            model = modelCondTuple[0]
            if model:
                modelNode = treeNode.AddChild()
                modelNode.Icon(model.Icon(), model.Icon())
                modelNode.Label(model.StringKey())
                modelNode.SetData(model)
                if modelCondTuple[1]:
                    FillColumns(application, modelNode, modelCondTuple[1][0]) #First condition is matched condition
                    for condition in modelCondTuple[1]:
                        condNode = modelNode.AddChild()
                        condNode.Label(condition.StringKey())
                        condNode.Icon(condition.Icon(), condition.Icon())
                        condNode.SetData(condition)
                        FillColumns(application, condNode, condition)

        treeNode.Expand()
    
def FillColumns(application, treeItem, condition):
    """ Add data in columns """
    index = 1
    curve = None
    if condition.Curve(): #Curve can be an empty collection
        curve = condition.Curve().First()
    
    for column in application.userSettings.At(application.userSettings.At('useConditionColumns')):
        if column == 'Currency':
            if curve:
                treeItem.Label(curve.Currency(), index)
        elif column == 'Value':
            if curve:
                treeItem.Label(FixFormat(curve.MinValue()), index)
        elif column == 'Type':
            if curve:
                treeItem.Label(curve.CurveType(), index)
        elif column == '#Portfolios':
            treeItem.Label(FixFormat(calcPrtfMatched(condition)), index)
        elif column == '#Depots':
            treeItem.Label(FixFormat(calcDepMatched(condition)), index)
        elif column == 'Priority':
            treeItem.Label(condition.Priority(), index)
        elif column == 'Mkt Group':
            treeItem.Label(condition.MarketGroup(), index)
        elif column == 'Market':
            treeItem.Label(condition.Market(), index)
        elif column == 'Market Segment':
            treeItem.Label(condition.Segment(), index)
        elif column == 'Instrument':
            treeItem.Label(condition.Instrument(), index)
        elif column == 'Client Group':
            treeItem.Label(condition.ClientGroup(), index)
        elif column == 'Client':
            treeItem.Label(condition.Client(), index)
        elif column == 'Counterparty Group':
            treeItem.Label(condition.CounterpartyGroup(), index)
        elif column == 'Counterparty':
            treeItem.Label(condition.Counterparty(), index)
        elif column == 'Broker Group':
            treeItem.Label(condition.BrokerGroup(), index)
        elif column == 'Broker':
            treeItem.Label(condition.Broker(), index)
        elif column == 'Depot':
            treeItem.Label(condition.Depot(), index)
        elif column == 'Account':
            treeItem.Label(condition.Account(), index)
        elif column == 'Portfolio':
            treeItem.Label(condition.Portfolio(), index)
        elif column == 'Exec type':
            treeItem.Label(condition.ExecutionType(), index)
        elif column == 'Buy/Sell':
            if condition.BuySell() != 'Undefined':
                treeItem.Label(condition.BuySell(), index)
        elif column == 'Instrument Type':
            if condition.InsType() != 'None':
                treeItem.Label(condition.InsType(), index)
        elif column == 'Paytype':
            if condition.PayType() != 'None':
                treeItem.Label(condition.PayType(), index)
        elif column == 'Underlying Instrument Type':
            if condition.UndInsType() != 'None':
                treeItem.Label(condition.UndInsType(), index)
        elif column == 'Instrument Filter':
            treeItem.Label(condition.InsFilter(), index)
        elif column == 'Portfolio Filter':
            treeItem.Label(condition.PortfolioFilter(), index)
        #Only for Charges
        if not IsBrokerageRiskModel(condition.Model()):
            if not curve: #Only check once.
                index += 1
                continue    
            if column == 'Curve Name':
                treeItem.Label(curve.Name(), index)
            elif column == 'Calculation Mode':
                treeItem.Label(curve.CalcMode(), index)
            elif column == 'Minimum Value':
                treeItem.Label(curve.MinValue(), index)
            elif column == 'Curve Type':
                treeItem.Label(curve.CurveType(), index)
            elif column == 'Curve Slope':
                if curve.Intervals().Size() > 0:
                    interval = curve.Intervals().First()
                    treeItem.Label(interval.Slope(), index)
        index += 1

def calcPrtfMatched(condition):
    if condition.Portfolio():
        return 1
    if condition.PortfolioFilter():
        return condition.PortfolioFilter().Query().Select().Size()
    return acm.FPhysicalPortfolio.Select('').Size()

def calcDepMatched(condition):
    if condition.Depot():
        return 1
    return acm.FDepot.Select('').Size()

def calcClntsMatched(condition):
    if condition.Client():
        return 1
    if condition.ClientGroup():
        return condition.ClientGroup().Parties().Size()
    return acm.FClient.Select('').Size()

""" End of file """
