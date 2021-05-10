""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorpActionColumns.py"
"""--------------------------------------------------------------------------
MODULE
    FCorpActionColumns

DESCRIPTION
    Functions supporting Corporate action columns.

-----------------------------------------------------------------------------"""


def GetEligiblePositionAttr(ins):
    #TODO: Read extensionAttribute from ColumnId in instrument settings
    return 'inventoryPosition'