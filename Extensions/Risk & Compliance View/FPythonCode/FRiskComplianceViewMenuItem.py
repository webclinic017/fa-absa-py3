""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceViewMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceMenuItem

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functions for menu items in risk and compliance view

-----------------------------------------------------------------------------"""

import acm
import FIntegratedWorkbench
from FUxCore import MenuItem
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FRiskComplianceCurrentActiveBusinessProcess import RiskComplianceCurrentActiveBusinessProcess
from FSheetUtils import ApplyGrouperInstanceToSheet, GetWorkbook, FindAppWithWorkbook
from FWorkflowMenuItem import MultiWorkflowMenuItem
from FTradeProgramWorkflow import TradeProgramWorkflow
from FRiskComplianceLogging import logger
from FIntegratedWorkbench import GetHandler
from FViewUtils import ViewSettings


class RiskComplianceViewMenuItem(MultiWorkflowMenuItem, IntegratedWorkbenchMenuItem):

    EVENT = None

    def __init__(self, extObj):
        IntegratedWorkbenchMenuItem.__init__(self, extObj,
                                            view='RiskComplianceView')
        MultiWorkflowMenuItem.__init__(self, extObj, TradeProgramWorkflow, self.EVENT)

    def BusinessProcesses(self):
        try:
            return self.Handler().BusinessProcesses()
        except StandardError as e:
            logger.debug(e)

    def Applicable(self):
        return True

    def Handler(self):
        return GetHandler(self.View(), RiskComplianceCurrentActiveBusinessProcess)


class ApproveForTradingMenuItem(RiskComplianceViewMenuItem):
    EVENT = 'Approve breaches'

class StartWorkbenchMenuItem(MenuItem, object):
    
    APP = None

    def __init__(self, _extObj, view='RiskComplianceView'):
        self._view = view
        self._frame = _extObj

    def Enabled(self):
        return True
    
    def Settings(self):
        return ViewSettings(self._view)
        
    def _IsShared(self):
        return self.Settings().IsShared()
            
    def Workbook(self):
        try:
            name = self.Settings().Workbook()
            return GetWorkbook(name, self._IsShared())
        except StandardError:
            pass
        
    @classmethod
    def SetApp(cls):
        try:
            str(cls.APP)
        except RuntimeError:
            cls.APP = None

    def Invoke(self, _eii):
        cls = type(self)
        cls.SetApp()
        if cls.APP is None:
            defaultWorkbook = self.Workbook()
            if defaultWorkbook:
                cls.APP = FindAppWithWorkbook(defaultWorkbook) or\
                acm.StartApplication(self.Settings().Application(), defaultWorkbook)
            else:
                cls.APP = FIntegratedWorkbench.LaunchView(self._view)
                self._SetDefaultContent(cls.APP)
        cls.APP.Restore()
        cls.APP.Activate()
        
    def _SetDefaultContent(self, appl):
        sheet = appl.ActiveSheet()
        sheet.InsertObject(self._DefaultQueryFolder(), 0)
        grouper = acm.Risk().GetGrouperFromName('Current State', 'FBusinessProcessGrouperSubject')
        ApplyGrouperInstanceToSheet(sheet, grouper)
        
    @staticmethod
    def _DefaultQueryFolder():
        q = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
        node = q.AddOpNode('OR')
        node.AddAttrNode('subject_type', 'EQUAL', 'DealPackage')
        
        node = q.AddOpNode('AND')
        node.AddAttrNode('createTime', 'GREATER_EQUAL', '-7d')
        node.AddAttrNode('createTime', 'LESS_EQUAL', None)
        
        node = q.AddOpNode('AND')
        node.AddAttrNode('updateTime', 'GREATER_EQUAL', None)
        node.AddAttrNode('updateTime', 'LESS_EQUAL', None)
        
        qf = acm.FASQLQueryFolder()
        qf.AsqlQuery( q )
        qf.Name = 'Trade Programs'
        return qf
           
def ApproveForTrading(eii):
    return ApproveForTradingMenuItem(eii)

def StartWorkbench(eii):
    return StartWorkbenchMenuItem(eii)