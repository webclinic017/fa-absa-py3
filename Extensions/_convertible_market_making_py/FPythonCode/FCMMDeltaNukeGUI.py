""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ConvertibleMarketMaking/etc/FCMMDeltaNukeGUI.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCMMDeltaNukeGUI

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FRunScriptGUI
import FAssetManagementUtils
from FCMMDeltaNuke import UpdateFallbackDelta

logger  = FAssetManagementUtils.logger
logDict = FAssetManagementUtils.logDict

class DeltaNukeGUI(FRunScriptGUI.AelVariablesHandler):

    @staticmethod
    def insertStoredFolder():
        q = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'AND')
        op = q.AddOpNode('OR')
        op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
        op = q.AddOpNode('AND')
        op.AddAttrNode('SubType', 'RE_LIKE_NOCASE', 'FInstrument')
        return q

    def __init__(self):
        queryFolders = DeltaNukeGUI.insertStoredFolder()
        variables = [
                     ['QUERYFOLDER', 'Query Folder:', 'FStoredASQLQuery', None, queryFolders, 0, 1, 'Select Query Folder', None, True],
                     ]

        sLog = 'Logmode 0 shows WARNING and ERROR messages. Logmode 1 shows INFORMATION messages, and also includes the messages from Logmode 0.\
                Logmode 2 shows DEBUG messages and includes all other message types. '

        variables += [
                      ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 2, 0, sLog],
                      ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)


ael_variables = DeltaNukeGUI()

def ael_main(params):
    logger.Reinitialize(level=logDict[ params['LOG_MODE'] ],
                        keep=None,
                        logOnce=None,
                        logToConsole=1,
                        logToPrime=None,
                        logToFileAtSpecifiedPath=None,
                        filters=None,
                        lock=None
                    )
    logger.info('--Nuke Update Started--')
    instruments=[]
    #Extract the convertible instruments from all query folders and add to a list
    for qfolder in params['QUERYFOLDER']:
        for inst in qfolder.Query().Select():
            if hasattr(inst, "IsKindOf") and inst.IsKindOf(acm.FConvertible):
                instruments.append(inst)
    UpdateFallbackDelta(instruments)
    logger.info('--Nuke Update Finished--\n')