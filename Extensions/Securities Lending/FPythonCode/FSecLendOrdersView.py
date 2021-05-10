""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersView.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendOrdersView

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The Order Manager workbench.

------------------------------------------------------------------------------------------------"""
from FSecLendMenuItem import SecLendWorkbenchMenuItem

class OrderManagerMenuItem(SecLendWorkbenchMenuItem):

    def __init__(self, extObj):
        SecLendWorkbenchMenuItem.__init__(self, extObj, view='SecLendOrdersView')


def CreateOrderManagerMenuItem(eii):
    return OrderManagerMenuItem(eii)