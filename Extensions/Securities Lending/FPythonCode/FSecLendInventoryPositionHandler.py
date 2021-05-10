""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryPositionHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendInventoryPositionHandler

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Workbench event handler/dispatcher.

-----------------------------------------------------------------------------"""
from FHandler import Handler
from FEvent import EventCallback


class SecLendInventoryPositionHandler(Handler):

    def __init__(self, dispatcher):
        super(SecLendInventoryPositionHandler, self).__init__(dispatcher)
        self._positionRows = None

    def PositionRows(self):
        return self._positionRows

    @EventCallback
    def OnInventoryViewInventoryViewPositionSelected(self, event):
        self._positionRows = event.PositionRows()