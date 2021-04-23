""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientView.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientView

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The Client View workbench.

------------------------------------------------------------------------------------------------"""
from FSecLendMenuItem import SecLendWorkbenchMenuItem
import importlib

def ReloadWorkbench():
    import FSecLendEvents
    importlib.reload(FSecLendEvents)
    import FSecLendClientPositionsPanel
    importlib.reload(FSecLendClientPositionsPanel)
    import FSecLendClientPositionsFilterPanel
    importlib.reload(FSecLendClientPositionsFilterPanel)
    import FSecLendClientFilterPanel
    importlib.reload(FSecLendClientFilterPanel)
    import FSecLendClientDetailsPanel
    importlib.reload(FSecLendClientDetailsPanel)
    import FSecLendClientSelectionPanel
    importlib.reload(FSecLendClientSelectionPanel)
    import FSecLendClientTradesPanel
    importlib.reload(FSecLendClientTradesPanel)


class ClientViewMenuItem(SecLendWorkbenchMenuItem):

    def __init__(self, extensionObject):
        super(ClientViewMenuItem, self).__init__(extensionObject, view='SecLendClientView')

def CreateClientViewMenuItem(eii):
    return ClientViewMenuItem(eii)
