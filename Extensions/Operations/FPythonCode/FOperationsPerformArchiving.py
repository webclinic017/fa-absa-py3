""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsPerformArchiving.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsPerformArchiving - Manages the archiving and archive logging for
                                  operations related objects.

    (c) Copyright 201X SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import acm, ael

#operations
from FOperationsArchivers import OperationsArchiver, JournalLinkArchiver, JournalInformationArchiver, SettlementArchiver
from FOperationsArchiveContainers import ConfirmationArchiveContainer, AccountingArchiveContainer, SettlementArchiveContainer

#BDP
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

#-------------------------------------------------------------------------------------------------------------------
def GetEntityDictFromArgs(args):
    entityDict = {}
    if "journals" in args:
        entityDict["journals"] = args["journals"]
    if "settlements" in args:
        entityDict["settlements"] = args["settlements"]
    if "confirmations" in args:
        entityDict["confirmations"] = args["confirmations"]
    return entityDict

#-------------------------------------------------------------------------------------------------------------------
def PerformOperationsArchiving(args):
    handler = OperationsArchiveHandler(args)
    handler.Perform()

#-------------------------------------------------------------------------------------------------------------------
class OperationsArchiveHandler():
    def __init__(self, args):
        self.args = args
        self.testmode = None
        self.entityDict = None
        self.reportPath = None
        self.reportFilename = None

    #-------------------------------------------------------------------------------------------------------------------
    def __ReadArguments(self, args):
        self.entityDict = GetEntityDictFromArgs(args)
        self.testmode = args["Testmode"]
        self.reportPath = args["report_path"]

    #-------------------------------------------------------------------------------------------------------------------
    def Perform(self):
        self.__ReadArguments(self.args)
        self.__CreateReportFileName()
        self.__ArchiveEntities()
        self.__GenerateReport(self.args)

    #-------------------------------------------------------------------------------------------------------------------
    def __ArchiveEntities(self):

        for (entityId, entities) in self.entityDict.items():
            try:
                if entities:
                    if entityId == "journals":
                        accountingArchiveContainer = AccountingArchiveContainer(entities)
                        accountingArchiver = OperationsArchiver(self.testmode, self.args)
                        self.__CallArchive(accountingArchiver, entityId, "Journal", accountingArchiveContainer.GetJournals())

                        journalLinkArchiver = JournalLinkArchiver(self.testmode, self.args)
                        if self.testmode:
                            journalLinkArchiver.LogTestMode()
                        else:
                            self.__CallArchive(journalLinkArchiver, "journal links", "JournalLink", accountingArchiveContainer.GetJournalLinks())

                        journalInformationArchiver = JournalInformationArchiver(self.testmode, self.args)
                        if self.testmode:
                            journalInformationArchiver.LogTestMode()
                        else:
                            self.__CallArchive(journalInformationArchiver, "journal informations", "JournalInformation", accountingArchiveContainer.GetJournalInformations())


                    elif entityId == "settlements":
                        settlementArchiveContainer = SettlementArchiveContainer(entities)
                        settlementArchiver = SettlementArchiver(self.testmode, self.args)

                        settlementArchiver.LogStart(entityId)
                        settlementArchiver.LogActiveSettlements(settlementArchiveContainer.GetActiveSettlements())
                        settlementArchiver.LogExcludedSettlements(settlementArchiveContainer.GetExcludedSettlements())
                        settlementArchiver.Archive(settlementArchiveContainer.GetEntityName(), settlementArchiveContainer.GetAllEntitiesToArchive())
                        settlementArchiver.LogEnd(entityId)


                    elif entityId == "confirmations":
                        confirmationArchiveContainer = ConfirmationArchiveContainer(entities)
                        confirmationArchiver = OperationsArchiver(self.testmode, self.args)
                        self.__CallArchive(confirmationArchiver, entityId, "Confirmation", confirmationArchiveContainer.GetAllEntitiesToArchive())

                    else:
                        raise TypeError("Type {} not supported".format(entityId))

            except TypeError as error:
                Logme()("------------------------------------", "ERROR")
                Logme()("Archiving of entities of type {} is not \n" \
                        "supported via the operations archiving script.".format(entityId), "ERROR")
                Logme()("", "ERROR")
                Logme()("{}".format(str(error)), "ERROR")
                Logme()("------------------------------------", "ERROR")
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

    #-------------------------------------------------------------------------------------------------------------------
    def __CreateReportFileName(self):
        if not self.reportPath:
            return
        import os
        if not os.path.exists(self.reportPath):
            os.makedirs(self.reportPath)
            Logme()("Created directory: {}".format(self.reportPath), 'ERROR')
        module = 'FOperationsArchive'
        d_str = acm.Time.DateToday()
        fileprefix = os.path.join(self.reportPath, "{}_{}".format(module, d_str))
        n = ''
        j = 0
        while os.path.exists(fileprefix + n + ".txt"):
            j = j + 1
            if j > 0:
                n = "_%d" % j
            if j > 100:
                Logme()("More than 100 report files exists! Abort execution!", 'ERROR')
                return
        self.reportFilename = os.path.normpath(fileprefix + n + ".txt")

    #-------------------------------------------------------------------------------------------------------------------
    def __GenerateReport(self, args):
        if not self.reportPath or not self.reportFilename:
            return
        try:
            fp = open(self.reportFilename, 'w')
        except Exception:
            Logme()("Failed to open file: {}. Can't generate report.".format(self.reportFilename), 'ERROR')
            return
        fp.write(self.BuildReportStr(args))
        fp.close()
        Logme()("Report generated!", 'INFO')

    #-------------------------------------------------------------------------------------------------------------------
    def BuildReportStr(self, args):
        #Header
        reportStr = Summary().buildHeader()
        reportStr += '\n'
        #Execution Parameters
        reportStr += Summary().buildExecutionParametersStr(args)
        reportStr += '\n'
        # Handling section
        logTables = []
        if Logme().getLogMode() < 2:
            logTables =  ['Instrument'] #
        reportStr += Summary().buildOkIdsStr(logTables)
        # Failed section
        reportStr += Summary().buildErrorsAndWarningsStr()
        reportStr += '\n'
        # Actions
        reportStr += Summary().buildActionStr()
        reportStr += '\n'
        return reportStr

    #-------------------------------------------------------------------------------------------------------------------
    def __CallArchive(self, archiver, entityId, entityName, entities):
        archiver.LogStart(entityId)
        archiver.Archive(entityName, entities)
        archiver.LogEnd(entityId)
