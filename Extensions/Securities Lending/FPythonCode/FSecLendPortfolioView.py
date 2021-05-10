""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendPortfolioView.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendPortfolioView

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The Portfolio View workbench.

------------------------------------------------------------------------------------------------"""
from FSecLendMenuItem import SecLendWorkbenchMenuItem

def ReloadWorkbench():
    pass


class PortfolioViewMenuItem(SecLendWorkbenchMenuItem):

    def __init__(self, extObj):
        SecLendWorkbenchMenuItem.__init__(self, extObj, view='SecLendPortfolioView')


def CreatePortfolioViewMenuItem(eii):
    return PortfolioViewMenuItem(eii)
