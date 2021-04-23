""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPerformArchiving.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionPerformArchiving - Manages the archiving and archive logging for
                                  corporate action related objects.

    (c) Copyright 201X FIS FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import acm

from FEntitiesArchiver import entitiesArchiver
from FCorpActionArchiveContainers import CorpActionArchiveContainer
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

def PerformCorpActionsArchiving(args):
    handler = CorpActionsArchiveHandler(args)
    handler.Perform()

class CorpActionsArchiveHandler():
    def __init__(self, args):
        self.args = args
        self.testmode = None
        self.entityDict = None

    def ReadArguments(self, args):
        self.corpActions = args.get("CorpActions", []) 
        self.testmode =  args.get("Testmode", 0)
        self.includeDividendEstimate = args.get("IncludeDividendEstimate", 0)
        self.beforeDate = args.get("BeforeDate", acm.Time.DateToday())

    def Perform(self):
        self.ReadArguments(self.args)
        self.ArchiveEntities()

    def ArchiveEntities(self):

        for action in self.corpActions:
            if not action:
                continue

            entityId = action.Name()
            try:
                archiveContainer = CorpActionArchiveContainer(action, self.includeDividendEstimate, self.beforeDate)
                if archiveContainer.IsValidToArchive():
                    archiver = entitiesArchiver(self.testmode, self.args)
                    archiver.LogStart(entityId)
                    archiver.Archive(entityId, archiveContainer.GetEntities())
                    archiver.LogEnd(entityId)
                else:
                    Logme()("Ingore {}, its ExDate or Record Date is after the specified before Date.".format(entityId), "WARNING")
                    Summary().ignore(action, Summary().ARCHIVE, "Not valid to archive", action.Oid())
                
            except Exception as error:
                Logme()("------------------------------------", "ERROR")
                Logme()("An exception occurred while processing {}:".format(entityId), "ERROR")
                Logme()("", "ERROR")
                Logme()("{}".format(str(error)), "ERROR")
                Logme()("", "ERROR")
                Logme()("The archiving of {} will be aborted.".format(entityId), "ERROR")
                Logme()("------------------------------------", "ERROR")

        Logme()(None, 'FINISH')
        Summary().log(self.args)
