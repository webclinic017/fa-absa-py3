""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerDialogs.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerDialogs

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Help file to the Portfolio Viewer Application that handles custom dialogs
    and functions related to them. 

-----------------------------------------------------------------------------"""
import FUxCore
import acm
import re

""" --- INSERT ITEMS WINDOWS --- """
def StartInsertParty(dialog, _):
    pty = acm.UX().Dialogs().SelectObjectsInsertItems(shell=dialog.m_fuxDlg.Shell(), aClass=acm.FParty, selectMany=False)
    if pty == None or pty.RecordType() != 'Party':
        return
    dialog.owner.SetData(pty.Name())

def StartInsertParties(application, _):
    parties = acm.UX().Dialogs().SelectObjectsInsertItems(shell=application.Shell(), aClass=acm.FParty, selectMany=True)
    if parties == None or parties.Size() < 1:
        return
    application.partiesSelected = parties
    tmp = ''
    for pty in parties:
        tmp +=  pty.Name() + ', '
    tmp = tmp[:-2]
    application.portfolioOwner.SetData(tmp)

def StartInsertClient(application, _):
    parties = acm.UX().Dialogs().SelectObjectsInsertItems(shell=application.Shell(), aClass=acm.FClient, selectMany=True)
    if parties == None or parties.Size() < 1:
        return
    application.partiesSelected = parties
    tmp = ''
    for pty in parties:
        tmp +=  pty.Name() + ', '
    tmp = tmp[:-2]
    application.depParentCtrl.SetData(tmp)

def StartInsertInstrument(application, _):
    instrument = acm.UX().Dialogs().SelectObjectsInsertItems(shell=application.Shell(), aClass=acm.FInstrument, selectMany=False)
    if instrument == None:
        return None
    application.insFilter.SetData(instrument.Name())
    application.overviewInsFilter.SetData(instrument.Name())
    application.insSelected = instrument
    return True

def StartInsertCurrency(application, _):
    curr = acm.UX().Dialogs().SelectObjectsInsertItems(shell=application.Shell(), aClass=acm.FCurrency, selectMany=False)
    if not curr:
        return None
    application.currFilter.SetData(curr.Name())
    application.overviewCurrFilter.SetData(curr.Name())
    application.currSelected = curr
    return True

""" --- CLEAR FIELDS --- """
def ClearParty(dialog, _):
    dialog.owner.SetData('')

def ClearParties(application, _):
    application.portfolioOwner.SetData('')
    application.partiesSelected = None

def ClearClients(application, _):
    application.partiesSelected = None
    application.depParentCtrl.SetData('')
    

""" --- CREATE NEW / EDIT PORTFOLIO DIALOG --- """
class newPortfolioDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.portfolio = None
        self.bindings = None
        self.m_fuxDlg = None
        self.addInfos = acm.FDictionary()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        pass

    def HandleApply( self ):
        self.bindings.Validate(True)
        if self.portfolio: #Editing portfolio
            return self.HandleApplyEdit()
        else: #Create new portfolio
            return self.HandleApplyNew()

    def HandleApplyNew(self):
        if len(self.name.GetData()):
            q = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')
            q.AddAttrNode('Name', 're_like_nocase', self.name.GetData())
            if q.Select().Size() > 0: #Make sure no portfolio has such a name. 
                return None
        else:
            return None

        name = self.name.GetData()
        assignInfo = self.assignInfo.GetData()
        typeChldNbr = self.typeChlNbr.GetData()
        ownerName = self.owner.GetData()
        if ownerName != "":
            owner = acm.FParty[ownerName]
        else:
            owner = None
        currency = acm.FCurrency[self.currency.GetData()]
        positionPairName = self.positionPair.GetData()
        if positionPairName != "":
            positionPair = acm.FCurrencyPair[positionPairName]
        else:
            positionPair = None
        isCompound = self.isComp.Checked()
        if isCompound:
            newPortfolio = acm.FCompoundPortfolio()
        else:
            newPortfolio = acm.FPhysicalPortfolio()
        newPortfolio.Name(name)
        if assignInfo != "":
            newPortfolio.AssignInfo(assignInfo)
        else:
            newPortfolio.AssignInfo(name)
        if owner:
            newPortfolio.PortfolioOwner(owner)
        newPortfolio.Currency(currency)
        if positionPair:
            newPortfolio.CurrencyPair(positionPair)
        if typeChldNbr:
            newPortfolio.TypeChlItem(typeChldNbr)

        for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
            binder = self.addInfos.At(addInfo.Name())
            if binder == None or binder.GetValue() == None or binder.GetValue == '': #Don't add
                continue
            newPortfolio.AddInfoValue(addInfo, binder.GetValue())

        newPortfolio.Commit()
        return True

    def HandleApplyEdit(self):
        changed = False
        prtf = self.portfolio
        name = self.name.GetData()
        assignInfo = self.assignInfo.GetData()
        typeCN = self.typeChlNbr.GetData()
        prtfOwner = self.owner.GetData()
        currency = self.currency.GetData()
        positionPair = self.positionPair.GetData()

        if name != prtf.Name():
            if len(name):
                q = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')
                q.AddAttrNode('Name', 're_like_nocase', name)
                if q.Select().Size() > 0:
                    return None
                changed = True
                prtf.Name(name)
            else:
                return None
        if (prtf.AssignInfo() != assignInfo):
            if assignInfo == "":
                return None
            changed = True
            prtf.AssignInfo(assignInfo)

        if prtf.TypeChlItem() != typeCN:
            changed = True
            if typeCN == '':
                typeCN = None
            prtf.TypeChlItem(typeCN)
        if (prtf.PortfolioOwner() and prtf.PortfolioOwner().Name() != prtfOwner) or (not prtf.PortfolioOwner() and prtfOwner != ""):
            changed = True
            prtf.PortfolioOwner(acm.FParty[prtfOwner])
        if prtf.Currency().Name() != currency and currency != "":
            changed = True
            prtf.Currency(acm.FCurrency[currency])
        if (prtf.CurrencyPair() and prtf.CurrencyPair().Name() != positionPair) or (not prtf.CurrencyPair() and positionPair != ""):
            changed = True
            prtf.CurrencyPair(acm.FCurrencyPair[positionPair])
        for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
            binder = self.addInfos.At(addInfo.Name())
            if binder == None or binder.GetValue() == None or binder.GetValue == '': #Don't add
                continue
            if prtf.AddInfoValue(addInfo) == binder.GetValue():
                continue
            changed = True
            prtf.AddInfoValue(addInfo, binder.GetValue())
        if changed:
            try:
                prtf.Commit()
            except:
                return None
            
        return True

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg

        #Get control of fields
        self.isComp = layout.GetControl('isComp')
        self.name = layout.GetControl('name')
        self.assignInfo = layout.GetControl('assignInfo')
        self.typeChlNbr = layout.GetControl('type_chlNbr')
        self.currency = layout.GetControl('curr')
        self.positionPair = layout.GetControl('posPair')
        self.owner = layout.GetControl('owner')
        self.openInsertParty = layout.GetControl('OpenInsertParty')
        self.clearParty = layout.GetControl('Clear')

        self.name.AddCallback("Changed", NameChanged, self)
        #Fill option boxes with data
        for curr in acm.FCurrency.Select('').SortByProperty('Name'):
            self.currency.AddItem(curr.Name())
        self.currency.SetData('EUR') #Needs to be filled - EUR is default
        self.positionPair.AddItem('')
        for posPair in acm.FCurrencyPair.Select('').SortByProperty('Name'):
            self.positionPair.AddItem(posPair.Name())
        self.typeChlNbr.AddItem('')
        choices = acm.FArray()
        choices.Add('')
        choices.AddAll(acm.FChoiceList.Select('list=PortfolioType'))
        self.typeChlNbr.Populate(choices)

        #Owner related
        self.owner.Editable(False)
        self.openInsertParty.AddCallback("Activate", StartInsertParty, self)
        self.clearParty.AddCallback("Activate", ClearParty, self)

        self.bindings.AddLayout(layout)

        #Add informative tooltip texts
        self.save = layout.GetControl('ok')
        self.save.ToolTip('Save portfolio and reload all portfolios in the application.')
        layout.GetControl('cancel').ToolTip('Discard changes and close dialog.')
    
        if self.portfolio: #Edit portfolio - fill fields with portfolio information
            self.HandleCreateEdit(dlg, layout)
        else: # Create new portfolio - fill fields with default information
            self.HandleCreateNew(dlg, layout)
        
        
    def HandleCreateNew(self, dlg, layout):
        self.m_fuxDlg.Caption('Create new portfolio')
        #Set default value in all additional info fields.
        for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
            binder = self.addInfos.At(addInfo.Name())
            if binder != None:
                binder.SetValue(addInfo.DefaultValue()) 
        self.save.Enabled(False)       

    def HandleCreateEdit(self, dlg, layout):
        self.m_fuxDlg.Caption(self.portfolio.Name())
        #Add Portfolio Data
        if self.portfolio.Compound():
            self.isComp.Checked(True)
        self.isComp.Editable(False)
        self.name.SetData(self.portfolio.Name())
        self.assignInfo.SetData(self.portfolio.AssignInfo())
        if self.portfolio.TypeChlItem():
            self.typeChlNbr.SetData(self.portfolio.TypeChlItem())
        if self.portfolio.PortfolioOwner():
            self.owner.SetData(self.portfolio.PortfolioOwner().Name())
        self.currency.SetData(self.portfolio.Currency().Name())
        if self.portfolio.CurrencyPair():
            self.positionPair.SetData(self.portfolio.CurrencyPair())
        #AddInfo Data
        for addInfo in self.portfolio.AddInfos():
            fld = self.addInfos.At(addInfo.AddInf().Name())
            if fld != None:
                fld.SetValue(addInfo.FieldValue())

def portfolioLayout(dialog):
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b. BeginHorzBox('None')
    b.  BeginVertBox('None')
    b.   AddSpace(10)
    b.   AddInput('name', 'Name*')
    b.   AddInput('assignInfo', 'Assignment Info')
    b.   AddComboBox('type_chlNbr', 'Type')
    b.   AddOption('curr', 'Currency')
    b.   AddOption('posPair', 'Position Pair')
    b.   BeginHorzBox('None')
    b.     AddInput('owner', 'Portfolio Owner')
    b.     AddSpace(1)
    b.     AddButton('OpenInsertParty', '...', 5, 5)
    b.     AddButton('Clear', 'C', 5, 5)
    b.   EndBox()
    b.   AddCheckbox('isComp', 'Compound Portfolio')
    b.  EndBox()
    b.  AddSpace(5)
    b.  BeginVertBox('None')
    b.  BeginVertBox('EtchedIn', 'Additional Infos')
    for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
        binder = dialog.addInfos.At(addInfo.Name())
        if binder != None:
            binder.BuildLayoutPart(b, addInfo.FieldName())
    b.   EndBox()
    b. EndBox()
    b. EndBox()
    b.   AddSpace(5)
    b.   BeginHorzBox('None')
    b.      AddFill()
    b.      AddButton('ok', 'Save')
    b.      AddButton('cancel', 'Cancel')
    b.      AddFill()
    b.   EndBox()
    b.EndBox()
    return b

def InitControls(dialog):
    dialog.bindings = acm.FUxDataBindings()
    dialog.bindings.AddDependent( dialog )
    for addInfo in acm.FPhysicalPortfolio().AddInfoSpecs():
        dataType = addInfo.DataTypeType()
        dataGroup = addInfo.DataTypeGroup()
        if dataType == 1: #Int
            dom = acm.GetDomain('int')
        elif dataType == 2: #Char
            dom = acm.GetDomain('char')
        elif dataType == 3: #String
            dom = acm.GetDomain('string')
        elif dataType == 4: #Double or FInstrument - Shared datatype nbr
            if dataGroup == 'Standard': #Double
                dom = acm.GetDomain('double')
            elif dataGroup == 'RecordRef': #FInstrument
                dom = acm.GetDomain('FInstrument')
        elif dataType == 5: #Bool
            dom = acm.GetDomain('bool')
        elif dataType == 6: #Date
            dom = acm.GetDomain('date')
        elif dataType == 7: #Time
            dom = acm.GetDomain('time')
        elif dataType == 17: #Portfolio
            dom = acm.GetDomain('FPhysicalPortfolio')
        elif dataType == 24: #Calendar
            dom = acm.GetDomain('FCalendar')
        elif dataType == 27: #Party
            dom = acm.GetDomain('FParty')
        elif dataType == 32: #ChoiceList
            dom = acm.GetDomain('FChoiceList')
        elif dataType == 36: #User
            dom = acm.GetDomain('FUser')
        else: #Unsupported type
            continue
        binder = dialog.bindings.AddBinder(re.sub('[^A-Za-z0-9]+', '', addInfo.Name()), dom, None)
        dialog.addInfos.AtPut(addInfo.Name(), binder)

def NameChanged(dlg, _):
    nameEntered = dlg.name.GetData()
    if nameEntered:
        dlg.save.Enabled(True)
    else:
        dlg.save.Enabled(False)

def StartEditDialog(application, portfolio):
    portfolioDialog = newPortfolioDialog()
    portfolioDialog.application = application
    portfolioDialog.portfolio = portfolio
    InitControls(portfolioDialog)
    builder = portfolioLayout(portfolioDialog)
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, portfolioDialog )

def StartCreationDialog(application, _):
    portfolioDialog = newPortfolioDialog()
    portfolioDialog.application = application
    InitControls(portfolioDialog)
    builder = portfolioLayout(portfolioDialog)
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Frame().Shell(), builder, portfolioDialog )


""" --- CREATE NEW DEPOT --- """
class CreateNewDepotDlg(FUxCore.LayoutDialog):
    """ A dialog window for creting new depots """
    def __init__(self):
        self.client = None
        self.application = None
        self.m_fuxDlg = None
        self.bindings = None
        self.dialogBindings = acm.FDictionary()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        pass

    def VerifyName(self):
        depotName = self.nameCtrl.GetData()
        if depotName == '':
            return False
        q = acm.CreateFASQLQuery('FParty', 'AND')
        q.AddAttrNode('Name', 're_like_nocase', depotName)
        if q.Select().Size() > 0:
            return False
        if not re.match("^[\w\-\040]*$", depotName): #Invalid characters
            return False
        return True

    def HandleApply(self):
        if not self.VerifyName():
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The depot name entered is invalid. Please make sure that the name is unique and only contains letters, numbers, spaces, "_" and "-" characters.')
            return None
        depot = acm.FDepot()
        depot.Name(self.nameCtrl.GetData())

        if self.ptyid2Ctrl.GetData():
            depot.Id2(self.ptyid2Ctrl.GetData())

        if self.parentCtrl.GetData():
            client = acm.FClient[self.parentCtrl.GetData()]
            if client:
                depot.Parent(client)

        depot.AimsEntity(self.aimsCtrl.Checked())
        depot.PnlDepot(self.pnlCtrl.Checked())
        depot.ShapingDepot(self.shapingCtrl.Checked())
        depot.WarehouseDepot(self.warehouseCtrl.Checked())
        depot.DefaultDepot(self.unknownCtrl.Checked())

        for addInfo in acm.FDepot().AddInfoSpecs():
            binder = self.dialogBindings.At(addInfo.Name())
            if binder and binder.GetValue() and binder.GetValue() != '':
                depot.AddInfoValue(addInfo.Name(), binder.GetValue())

        try:   
            depot.Commit()
        except Exception as e:
            print(str(e))
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'An error occurred while saving. Read the Python log for more information.')
            return None
        
        for alias in acm.FPartyAliasType.Select(''):
            binder = self.dialogBindings.At(alias.Name())
            if binder and binder.GetValue() and binder.GetValue() != '':
                newAlias = acm.FPartyAlias()
                newAlias.Type(alias)
                newAlias.Party(depot)
                newAlias.Name(binder.GetValue())
                try: 
                    newAlias.Commit()
                except:
                    print('The creation of alias %s failed. Please create the alias in the Party Definition window.'%alias.Name())

        return True

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Create new depot')
        self.bindings.AddLayout(layout)

        self.nameCtrl = layout.GetControl('name')
        self.ptyid2Ctrl = layout.GetControl('ptyid2')

        self.parentCtrl = layout.GetControl('parent')
        self.openInsertPartyBtn = layout.GetControl('OpenInsertParty')
        self.clearPartyBtn = layout.GetControl('Clear')
        self.parentCtrl.SetData(self.client.Name())
        self.parentCtrl.Editable(False)
        self.openInsertPartyBtn.AddCallback("Activate", InsertClient, self)
        self.clearPartyBtn.AddCallback("Activate", ClearClient, self)

        self.aimsCtrl = layout.GetControl('aims')
        self.pnlCtrl = layout.GetControl('pnl')
        self.shapingCtrl = layout.GetControl('shaping')
        self.warehouseCtrl = layout.GetControl('warehouse')
        self.warehouseCtrl.Editable(False)
        self.unknownCtrl = layout.GetControl('unknown')
        self.shapingCtrl.AddCallback("Activate", ShapingCtrlChecked, self)
        self.unknownCtrl.AddCallback("Activate", UnknownCtrlChecked, self)

        for addInfo in acm.FDepot().AddInfoSpecs(): #Add tool tips and default values.
            binder = self.dialogBindings.At(addInfo.Name())
            if binder:
                if addInfo.DefaultValue():
                    binder.SetValue(addInfo.DefaultValue())
                if addInfo.Description():
                    binder.ToolTip(addInfo.Description())
        for alias in acm.FPartyAliasType.Select(''):
            binder = self.dialogBindings.At(alias.Name())
            if binder:
                if alias.AliasTypeDescription():
                    binder.ToolTip(alias.AliasTypeDescription())

    def buildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    BeginVertBox('None')
        b.      AddInput('name', 'Name')
        b.      AddInput('ptyid2', 'Alias')
        b.      BeginHorzBox('None')
        b.        AddInput('parent', 'Parent')
        b.        AddSpace(1)
        b.        AddButton('OpenInsertParty', '...', 5, 5)
        b.        AddButton('Clear', 'C', 5, 5)
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Inst Sales')
        b.        AddCheckbox('aims', 'AIMS Entity')
        b.        AddCheckbox('pnl', 'Profit/Loss Depot')
        b.        AddCheckbox('shaping', 'Shaping Depot')
        b.        AddCheckbox('warehouse', 'Warehouse Depot')
        b.        AddCheckbox('unknown', 'Unknown Depot')
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('None')
        b.      BeginVertBox('EtchedIn', 'Additional Infos')

        #Add input fields for additional infos.
        for addInfo in acm.FDepot().AddInfoSpecs():
            binder = self.dialogBindings.At(addInfo.Name())
            if binder:
                binder.BuildLayoutPart(b, addInfo.FieldName())
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Aliases')

        #Add aliases (from this GUI you can create one at a time)
        for alias in acm.FPartyAliasType.Select(''):
            binder = self.dialogBindings.At(alias.Name())
            if binder:
                binder.BuildLayoutPart(b, alias.Name())

        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'Save')
        b.    AddButton('cancel', 'Cancel')
        b.    AddFill()
        b.  EndBox()
        b.EndBox()
        return b

def InitDepotControls(dialog):
    dialog.bindings = acm.FUxDataBindings()
    dialog.bindings.AddDependent(dialog)
    for alias in acm.FPartyAliasType.Select(''):
        binder = dialog.bindings.AddBinder(alias.Name(), acm.GetDomain('string'), None)
        dialog.dialogBindings.AtPut(alias.Name(), binder)

    for addInfo in acm.FDepot().AddInfoSpecs():
        dataType = addInfo.DataTypeType()
        dataGroup = addInfo.DataTypeGroup()
        if dataType == 1: #Int
            dom = acm.GetDomain('int')
        elif dataType == 2: #Char
            dom = acm.GetDomain('char')
        elif dataType == 3: #String
            dom = acm.GetDomain('string')
        elif dataType == 4: #Double or FInstrument - Shared datatype nbr
            if dataGroup == 'Standard': #Double
                dom = acm.GetDomain('double')
            elif dataGroup == 'RecordRef': #FInstrument
                dom = acm.GetDomain('FInstrument')
        elif dataType == 5: #Bool
            dom = acm.GetDomain('bool')
        elif dataType == 6: #Date
            dom = acm.GetDomain('date')
        elif dataType == 7: #Time
            dom = acm.GetDomain('time')
        elif dataType == 17: #Portfolio
            dom = acm.GetDomain('FPhysicalPortfolio')
        elif dataType == 24: #Calendar
            dom = acm.GetDomain('FCalendar')
        elif dataType == 27: #Party
            dom = acm.GetDomain('FParty')
        elif dataType == 32: #ChoiceList
            dom = acm.GetDomain('FChoiceList')
        elif dataType == 36: #User
            dom = acm.GetDomain('FUser')
        else: #Unsupported type
            continue
        binder = dialog.bindings.AddBinder(re.sub('[^A-Za-z0-9]+', '', addInfo.Name()), dom, None)
        dialog.dialogBindings.AtPut(addInfo.Name(), binder)

def InsertClient(dialog, cd):
    pty = acm.UX().Dialogs().SelectObjectsInsertItems(dialog.m_fuxDlg.Shell(), acm.FParty, False)
    if not pty:
        ClearClient(dialog, None)
        return
    dialog.parentCtrl.SetData(pty.Name())

def ClearClient(dialog, cd):
    dialog.parentCtrl.SetData('')

def UnknownCtrlChecked(dialog, cd):
    b = True
    if dialog.unknownCtrl.Checked():
        dialog.pnlCtrl.Checked(False)
        dialog.shapingCtrl.Checked(False)
        dialog.warehouseCtrl.Checked(False)
        b = False
    
    dialog.pnlCtrl.Editable(b)
    dialog.shapingCtrl.Editable(b)
    dialog.warehouseCtrl.Editable(b)

def ShapingCtrlChecked(dialog, cd):
    if dialog.shapingCtrl.Checked():
        dialog.warehouseCtrl.Editable(True)
    else:
        dialog.warehouseCtrl.Editable(False)
        dialog.warehouseCtrl.Checked(False)

def NewDepotDlg(application):
    dlg = CreateNewDepotDlg()
    dlg.application = application
    if application.tabs.GetActivePage() == 1:
        item = application.clntView.GetSelectedItem()
    elif application.tabs.GetActivePage() == 2:
        item = application.depTree.GetSelectedItem()
    else:
        return None
    if (not item) or (not item.GetData()) or (not item.GetData().Type() == 'Client'):
        return None
    dlg.client = item.GetData()
    InitDepotControls(dlg)
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)


""" --- SELECT ADDITIONAL INFOS --- """
class AdditionalInfoSelection(FUxCore.LayoutDialog):
    """ Class for adding additional infos to search with. """
    def __init__(self):
        self.application = None
        self.dlg = None
        self.dialogBindings = acm.FDictionary()
        self.addInfos = None

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        pass

    def HandleApply(self):
        if self.application.userSettings.At('defDataType') == 'Depot':
            qry = acm.CreateFASQLQuery(acm.FDepot, 'AND')
        elif self.application.userSettings.At('defDataType') == 'Portfolio':
            qry = acm.CreateFASQLQuery(acm.FPhysicalPortfolio, 'AND')

        valuesSet = False
        qryMode = self.queryMode.GetData()
        node = qry.AddOpNode(qryMode)
        retStr = ''
        for addInfo in self.addInfos:
            binder = self.dialogBindings.At(addInfo.Name())
            if binder and binder.GetValue():
                valuesSet = True
                dataType = addInfo.DataTypeType()
                dataGroup = addInfo.DataTypeGroup()
                if dataGroup == 'Standard' and (dataType == 1 or dataType == 4): #Int or double
                    node.AddAttrNodeNumerical('AdditionalInfo.%s'%addInfo.FieldName(), binder.GetValue(), binder.GetValue())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), str(binder.GetValue()), qryMode)
                elif dataGroup == 'Standard' and (dataType == 2 or dataType == 3 or dataType == 6): #Char, string, date
                    node.AddAttrNode('AdditionalInfo.%s'%addInfo.FieldName(), 'EQUAL', binder.GetValue())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), binder.GetValue(), qryMode)
                elif dataGroup == 'Standard' and dataType == 5:#Bool
                    node.AddAttrNodeBool('AdditionalInfo.%s'%addInfo.FieldName(), binder.GetValue())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), str(binder.GetValue()), qryMode)
                elif dataGroup == 'Standard' and dataType == 7: #Time
                    node.AddAttrNodeUTCTime('AdditionalInfo.%s'%addInfo.FieldName(), binder.GetValue(), binder.GetValue())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), str(binder.GetValue()), qryMode)
                elif dataGroup == 'RecordRef' and (dataType == 4 or dataType == 17 or dataType == 24): #Instrument, portfolio, calendar
                    node.AddAttrNode('AdditionalInfo.%s.Name'%addInfo.FieldName(), 'EQUAL', binder.GetValue().Name())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), binder.GetValue().Name(), qryMode)
                elif dataGroup == 'RecordRef' and (dataType == 27 or dataType == 32 or dataType == 36): #Party,ChoiceList,User
                    node.AddAttrNode('AdditionalInfo.%s.Name'%addInfo.FieldName(), 'EQUAL', binder.GetValue().Name())
                    retStr += '%s=%s %s '%(addInfo.FieldName(), binder.GetValue().Name(), qryMode)

        if valuesSet:
            self.application.addInfoNode = node
            shortenStrBy = len(self.queryMode.GetData()) + 2
            self.application.addInfosCtrl.SetData(retStr[:-shortenStrBy])
        return True

    def HandleCreate(self, dlg, layout):
        dlg.Caption('Set additional info attributes') 
        self.bindings.AddLayout(layout)
        self.queryMode = layout.GetControl('queryMode')
        self.queryMode.AddItem('AND')
        self.queryMode.AddItem('OR')
        self.queryMode.SetData('AND')

    def InitControls(self):
        self.bindings = acm.FUxDataBindings()
        self.bindings.AddDependent(self)
        self.addInfos = []
        if self.application.userSettings.At('defDataType') == 'Portfolio':
            self.addInfos = acm.FPhysicalPortfolio().AddInfoSpecs()
        elif self.application.userSettings.At('defDataType') == 'Depot':
            self.addInfos = acm.FDepot().AddInfoSpecs()

        for addInfo in self.addInfos:
            dataType = addInfo.DataTypeType()
            dataGroup = addInfo.DataTypeGroup()
            if dataType == 1: #Int
                dom = acm.GetDomain('int')
            elif dataType == 2: #Char
                dom = acm.GetDomain('char')
            elif dataType == 3: #String
                dom = acm.GetDomain('string')
            elif dataType == 4: #Double or FInstrument - Shared datatype nbr
                if dataGroup == 'Standard': #Double
                    dom = acm.GetDomain('double')
                elif dataGroup == 'RecordRef': #FInstrument
                    dom = acm.GetDomain('FInstrument')
            elif dataType == 5: #Bool
                dom = acm.GetDomain('bool')
            elif dataType == 6: #Date
                dom = acm.GetDomain('date')
            elif dataType == 7: #Time
                dom = acm.GetDomain('time')
            elif dataType == 17: #Portfolio
                dom = acm.GetDomain('FPhysicalPortfolio')
            elif dataType == 24: #Calendar
                dom = acm.GetDomain('FCalendar')
            elif dataType == 27: #Party
                dom = acm.GetDomain('FParty')
            elif dataType == 32: #ChoiceList
                dom = acm.GetDomain('FChoiceList')
            elif dataType == 36: #User
                dom = acm.GetDomain('FUser')
            else: #Unsupported type
                continue
            binder = self.bindings.AddBinder(re.sub('[^A-Za-z0-9]+', '', addInfo.Name()), dom, None)
            self.dialogBindings.AtPut(addInfo.Name(), binder)

    def BuildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. AddOption('queryMode', 'Additional Info Query Mode')
        #Add input fields for additional infos.
        for addInfo in self.addInfos:
            binder = self.dialogBindings.At(addInfo.Name())
            if binder:
                binder.BuildLayoutPart(b, addInfo.FieldName())
        b. AddSpace(5)
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Save')
        b.  AddButton('cancel', 'Cancel')
        b.  AddFill()
        b. EndBox()
        b.EndBox()
        return b

def OpenAdditionalInfoDlg(application):
    dlg = AdditionalInfoSelection()
    dlg.application = application
    dlg.InitControls()
    builder = dlg.BuildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)

""" End of file """
