""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerConditionsDlg.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerConditionsDialog

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Help File to the Portfolio Viewer Application that handles creations of 
    new conditions, shows dialogs and handles related functions.

-----------------------------------------------------------------------------"""
import FUxCore
import acm
import re

""" Dialog for copying conditions from one item to another. """
class CopyConditionsDlg(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.toItem = None
        self.fromItem = None

    def HandleApply(self):
        #Copy the selected conditions and then close the dialog.
        for item in self.modelsList.GetCheckedItems():
            condition = item.GetData()
            if condition != None:
                self.CopyCondition(condition)
        return True

    def CopyCondition(self, condition):
        newCondition = condition.Clone()
        if self.toItem.Class() == acm.FPhysicalPortfolio or self.toItem.Class() == acm.FCompoundPortfolio:
            newCondition.Portfolio(self.toItem)
        elif self.toItem.Class() == acm.FClient:
            newCondition.Client(self.toItem)
        elif self.toItem.Class() == acm.FDepot:
            newCondition.Depot(self.toItem)

        if self.toItem.Class() != self.fromItem.Class() and \
            not ((self.toItem.Class() == acm.FPhysicalPortfolio and self.fromItem.Class() == acm.FCompoundPortfolio) or \
               (self.toItem.Class() == acm.FCompoundPortfolio and self.fromItem.Class() == acm.FPhysicalPortfolio)):
            if self.fromItem.Class() == acm.FClient:
                newCondition.Client(None)
            elif self.fromItem.Class() == acm.FDepot:
                newCondition.Depot(None)
            elif self.fromItem.Class() == acm.FPhysicalPortfolio or self.fromItem.Class() == acm.FCompoundPortfolio:
                newCondition.Portfolio(None)
        
        if self.IsDuplicate(newCondition, condition.Model().Conditions()):
            print(condition.Model().Name() + ' condition not added. Duplicate to one already existing.')
            return
        try:
            newCondition.Commit()
            print('Added condition ' + newCondition.Name() + ' to model ' + condition.Model().Name())
        except:
            print('Could not copy condition ' + condition.Name() + ' for model ' + condition.Model().Name())

    def IsDuplicate(self, newCondition, modelConditions):
        for condition in modelConditions:
            if condition.Account() == newCondition.Account() and condition.Broker() == newCondition.Broker() and \
                condition.BrokerGroup() == newCondition.BrokerGroup() and condition.Client() == newCondition.Client() and \
                condition.ClientGroup() == newCondition.ClientGroup() and condition.Counterparty() == newCondition.Counterparty() and \
                condition.CounterpartyGroup() == newCondition.CounterpartyGroup() and \
                condition.Currency() == newCondition.Currency() and condition.Depot() == newCondition.Depot() and \
                condition.ExecutionType() == newCondition.ExecutionType() and condition.InsFilter() == newCondition.ExecutionType() and \
                condition.Instrument() == newCondition.Instrument() and condition.Market() == newCondition.Market() and \
                condition.MarketGroup() == newCondition.MarketGroup() and condition.Portfolio() == newCondition.Portfolio() and \
                condition.PortfolioFilter() == newCondition.PortfolioFilter() and condition.Segment() == newCondition.Segment():
                return True
        return False

    def HandleCreate(self, dlg, layout):
        dlg.Caption('Select models to copy conditions from')
        fromLabel = layout.GetControl('fromLabel')
        toLabel = layout.GetControl('toLabel')
        checkAll = layout.GetControl('checkAll')
        clearAll = layout.GetControl('clearAll')
        self.modelsList = layout.GetControl('modelsList')

        fromLabel.Label('From: '+ self.fromItem.Name() + ' ('+ self.fromItem.Class().DisplayName()+')')
        toLabel.Label('To: '+ self.toItem.Name() + ' ('+ self.toItem.Class().DisplayName()+')')
        checkAll.AddCallback('Activate', self.CheckCallback, True)
        clearAll.AddCallback('Activate', self.CheckCallback, False)

        self.modelsList.AddColumn('Name')
        self.modelsList.AddColumn('Category')
        self.modelsList.AddColumn('Type')
        self.modelsList.AddColumn('Value')
        self.modelsList.ShowColumnHeaders()
        self.modelsList.ShowCheckboxes()
        self.modelsList.EnableMultiSelect()

        root = self.modelsList.GetRootItem()
        for modelCategory in self.application.userSettings.At('modelCategories'):
            qry = acm.CreateFASQLQuery(acm.FConditionalValueModel, 'AND')
            qry.AddAttrNode('modelCategory', 'EQUAL', modelCategory)
            for model in qry.Select():
                condition = self.GetCopyableCondition(model)
                if condition:
                    node = root.AddChild()
                    node.Label(model.Name())
                    node.Label(modelCategory, 1)
                    curve = condition.Curve().First()
                    if curve:
                        node.Label(curve.CurveType(), 2)
                        node.Label(curve.MinValue(), 3)
                    node.SetData(condition)
        for i in range(0, 4):
            self.modelsList.AdjustColumnWidthToFitItems(i)

    def GetCopyableCondition(self, model):
        qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
        qry.AddAttrNode('Model.Name', 'EQUAL', model.Name())
        if self.application.userSettings.At('defDataType') == 'Portfolio':
            qry.AddAttrNode('Portfolio.Name', 'EQUAL', self.fromItem.Name())

        elif self.application.userSettings.At('defDataType') == 'Depot' and self.fromItem.Type() == 'Client':
            qry.AddAttrNode('Client.Name', 'EQUAL', self.fromItem.Name())
        elif self.application.userSettings.At('defDataType') == 'Depot' and self.fromItem.Type() == 'Depot':
            qry.AddAttrNode('Depot.Name', 'EQUAL', self.fromItem.Name())
        else:  
            return None

        res = qry.Select()
        for item in res.SortByProperty('Priority'):
            if self.toItem:
                if not self.CompareWithFilterlist(item, model.FilterList()):
                    continue #Find other one that might match. Is this correct behaviour? 
            return item
        return None

    def CompareWithFilterlist(self, condition, filterList):
        """ Check if the classes are equal (CompoundPortfolio==PhysicalPortfolio for conditions) """
        if  self.toItem.Class() == self.fromItem.Class() or \
            (self.toItem.Class() == acm.FCompoundPortfolio and self.fromItem.Class() == acm.FPhysicalPortfolio) or \
            (self.fromItem.Class() == acm.FCompoundPortfolio and self.toItem.Class() == acm.FPhysicalPortfolio):
            return True

        for filtr in  filterList.Filters(): #Make sure the filter list will support the new condition.
            if ((filtr.Account() and condition.Account()) or (not filtr.Account() and not condition.Account())) and \
                ((filtr.Broker() and condition.Broker()) or (not filtr.Broker() and not condition.Broker())) and \
                ((filtr.BrokerGroup() and condition.BrokerGroup()) or (not filtr.BrokerGroup() and not condition.BrokerGroup())) and \
                ((filtr.BuySell() and condition.BuySell() != 'Undefined') or (not filtr.BuySell() and condition.BuySell() == 'Undefined')) and \
                ((filtr.ClientGroup() and condition.ClientGroup()) or (not filtr.ClientGroup() and not condition.ClientGroup())) and \
                ((filtr.Counterparty() and condition.Counterparty()) or (not filtr.Counterparty() and not condition.Counterparty())) and \
                ((filtr.CounterpartyGroup() and condition.CounterpartyGroup()) or (not filtr.CounterpartyGroup() and not condition.CounterpartyGroup())) and \
                ((filtr.Currency() and condition.Currency()) or (not filtr.Currency() and not condition.Currency())) and \
                ((filtr.ExecutionType() and condition.ExecutionType()) or (not filtr.ExecutionType() and not condition.ExecutionType())) and \
                ((filtr.InsFilter() and condition.InsFilter()) or (not filtr.InsFilter() and not condition.InsFilter())) and \
                ((filtr.Instrument() and condition.Instrument()) or (not filtr.Instrument() and not condition.Instrument())) and \
                ((filtr.InsType() and condition.InsType() != 'None') or (not filtr.InsType() and condition.InsType() == 'None')) and \
                ((filtr.Market() and condition.Market()) or (not filtr.Market() and not condition.Market())) and \
                ((filtr.MarketGroup() and condition.MarketGroup()) or (not filtr.MarketGroup() and not condition.MarketGroup())) and \
                ((filtr.PayType() and condition.PayType() != 'None' ) or (not filtr.PayType() and condition.PayType() == 'None')) and \
                ((filtr.PortfolioFilter() and condition.PortfolioFilter()) or (not filtr.PortfolioFilter() and not condition.PortfolioFilter())) and \
                ((filtr.Segment() and condition.Segment()) or (not filtr.Segment() and not condition.Segment())) and \
                ((filtr.UndInsType() and condition.UndInsType() != 'None') or (not filtr.UndInsType() and condition.UndInsType() == 'None')) :
 
                #Type checking
                if self.toItem.Class() == acm.FClient and filtr.Client():
                    if self.fromItem.Class() == acm.FDepot and not filtr.Depot():
                        if (condition.Portfolio() and filtr.Portfolio()) or (not condition.Portfolio() and not filtr.Portfolio()):
                            return True
                    elif (self.fromItem.Class() == acm.FPhysicalPortfolio or self.fromItem.Class() == acm.FCompoundPortfolio) and not filtr.Portfolio():
                        if (condition.Depot() and filtr.Depot()) or (not condition.Depot() and not filtr.Depot()):
                            return True

                elif self.toItem.Class() == acm.FDepot and filtr.Depot():
                    if self.fromItem.Class() == acm.FClient and not filtr.Client():
                        if (condition.Portfolio() and filtr.Portfolio()) or (not condition.Portfolio() and not filtr.Portfolio()):
                            return True   
                    elif (self.fromItem.Class() == acm.FPhysicalPortfolio or self.fromItem.Class() == acm.FCompoundPortfolio) and not filtr.Portfolio():
                        if (condition.Client() and filtr.Client()) or (not condition.Client() and not filtr.Client()):
                            return True

                elif (self.toItem.Class() == acm.FPhysicalPortfolio or self.toItem.Class() == acm.FCompoundPortfolio) and filtr.Portfolio():
                    if self.fromItem.Class() == acm.FClient and not filtr.Client():
                        if (condition.Depot() and filtr.Depot()) or (not condition.Depot() and not filtr.Depot()):
                            return True   
                    elif self.fromItem.Class() == acm.FDepot and not filtr.Depot():
                        if (condition.Client() and filtr.Client()) or (not condition.Client() and not filtr.Client()):
                            return True
        return False

    
    def CheckCallback(self, check, _):
        for listItem in self.modelsList.GetRootItem().Children():
            listItem.Check(check)

    def buildLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.  AddLabel('fromLabel', 'From: THE NAME OF SELECTED ITEM (THE CLASS NAME)')
        builder.  AddLabel('toLabel', 'To: THE NAME OF SELECTED ITEM (THE CLASS NAME)')
        builder.  BeginHorzBox('None')
        builder.    AddFill()
        builder.    AddButton('checkAll', 'Check all')
        builder.    AddButton('clearAll', 'Uncheck all')
        builder.  EndBox()
        builder.  AddList('modelsList', 15, -1, 60, -1)
        builder.  AddSpace(5)
        builder.  BeginHorzBox('None')
        builder.     AddFill()
        builder.     AddButton('ok', 'Ok')
        builder.     AddButton('cancel', 'Cancel')
        builder.     AddFill()
        builder.  EndBox()
        builder.EndBox()
        return builder

def FindCopyToItem(application, fromItem):
    classes = acm.FArray()

    classes.Add(fromItem.Class())
    if classes.First() != acm.FClient:
        classes.Add(acm.FClient)
    if classes.First() != acm.FDepot:
        classes.Add(acm.FDepot)
    if classes.First() == acm.FCompoundPortfolio:
        classes.Remove(classes.First())
        classes.AtInsert(0, acm.FPhysicalPortfolio)
    elif classes.First() != acm.FPhysicalPortfolio:
        classes.Add(acm.FPhysicalPortfolio)

    item = acm.UX().Dialogs().SelectObjectsInsertItemsWithProviders(application.Shell(), classes, False)
    if item == fromItem:
        val = acm.UX().Dialogs().MessageBoxYesNo(application.Shell(), 'Warning', 'Cannot copy to self. Do you want to select another item?')
        if val == 'Button1': #select new
            return FindCopyToItem(application, fromItem)
        else: #cancel
            return None
    return item

def StartCopyConditions(application, fromItem):
    dlg = CopyConditionsDlg()
    dlg.application = application
    dlg.fromItem = fromItem
    #Are there any conditions?
    haveConditions = False
    for modelCategory in application.userSettings.At('modelCategories'):
        qry = acm.CreateFASQLQuery(acm.FConditionalValueModel, 'AND')
        qry.AddAttrNode('modelCategory', 'EQUAL', modelCategory)
        for model in qry.Select():
            condition = dlg.GetCopyableCondition(model)
            if condition:
                haveConditions = True 
                break
    if not haveConditions:
        acm.UX().Dialogs().MessageBoxInformation(application.Shell(), 'No conditions available to copy from the selected item.')
        return
    
    #Get the copy to-item
    toItem = FindCopyToItem(application, fromItem) 
    if not toItem:
        return
    
    dlg.toItem = toItem
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)

""" ----------------------------------------------------------------- """
""" --------------------- CREATE NEW CONDITION ---------------------- """
""" ----------------------------------------------------------------- """

""" Class for selecting conditional value model for new conditions. """
class SelectConditionalModelTypeDlg(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.model = None

    def HandleApply(self):
        if (not self.model.GetData()) or self.model.GetData() == '':
            return None #Nothing selected
        model = acm.FConditionalValueModel[self.model.GetData()]
        return model

    def HandleCreate(self, dlg, layout):
        dlg.Caption('Select a model for the new condition')
        
        self.modType = layout.GetControl('modType')
        self.model = layout.GetControl('model')
        self.saveBtn = layout.GetControl('ok')

        modelTypes = ['AMS Limits', 'Collateral', 'Margin']
        for modelType in modelTypes:
            self.modType.AddItem(modelType)
        self.modType.SetData('AMS Limits')
        self.modType.AddCallback('Changed', self.populateModels, None)
        self.populateModels(None, None)

    def populateModels(self, a, b):
        self.model.Clear() #Remove old data
        t = self.modType.GetData()
        res = acm.FConditionalValueModel.Select('modelCategory=%s'%t)
        if res.Size() > 0:  
            self.saveBtn.Editable(True)
            for model in res:
                self.model.AddItem(model)
            self.model.SetData(res[0])
        else:
            self.saveBtn.Editable(False)

    def buildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. AddOption('modType', 'Select model category')
        b. AddOption('model', 'Select model', 30)
        b. AddSpace(5)
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Ok')
        b.  AddButton('cancel', 'Cancel')
        b.  AddFill()
        b. EndBox()
        b.EndBox()
        return b

def StartNewConditionDlg(application):
    dlg = SelectConditionalModelTypeDlg()
    dlg.application = application
    builder = dlg.buildLayout()
    model = acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg) #User selects model
    if (not model):
        return
    return OpenConditionDlg(application, model, None)

def OpenConditionDlg(application, model, condition):
    dlg = NewConditionDlg()
    dlg.application = application
    dlg.InitControls()
    dlg.model = model
    if condition:
        dlg.condition = condition
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)

def StartNewPortfolioConditionDlg(application, _):
    treeItem = application.treeView.GetSelectedItem()
    listItem = application.prfView.GetSelectedItem()
    if treeItem == None or listItem == None: #potential error handling
        return
    return ShowNewPortfolioConditionDlg(application, treeItem.GetData(), listItem.GetData())

def ShowNewPortfolioConditionDlg(application, model, portfolio):
    dlg = NewConditionDlg()
    dlg.InitControls()
    dlg.model = model
    dlg.portfolio = portfolio
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)

def StartNewDepotConditionDlg(application):
    treeItem = application.treeView.GetSelectedItem()
    item = None
    if application.tabs.GetActivePage() == 0:
        item = application.depView.GetSelectedItem()
    elif application.tabs.GetActivePage() == 2:
        item = application.depTree.GetSelectedItem()
    if treeItem == None or item == None: #potential error handling
        return
    return ShowNewDepotConditionDlg(application, treeItem.GetData(), item.GetData())

def ShowNewDepotConditionDlg(application, model, depot):
    dlg = NewConditionDlg()
    dlg.InitControls()
    dlg.model = model
    dlg.depot = depot
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)


def StartNewClientConditionDlg(application):
    treeItem = application.treeView.GetSelectedItem()
    item = None
    if application.tabs.GetActivePage() == 1:
        item = application.clntView.GetSelectedItem()
    elif application.tabs.GetActivePage() == 2:
        item = application.depTree.GetSelectedItem()
    if treeItem == None or item == None: #potential error handling
        return
    return ShowNewClientConditionDlg(application, treeItem.GetData(), item.GetData())

def ShowNewClientConditionDlg(application, model, client):
    dlg = NewConditionDlg()
    dlg.InitControls()
    dlg.model = model
    dlg.client = client
    builder = dlg.buildLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), builder, dlg)


""" Class for creating and editing conditions. """
class NewConditionDlg(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.model = None
        self.portfolio = None
        self.depot = None
        self.client = None
        self.condition = None

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        pass

    def InitControls(self):
        self.bindings = acm.FUxDataBindings()
        self.bindings.AddDependent(self)
        self.startDayCtrl = self.bindings.AddBinder('startDateCtrl', acm.GetDomain('date'), None)
        self.endDayCtrl = self.bindings.AddBinder('endDateCtrl', acm.GetDomain('date'), None)
        self.valueCtrl = self.bindings.AddBinder('valueCtrl', acm.GetDomain('double'), None)

    def HandleApply(self):
        if not MatchesAnyFilter(self, self.model):
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The combination of selected condition parameters does not match any row in the condition filter list.')
            return None
        if Duplicate(self, self.model):
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Warning: Duplicate condition')
            return None
        if not self.ValidDates():
            return None
        if self.condition: #Edit condition option selected
            return self.HandleApply_EditCondition()

        return self.HandleApply_NewCondition()

    def HandleApply_NewCondition(self):
        newCondition = acm.FCondition()
        newCondition.Model(self.model)

        if self.accountCtrl.GetData():
            newCondition.Account(acm.FAccount[self.accountCtrl.GetData()])
        if self.brokerCtrl.GetData():
            newCondition.Broker(acm.FBroker[self.brokerCtrl.GetData()])
        if self.brokerGrpCtrl.GetData():
            newCondition.BrokerGroup(acm.FPartyGroup[self.brokerGrpCtrl.GetData()])
        newCondition.BuySell(self.b_s_Ctrl.GetData())
        if self.clientCtrl.GetData():
            newCondition.Client(acm.FClient[self.clientCtrl.GetData()])
        if self.clientGrpCtrl.GetData():
            newCondition.ClientGroup(acm.FPartyGroup[self.clientGrpCtrl.GetData()])
        if self.cptyCtrl.GetData():
            newCondition.Counterparty(acm.FCounterParty[self.cptyCtrl.GetData()])
        if self.cptyGrpCtrl.GetData():
            newCondition.CounterpartyGroup(acm.FPartyGroup[self.cptyGrpCtrl.GetData()])
        if self.conCurrCtrl.GetData():
            newCondition.Currency(acm.FCurrency[self.conCurrCtrl.GetData()])
        if self.depotCtrl.GetData():
            newCondition.Depot(acm.FDepot[self.depotCtrl.GetData()])
        if self.execCtrl.GetData(): 
            execType = acm.FChoiceList[self.execCtrl.GetData()]
            if execType and execType.List() == 'Execution Type':
                newCondition.ExecutionType(acm.FChoiceList[self.execCtrl.GetData()])
        if self.insQryCtrl.GetData():
            newCondition.InsFilter(acm.FStoredASQLQuery[self.insQryCtrl.GetData()])
        if self.insCtrl.GetData():
            newCondition.Instrument(acm.FInstrument[self.insCtrl.GetData()])
        newCondition.InsType(self.insTypeCtrl.GetData())
        if self.mktCtrl.GetData():
            newCondition.Market(acm.FMarketPlace[self.mktCtrl.GetData()])
        if self.mktGrpCtrl.GetData():
            newCondition.MarketGroup(acm.FPartyGroup[self.mktGrpCtrl.GetData()])
        if self.mktSegCtrl.GetData():
            newCondition.Segment(acm.FMarketSegment[self.mktSegCtrl.GetData()])
        newCondition.PayType(self.payTypeCtrl.GetData())
        if self.prfCtrl.GetData():
            newCondition.Portfolio(acm.FPhysicalPortfolio[self.prfCtrl.GetData()])
        if self.prfQryCtrl.GetData():
            newCondition.PortfolioFilter(acm.FStoredASQLQuery[self.prfQryCtrl.GetData()])
        newCondition.UndInsType(self.undInsTypeCtrl.GetData())

        #Validation period 
        startDay = self.startDayCtrl.GetValue()
        endDay = self.endDayCtrl.GetValue()
        if startDay != None:
            newCondition.StartDay(startDay)
        if endDay != None:
            newCondition.EndDay(endDay)

        newCurve = acm.FValueCurve()
        newCurve.CurveType(self.type.GetData())
        if self.currency.GetData() != '':
            newCurve.Currency(acm.FCurrency[self.currency.GetData()])
        val = self.valueCtrl.GetValue()    
        newCurve.MinValue(val)
        newCurve.Condition(newCondition)
       
        try:
            acm.BeginTransaction()
            newCondition.Commit()
            newCurve.Commit()
            acm.CommitTransaction()
            return True
        except:
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'An error occurred while trying to save the condition.')
            return None  

    def HandleApply_EditCondition(self):
        """ Look for attributes edited. """
        if self.condition.BuySell() != self.b_s_Ctrl.GetData():
            self.condition.BuySell(self.b_s_Ctrl.GetData())
        if self.condition.InsType() != self.insTypeCtrl.GetData():
            self.condition.InsType(self.insTypeCtrl.GetData())
        if self.condition.PayType() != self.payTypeCtrl.GetData():
            self.condition.PayType(self.payTypeCtrl.GetData())
        if self.condition.UndInsType() != self.undInsTypeCtrl.GetData():
            self.condition.UndInsType(self.undInsTypeCtrl.GetData())
        if not self.condition.MarketGroup() or self.mktGrpCtrl.GetData() != self.condition.MarketGroup().Name():
            self.condition.MarketGroup(acm.FPartyGroup[self.mktGrpCtrl.GetData()])
        if not self.condition.Market() or self.mktCtrl.GetData() != self.condition.Market().Name():
            self.condition.Market(acm.FMarketPlace[self.mktCtrl.GetData()])
        if not self.condition.Segment() or self.mktSegCtrl.GetData() != self.condition.Segment().Name():
            self.condition.Segment(acm.FMarketSegment[self.mktSegCtrl.GetData()])
        if not self.condition.Instrument() or self.insCtrl.GetData() != self.condition.Instrument().Name():
            self.condition.Instrument(acm.FInstrument[self.insCtrl.GetData()])
        if not self.condition.Currency() or self.conCurrCtrl.GetData() != self.condition.Currency().Name():
            self.condition.Currency(acm.FCurrency[self.conCurrCtrl.GetData()])
        if not self.condition.ExecutionType() or self.execCtrl.GetData() != self.condition.ExecutionType().Name():
            cList = acm.FChoiceList[self.execCtrl.GetData()]
            if cList and not cList.List() == 'Execution Type': 
                self.condition.ExecutionType(None)
            else:
                self.condition.ExecutionType(cList)
        if not self.condition.InsFilter() or self.insQryCtrl.GetData() != self.condition.InsFilter().Name():
            self.condition.InsFilter(acm.FStoredASQLQuery[self.insQryCtrl.GetData()])
        if not self.condition.ClientGroup() or self.clientGrpCtrl.GetData() != self.condition.ClientGroup().Name():
            self.condition.ClientGroup(acm.FPartyGroup[self.clientGrpCtrl.GetData()])
        if not self.condition.Client() or self.clientCtrl.GetData() != self.condition.Client().Name():
            self.condition.Client(acm.FClient[self.clientCtrl.GetData()])
        if not self.condition.CounterpartyGroup() or self.cptyGrpCtrl.GetData() != self.condition.CounterpartyGroup().Name():
            self.condition.CounterpartyGroup(acm.FPartyGroup[self.cptyGrpCtrl.GetData()])
        if not self.condition.Counterparty() or self.cptyCtrl.GetData() != self.condition.Counterparty().Name():
            self.condition.Counterparty(acm.FCounterParty[self.cptyCtrl.GetData()])
        if not self.condition.BrokerGroup() or self.brokerGrpCtrl.GetData() != self.condition.BrokerGroup().Name():
            self.condition.BrokerGroup(acm.FPartyGroup[self.brokerGrpCtrl.GetData()])
        if not self.condition.Broker() or self.brokerCtrl.GetData() != self.condition.Broker().Name():
            self.condition.Broker(acm.FBroker[self.brokerCtrl.GetData()])
        if not self.condition.Depot() or self.depotCtrl.GetData() != self.condition.Depot().Name():
            self.condition.Depot(acm.FDepot[self.depotCtrl.GetData()])
        if not self.condition.Account() or self.accountCtrl.GetData() != self.condition.Account().Name():
            self.condition.Account(acm.FAccount[self.accountCtrl.GetData()])
        if not self.condition.Portfolio() or self.prfCtrl.GetData() != self.condition.Portfolio().Name():
            if self.prfCtrl.GetData(): #Portfolio might open an entry for empty string
                self.condition.Portfolio(acm.FPhysicalPortfolio[self.prfCtrl.GetData()])
        if not self.condition.PortfolioFilter() or self.prfQryCtrl.GetData() != self.condition.PortfolioFilter().Name():
            self.condition.PortfolioFilter(acm.FStoredASQLQuery[self.prfQryCtrl.GetData()])
        
        startDay = self.startDayCtrl.GetValue()
        endDay = self.endDayCtrl.GetValue()
        if startDay != None:
            self.condition.StartDay(startDay)
        if endDay != None:
            self.condition.EndDay(endDay)

        if self.condition.Curve().Size() > 0: #Has curve
            curve = self.condition.Curve()[0]
            if curve.CurveType() != self.type.GetData():
                curve.CurveType(self.type.GetData())
            if curve.MinValue() != self.valueCtrl.GetValue():
                curve.MinValue(self.valueCtrl.GetValue())
            if self.currency.Visible() and curve.Currency() != self.currency.GetData():
                curve.Currency(self.currency.GetData())
            elif not self.currency.Visible(): #Remove any potential currencies in the field when saving. 
                curve.Currency(None)
        else: #Add new Curve
            newCurve = acm.FValueCurve()
            newCurve.CurveType(self.type.GetData())
            if self.currency.Visible():
                newCurve.Currency(acm.FCurrency[self.currency.GetData()])
            val = self.valueCtrl.GetValue()    
            newCurve.MinValue(val)
            newCurve.Condition(self.condition)
            newCurve.Commit()

        self.condition.Commit() #Commit changes to save in database
        return True

    def ValidDates(self):
        startDay = self.startDayCtrl.GetValue()
        endDay = self.endDayCtrl.GetValue()
        if startDay != None and endDay != None:
            if endDay < startDay:
                acm.UX.Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Please use an end day later than the start day.')
                return False
        return True

    def UpdateAffectLabel(self, value, _):
        affectedItems = 0
        dType = ''
        if self.application.conditionTabs.GetActivePage() == 0: #Detailed view only shows one type of condition at a time
            dType = self.application.GetActiveDataType()
        elif self.application.conditionTabs.GetActivePage() == 1: #Overview - type is the type of the selected item in tree.
            if self.application.conditionOverviewTree.GetSelectedItem() and self.application.conditionOverviewTree.GetSelectedItem().GetData():
                item = self.application.conditionOverviewTree.GetSelectedItem().GetData()
                if item.RecordType() == 'Portfolio':
                    dType = 'Portfolio'
                elif item.RecordType() == 'Party' and (item.Type() == 'Client' or item.Type() == 'Depot'):
                    dType = item.Type()

        if dType == 'Portfolio':
            if self.prfCtrl.GetData():
                affectedItems = 1
            elif self.prfQryCtrl.GetData():
                affectedItems = (acm.FStoredASQLQuery[self.prfQryCtrl.GetData()]).Query().Select().Size()
            else:
                affectedItems = acm.FPhysicalPortfolio.Select('').Size()
        elif dType == 'Depot':
            if self.depotCtrl.GetData():
                affectedItems = 1
            else:
                affectedItems = acm.FDepot.Select('').Size()
        elif dType == 'Client':
            if self.clientCtrl.GetData():
                affectedItems = 1
            elif self.clientGrpCtrl.GetData():
                affectedItems = (acm.FPartyGroup[self.clientGrpCtrl.GetData()]).Parties().Size()
            else:
                affectedItems = acm.FClient.Select('').Size()

        inPlural = ''
        if affectedItems != 1:
            inPlural = 's'

        self.affectLabel.Label('The value of this condition might affect %d %s%s.'%(affectedItems, (dType).lower(), inPlural))

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('New %s condition'%self.model.Name())
        
        self.bindings.AddLayout(layout)
        
        self.mktGrpCtrl = layout.GetControl('marketGrp')
        self.mktCtrl = layout.GetControl('market')
        self.mktSegCtrl = layout.GetControl('mktSegment')
        self.insMktSegBtn = layout.GetControl('insertSegment')
        self.clearMktSegBtn = layout.GetControl('clearSegment')
        self.insCtrl = layout.GetControl('instrument')
        self.insInstrBtn = layout.GetControl('insertInstr')
        self.clearInstrBtn = layout.GetControl('clearInstr')
        self.conCurrCtrl = layout.GetControl('conditionCurrency')
        self.b_s_Ctrl = layout.GetControl('b_s_Condition')
        self.execCtrl = layout.GetControl('execType')
        self.insTypeCtrl = layout.GetControl('insType')
        self.payTypeCtrl = layout.GetControl('payType')
        self.undInsTypeCtrl = layout.GetControl('undInsType')
        self.insQryCtrl = layout.GetControl('insQry')
        self.clientGrpCtrl = layout.GetControl('clientGrp')
        self.clientCtrl = layout.GetControl('client')
        self.insClientBtn = layout.GetControl('insertClient')
        self.clearClientBtn = layout.GetControl('clearClient')
        self.cptyGrpCtrl = layout.GetControl('cptyGroup')
        self.cptyCtrl = layout.GetControl('cpty')
        self.insCptyBtn = layout.GetControl('insertCpty')
        self.clearCptyBtn = layout.GetControl('clearCpty')
        self.brokerGrpCtrl = layout.GetControl('brkGrp')
        self.brokerCtrl = layout.GetControl('broker')
        self.insBrokerBtn = layout.GetControl('insertBroker')
        self.clearBrokerBtn = layout.GetControl('clearBroker')
        self.depotCtrl = layout.GetControl('depot')
        self.insDepotBtn = layout.GetControl('insertDepot')
        self.clearDepotBtn = layout.GetControl('clearDepot')
        self.accountCtrl = layout.GetControl('account')
        self.prfCtrl = layout.GetControl('prtf')
        self.insertPrfBtn = layout.GetControl('insertPrf')
        self.clearPrfBtn = layout.GetControl('clearPrf')
        self.prfQryCtrl = layout.GetControl('prfQry')

        self.allFields = [
            self.mktGrpCtrl, self.mktCtrl, self.mktSegCtrl, self.insMktSegBtn, self.clearMktSegBtn, self.insCtrl,\
            self.insInstrBtn, self.clearInstrBtn, self.conCurrCtrl, self.b_s_Ctrl, self.execCtrl, self.insTypeCtrl,\
            self.payTypeCtrl, self.undInsTypeCtrl, self.insQryCtrl, self.clientGrpCtrl, self.clientCtrl,\
            self.insClientBtn, self.clearClientBtn, self.cptyGrpCtrl, self.cptyCtrl, self.insCptyBtn, self.clearCptyBtn,\
            self.brokerGrpCtrl, self.brokerCtrl, self.insBrokerBtn, self.clearBrokerBtn, self.depotCtrl, self.insDepotBtn,\
            self.clearDepotBtn, self.accountCtrl, self.prfCtrl, self.insertPrfBtn, self.clearPrfBtn, self.prfQryCtrl
            ]
        for fld in self.allFields:
            fld.Visible(False)

        #ADD DATA TO FIELDS
        #Items to option ctrl
        AddItemsToOptionCtrl(self.accountCtrl, acm.FAccount.Select('').SortByProperty('Name'))
        AddItemsToOptionCtrl(self.conCurrCtrl, acm.FCurrency.Select('').SortByProperty('Name'))
        AddItemsToOptionCtrl(self.execCtrl, acm.FChoiceList.Select('list=Execution Type').SortByProperty('Name'))
        #Enums
        AddEnumItemsToOptionCtrl(self.b_s_Ctrl, acm.FEnumeration['enum(BuyOrSell)'].Values(), 'Undefined')
        AddEnumItemsToOptionCtrl(self.payTypeCtrl, acm.FEnumeration['enum(PayType)'].Values(), 'None')
        #Broker
        AddItemsToOptionCtrl(self.brokerGrpCtrl, acm.FPartyGroup.Select('groupType=Broker Group').SortByProperty('Name'))
        self.brokerCtrl.Editable(False)
        self.insBrokerBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FBroker, self.brokerCtrl]) #Send self and acm type
        self.clearBrokerBtn.AddCallback('Activate', ClearFieldOfType, self.brokerCtrl)
        #Client
        if self.client != None:
            self.clientCtrl.SetData(self.client)
        AddItemsToOptionCtrl(self.clientGrpCtrl, acm.FPartyGroup.Select('groupType=Client Group').SortByProperty('Name'))
        self.clientCtrl.Editable(False)
        self.insClientBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FClient, self.clientCtrl])
        self.clearClientBtn.AddCallback('Activate', ClearFieldOfType, self.clientCtrl)
        #Counterparty
        AddItemsToOptionCtrl(self.cptyGrpCtrl, acm.FPartyGroup.Select('groupType=Counterparty group').SortByProperty('Name'))
        self.cptyCtrl.Editable(False)
        self.insCptyBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FCounterParty, self.cptyCtrl])
        self.clearCptyBtn.AddCallback('Activate', ClearFieldOfType, self.cptyCtrl)
        #Depot
        if self.depot != None:
            self.depotCtrl.SetData(self.depot)
        self.depotCtrl.Editable(False)
        self.insDepotBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FDepot, self.depotCtrl])
        self.clearDepotBtn.AddCallback('Activate', ClearFieldOfType, self.depotCtrl)
        #Instrument
        AddItemsToOptionCtrl(self.insQryCtrl, acm.FStoredASQLQuery.Select('subType=FInstrument').SortByProperty('Name'))
        self.insCtrl.Editable(False)
        self.insInstrBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FInstrument, self.insCtrl])
        self.clearInstrBtn.AddCallback('Activate', ClearFieldOfType, self.insCtrl)
        insTypes = acm.FEnumeration['enum(InsType)'].Values()
        AddEnumItemsToOptionCtrl(self.insTypeCtrl, insTypes, 'None')
        AddEnumItemsToOptionCtrl(self.undInsTypeCtrl, insTypes, 'None')
        #Market
        AddItemsToOptionCtrl(self.mktGrpCtrl, acm.FPartyGroup.Select('groupType=Market Group').SortByProperty('Name'))
        AddItemsToOptionCtrl(self.mktCtrl, acm.FMarketPlace.Select('').SortByProperty('Name'))
        self.mktSegCtrl.Editable(False)
        self.insMktSegBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FMarketSegment, self.mktSegCtrl])
        self.clearMktSegBtn.AddCallback('Activate', ClearFieldOfType, self.mktSegCtrl)
        #Portfolio
        if self.portfolio != None:
            self.prfCtrl.SetData(self.portfolio)
        self.prfCtrl.Editable(False)
        self.insertPrfBtn.AddCallback('Activate', OpenInsertItemsOfType, [self, acm.FPhysicalPortfolio, self.prfCtrl])
        self.clearPrfBtn.AddCallback('Activate', ClearFieldOfType, self.prfCtrl)
        AddItemsToOptionCtrl(self.prfQryCtrl, acm.FStoredASQLQuery.Select('subType=FPhysicalPortfolio').SortByProperty('Name'))

        #Make available fields visible if any filter uses that filter.
        for filtr in self.model.FilterList().Filters():
            self.setVisible(filtr.Account(), [self.accountCtrl])
            self.setVisible(filtr.Broker(), [self.brokerCtrl, self.insBrokerBtn, self.clearBrokerBtn])
            self.setVisible(filtr.BrokerGroup(), [self.brokerGrpCtrl])            
            self.setVisible(filtr.BuySell(), [self.b_s_Ctrl])
            self.setVisible(filtr.Client(), [self.clientCtrl, self.insClientBtn, self.clearClientBtn])
            self.setVisible(filtr.ClientGroup(), [self.clientGrpCtrl])
            self.setVisible(filtr.Counterparty(), [self.cptyCtrl, self.insCptyBtn, self.clearCptyBtn])
            self.setVisible(filtr.CounterpartyGroup(), [self.cptyGrpCtrl])
            self.setVisible(filtr.Currency(), [self.conCurrCtrl])
            self.setVisible(filtr.Depot(), [self.depotCtrl, self.insDepotBtn, self.clearDepotBtn])
            self.setVisible(filtr.ExecutionType(), [self.execCtrl])
            self.setVisible(filtr.InsFilter(), [self.insQryCtrl])
            self.setVisible(filtr.Instrument(), [self.insCtrl, self.insInstrBtn, self.clearInstrBtn])
            self.setVisible(filtr.InsType(), [self.insTypeCtrl])
            self.setVisible(filtr.Market(), [self.mktCtrl])
            self.setVisible(filtr.MarketGroup(), [self.mktGrpCtrl])
            self.setVisible(filtr.PayType(), [self.payTypeCtrl])
            self.setVisible(filtr.Portfolio(), [self.prfCtrl, self.insertPrfBtn, self.clearPrfBtn])
            self.setVisible(filtr.PortfolioFilter(), [self.prfQryCtrl])
            self.setVisible(filtr.Segment(), [self.mktSegCtrl, self.insMktSegBtn, self.clearMktSegBtn])
            self.setVisible(filtr.UndInsType(), [self.undInsTypeCtrl])

        #Condition data fields.
        self.type = layout.GetControl('type')
        self.valueCtrl.SetValue(0)
        self.currency = layout.GetControl('currency')
        self.currency.Visible(False) #Not used in all conditions.
        self.suitCategory()

        if self.condition: #If set - edit condition mode (read all condition data)
            populateWData(self, self.condition)

        self.affectLabel = layout.GetControl('affectLabel')
        self.updateAffectValue = layout.GetControl('updateAffectValue')
        if not self.condition:
            self.affectLabel.Visible(False)
            self.updateAffectValue.Visible(False)
        else:
            self.updateAffectValue.AddCallback('Activate', self.UpdateAffectLabel, None)
            self.UpdateAffectLabel(None, None)

    def setVisible(self, hasField, fieldsToShow):
        #Use to set certain fields visible based on if it has the field.
        if hasField:
            for field in fieldsToShow: 
                field.Visible(True)

    def suitCategory(self):
        modelCategory = self.model.ModelCategory()
        if modelCategory == 'AMS Limits':
            self.type.AddItem('Flat Rate')
            self.type.SetData('Flat Rate')
            if 'Value' in self.model.Name():
                currencies = acm.FCurrency.Select('').SortByProperty('Name')
                for curr in currencies:
                    self.currency.AddItem(curr.Name())
                self.currency.SetData('EUR')
                self.currency.Visible(True)

        elif modelCategory == 'Collateral':
            if self.model.Name() == 'Haircut':
                self.type.AddItem('Percentage')
                self.type.SetData('Percentage')
            else: #Quantity Cap, Price Cap or Value Cap.
                self.type.AddItem('Flat Rate')
                self.type.SetData('Flat Rate')
                if self.model.Name() == 'Price Cap' or self.model.Name() == 'Value Cap':
                    currencies = acm.FCurrency.Select('').SortByProperty('Name')
                    for curr in currencies:
                        self.currency.AddItem(curr.Name())
                    self.currency.SetData('EUR')
                    self.currency.Visible(True)
        elif modelCategory == 'Margin':
            self.type.AddItem('Percentage')
            if self.model.Name() == 'Initial Margin':
                self.type.AddItem('Basis Points')
                self.type.AddItem('Per Unit')
                self.type.AddCallback('Changed', self.enableCurrency, None)
            self.type.SetData('Percentage')

    def enableCurrency(self, data, _):
        if self.type.GetData() == 'Per Unit':
            self.currency.Visible(True)
            currencies = acm.FCurrency.Select('').SortByProperty('Name')
            for curr in currencies:
                self.currency.AddItem(curr.Name())
            self.currency.SetData('EUR')
        else: 
            self.currency.SetData('')
            self.currency.Visible(False)

    def buildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('EtchedIn', 'Condition')
        b.    BeginVertBox('None')
        b.      AddOption('marketGrp', 'Market Group')
        b.      AddOption('market', 'Market')
        b.      BeginHorzBox('None')
        b.        AddInput('mktSegment', 'Market Segment')
        b.        AddButton('insertSegment', '...', True, True)
        b.        AddButton('clearSegment', 'C', True, True)
        b.      EndBox()
        b.      BeginHorzBox('None')
        b.        AddInput('instrument', 'Instrument')
        b.        AddButton('insertInstr', '...', True, True)
        b.        AddButton('clearInstr', 'C', True, True)
        b.      EndBox()
        b.      AddOption('conditionCurrency', 'Currency')
        b.      AddOption('b_s_Condition', 'B/S condition')
        b.      AddOption('execType', 'Execution type')
        b.      AddOption('insType', 'Ins type')
        b.      AddOption('payType', 'Pay type')
        b.      AddOption('undInsType', 'Und ins type')
        b.      AddOption('insQry', 'Ins Query')
        b.    EndBox()
        b.    BeginVertBox('None')
        b.      AddOption('clientGrp', 'Client Group')
        b.      BeginHorzBox('None')
        b.        AddInput('client', 'Client')
        b.        AddButton('insertClient', '...', True, True)
        b.        AddButton('clearClient', 'C', True, True)
        b.      EndBox()
        b.      AddOption('cptyGroup', 'Counterparty Group')
        b.      BeginHorzBox('None')
        b.        AddInput('cpty', 'Counterparty')
        b.        AddButton('insertCpty', '...', True, True)
        b.        AddButton('clearCpty', 'C', True, True)
        b.      EndBox()
        b.      AddOption('brkGrp', 'Broker Group')
        b.      BeginHorzBox('None')
        b.        AddInput('broker', 'Broker')
        b.        AddButton('insertBroker', '...', True, True)
        b.        AddButton('clearBroker', 'C', True, True)
        b.      EndBox()
        b.      BeginHorzBox('None')
        b.        AddInput('depot', 'Depot')
        b.        AddButton('insertDepot', '...', True, True)
        b.        AddButton('clearDepot', 'C', True, True)
        b.      EndBox()
        b.      AddOption('account', 'Account')
        b.      BeginHorzBox('None')
        b.        AddInput('prtf', 'Portfolio')
        b.        AddButton('insertPrf', '...', True, True)
        b.        AddButton('clearPrf', 'C', True, True)
        b.      EndBox()
        b.      AddOption('prfQry', 'Portfolio Query')
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Condition validity period')
        self.startDayCtrl.BuildLayoutPart(b, 'Start day')
        self.endDayCtrl.BuildLayoutPart(b, 'End day')
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Data')
        b.    AddOption('type', 'Type')
        b.    BeginVertBox('None')
        self.valueCtrl.BuildLayoutPart(b, 'Value')
        b.      AddOption('currency', 'Currency')
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Note!')
        b.    AddLabel('affectLabel', 'The value of this condition might affect 2000000 portfolios.')
        b.    AddFill()
        b.    AddButton('updateAffectValue', 'Refresh', True, True)
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginHorzBox('None')
        b.   AddFill()
        b.   AddButton('ok', 'Save')
        b.   AddButton('cancel', 'Cancel')
        b.   AddFill()
        b.  EndBox()
        b.EndBox()
        return b

def OpenInsertItemsOfType(inputData, _):
    """ Opens Insert Items with the specified type """
    dialog = inputData[0]
    acmType = inputData[1]
    fld = inputData[2]
    selItem = acm.UX().Dialogs().SelectObjectsInsertItems(dialog.m_fuxDlg.Shell(), acmType, False)
    if selItem:
        fld.SetData(selItem)

def ClearFieldOfType(inputField, _):
    inputField.SetData('')

def AddItemsToOptionCtrl(ctrl, items):
    ctrl.AddItem('')
    for it in items:
        ctrl.AddItem(it.Name())
    ctrl.SetData('')

def AddEnumItemsToOptionCtrl(ctrl, items, defaultVal):
    for it in items:
        ctrl.AddItem(it)
    ctrl.SetData(defaultVal)

def MatchesAnyFilter(dialog, model):
    """ Returns true if the model has any filter list matching the model"""
    filterAttr = acm.FArray()
    filterAttr.AddAll(['Account', 'Broker', 'BrokerGroup', 'BuySell', 'Client', 'ClientGroup', 'Counterparty',\
        'CounterpartyGroup', 'Currency', 'Depot', 'ExecutionType', 'InsFilter', 'Instrument', 'InsType', 'Market',\
        'MarketGroup', 'PayType', 'Portfolio', 'PortfolioFilter', 'Segment', 'UndInsType'])

    condAttr = acm.FArray()
    for i in range (0, filterAttr.Size()):
        condAttr.AtInsert(i, False)

    if dialog.accountCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Account'), True)
    if dialog.brokerCtrl.GetData() != '':
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Broker'), True)
    if dialog.brokerGrpCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('BrokerGroup'), True)
    if dialog.b_s_Ctrl.GetData() != 'Undefined':
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('BuySell'), True)
    if dialog.clientCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Client'), True)
    if dialog.clientGrpCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('ClientGroup'), True)
    if dialog.cptyCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Counterparty'), True)
    if dialog.cptyGrpCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('CounterpartyGroup'), True)
    if dialog.conCurrCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Currency'), True)
    if dialog.depotCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Depot'), True)
    if dialog.execCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('ExecutionType'), True)
    if dialog.insQryCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('InsFilter'), True)
    if dialog.insCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Instrument'), True)
    if dialog.insTypeCtrl.GetData() != 'None':
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('InsType'), True)
    if dialog.mktCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Market'), True)
    if dialog.mktGrpCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('MarketGroup'), True)
    if dialog.payTypeCtrl.GetData() != 'None':
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('PayType'), True)
    if dialog.prfCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Portfolio'), True)
    if dialog.prfQryCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('PortfolioFilter'), True)
    if dialog.mktSegCtrl.GetData():
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('Segment'), True)
    if dialog.undInsTypeCtrl.GetData() != 'None':
        condAttr.AtPut(filterAttr.IndexOfFirstEqual('UndInsType'), True)

    qry = acm.CreateFASQLQuery(acm.FConditionFilter, 'AND')
    qry.AddAttrNode('FilterList.Models.Name', 'EQUAL', model.Name())
    #Loop 
    for i in range (0, filterAttr.Size()):
        qry.AddAttrNodeBool(filterAttr.At(i), condAttr.At(i))
    res = qry.Select()
    if res.Size() > 0:
        return True
    return False

def Duplicate(dialog, model):
    """ Check all input fields and deter if the condition parameters will generate
        a condition identical to one that already exists for the selected model. 
        Returns true if one such condition exists.
    """
    qry = acm.CreateFASQLQuery(acm.FCondition, 'AND')
    qry.AddAttrNode('Model.Name', 'EQUAl', model.Name())

    if dialog.accountCtrl.GetData():
        qry.AddAttrNode('Account.Name', 'EQUAL', dialog.accountCtrl.GetData())
    if dialog.brokerCtrl.GetData() != '':
        qry.AddAttrNode('Broker.Name', 'EQUAL', dialog.brokerCtrl.GetData())
    if dialog.brokerGrpCtrl.GetData():
        qry.AddAttrNode('BrokerGroup.Name', 'EQUAL', dialog.brokerGrpCtrl.GetData())
    qry.AddAttrNode('BuySell', 'EQUAL', dialog.b_s_Ctrl.GetData())
    if dialog.clientCtrl.GetData():
        qry.AddAttrNode('Client.Name', 'EQUAL', dialog.clientCtrl.GetData())
    if dialog.clientGrpCtrl.GetData():
        qry.AddAttrNode('ClientGroup.Name', 'EQUAL', dialog.clientGrpCtrl.GetData())
    if dialog.cptyCtrl.GetData():
        qry.AddAttrNode('Counterparty.Name', 'EQUAL', dialog.cptyCtrl.GetData())
    if dialog.cptyGrpCtrl.GetData():
        qry.AddAttrNode('CounterpartyGroup.Name', 'EQUAL', dialog.cptyGrpCtrl.GetData())
    if dialog.conCurrCtrl.GetData():
        qry.AddAttrNode('Currency.Name', 'EQUAL', dialog.conCurrCtrl.GetData())
    if dialog.depotCtrl.GetData():
        qry.AddAttrNode('Depot.Name', 'EQUAL', dialog.depotCtrl.GetData())
    if dialog.execCtrl.GetData():
        qry.AddAttrNode('ExecutionType.Name', 'EQUAL', dialog.execCtrl.GetData())
    if dialog.insQryCtrl.GetData():
        qry.AddAttrNode('InsFilter.Name', 'EQUAL', dialog.insQryCtrl.GetData())
    if dialog.insCtrl.GetData():
        qry.AddAttrNode('Instrument.Name', 'EQUAL', dialog.insCtrl.GetData())
    qry.AddAttrNode('InsType', 'EQUAL', dialog.insTypeCtrl.GetData())
    if dialog.mktCtrl.GetData():
        qry.AddAttrNode('Market.Name', 'EQUAL', dialog.mktCtrl.GetData())
    if dialog.mktGrpCtrl.GetData():
        qry.AddAttrNode('MarketGroup.Name', 'EQUAL', dialog.mktGrpCtrl.GetData())
    qry.AddAttrNode('PayType', 'EQUAL', dialog.payTypeCtrl.GetData())
    if dialog.prfCtrl.GetData():
        qry.AddAttrNode('Portfolio.Name', 'EQUAL', dialog.prfCtrl.GetData())
    if dialog.prfQryCtrl.GetData():
        qry.AddAttrNode('PortfolioFilter.Name', 'EQUAL', dialog.prfQryCtrl.GetData())
    if dialog.mktSegCtrl.GetData():
        qry.AddAttrNode('Segment.Name', 'EQUAL', dialog.mktSegCtrl.GetData())
    qry.AddAttrNode('UndInsType', 'EQUAL', dialog.undInsTypeCtrl.GetData())
    if dialog.startDayCtrl.GetValue():
        qry.AddAttrNode('StartDay', 'EQUAL', dialog.startDayCtrl.GetValue())
    if dialog.endDayCtrl.GetValue():
        qry.AddAttrNode('EndDay', 'EQUAL', dialog.endDayCtrl.GetValue())

    for condition in qry.Select(): #Loop through rest of conditions to find identical ones
        if IdenticalCondition(dialog, condition):
            return True
    return False

def IdenticalCondition(dialog, condition):
    """ Checks all input fields in the dialog, and if this condition will be 
        identical with the given condition the function returns true. """
    if condition == dialog.condition: #Editing condition - found self as identical, skip!
        return False

    execType = acm.FChoiceList[dialog.execCtrl.GetData()]

    if condition.Account() != acm.FAccount[dialog.accountCtrl.GetData()]:
        return False
    if condition.Broker() != acm.FBroker[dialog.brokerCtrl.GetData()]:
        return False
    if condition.BrokerGroup() != acm.FPartyGroup[dialog.brokerGrpCtrl.GetData()]:
        return False
    if condition.BuySell() != dialog.b_s_Ctrl.GetData():
        return False
    if condition.Client() != acm.FClient[dialog.clientCtrl.GetData()]:
        return False
    if condition.ClientGroup() != acm.FPartyGroup[dialog.clientGrpCtrl.GetData()]:
        return False
    if condition.Counterparty() != acm.FCounterParty[dialog.cptyCtrl.GetData()]:
        return False
    if condition.CounterpartyGroup() != acm.FPartyGroup[dialog.cptyGrpCtrl.GetData()]:
        return False
    if condition.Currency() != acm.FCurrency[dialog.conCurrCtrl.GetData()]:
        return False
    if condition.Depot() != acm.FCurrency[dialog.depotCtrl.GetData()]:
        return False
    if dialog.execCtrl.GetData() and execType.List() == 'Execution Type' and condition.ExecutionType() != execType:
        return False
    if condition.InsFilter() != acm.FStoredASQLQuery[dialog.insQryCtrl.GetData()]:
        return False
    if condition.Instrument() != acm.FInstrument[dialog.insCtrl.GetData()]:
        return False
    if condition.InsType() != dialog.insTypeCtrl.GetData():
        return False
    if condition.Market() != acm.FMarketPlace[dialog.mktCtrl.GetData()]:
        return False
    if condition.MarketGroup() != acm.FPartyGroup[dialog.mktGrpCtrl.GetData()]:
        return False
    if condition.PayType() != dialog.payTypeCtrl.GetData():
        return False
    if dialog.prfCtrl.GetData() == '':
        if condition.Portfolio():
            return False
    elif condition.Portfolio() != acm.FPhysicalPortfolio[dialog.prfCtrl.GetData()]:
        return False
    if condition.PortfolioFilter() != acm.FStoredASQLQuery[dialog.prfQryCtrl.GetData()]:
        return False
    if condition.Segment() != acm.FMarketSegment[dialog.mktSegCtrl.GetData()]:
        return False
    if condition.UndInsType() != dialog.undInsTypeCtrl.GetData():
        return False
    if condition.StartDay() == '':
        if dialog.startDayCtrl.GetValue(): 
            return False
    elif condition.StartDay() != dialog.startDayCtrl.GetValue():
        return False
    if condition.EndDay() == '':
        if dialog.endDayCtrl.GetValue():
            return False
    elif condition.EndDay() != dialog.endDayCtrl.GetValue():
        return False
    return True

def populateWData(dialog, condition):
    """ Fill dialog with data """
    dialog.m_fuxDlg.Caption('Edit ' + condition.Model().Name() + ' condition')
    if condition.MarketGroup():
        dialog.mktGrpCtrl.SetData(condition.MarketGroup())
    if condition.Market():
        dialog.mktCtrl.SetData(condition.Market())
    if condition.Segment():
        dialog.mktSegCtrl.SetData(condition.Segment())
    if condition.Instrument():
        dialog.insCtrl.SetData(condition.Instrument())
    if condition.Currency():
        dialog.conCurrCtrl.SetData(condition.Currency())
    if condition.ExecutionType():
        dialog.execCtrl.SetData(condition.ExecutionType())
    
    dialog.b_s_Ctrl.SetData(condition.BuySell())
    dialog.insTypeCtrl.SetData(condition.InsType())
    dialog.payTypeCtrl.SetData(condition.PayType())
    dialog.undInsTypeCtrl.SetData(condition.UndInsType())

    if condition.InsFilter():
        dialog.insQryCtrl.SetData(condition.InsFilter())
    if condition.ClientGroup():
        dialog.clientGrpCtrl.SetData(condition.ClientGroup())
    if condition.Client():
        dialog.clientCtrl.SetData(condition.Client())
    if condition.CounterpartyGroup():
        dialog.cptyGrpCtrl.SetData(condition.CounterpartyGroup())
    if condition.Counterparty():
        dialog.cptyCtrl.SetData(condition.Counterparty())
    if condition.BrokerGroup():
        dialog.brokerGrpCtrl.SetData(condition.BrokerGroup())
    if condition.Broker():
        dialog.brokerCtrl.SetData(condition.Broker())
    if condition.Depot():
        dialog.depotCtrl.SetData(condition.Depot())
    if condition.Account():
       dialog.accountCtrl.SetData(condition.Account())
    if condition.Portfolio():
        dialog.prfCtrl.SetData(condition.Portfolio())
    if condition.PortfolioFilter():
        dialog.prfQryCtrl.SetData(condition.PortfolioFilter())

    if condition.StartDay():
        dialog.startDayCtrl.SetValue(condition.StartDay())
    if condition.EndDay():
        dialog.endDayCtrl.SetValue(condition.EndDay())

    if condition.Curve().Size() > 0:
        curve = condition.Curve()[0]
        dialog.valueCtrl.SetValue(curve.MinValue())
        dialog.type.SetData(curve.CurveType())
        if condition.Model().Name() == 'Initial Margin':
            dialog.enableCurrency(None, None)
        if curve.Currency():
            dialog.currency.SetData(curve.Currency())

""" End of file """
