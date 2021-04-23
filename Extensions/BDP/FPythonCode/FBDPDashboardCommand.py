""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardCommand.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

import collections
import os.path


import acm
import FBDPDashboardViews
import FBDPDashboardQuery

class ViewHandler(object):

    def __init__(self, viewType, viewName, viewDetail):

        self.__viewType = viewType
        self.__viewName = viewName
        self.__querySpecList = viewDetail # details are the query specs
        self.__qryResultCache = {}
        self.__viewLevelStack = self.InitViewLevelStack()
    
    def InitViewLevelStack(self):

        viewLevel0 = FBDPDashboardViews._ViewLevel(self.__querySpecList[0], qryCond='',
                subTitle='', qryResultCache=self.__qryResultCache)
        return [viewLevel0]
        
    def GetCurrentViewLevel(self):
        return self.__viewLevelStack[-1]
    
    def GetCurrentViewLevelName(self):
        return self.GetCurrentViewLevel().getLevelName()
        
    def GetCurrentViewResult(self, forceRefresh):
        view = self.GetCurrentViewLevel()
        view.updateViewLevelResult(forceRefresh)
        resultDataList = view.getResultDataList()
        return resultDataList
        
    def GetCurrentViewQuery(self):
        view = self.GetCurrentViewLevel()
        return view.getQueryStatements()
    
    def ResetToRootLevel(self):
        self.__viewLevelStack = self._initViewLevelStack()
        
    def GetCacheResults(self):
        return self.__qryResultCache
        
    def HasFurtherDrillDown(self):
        if len(self.__viewLevelStack) >= len(self.__querySpecList):
            return False
        return True
    
    def DrillDown(self, drillDownCategoryName):
        if not self.HasFurtherDrillDown():
            print('No further drill down configured')
            return
        if drillDownCategoryName == FBDPDashboardQuery.CATEGORY_NAME_OTHERS:
            print('No drill down implemented for Others category yet.')
            return
        elif drillDownCategoryName == FBDPDashboardQuery.CATEGORY_NAME_NIL:
            print('No drill down implemented for \'Nil\' category.')
            return
            
        currentView = self.GetCurrentViewLevel()
        drillDownSubTitle = currentView.getDrillDownSubTitle(
                drillDownCategoryName)
        drillDownQueryCondition = currentView.getDrillDownQueryCondition(
                drillDownCategoryName)
        drillDownLevelNum = len(self.__viewLevelStack)
        drillDownViewLevel = FBDPDashboardViews._ViewLevel(self.__querySpecList[
                drillDownLevelNum], drillDownQueryCondition, drillDownSubTitle,
                self.__qryResultCache)
        self.__viewLevelStack.append(drillDownViewLevel)
        
    def GoBackLevel(self):
        if len(self.__viewLevelStack) > 1:
            self.__viewLevelStack.pop()

        
class BDPDashboardCommand(object):

    def __init__(self):
        self.__configuator = FBDPDashboardViews._Configurator()
        self.viewTypes = self.__configuator.getViewTypes()
        
    def LoadConfig(self, path):
        self.__configuator.load(path)
        self.viewTypes = self.__configuator.getViewTypes()
        
    def GetViewTypes(self):
        return self.viewTypes
        
    def GetViewNames(self, type):
        viewDetailConfig = self.__configuator.getViewCollection(type)
        return viewDetailConfig.keys()
        
    def GetViewHandler(self, viewType, viewName):
        resultCache = {}
        viewDetailConfig = self.__configuator.getViewCollection(viewType)
        viewHandler = ViewHandler(viewType, viewName, viewDetailConfig[viewName])
        return viewHandler
