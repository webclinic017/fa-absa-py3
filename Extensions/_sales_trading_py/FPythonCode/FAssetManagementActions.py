""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FAssetManagementActions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAssetManagementActions

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm


def OnDoubleClickCell(eii):
    try:
        cell = eii.Parameter('sheet').Selection().SelectedCell()
        rowObject = cell.RowObject()
        app = acm.GetDefaultApplication(rowObject.Class())
        acm.StartApplication(app, rowObject)
    except Exception:
        pass
