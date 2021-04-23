""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerDockedPane.py"
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerDockedPane

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
   	Module containing the code for the docked pane in the Portfolio Viewer
   	application. Displays and handles the search fields.
-----------------------------------------------------------------------------"""

import FUxCore
import acm
import PortfolioViewerDialogs
import PortfolioViewerFunctions

""" Additional class that handles the layout pane containing portfolio or depot filters """
class FilterPanel(FUxCore.LayoutPanel):
    def __init__(self):
        self.parent = None

    def SetParent(self, parent):
        self.parent = parent

    def HandleCreate( self ):
        layout = self.SetLayout(self.CreateLayout())

        self.parent.nameFld = layout.GetControl('NameField')
        self.parent.dateFld = layout.GetControl('DateField')
        
        self.parent.addInfosCtrl = layout.GetControl('addInfos')
        self.parent.addInfosCtrl.Editable(False)
        self.parent.openSelectAddInfosBtn = layout.GetControl('openSelectAddInfos')
        self.parent.openSelectAddInfosBtn.AddCallback("Activate", PortfolioViewerFunctions.OpenAdditionalInfosDlg, self.parent)
        self.parent.clearAddInfosBtn = layout.GetControl('clearAddInfos')
        self.parent.clearAddInfosBtn.AddCallback("Activate", PortfolioViewerFunctions.ClearAdditionalInfos, self.parent)
        
        self.parent.commonFields = [self.parent.nameFld, self.parent.dateFld, self.parent.addInfosCtrl]
        for f in self.parent.commonFields:
            f.AddCallback('Activate', PortfolioViewerFunctions.CommonSearch, self.parent)
        
        self.HandlePortfolioCtrls(layout)
        self.HandleDepotCtrls(layout)
        self.parent.panelInstantiated = True #Makes sure that fields are instantiated to avoid exceptions

    def HandlePortfolioCtrls(self, layout):
        self.parent.currFld = layout.GetControl('CurrField')
        self.parent.portfolioOwner = layout.GetControl('PrtfOwner')
        self.parent.openInsertParties = layout.GetControl('OpenInsertParty')
        self.parent.clearParties = layout.GetControl('Clear')
        self.parent.compParentFld = layout.GetControl('CompoundParent')
        self.parent.openInsertCompoundPrtf = layout.GetControl('OpenInsertCompoundPortfolio')
        self.parent.clearCompPrtf = layout.GetControl('ClearCPortfolios')
        self.parent.compFld = layout.GetControl('CompoundField')

        self.parent.currFld.AddItem('')
        for currency in acm.FCurrency.Select('').SortByProperty('Name'):
            self.parent.currFld.AddItem(currency.Name())
        self.parent.currFld.SetData('')

        #Portfolio owner
        self.parent.portfolioOwner.Editable(False)
        self.parent.openInsertParties.AddCallback('Activate', PortfolioViewerDialogs.StartInsertParties, self.parent)
        self.parent.clearParties.AddCallback('Activate', PortfolioViewerDialogs.ClearParties, self.parent)

        #Compound Node
        self.parent.compParentFld.Editable(False)
        self.parent.compParentFld.ToolTip('Only show physical portfolios that belong to this compound portfolio.')
        self.parent.openInsertCompoundPrtf.AddCallback('Activate', PortfolioViewerFunctions.StartInsertCompoundPortfolio, self.parent)
        self.parent.clearCompPrtf.AddCallback('Activate', PortfolioViewerFunctions.ClearCompound, self.parent)

        self.parent.compFld.AddItem('')
        self.parent.compFld.AddItem('Yes')
        self.parent.compFld.AddItem('No')
        self.parent.compFld.SetData('')
        self.parent.portfolioInputFields = [self.parent.currFld, self.parent.portfolioOwner, self.parent.compParentFld, self.parent.compFld]
        for fld in self.parent.portfolioInputFields:
            fld.AddCallback('Activate', PortfolioViewerFunctions.PortfolioSearch, self.parent)
        
    def HandleDepotCtrls(self, layout):
        self.parent.depOrClntCtrl = layout.GetControl('DepotOrClient')
        self.parent.ptyId2Ctrl = layout.GetControl('ptyid2')
        self.parent.aliasTypeCtrl = layout.GetControl('aliasType')
        self.parent.aliasNameCtrl = layout.GetControl('aliasName')
        self.parent.aimsEntCtrl = layout.GetControl('aimsEnt')
        self.parent.fixClientCtrl = layout.GetControl('fixClient')
        self.parent.unknownDepotCtrl = layout.GetControl('unknownDep')
        self.parent.pnlDepotCtrl = layout.GetControl('pnlDep')
        self.parent.shpDepotCtrl = layout.GetControl('shpDepot')
        self.parent.warehouseDepCtrl = layout.GetControl('warehouseDep')
        self.parent.depParentOptionCtrl = layout.GetControl('depParentOption')
        self.parent.depParentCtrl = layout.GetControl('depParent')
        self.parent.openInsClientBtn = layout.GetControl('openInsClient')
        self.parent.clearClientBtn = layout.GetControl('clearClient')
        self.parent.clientHasDepotsCtrl = layout.GetControl('clientHasDepots')
        self.parent.comCtrl = layout.GetControl('commissionSlope')
        self.parent.comSlopeCtrl = layout.GetControl('commissionSlopeValue')
        self.parent.comShrCtrl = layout.GetControl('csaSlope')
        self.parent.comShrSlopeCtrl = layout.GetControl('csaSlopeValue')

        #All depot fields
        self.parent.depotInputFields = [self.parent.depOrClntCtrl, self.parent.ptyId2Ctrl, self.parent.aimsEntCtrl,\
                self.parent.fixClientCtrl, self.parent.unknownDepotCtrl, self.parent.pnlDepotCtrl,\
                self.parent.aliasTypeCtrl, self.parent.aliasNameCtrl, self.parent.shpDepotCtrl,\
                self.parent.warehouseDepCtrl, self.parent.depParentOptionCtrl, self.parent.depParentCtrl,\
                self.parent.openInsClientBtn, self.parent.clearClientBtn, self.parent.clientHasDepotsCtrl,\
                self.parent.comCtrl, self.parent.comSlopeCtrl, self.parent.comShrCtrl, self.parent.comShrSlopeCtrl]
        
        #Customize fields
        self.parent.depOrClntCtrl.AddItem('Client')
        self.parent.depOrClntCtrl.AddItem('Depot')
        self.parent.depOrClntCtrl.SetData('Depot')
        self.parent.depOrClntCtrl.AddCallback('Changed', PortfolioViewerFunctions.ClientDepotSwitch, self.parent)

        self.parent.ptyId2Ctrl.ToolTip('Alias of the depot (PartyId2)')

        self.parent.aliasTypeCtrl.AddItem('')
        for aliasT in acm.FPartyAliasType.Select(''):
            self.parent.aliasTypeCtrl.AddItem(aliasT.Name())
        self.parent.aliasTypeCtrl.SetData('')
        self.parent.aliasTypeCtrl.AddCallback('Changed', PortfolioViewerFunctions.EnableAliasField, self.parent)
        self.parent.aliasNameCtrl.Enabled(False)

        self.parent.depParentOptionCtrl.AddItem('')
        self.parent.depParentOptionCtrl.AddItem('With parent')
        self.parent.depParentOptionCtrl.AddItem('Without parent')
        self.parent.depParentOptionCtrl.SetData('')
        self.parent.depParentOptionCtrl.AddCallback('Changed', PortfolioViewerFunctions.DepotParentOptionSwitch, self.parent)

        self.parent.depParentCtrl.Editable(False)
        self.parent.openInsClientBtn.AddCallback('Activate', PortfolioViewerDialogs.StartInsertClient, self.parent)
        self.parent.clearClientBtn.AddCallback('Activate', PortfolioViewerDialogs.ClearClients, self.parent)

        self.parent.clientHasDepotsCtrl.AddItem('')
        self.parent.clientHasDepotsCtrl.AddItem('Has no depots')
        self.parent.clientHasDepotsCtrl.AddItem('Has depots')
        self.parent.clientHasDepotsCtrl.SetData('')

        self.parent.comCtrl.AddItem('')
        self.parent.comCtrl.AddItem('No commission condition for depot')
        self.parent.comCtrl.AddItem('Commission condition for depot exists. Curve slope:')
        self.parent.comCtrl.SetData('')
        self.parent.comCtrl.AddCallback("Changed", PortfolioViewerFunctions.CommissionSearchFieldsSwitch, (self.parent, 'Commission'))
        self.parent.comSlopeCtrl.Enabled(False)
        self.parent.comShrCtrl.AddItem('')
        self.parent.comShrCtrl.AddItem('No commission sharing condition for depot')
        self.parent.comShrCtrl.AddItem('Commission sharing condition for depot exists. Curve slope:')
        self.parent.comShrCtrl.SetData('')
        self.parent.comShrCtrl.AddCallback("Changed", PortfolioViewerFunctions.CommissionSearchFieldsSwitch, (self.parent, 'Commission Sharing'))
        self.parent.comShrSlopeCtrl.Enabled(False)

        tmp = [self.parent.aimsEntCtrl, self.parent.fixClientCtrl, self.parent.unknownDepotCtrl,\
               self.parent.pnlDepotCtrl, self.parent.warehouseDepCtrl, self.parent.shpDepotCtrl]
        for f in tmp:
            f.AddItem('')
            f.AddItem('Yes')
            f.AddItem('No')
            f.SetData('')

        for fld in self.parent.depotInputFields:
            fld.AddCallback('Activate', PortfolioViewerFunctions.PartySearch, self.parent)
        
    def CreateLayout(self):
        """ Create the layout of the application """
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.  BeginHorzBox('None')
        builder.    AddSpace(5)
        builder.    BeginVertBox('None')
        builder.      AddSpace(3)
        builder.      AddOption('DepotOrClient', 'Select Search Type') #Select depot or client
        builder.      AddSpace(3)
        builder.      AddInput('NameField', 'Portfolio Name', 20)
        builder.      AddInput('DateField', 'Update Time (from)', 20)
        # Portfolio specific input fields
        builder.      AddOption('CurrField', 'Currency', 20)
        builder.      BeginHorzBox('None')
        builder.        AddInput('PrtfOwner', 'Portfolio Owner(s)', 12)
        builder.        AddSpace(1)
        builder.        AddButton('OpenInsertParty', '...', 5, 5)
        builder.        AddButton('Clear', 'C', 5, 5)
        builder.      EndBox()
        builder.      BeginHorzBox('None')
        builder.        AddInput('CompoundParent', 'Compound Portfolio', 12)
        builder.        AddSpace(1)
        builder.        AddButton('OpenInsertCompoundPortfolio', '...', 5, 5)
        builder.        AddButton('ClearCPortfolios', 'C', 5, 5)
        builder.      EndBox()
        builder.      AddOption('CompoundField', 'Is Compound', 20)
        # Depot or client specific input fields
        builder.      AddInput('ptyid2', 'Alias', 20)
        builder.      AddSpace(3)
        builder.      AddOption('aliasType', 'Alias Type', 20)
        builder.      AddInput('aliasName', 'Alias', 20)
        builder.      AddSpace(3)
        builder.      AddOption('aimsEnt', 'AIMS Entity', 20)
        builder.      AddOption('fixClient', 'FIX Client', 20)
        builder.      AddOption('pnlDep', 'Profit/Loss Depot', 20)
        builder.      AddOption('shpDepot', 'Shaping Depot', 20)
        builder.      AddOption('warehouseDep', 'Warehouse Depot', 20)
        builder.      AddOption('unknownDep', 'Unknown Depot', 20)
        builder.      AddSpace(3)
        builder.      BeginHorzBox('None')
        builder.        AddInput('addInfos', 'Additional Infos', 12)
        builder.        AddSpace(1)
        builder.        AddButton('openSelectAddInfos', '...', 5, 5)
        builder.        AddButton('clearAddInfos', 'C', 5, 5)
        builder.      EndBox()
        builder.      AddSpace(3)
        builder.      BeginVertBox('EtchedIn', 'Depot Parent')
        builder.        AddOption('depParentOption', 'Parent Filter', 20)
        builder.        BeginHorzBox('None')
        builder.          AddInput('depParent', 'Select Parents (Clients)', 12)
        builder.          AddSpace(1)
        builder.          AddButton('openInsClient', '...', 5, 5)
        builder.          AddButton('clearClient', 'C', 5, 5)
        builder.        EndBox()
        builder.      EndBox()
        builder.      AddOption('clientHasDepots', 'Depots', 20)
        builder.      AddSpace(3)
        builder.      BeginVertBox('EtchedIn', 'Condition Attributes')
        builder.        BeginHorzBox('None')
        builder.          AddOption('commissionSlope', 'Commission')
        builder.          AddInput('commissionSlopeValue', '', 5, 5)
        builder.        EndBox()
        builder.        BeginHorzBox('None')
        builder.        AddOption('csaSlope', 'Commission Sharing')
        builder.          AddInput('csaSlopeValue', '', 5, 5)
        builder.        EndBox()
        builder.      EndBox()
        #Common
        builder.    EndBox()
        builder.    AddSpace(5)
        builder.  EndBox()
        builder.EndBox()
        return builder

""" End of file """
