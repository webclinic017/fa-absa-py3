""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRulesUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRulesUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Utility functions for compliance rules
-----------------------------------------------------------------------------"""
import acm
import FUxCore
from ACMPyUtils import Transaction
from FAssetManagementUtils import GetLogger, GetFunction
logger = GetLogger('Rules')


def RuleInterface(rule):
    interface = rule.Definition().Class().Interface()
    try:
        return GetFunction(interface)
    except StandardError as e:
        raise StandardError('Could not find an interface for rule {0}. {1}'.format(rule.Name(), e))

# ********************************* Utils for finding applied rules *********************************

def GetAppliedRules(entity):   
    return acm.FAppliedRule.Select('targetId = {0} and targetType = "{1}" and inactive=false'.format(entity.Oid(), entity.RecordType()))
        
def _AllOwnerPortfolios(portfolio):
    portfolios = []
    for link in portfolio.MemberLinks():
        if link.OwnerPortfolio():
            portfolios.extend(_AllOwnerPortfolios(link.OwnerPortfolio()))
        else:
            portfolios.append(portfolio)
    return portfolios

def AllPortfoliosForTrades(trades):
    portfolios = {trade.Portfolio() for trade in trades}
    compoundPortfolios = set()
    for p in portfolios:
        compoundPortfolios.update(_AllOwnerPortfolios(p))
    portfolios.update(compoundPortfolios)
    return portfolios


# ********************************* Alerts *********************************
def GetAlert(appliedRule, threshold, subject): 
    query = ('appliedRule = {0} and threshold = {1}' 
             ' and subjectId = {2} and subjectType = "{3}"').format(appliedRule.Oid(), 
                                               threshold.Oid(), 
                                               subject.Oid(),
                                               subject.RecordType())
    return acm.FAlert.Select01(query, '')


class AlertSheetDialog(FUxCore.LayoutDialog):

    def __init__(self, alerts):
        self.m_closeBtn = None
        self._alerts = alerts
        self.m_sheet = None
        self._sheetCtrl = None
        
    def HandleApply(self):
        return 1
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Compliance Check Result')
        self.m_sheetCtrl = layout.GetControl('sheet')
        self._sheet = self.m_sheetCtrl.GetCustomControl()
        for alert in self._alerts:
            self._sheet.InsertObject(alert, 'IOAP_LAST')
        
    @staticmethod
    def CreateLayout():
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddCustom('sheet', 'sheet.FAlertSheet', 1000, 250)
        b.  BeginHorzBox('None')
        b.          AddFill()
        b.          AddButton('ok', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
