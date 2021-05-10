""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportColumnSelection.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportColumnSelection - Base class for tabs

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    The base class for the tabs in the GUI

----------------------------------------------------------------------------"""

import acm

import FRunScriptGUI
import FColumnSelectItem

def getStoredScenarios():
    return sorted([s.Name() for s in acm.FStoredScenario.Select("")])

def customDialog(shell, params):
    customDlg = FColumnSelectItem.SelectColumnsCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def riskFactorCustomDialog(shell, params):
    customDlg = FColumnSelectItem.SelectRiskFactorColumnsCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

class MarketRiskExportColumnSelection(FRunScriptGUI.AelVariablesHandler):
     def __init__(self, variables, name, tabName, defaultColumn):
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, name)
        ttColumn = 'Select column to export value'
        self.createVariable(
                        ['column_name' + tabName,
                        'Column name' + tabName,
                        'string', [], defaultColumn,
                        0, 1, ttColumn, None, False, customDialog])

class MarketRiskExportRiskFactorColumnSelection(FRunScriptGUI.AelVariablesHandler):
     def __init__(self, variables, name, tabName, defaultColumn):
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, name)
        ttColumn = 'Select position sheet column to export value'
        self.createVariable(
                        ['column_name' + tabName,
                        'Column name' + tabName,
                        'string', [], defaultColumn,
                        0, 1, ttColumn, None, False, riskFactorCustomDialog])                        
