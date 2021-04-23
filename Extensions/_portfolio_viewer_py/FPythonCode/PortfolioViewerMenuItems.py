""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerMenuItems.py"
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerMenuItems

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
   	Module containing the code for the menu items used in ribbons and 
    right click menus in the Portfolio Viewer application.
-----------------------------------------------------------------------------"""

import FUxCore
import acm
import PortfolioViewerDialogs
import PortfolioViewerFunctions
import PortfolioViewerConditionsDlg as ConditionalFunctions

""" --- Class that handles ribbons and actions --- """
class MenuItems(FUxCore.MenuItem):
    def __init__(self):
        self.m_application = None
        
    def Invoke(self, cd):
        commandName = cd.Definition().GetName().Text()
        if commandName == 'ViewSettings':
            PortfolioViewerFunctions.OpenSettings(self.m_application)

        #Column commands
        elif commandName == 'columnSelection_list':
            if self.m_application.userSettings.At('defDataType') == 'Portfolio':
                PortfolioViewerFunctions.ColumnSelection(self.m_application, 'Portfolio')
            else:
                PortfolioViewerFunctions.ColumnSelection(self.m_application, 'Depot')
        elif commandName == 'columnsSelection_clnt':
            PortfolioViewerFunctions.ColumnSelection(self.m_application, 'Client')
        elif commandName == 'columnSelection_cond':
            PortfolioViewerFunctions.ColumnSelection(self.m_application, 'Condition')
        
        #Create new commands
        elif commandName == 'new_prfOrDepot':
            if self.m_application.userSettings.At('defDataType') == 'Portfolio':
                if PortfolioViewerDialogs.StartCreationDialog(self.m_application, None): #Portfolio created
                    PortfolioViewerFunctions.PortfolioSearch(self.m_application, None) #Reload results
            elif self.m_application.userSettings.At('defDataType') == 'Depot':
                acm.UX().SessionManager().StartApplication('Party Definition', None)
        elif commandName == 'new_condition':
            if ConditionalFunctions.StartNewConditionDlg(self.m_application):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)

        elif commandName == 'ClearFields':
            PortfolioViewerFunctions.clearAllFields(self.m_application)
        elif commandName == 'DoSearch':
            if self.m_application.userSettings.At('defDataType') == 'Portfolio':
                PortfolioViewerFunctions.PortfolioSearch(self.m_application, None)
            elif self.m_application.userSettings.At('defDataType') == 'Depot':
                PortfolioViewerFunctions.PartySearch(self.m_application, None)
        elif commandName == 'CondModels':
            acm.UX().SessionManager().StartApplication('Charges', None)

        #portfolio right click commands
        elif commandName == 'setCompoundNode':
            PortfolioViewerFunctions.SetCompoundNode(self.m_application, None)
        elif commandName == 'openInAdminConsole':
            PortfolioViewerFunctions.OpenConditionCustom(self.m_application, True)
        elif commandName == 'openPortfolio':
            PortfolioViewerFunctions.OpenPortfolio(self.m_application, None)
        
        #client and depot right click commands
        elif commandName == 'ClientGroups':
            acm.UX().SessionManager().StartApplication('Party Groups', acm.FPartyGroup[cd.Definition().GetTooltip().Text()])
        elif commandName == 'newDepotWParent':
            if PortfolioViewerDialogs.NewDepotDlg(self.m_application):
                PortfolioViewerFunctions.PartySearch(self.m_application, None)

        #Shared right click commands (portfolio and depot)
        elif commandName == 'showConditions':
            PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)
        
        #Conditions and commissions
        elif commandName == 'openSelCondition':
            PortfolioViewerFunctions.OpenConditionCustom(self.m_application, None)
        elif commandName == 'newPrfCondition':
            if PortfolioViewerFunctions.NewPortfolioCondition(self.m_application, None):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)
        elif commandName == 'newDepCondition':
            if PortfolioViewerFunctions.NewPartyCondition(self.m_application, None):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)
        elif commandName == 'newCondforModel':
            if ConditionalFunctions.OpenConditionDlg(self.m_application, self.m_application.treeView.GetSelectedItem().GetData(), None):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)

        elif commandName == 'copyConditions':
            PortfolioViewerFunctions.CopyConditionsFrom(self.m_application)

        # Condition overview commands
        elif commandName == 'overviewModelsUpdateCondition':
            model = acm.FConditionalValueModel[cd.Definition().GetTooltip().Text()]
            if PortfolioViewerFunctions.ChangeConditionValue(self.m_application, model):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)
        elif commandName == 'overviewModelsSpecialCondition':
            model = acm.FConditionalValueModel[cd.Definition().GetTooltip().Text()]
            if PortfolioViewerFunctions.NewOverviewCondition(self.m_application, model):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)
        elif commandName == 'overviewModelsDefaultCondition':
            model = acm.FConditionalValueModel[cd.Definition().GetTooltip().Text()]
            if ConditionalFunctions.OpenConditionDlg(self.m_application, model, None):
                PortfolioViewerFunctions.UpdateConditionalModels(self.m_application, None)

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

class TypeMenuItems(FUxCore.MenuItem):
    def __init__(self):
        self.m_application = None
        self.checked = False
        
    def Invoke(self, cd):
        commandName = cd.Definition().GetName().Text()
        if commandName == 'use_Portfolio':
            self.m_application.userSettings.AtPut('defDataType', 'Portfolio')
            PortfolioViewerFunctions.ChangeType(self.m_application, None)
        elif commandName == 'use_Depot':
            self.m_application.userSettings.AtPut('defDataType', 'Depot')
            PortfolioViewerFunctions.ChangeType(self.m_application, None)
        else: 
            pass
            
    def Applicable(self):
        return True

    def Checked(self):
        return self.checked

    def SetApplication(self, application):
        self.m_application = application

""" End of file """
