""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/blacklistedCurrencyPairFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    blacklistedCurrencyPairFilter

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FUxCore

def ael_custom_dialog_show(shell, params):

    selectedAsqlQuery = None
    dialog = CurrencyPairBlacklistParameters()
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog)

def ael_custom_dialog_main(parameters, dictExtra):
    config = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues( parameters )
    columnLabel = parameters.At('ExclusionListCurrencyPairQuery').Name()
    config = acm.Sheet().Column().CreatorConfigurationFromInitialCustomLabel( acm.FSymbol(columnLabel), config )
    return_value = {acm.FSymbol("columnCreatorConfiguration") : config}
    return return_value


class CurrencyPairBlacklistParameters(FUxCore.LayoutDialog):

    def __init__(self):
        self.bindings = acm.FUxDataBindings()
        self.bindings.AddDependent( self )
        self.availableFilters = acm.FStoredASQLQuery.Select('subType = "FCurrencyPair" and user = 0')
        self.filterCtrl = self.bindings.AddBinder(
            'filter',
            acm.GetDomain("FStoredASQLQuery"),
            None,
            self.availableFilters,
            False,
            True,
            30)
        self.excludeSpotCtrl = self.bindings.AddBinder('excludeSpot', acm.GetDomain("bool"), None)

    def HandleApply(self):
        d = acm.FDictionary()
        filter = self.filterCtrl.GetValue()
        if filter:
            d = acm.FDictionary()
            d.AtPut(acm.FSymbol('ExclusionListCurrencyPairQuery'), self.filterCtrl.GetValue())
            d.AtPut(acm.FSymbol('ExclusionListIgnoreFXSpot'), self.excludeSpotCtrl.GetValue())
            return d

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox("None")
        self.filterCtrl.BuildLayoutPart(b, 'Filter')
        b.AddButton('newFilter', 'New')
        b.AddButton('editFilter', 'Edit')
        b.EndBox()
        b.BeginHorzBox("None")
        self.excludeSpotCtrl.BuildLayoutPart(b, 'Ignore spot dated' )
        b.EndBox()
        b.BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Ok')
        b.  AddButton('cancel', 'Cancel')
        b.EndBox()
        b.EndBox()
        return b

    def HandleCreate( self, dlg, layout):
        self.dialog = dlg
        self.dialog.Caption = 'Select filter..'
        self.bindings.AddLayout(layout)
        self.newBtn = layout.GetControl("newFilter")
        self.newBtn.AddCallback( "Activate", self.OnNewClicked, None )
        self.editBtn = layout.GetControl("editFilter")
        self.editBtn.AddCallback( "Activate", self.OnEditClicked, None )

    def OnNewClicked(self, *args):
        newFolder = self.CreateNewFolder()
        if newFolder:
            self.filterCtrl.SetValue(newFolder)

    def OnEditClicked(self, *args):
        currentFolder = self.filterCtrl.GetValue()
        if currentFolder:
            newFolder = self.EditFolder(currentFolder)
            if newFolder:
                self.filterCtrl.SetValue(newFolder)

    def CreateQueryWithItems(self, pairs):
        query = acm.CreateFASQLQuery("FCurrencyPair", "AND")
        node = query.AddOpNode('OR')
        for p in pairs:
            node.AddAttrNode('Name', 'EQUAL', p.Name())
        return query

    def CreateOrReplaceFilter(self, pairs, nameOrFolder):
        if type(nameOrFolder) is not acm._pyClass(acm.FStoredASQLQuery):
            folder = acm.FStoredASQLQuery()
            folder.Name = nameOrFolder
        else:
            folder = nameOrFolder.StorageImage()
        query = self.CreateQueryWithItems(pairs)
        folder.AutoUser = False
        folder.User = None
        folder.Query = query
        return self.SaveFolder(folder)

    def ConfirmOverride(self, folder):
        infoStr = '"{0}" already exist as a {1}-filter. ' \
            'Are you sure you wish to replace it?'.format(folder.Name(), folder.SubType())
        answer = acm.UX().Dialogs().MessageBoxYesNoCancel(self.dialog.Shell(), 'Information', infoStr)
        if answer == 'Button1':
            return True
        else:
            return False

    def ValidateName(self, shell, name, *args):
        existing = acm.FStoredASQLQuery[name]
        if existing is not None:
            return self.ConfirmOverride(existing)
        return True

    def AllCurrencyPairs(self):
        return acm.FCurrencyPair.Select(None)

    def CreateNewFolder(self):
        pairs = self.SelectCurrencyPairs()
        nameOrFolder = None
        if pairs:
            nameOrFolder = acm.UX().Dialogs().SaveObjectAs(
                self.dialog.Shell(),
                'Save as',
                'Currency pair filter',
                self.availableFilters,
                [],
                self.ValidateName,
                [])
            if nameOrFolder:
                return self.CreateOrReplaceFilter(pairs, nameOrFolder)

    def SelectCurrencyPairs(self, initiallySelected = None):
        return acm.UX().Dialogs().SelectSubset(
            self.dialog.Shell(),
            self.AllCurrencyPairs(),
            'Currency pairs',
            True,
            initiallySelected)

    def EditFolder(self, currentFolder):
        pairs = self.SelectCurrencyPairs(currentFolder.Query().Select())
        if pairs and self.ConfirmOverride(currentFolder):
            return self.CreateOrReplaceFilter(pairs, currentFolder)

    def SaveFolder(self, folder):
        try:
            folder.Commit()
            return folder
        except StandardError as e:
            acm.UX().Dialogs().MessageBoxOKCancel(self.dialog.Shell(), 'Error', 'Error: ' + str(e))
