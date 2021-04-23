""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryView.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInventoryView

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The Inventory View workbench.

------------------------------------------------------------------------------------------------"""

from FSecLendMenuItem import SecLendWorkbenchMenuItem
import importlib

def ReloadWorkbench():
    import FSecLendUtils
    importlib.reload(FSecLendUtils)
    import FSecLendColumns
    importlib.reload(FSecLendColumns)
    import FSecLendEvents
    importlib.reload(FSecLendEvents)
    import FSecLendInventoryActiveLoansPanels
    importlib.reload(FSecLendInventoryActiveLoansPanels)
    import FSecLendInventoryAvailabilityPanels
    importlib.reload(FSecLendInventoryAvailabilityPanels)
    import FSecLendInventoryFilterPanel
    importlib.reload(FSecLendInventoryFilterPanel)
    import FSecLendInventoryWorkbookPanel
    importlib.reload(FSecLendInventoryWorkbookPanel)

class InventoryViewMenuItem(SecLendWorkbenchMenuItem):

    def __init__(self, extObj):
        SecLendWorkbenchMenuItem.__init__(self, extObj, view='SecLendInventoryView')

def CreateInventoryViewMenuItem(eii):
    return InventoryViewMenuItem(eii)
