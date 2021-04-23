""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ClientViewer/etc/ClientViewerApplication.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    ClientViewerApplication

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import FUxCore
import acm
import time

LOAD_RANGE = 0
SHOW_ALL_COMMISSIONS = False
parentAdded = False
selectedItem = None

""" Start-up functions """
def StartApplication(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0)

def ReallyStartApplication(shell, count):
    """ Start the application called 'Client Viewer' (this application) """
    acm.UX().SessionManager().StartApplication('Client Viewer', None)

def CreateApplicationInstance():
    return clientViewerApplication()

""" Additional class that handles ribbons and actions. """
class menuItems(FUxCore.MenuItem):
    def __init__(self):
        self.m_application = None
        
    def Invoke(self, cd):
        commandName = cd.Definition().GetName().Text()
        if commandName == 'ClearFields':
            clearAllFields(self.m_application)
        elif commandName == 'GoToSearch':
            goToSearch(self.m_application)
        elif commandName == 'DoSearch':
            NewSearch(self.m_application, None)
        elif commandName == 'LoadParties':
            LoadFilteredParties(self.m_application, None)
        elif commandName == 'PartyDefinition':
            acm.UX().SessionManager().StartApplication('Party Definition', None) 
        elif commandName == 'Charges':
            acm.UX().SessionManager().StartApplication('Charges', None) 
        elif commandName == 'addDepot':
            addDepotWindow(self.m_application)
        elif commandName == 'openCom':
            openCommission(self.m_application)
        elif commandName == 'openComS':
            openCommissionSharing(self.m_application)
        elif commandName == 'deleteWithDep':
            deleteWithDependencies(self.m_application)
        elif commandName == 'ClientGroups':
            acm.UX().SessionManager().StartApplication('Party Groups', acm.FPartyGroup[cd.Definition().GetTooltip().Text()])
        elif commandName == 'deleteWithDep_multi':
            deleteWithDependenciesMulti(self.m_application)
        else: 
            pass
            
    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

    def SetApplication(self, application):
        self.m_application = application

def goToSearch(application):
    application.searchMode.SetFocus()

def clearAllFields(application):
    """ A function that clears all fields to enable a new search. """
    for f in application.allFlds:
        f.SetData('')
    application.searchMode.SetData('Client')
    application.orderBy.SetData('Name (A-Z)')

def addDepotWindow(application):
    """ If the user has a runscript used for adding depots, call it instead of using ClientViewer default function. """
    try:
        useRunscript = int(ParameterFromName('ClientViewerParameters').Value().At('AddDepot_UseRunscript').Text())
        runscriptName = ParameterFromName('ClientViewerParameters').Value().At('AddDepot_RunScriptName').Text()
    except:
        useRunscript = False
    if useRunscript == 1:
        acm.RunModuleWithParameters(runscriptName, acm.GetDefaultContext()) 
    else:
        NewDepot(application, None)

def openCommission(application):
    tree = application.treeView
    item = tree.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    depot = item.GetData()
    if depot.Type() != 'Depot':
        return
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('model.modelCategory', 'equal', 'commission')
    qry.AddAttrNode('Depot.Id', 'EQUAL', depot.Id())
    for cond in qry.Select():
        acm.UX().SessionManager().StartApplication('Charges', cond)
        break

def openCommissionSharing(application):
    tree = application.treeView
    item = tree.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    depot = item.GetData()
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('model.modelCategory', 'equal', 'commission sharing')
    qry.AddAttrNode('Depot.Id', 'EQUAL', depot.Id())
    for cond in qry.Select():
        acm.UX().SessionManager().StartApplication('Charges', cond)
        break

def deleteWithDependencies(application):
    if application.treeView.GetSelectedItem():
        StartDeleteDialog(application, application.treeView.GetSelectedItem(), False)

def deleteWithDependenciesMulti(application):
    if application.treeView.GetSelectedItems().Size() > 1:
        StartDeleteDialog(application, application.treeView.GetSelectedItems(), True)

''' -- Additional Class that warns user when creating depot -- '''
def StartDialog(application, client):
    builder = dialogLayout()
    customDlg = depotDialog()
    customDlg.parent = client
    customDlg.application = application
    acm.UX().Dialogs().ShowCustomDialogModal(application.Frame().Shell(), builder, customDlg )

class depotDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.nameInput = ""
        self.parent = None
        self.application = None

    def HandleApply( self ):
        if len(self.nameInput.GetData()):
            if acm.FParty[self.nameInput.GetData()] != None:
                return None
        else:
            return None
        addNewDepotToClient(self.application, self.parent, self.nameInput.GetData())
        return True

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Add depot to %s'%self.parent.Name())
        self.nameInput = layout.GetControl('name')

def dialogLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.   AddLabel('Info', 'Enter a unique name for the depot')
    b.   AddInput('name', 'Name')
    b.   BeginHorzBox('None')
    b.      AddButton('ok', 'OK')
    b.      AddButton('cancel', 'Cancel')
    b.   EndBox()
    b.EndBox()
    return b

""" -- Additional class for deletion of parties with dependencies such as commissions etc. -- """
def StartDeleteDialog(application, parties, manySelected):
    customDlg = DeleteDepot()
    if manySelected: 
        depots = acm.FArray()
        dependencies = acm.FArray()
        for party in parties: 
            depots.Add(party.GetData())
            qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
            qry.AddAttrNode('Depot.Id', 'EQUAL', party.GetData().Id())
            dependencies.AddAll(qry.Select())
        customDlg.parties = depots
        depot = None
    else: 
        depot = parties.GetData()
        qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
        qry.AddAttrNode('Depot.Id', 'EQUAL', depot.Id())
        dependencies = qry.Select()
        customDlg.party = depot
        depots = None
    customDlg.dependencies = dependencies
    customDlg.application = application
    builder = deleteDialogLayout(depot, depots, dependencies)
    acm.UX().Dialogs().ShowCustomDialogModal(application.Frame().Shell(), builder, customDlg )

class DeleteDepot(FUxCore.LayoutDialog):
    def __init__(self):
        self.party = None
        self.parties = None
        self.dependencies = None
        self.application = None

    def HandleApply(self):
        if self.dependencies.Size() > 0:
            for condition in self.dependencies:
                condition.Delete()
        if self.party != None:
            self.party.Delete() 
        elif self.parties != None:
            for depot in self.parties:
                try:
                    depot.Delete()
                except:
                    print('Unsuccessful removal of ', depot.Name(), '. Check other dependencies')
        NewSearch(self.application, None)
        return True

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Delete depot(s)') 

def deleteDialogLayout(depot, depots, dependencies):
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    if depot != None:
        b.   AddLabel('DepName', 'Are you sure you want to delete "%s"?'%(depot.Name()))
    elif depots != None:
        b.AddLabel('DepName', 'Are you sure you want to delete the following depots?')
        count = 0
        for pty in depots:
            b.    AddLabel('Pty%s'%count, ' "%s"'%pty.Name(), 24, 24)
            count += 1
    if dependencies.Size() > 0:
        b.   AddLabel('Also', 'This will also delete:')
        count = 0
        for condition in dependencies:
            b.    AddLabel('Dep%s'%count, '     "%s" (%s)'%(condition.Name(), condition.Model().ModelCategory()), 24, 24)
            count += 1
    b.   BeginHorzBox('None')
    b.      AddButton('ok', 'OK')
    b.      AddButton('cancel', 'Cancel')
    b.   EndBox()
    b.EndBox()
    return b

""" -------- """

def ParameterFromName(name):
    return acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, name) 

def CommissionChange(application, cd):
    status = application.commFld.GetData()
    if status == '':
        application.commSlopeFld.Editable(False)
    elif status == 'No group':
        application.commSlopeFld.Editable(False)
    elif status == 'Enter Slope':
        application.commSlopeFld.Editable(True)

def CommissionSharingChange(application, cd):
    status = application.commShrFld.GetData()
    if status == '':
        application.commShrSlopeFld.Editable(False)
    elif status == 'No group':
        application.commShrSlopeFld.Editable(False)
    elif status == 'Enter Slope':
        application.commShrSlopeFld.Editable(True)

def NewDepot(application, cd):
    """ If add depot is pressed, make sure the selected
        party is a client and then add a depot to it. """
    tree = application.treeView
    item = tree.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    client = item.GetData()
    if client.Type() == 'Client': #Can only add depot to clients
        StartDialog(application, client)

def addNewDepotToClient(application, client, depotName):
    """ A method that creates a new party of type depot and adds the
        client as its parent and creates a name for the party. It opens 
        the Party Definition for the new party.  """
    newDepot = acm.FDepot()
    newDepot.AimsEntity(client.AimsEntity()) #Transfer parent settings
    newDepot.Parent(client)
    newDepot.Name(depotName)
    newDepot.Commit()
    acm.UX().SessionManager().StartApplication('Party Definition', newDepot)
    NewSearch(application, None)

def getCommission(depot):
    """ Returns a list of commissions of the given depot """
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('model.modelCategory', 'equal', 'commission')
    qry.AddAttrNode('Depot.Id', 'EQUAL', depot.Id())
    for cond in qry.Select():
        return cond
    return None

def getCommissionSharing(depot):
    """ Returns one commission sharing condition belonging to the 
        given depot. """
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('model.modelCategory', 'equal', 'commission sharing')
    qry.AddAttrNode('Depot.Id', 'EQUAL', depot.Id())
    for cond in qry.Select():
        return cond
    return None

def SearchModeChanged(application, cd):
    """ Method called when the combobox search mode value is changed.
        Makes sure that the correct fields are editable. """
    mode = application.searchMode.GetData()
    if mode == 'Depot':
        for box in application.depBoxes:
            box.Editable(mode == 'Depot')
        for field in application.comFields:
            field.Editable(True)
        CommissionChange(application, None)
        CommissionSharingChange(application, None)
        application.defBlkAcc.Editable(True)
        application.noClient.Editable(True)
        application.fixClnt.Editable(False)
        application.noDepots.Editable(False)
    elif mode == 'Client':
        for box in application.depBoxes:
            box.Editable(False)
        for field in application.comFields:
            field.Editable(False)
        application.defBlkAcc.Editable(False)
        application.noClient.Editable(False)
        application.fixClnt.Editable(True)
        application.noDepots.Editable(True)

def NewSearch(application, cd):
    application.treeView.Clear()
    global parentAdded
    parentAdded = False
    
    """ Create queries """
    if application.searchMode.GetData() == 'Client':
        qry = acm.CreateFASQLQuery(acm.FClient, 'AND')
    elif application.searchMode.GetData() == 'Depot':
        qry = acm.CreateFASQLQuery(acm.FDepot, 'AND')
    
    """ Add common attributes """
    name = application.applicationPane.GetControl('NameField').GetData()
    date = application.dateFld.GetData()
    ptyid2 = application.ptyid2Fld.GetData()
    aims = application.aimsEnt.GetData()
    numDec = application.trdPriceNODec.GetData()
    aliasName = application.aliasNameFld.GetData()
    aliasType = application.aliasType.GetData()
    if name != '':
        qry.AddAttrNode('Id', 'RE_LIKE_NOCASE', '*%s*'%(name))
    if date != '':
        qry.AddAttrNode('UpdateTime', 'GREATER', date)
    if ptyid2 != '':
        qry.AddAttrNode('Id2', 'RE_LIKE_NOCASE', '*%s*'%(ptyid2))
    if aims != '':
        if aims == 'Yes':
            qry.AddAttrNodeBool('AimsEntity', True)
        else:
            qry.AddAttrNodeBool('AimsEntity', False)
    if numDec != '':
        try:
            qry.AddAttrNode('AdditionalInfo.TradePriceNumOfDec', 'EQUAL', numDec)
        except:
            pass
    if aliasName != '':
        qry.AddAttrNode('Aliases.Type.Name', 'RE_LIKE_NOCASE', '*%s*'%(aliasType))
        qry.AddAttrNode('Aliases.Name', 'RE_LIKE_NOCASE', '*%s*'%(aliasName))
    elif aliasType != '': #Show all parties with alias of given type. 
        qry.AddAttrNode('Aliases.Type.Name', 'RE_LIKE_NOCASE', '*%s*'%(aliasType))
    """ Add specific attributes (for Client) """        
    if application.searchMode.GetData() == 'Client':
        fix = application.fixClnt.GetData()
        if fix != '':
            if fix == 'Yes':
                qry.AddAttrNodeBool('FixClient', True)
            else:
                qry.AddAttrNodeBool('FixClient', False)
        
        noDepots = application.noDepots.GetData()
        if noDepots != '':
            if noDepots == 'Has depots':
                qry.AddAttrNode('Children.Name', 'NOT_EQUAL', '')
                res = qry.Select()
            else: #No depots
                res = qry.Select()
                qry.AddAttrNode('Children.Name', 'NOT_EQUAL', '')
                removeRes = qry.Select() #Remove results from query above. 
                res = res.RemoveAll(removeRes)
        else:
            res = qry.Select()
        application.clientMode = True
        filteredParties = res 
    elif application.searchMode.GetData() == 'Depot':
        sDep = application.shpDepot.GetData()
        if sDep != '':
            if sDep == 'Yes':
                qry.AddAttrNodeBool('ShapingDepot', True)
            else:
                qry.AddAttrNodeBool('ShapingDepot', False)
        wDep = application.warehDepot.GetData()
        if wDep != '':
            if wDep == 'Yes':
                qry.AddAttrNodeBool('WarehouseDepot', True)
            else:
                qry.AddAttrNodeBool('WarehouseDepot', False)
        plDep = application.pnlDepot.GetData() 
        if plDep != '':
            if plDep == 'Yes':
                qry.AddAttrNodeBool('PnlDepot', True)
            else:
                qry.AddAttrNodeBool('PnlDepot', False)
        uDep = application.unknDepot.GetData()
        if uDep != '':
            if uDep == 'Yes':
                qry.AddAttrNodeBool('DefaultDepot', True)
            else:
                qry.AddAttrNodeBool('DefaultDepot', False)             
        defBlk = application.defBlkAcc.GetData()
        if defBlk != '':
            try:
                if defBlk == 'Yes':
                    qry.AddAttrNodeBool('AdditionalInfo.DefBlockAccount', True)
                else:
                    qry.AddAttrNodeBool('AdditionalInfo.DefBlockAccount', False)
            except:
                pass
        noCl = application.noClient.GetData()
        if noCl == 'Has no client as parent':
            filteredParties = qry.Select()
            qry.AddAttrNode('Parent.Type', 'Equal', 'Client')
            removeItems = qry.Select()
            filteredParties = filteredParties.RemoveAll(removeItems)
        else: # noCl == '' or 'Belongs to a client'
            if noCl == 'Belongs to a client':
                qry.AddAttrNode('Parent.Type', 'Equal', 'Client')
            filteredParties = qry.Select()
        application.clientMode = False

        comGrp = application.commFld.GetData()
        if comGrp != '':
            resCom = acm.FSet()
            comQry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
            comQry.AddAttrNode('model.modelCategory', 'equal', 'commission')
            if comGrp == 'No group':
                for com in comQry.Select():
                    depot = com.Depot()
                    if depot != None:
                        resCom.Add(depot)
                filteredParties = filteredParties.RemoveAll(resCom)
            else:
                #Search for the given slope. 
                slope = application.commSlopeFld.GetData()
                for com in comQry.Select():
                    depot = com.Depot()
                    if depot != None:
                        for curve in com.Curve():
                            for interval in curve.Intervals():
                                if slope == '' or str(interval.Slope()) == slope:
                                    resCom.Add(depot)
                filteredParties = filteredParties.Intersection(resCom)
        comShrGrp = application.commShrFld.GetData()    
        if comShrGrp != '':
            resComShr = acm.FSet()
            comShrQry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
            comShrQry.AddAttrNode('model.modelCategory', 'equal', 'commission sharing')
            if comShrGrp == 'No group':
                for com in comShrQry.Select():
                    depot = com.Depot()
                    if depot != None:
                        resComShr.Add(depot)
                filteredParties = filteredParties.RemoveAll(resComShr)
            else:
                #Search for the given slope. 
                slope = application.commShrSlopeFld.GetData()
                for com in comShrQry.Select():
                    depot = com.Depot()
                    if depot != None:
                        for curve in com.Curve():
                            for interval in curve.Intervals():
                                if slope == '' or str(interval.Slope()) == slope:
                                    resComShr.Add(depot)
                filteredParties = filteredParties.Intersection(resComShr)
        
    """ Account groups """
    accGrps = application.accountGrps.GetData()
    
    if accGrps != '':
        res = acm.FSet()
        accGrps = accGrps.split(',')
        for i in range (len(accGrps)):
            accQry = acm.CreateFASQLQuery(acm.FParty, 'OR')
            for j in range (1, 11):
                try: 
                    accQry.AddAttrNode('AdditionalInfo.AccountGroup%i'%j, 'RE_LIKE_NOCASE', '*%s*'%accGrps[i])
                except:
                    pass
            if i == 0:
                res = accQry.Select()
            else:
                res = res.Intersection(accQry.Select())
                
        filteredParties = filteredParties.Intersection(res)


    sortby=application.orderBy.GetData() #Sort data. 
    application.filteredParties = filteredParties.AsIndexedCollection().SortByProperty(getSortOn(sortby), getSortOrder(sortby))

    application.noParties = application.filteredParties.Size()
    application.nextParty = 0
    if application.noParties >= LOAD_RANGE:
        application.addMoreClients.Editable(True)
    application.skippedDepots = 0
    LoadFilteredParties(application, None)

def getSortOrder(sort_by):
    if '(A-Z)' in sort_by or '(Ascending)' in sort_by:
        return True 
    elif '(Z-A)' in sort_by or '(Descending)' in sort_by:
        return False
    return True

def getSortOn(sort_by):
    if 'Name' in sort_by:
        return "StringKey"
    elif 'Update Time' in sort_by:
        return "UpdateTime" 
    for pType in  acm.CreateFASQLQuery(acm.FPartyAliasType, 'AND').Select():
        if pType.Name() in sort_by:
            return ("PartyAlias."+pType.Name())
    return "StringKey"

def TreeSelectionChange(application, cd):
    item = application.treeView.GetSelectedItem()
    if item == None or item.GetData() == None:
        application.depotConditions.Clear()
        return
    party = item.GetData()
    global selectedItem
    if party == selectedItem: #Only continue if new selection
        return
    selectedItem = party
    if party.Type() == 'Client':
        application.depotConditions.Clear()
    elif party.Type() == 'Depot':
        FillList(application, party)

def FillList(application, depot):
    depCondList = application.depotConditions
    depCondList.Clear()
    rootItem = depCondList.GetRootItem()
    #Find all commission conditions
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('model.modelCategory', 'Equal', 'Commission')
    res = qry.Select() 

    #Remove all conditions with client group, client or depot. 
    qry = acm.CreateFASQLQuery(acm.FCondition, 'OR')
    qry.AddAttrNode('clientGroup.Name', 're_like_nocase', '*')
    qry.AddAttrNode('client.Name', 're_like_nocase', '*')
    qry.AddAttrNode('depot.Name', 're_like_nocase', '*')
    res = res.RemoveAll(qry.Select())
    
    #Add commission condition with correct client group, client or depot
    qry = acm.CreateFASQLQuery(acm.FCondition, 'OR')
    if depot.Parent() != None:
        a = qry.AddOpNode('AND')
        a.AddAttrNode('model.modelCategory', 'EQUAL', 'Commission')
        a.AddAttrNode('clientGroup.Parties.Party.Name', 'EQUAL', depot.Parent().Name())
        b = qry.AddOpNode('AND')
        b.AddAttrNode('model.modelCategory', 'EQUAL', 'Commission')
        b.AddAttrNode('client.Name', 'EQUAL', depot.Parent().Name())
    c = qry.AddOpNode('AND')
    c.AddAttrNode('model.modelCategory', 'EQUAL', 'Commission')
    c.AddAttrNode('depot.Name', 'EQUAL', depot.Name())
    res = res.Union(qry.Select())
    
    res = res.AsIndexedCollection()
    for condition in res.SortByProperty('Priority'):
        if ((condition.Client() != None) and (condition.Client() != depot.Parent())) or ((condition.Depot() != None) and (condition.Depot() != depot)):
            continue
        item = rootItem.AddChild()
        item.Label(condition.StringKey())
        FillColumns(item, condition)
        item.SetData(condition)

def FillColumns(listItem, condition):
    listItem.Label(condition.Priority(), 1)
    listItem.Label(condition.MarketGroup(), 2)
    listItem.Label(condition.Market(), 3)
    listItem.Label(condition.Segment(), 4)
    listItem.Label(condition.Instrument(), 5)
    listItem.Label(condition.Currency(), 6)
    listItem.Label(condition.ClientGroup(), 7)
    listItem.Label(condition.Client(), 8)
    listItem.Label(condition.Depot(), 9)
    if condition.BuySell() == 'Undefined':
        listItem.Label('', 10)
    else:
        listItem.Label(condition.BuySell(), 10)
    for curve in condition.Curve():
        listItem.Label(curve.CalcMode(), 11)
        listItem.Label(curve.CurveType(), 12)
        for interval in curve.Intervals():
            listItem.Label(interval.Slope(), 13)

def OpenParty(application, cd):
    item = application.treeView.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    acm.UX().SessionManager().StartApplication('Party Definition', item.GetData())

def OpenCondition(application, cd):
    item = application.depotConditions.GetSelectedItem()
    if item == None or item.GetData() == None:
        return
    acm.UX().SessionManager().StartApplication('Charges', item.GetData())

def partyAdded(treeRoot, party):
    """ If the party is added to the root, return true. False otherwise. """
    for child in treeRoot.Children():
        if child.GetData() == party:
            return True
    return False
            
def AddChild(application, child, item):
    """ Add a child of type depot to the client """
    if child.Type() == 'Depot': #Only interested in depot
        treeChild = item.AddChild()
        AddItem(application, child, treeChild)

def AddItem(application, party, item):
    """Calls all column functions"""
    item.Label(party.Name())
    item.Icon(party.Icon(), party.Icon())
    item.SetData(party)
    i = 1
    for col in application.columns:
        if col == 'AIMS Entity':
            if party.AimsEntity():
                item.Label('Yes', i)
            else:
                item.Label('No', i)
        elif acm.CreateFASQLQuery(acm.FPartyAliasType, 'AND').Select().Includes(col):
            str = ""
            for alias in party.Aliases():
                if alias.Type() == col:
                    str += alias.Alias() + ", "
            str = str[:-2]
            item.Label(str, i)
        elif col == 'AccountGroups':
            str = ""
            addInfos = party.AddInfos()
            for addInfo in addInfos:
                if 'AccountGroup' == addInfo.AddInf().Name()[:12]:
                    str += addInfo.FieldValue() + ", "
            item.Label(str[:-2], i)
        elif col == 'TradePriceNumOfDec':
            try:
                addInfo = party.AdditionalInfo().TradePriceNumOfDec()
                item.Label(addInfo, i)
            except:
                pass
        elif col == 'Update Time':
            item.Label(acm.Time.DateFromTime(party.UpdateTime()), i)
        elif col == 'PtyId2':
            item.Label(party.Id2(), i)

        if party.Type() == 'Client':
            if col == 'Fix Client':
                if party.FixClient()=='Yes':
                    item.Label('Yes', i)
                else:
                    item.Label('No', i)
        elif party.Type() == 'Depot':
            if col == 'Shaping Depot':
                if party.ShapingDepot():
                    item.Label('Yes', i)
            elif col == 'Warehouse Depot':
                if party.WarehouseDepot():
                    item.Label('Yes', i)
            elif col == 'Profit/Loss Depot':
                if party.PnlDepot():
                    item.Label('Yes', i)
            elif col == 'Unknown Depot':
                if party.DefaultDepot():
                    item.Label('Yes', i)
            elif col == 'DefBlockAccount':
                try:
                    addInfo = party.AdditionalInfo().DefBlockAccount()
                    if addInfo==True:
                        item.Label("Yes", i)
                    elif addInfo == False:
                        item.Label("No", i)
                except:
                    pass
            elif col == 'Commission: Slope':
                qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
                qry.AddAttrNode('model.modelCategory', 'equal', 'commission')
                qry.AddAttrNode('Depot.Id', 'EQUAL', party.Id())
                for cond in qry.Select():
                    for curve in cond.Curve():
                        for interval in curve.Intervals():
                            item.Label(interval.Slope(), i)
            elif col == 'Commission Sharing: Slope':
                qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
                qry.AddAttrNode('model.modelCategory', 'equal', 'commission sharing')
                qry.AddAttrNode('Depot.Id', 'EQUAL', party.Id())
                for cond in qry.Select():
                    for curve in cond.Curve():
                        for interval in curve.Intervals():
                            item.Label(interval.Slope(), i)
        i += 1

def AddDepotWithoutClient(application, depot): 
    global parentAdded
    treeRoot = application.treeView.GetRootItem()
    if not parentAdded:
        treeClient = treeRoot.AddChild(False)
        treeClient.Label('Depots with no client')
        treeClient.Icon('GreenBall', 'GreenBall')
        treeClient.SetData(None)
        parentAdded = True
    else:
        findItem = treeRoot.FirstChild()
        while findItem:
            if findItem.GetData() == None:
                treeClient = findItem
                break
            findItem = findItem.Sibling()
    AddChild(application, depot, treeClient)
    treeClient.Expand()

def LoadFilteredParties(application, cd):
    treeRoot = application.treeView.GetRootItem()
    if application.clientMode: #Searched for clients
        for i in range(application.nextParty, (application.nextParty+LOAD_RANGE)):
            if i >= application.noParties:
                application.addMoreClients.Editable(False)
                i = i-1
                break
            client = application.filteredParties.At(i)
            treeClient = treeRoot.AddChild()
            AddItem(application, client, treeClient)
            children = client.Children()
            for child in children:
                AddChild(application, child, treeClient)
    else: #Depot mode (Searched for depots)
        for i in range(application.nextParty, (application.nextParty+LOAD_RANGE)):
            if i >= application.noParties:
                application.addMoreClients.Editable(False)
                i = i-1
                break
            depot = application.filteredParties.At(i)
            parent = depot.Parent()
            if parent == None:
                AddDepotWithoutClient(application, depot)
                continue
            elif parent.Type() != 'Client':
                application.skippedDepots += 1
                continue
            if not partyAdded(treeRoot, parent):
                treeClient = treeRoot.AddChild()
                AddItem(application, parent, treeClient)
            else:
                findItem = treeRoot.FirstChild()
                while findItem:
                    if findItem.GetData() == parent:
                        treeClient = findItem
                        break
                    findItem = findItem.Sibling()
            AddChild(application, depot, treeClient)
            treeClient.Expand()
    application.nextParty = i+1
    application.addedClients.Label("Shows %i/%i"%(application.nextParty-application.skippedDepots, application.noParties-application.skippedDepots))


class clientViewerApplication(FUxCore.LayoutApplication):
    """ The application class, creates an overview of clients and depots that exist in the database.  """
    
    def __init__(self):
        global LOAD_RANGE, SHOW_ALL_COMMISSIONS
        try:
            LOAD_RANGE = int(ParameterFromName('ClientViewerParameters').Value().At('LoadRange').Text())
        except:
            LOAD_RANGE = 300
        try:
            if int(ParameterFromName('ClientViewerParameters').Value().At('ShowCommissionView').Text()) == 1:
                SHOW_ALL_COMMISSIONS = True
            else:
                SHOW_ALL_COMMISSIONS = False
        except:
            pass
        FUxCore.LayoutApplication.__init__(self)
        self.columns = acm.FArray()
        self.columns.AddAll(['Update Time', 'PtyId2'])
        self.columns.AddAll(acm.CreateFASQLQuery(acm.FPartyAliasType, 'AND').Select())
        self.columns = self.columns.AddAll(['AIMS Entity', 'AccountGroups', 'TradePriceNumOfDec',\
                    'Commission: Slope', 'Commission Sharing: Slope', 'DefBlockAccount',\
                    'Shaping Depot', 'Warehouse Depot', 'Profit/Loss Depot', 'Unknown Depot', 'Fix Client'])
        self.applicationPane = None
        self.clientMode = True
        self.noParties = 0
        self.nextParty = 0
        self.filteredParties = None
        self.skippedDepots = 0
        
    
    def CreateCommandCB(self):
        """ Create a command item. """
        mItems = menuItems()
        mItems.SetApplication(self)
        return mItems

    def DoChangeCreateParameters( self, createParams ):
        createParams.AutoShrink(True)
    
    def HandleCreate( self, creationContext ):
        builder = buildLayout()
        pane = creationContext.AddPane(builder, 'Pane')
        self.applicationPane = pane
        
        self.searchMode = pane.GetControl('SearchMode')
        self.searchMode.AddItem('Client')
        self.searchMode.AddItem('Depot')
        self.searchMode.SetData('Client')
        self.searchMode.AddCallback("Changed", SearchModeChanged, self)

        self.orderBy = pane.GetControl('SortBy')
        self.orderBy.AddItem('Name (A-Z)')
        self.orderBy.AddItem('Name (Z-A)')
        self.orderBy.AddItem('Update Time (Ascending)')
        self.orderBy.AddItem('Update Time (Descending)')
        for aType in acm.CreateFASQLQuery(acm.FPartyAliasType, 'AND').Select():
            self.orderBy.AddItem("Alias: " + aType.Name() +' (A-Z)')
            self.orderBy.AddItem("Alias: " + aType.Name() +' (Z-A)')
        self.orderBy.SetData('Name (A-Z)')
        
        self.aimsEnt = pane.GetControl('AimsEnt')
        self.aimsEnt.AddItem('')
        self.aimsEnt.AddItem('Yes')
        self.aimsEnt.AddItem('No')

        self.dateFld = pane.GetControl('DateField')
        self.ptyid2Fld = pane.GetControl('PtyId2Field')
        
        self.accountGrps = pane.GetControl('AccountGroups')
        self.trdPriceNODec = pane.GetControl('TradePriceNumOfDec')
        
        self.aliasType = pane.GetControl('AliasType')
        self.aliasType.AddItem('')
        self.aliasNameFld = pane.GetControl('AliasName')
        for aliasT in acm.FPartyAliasType.Select(""):
            self.aliasType.AddItem(aliasT.Name())
        
        """ Client search specifics: """
        self.noDepots = pane.GetControl('NoDepots')
        self.noDepots.AddItem('')
        self.noDepots.AddItem('Has no depots')
        self.noDepots.AddItem('Has depots')
        self.fixClnt = pane.GetControl('Fixcl')
        self.fixClnt.AddItem('')
        self.fixClnt.AddItem('Yes')
        self.fixClnt.AddItem('No')
        
        """ Depot search specifics: """
        self.noClient = pane.GetControl('NoClient')
        self.noClient.AddItem('')
        self.noClient.AddItem('Has no client as parent')
        self.noClient.AddItem('Belongs to a client')
        self.noClient.Editable(False)
        self.shpDepot = pane.GetControl('ShapingDepot')   
        self.warehDepot = pane.GetControl('WarehouseDepot') 
        self.pnlDepot = pane.GetControl('ProfitAndLossDepot') 
        self.unknDepot = pane.GetControl('UnkownDepot') 
        self.defBlkAcc = pane.GetControl('DefBlockAccount')
        self.depBoxes = [self.shpDepot, self.warehDepot, \
                            self.pnlDepot, self.unknDepot, \
                            self.defBlkAcc]
        for box in self.depBoxes:
            box.AddItem('')
            box.AddItem('Yes')
            box.AddItem('No')
            box.Editable(False)

        """ Commission and CSA specifics: """
        self.commFld = pane.GetControl('CommissionMode')
        self.commSlopeFld = pane.GetControl('Commission_Slope')
        self.commShrFld = pane.GetControl('CommissionSMode')
        self.commShrSlopeFld = pane.GetControl('CommissionSharing_Slope')
        for field in [self.commFld, self.commShrFld]:
            field.AddItem('')
            field.AddItem('No group')
            field.AddItem('Enter Slope')
            field.Editable(False)

        self.commFld.AddCallback('Changed', CommissionChange, self)
        self.commSlopeFld.Editable(False)
        self.commShrFld.AddCallback('Changed', CommissionSharingChange, self)
        self.commShrSlopeFld.Editable(False)

        self.comFields = [self.commFld, self.commShrFld, \
                                    self.commSlopeFld, self.commShrSlopeFld]

        self.allFlds = [self.searchMode, self.orderBy, self.aimsEnt, pane.GetControl('NameField'),\
                self.dateFld, self.ptyid2Fld, self.aliasType, self.aliasNameFld,\
                self.accountGrps, self.noDepots, self.fixClnt,\
                self.noClient, self.shpDepot,\
                self.warehDepot, self.pnlDepot, self.unknDepot,\
                self.defBlkAcc, self.trdPriceNODec, self.commFld,\
                self.commShrFld, self.commSlopeFld, self.commShrSlopeFld]
        for fld in self.allFlds:
            fld.AddCallback('Activate', NewSearch, self)

        """ Tree view """
        self.treeView = pane.GetControl('MyTree')
        self.treeView.EnableMultiSelect(True)
        self.treeView.AddCallback("ContextMenu", self.TreeContextMenuCB, None)
        self.treeView.AddCallback("DefaultAction", OpenParty, self)
        self.treeView.ColumnLabel(0, 'Name')
        self.treeView.ColumnWidth(0, 175)
        for col in self.columns:
            if col in ['Commission: Slope', 'Commission Sharing: Slope', 'AccountGroups']:
                self.treeView.AddColumn(col, 100) #Wider Columns
            elif col in ['AIMS Entity', 'Fix Client']:
                self.treeView.AddColumn(col, 55) #Smaller Columns
            else:
                self.treeView.AddColumn(col, 85)
        
        self.treeView.ShowColumnHeaders()
        self.treeView.SetIndent(20)
        
        """ Depot Conditions view """
        if SHOW_ALL_COMMISSIONS:
            self.depotConditions = pane.GetControl('DepotConditions')
            self.depotConditions.ShowColumnHeaders()
            
            #print model
            self.depotConditionColumns = ['Name', 'Priority', 'Mkt Group', 'Market', 'Mkt segment', 'Instrument',\
                                'Currency', 'Client Group', 'Client', 'Depot', 'Buy/Sell', 'Calc Mode', 'Curve Type', 'Slope'] #Add dynamically
            for col in self.depotConditionColumns:
                self.depotConditions.AddColumn(col, 70)
            self.depotConditions.AddCallback("DefaultAction", OpenCondition, self)

            self.treeView.AddCallback("SelectionChanged", TreeSelectionChange, self)

        """ Add data to GUI. """
        self.filteredParties = acm.FClient.Select('').SortByProperty("StringKey")
        self.noParties = self.filteredParties.Size()
        self.addMoreClients = pane.GetControl('GetMore')
        self.addMoreClients.AddCallback("Activate", LoadFilteredParties, self)
        self.addedClients = pane.GetControl('Shows')
        LoadFilteredParties(self, None)

    @FUxCore.aux_cb
    def TreeContextMenuCB(self, ud, cd): 
        #cd contains a dictionary containing a FUxContextMenuBuilder at key 'menuBuilder'
        #For a FUxTreeControl it also contains an FArray of FUxTreeItems representing the selected items at key 'items'
        menuBuilder = cd.At('menuBuilder')
        items = cd.At('items')
        objects = acm.FArray()
        for item in items:
            objects.Add(item.GetData())
        acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, objects, True, self.AddCustomContextItemsCB, None)

    def AddCustomContextItemsCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        party = self.treeView.GetSelectedItem().GetData()
        parties = self.treeView.GetSelectedItems()
        if parties.Size() < 2: #Menu for one element.
            if party == None:
                return
            elif party.Type() == 'Client':
                commands = acm.FArray()
                commands.Add(['addDepot', '', 'Add Depot', '', '', '', self.CreateCommandCB, False])
                qry = acm.CreateFASQLQuery(acm.FPartyGroupLink, 'AND')
                qry.AddAttrNode('PartyGroup.GroupType', 'EQUAL', 'Client Group')
                qry.AddAttrNode('Party.Id', 'EQUAL', party.Id())
                if qry.Select().Size()>0:
                    clientGroups = acm.FArray()
                    for link in qry.Select():
                        clientGroups.Add(['ClientGroups', '', 'Client Groups/%s'%link.PartyGroup().Name(), '%s'%link.PartyGroup().Name(),\
                            '', '', self.CreateCommandCB, False])
                    commands.AddAll(clientGroups)
                
            elif party.Type() == 'Depot':
                commands = acm.FArray()
                if getCommission(party) or getCommissionSharing(party): #Show alternatives only if available
                    commands.Add(['deleteWithDep', '', 'Delete with dependencies', '', '', '', self.CreateCommandCB, False])
                    if getCommission(party):
                        commands.Add(['openCom', '', 'Open Commission',        '', '', '', self.CreateCommandCB, False])
                    if getCommissionSharing(party):
                        commands.Add(['openComS', '', 'Open Commission Sharing', '', '', '', self.CreateCommandCB, False])
            else:
                commands = []
        else:
            commands = []
            for pty in parties:
                if pty.GetData().Type() == 'Client': #Customize for depots only. 
                    commands = []
                    break
                if getCommission(pty.GetData()) or getCommissionSharing(pty.GetData()): #Show alternatives only if available
                    commands = [['deleteWithDep_multi', '', 'Delete with dependencies', '', '', '', self.CreateCommandCB, False]]
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))

    def HandleRegisterCommands(self, builder):
        commands = [
            ['ClearFields',    'View', 'Clear Fields',     'Clear all fields', '', '', self.CreateCommandCB, False],\
            ['DoSearch',       'View', 'Search',           '',               '', '', self.CreateCommandCB, False],\
            ['PartyDefinition', 'View', 'Party Definition', '',                '', '', self.CreateCommandCB, False],\
            ['Charges',        'View', 'Charges',          '',                '', '', self.CreateCommandCB, False]]
        fileCommands = acm.FSet()
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)

    def HandleStandardFileCommandEnabled(self, commandName):
        return False

    def HandleCanStoreLayout(self):
        return False #Not implemented

    def DynamicMenuCB(self, ud, cd):
        menuBuilder = cd.At('menuBuilder')
        commands = [
            ['item1', '', 'This is dynamic',     '', '', '', self.CreateCommandCB, False],\
            ['item2', '', 'Also dynamic', '', '', '', self.CreateCommandCB, False]]
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))


    def DoChangeCreateParameters( self, createParams ):
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(False)
        createParams.LimitMinSize(False)
        createParams.AutoShrink(False)
        createParams.AdjustPanesWhenResizing(True)
        createParams.ShowMostRecentlyUsedList(True)
        
    def GetApplicationIcon(self):
        if acm.Version() < '2015.3.1':
            return "AdminConsole"
        return "FClient"
        
def buildLayout():
    """ Create the layout """
    builder = acm.FUxLayoutBuilder()
    builder.BeginHorzBox('None', 'My Control View')
    builder.  BeginVertBox('None', '', 'SearchFields')
    builder.    AddSpace(10)
    builder.    BeginHorzBox('None')
    builder.      AddSpace(5)
    builder.      BeginVertBox('None')
    builder.        AddOption('SearchMode', 'Search mode', 25, 25)
    builder.        AddOption('SortBy', 'Sort by', 25, 25)
    builder.        AddInput('NameField', 'Name', 25, 25)
    builder.        AddInput('DateField', 'Update Time (from)', 25, 25)
    builder.        AddInput('PtyId2Field', 'PtyId2', 25, 25)
    builder.        AddInput('AccountGroups', 'AccountGroups', 25, 25)
    builder.        AddInput('TradePriceNumOfDec', 'TradePriceNumOfDec', 25, 25)
    builder.        AddOption('AimsEnt', 'AIMS Entity', 25, 25)
    builder.        AddOption('AliasType', 'Alias type', 25, 25)
    builder.        AddInput('AliasName', 'Alias', 25, 25)
    builder.      EndBox()
    builder.    EndBox()
    builder.    AddSpace(5)
    builder.    BeginVertBox('EtchedIn', 'Client search')
    builder.      AddOption('NoDepots', 'Depots', 25, 25)
    builder.      AddOption('Fixcl', 'FIX Client', 25, 25)
    builder.    EndBox()
    builder.    AddSpace(5)
    builder.    BeginVertBox('EtchedIn', 'Depot search')
    builder.      AddOption('NoClient', 'Client', 25, 25)
    builder.      AddOption('ShapingDepot', 'Shaping Depot', 25, 25)
    builder.      AddOption('WarehouseDepot', 'Warehouse Depot', 25, 25)
    builder.      AddOption('ProfitAndLossDepot', 'Profit/Loss Depot', 25, 25)
    builder.      AddOption('UnkownDepot', 'Unknown Depot', 25, 25)
    builder.      AddOption('DefBlockAccount', 'DefBlockAccount', 25, 25)
    builder.      BeginVertBox('EtchedIn', 'Commissions/CSA')
    builder.        AddOption('CommissionMode', 'Commission', 22, 22)
    builder.        AddInput('Commission_Slope', '     Slope', 22, 22)
    builder.        AddOption('CommissionSMode', 'Commission Sharing', 22, 22)
    builder.        AddInput('CommissionSharing_Slope', '     Slope', 22, 22)
    builder.      EndBox()    
    builder.    EndBox()
    builder.  EndBox()
    builder.  BeginVertBox('None')
    builder.    BeginVertBox('EtchedIn', 'Tree View')
    builder.      AddTree('MyTree', 400, 250, -1, -1)
    builder.      BeginHorzBox('None')
    builder.        AddButton('GetMore', 'Show more results', True)
    builder.        AddSpace(10)
    builder.        AddLabel('Shows', 'Shows 1999999/1999999', -1, -1)
    builder.      EndBox()
    builder.    EndBox()
    builder.    AddSpace(2)
    if SHOW_ALL_COMMISSIONS:
        builder.    AddList('DepotConditions', 7, 7, 10, 100)
    builder.  EndBox()
    builder.EndBox()
    return builder
