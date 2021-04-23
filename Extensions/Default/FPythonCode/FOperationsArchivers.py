""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsArchivers.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsArchivers - Archiver classes for operations related objects.

    (c) Copyright 2018 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm, ael

#operations
from FOperationsRollbackWrapper import FOperationsRollbackWrapper

#BDP
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

BATCH_SIZE = 1000

class OperationsArchiver():

    def __init__(self, testmode, args):
        self.__args = args
        self.__testmode = testmode
        self.archivedEntitiesCounter = 0
        self.archivedEntitiesAfterLastTransaction = 0
        self.processedEntitiesCounter = 0
        self.archivedEntitiesInBatch = []
        self.ignoredEntitiesInBatch = []
        self.entityName = ""
        self.rollbackEnabled = self.__args['rollback']
        self.rollback = None
        self.currentEntity = None

    def Archive(self, entityName, entitiesToArchive):

        self.entityName = entityName
        self.rollback = FOperationsRollbackWrapper(self.rollbackEnabled, self.entityName, 0, self.Arguments())
        self.archivedEntitiesCounter = 0
        self.archivedEntitiesAfterLastTransaction = 0
        self.processedEntitiesCounter = 0
        self.archivedEntitiesInBatch = []
        self.ignoredEntitiesInBatch = []
        self.currentEntity = None
        try:
            self.__ArchiveEntities(entitiesToArchive)
        except Exception as error:
            if not self.InTestmode():
                self.rollback.abortTransaction()
            self.LogFailedCommitTransaction(error, self.archivedEntitiesInBatch)
            return

    def __ArchiveEntities(self, acmObjects):
        for acmEntity, linkedObjects in acmObjects.iteritems():
            self.currentEntity = acmEntity
            self.processedEntitiesCounter += 1
            aelEntity = self.GetAelEntity(self.currentEntity)
            if self.EntityShouldBeArchived(aelEntity):
                while aelEntity:
                    if self.archivedEntitiesAfterLastTransaction == 0:
                        if not self.InTestmode():
                            self.rollback.beginTransaction()

                    aelEntityClone = aelEntity.clone()
                    if not self.InTestmode():
                        aelEntityClone.archive_status = 1
                        self.rollback.add(aelEntityClone, ['archive_status'], 'Update')
                    self.archivedEntitiesInBatch.append(self.currentEntity)
                    self.archivedEntitiesCounter += 1
                    self.archivedEntitiesAfterLastTransaction += 1

                    if linkedObjects:
                        self.currentEntity = linkedObjects.pop()
                        aelEntity = self.GetAelEntity(self.currentEntity)
                    else:
                        aelEntity = None
            else:
                self.ignoredEntitiesInBatch.append(self.currentEntity)


            if self.archivedEntitiesAfterLastTransaction >= BATCH_SIZE:
                    if not self.InTestmode():
                        self.rollback.commitTransaction()
                    self.archivedEntitiesAfterLastTransaction = 0
                    self.LogArchivedEntities()
                    self.LogIgnoredEntities()
                    self.archivedEntitiesInBatch = []
                    self.ignoredEntitiesInBatch = []

        if self.archivedEntitiesInBatch:
            if not self.InTestmode():
                self.rollback.commitTransaction()
            self.archivedEntitiesAfterLastTransaction = 0
            self.LogArchivedEntities()

        if self.ignoredEntitiesInBatch:
            self.LogIgnoredEntities()

    def InTestmode(self):
        return self.__testmode

    def Arguments(self):
        return self.__args

    def GetAelEntity(self, entity):
        e = None
        if entity:
            exec("e = ael.%s[entity.Oid()]" % entity.RecordType())
        return e

    def IsArchived(self, aelEntity):
        return True if aelEntity and aelEntity.archive_status else False

    def EntityShouldBeArchived(self, aelEntity):
        return not self.IsArchived(aelEntity)

    def LogArchivedEntities(self):
        Logme()("Processed {} {}s so far".format(self.processedEntitiesCounter, self.entityName))
        for archivedEntity in self.archivedEntitiesInBatch:
            Summary().ok(archivedEntity, Summary().ARCHIVE, archivedEntity.Oid())

    def LogIgnoredEntities(self):
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, Summary().ARCHIVE, "already archived", ignoredEntity.Oid())

    def LogFailedCommitTransaction(self, error, failedEntitiesInBatch):
        Logme()("------------------------------------", "ERROR")
        Logme()("An exception occurred while processing {} {} which caused the current transaction to be aborted:".format(self.currentEntity.ClassName(), self.currentEntity.Oid()), "ERROR")
        Logme()("", "ERROR")
        Logme()("{}".format(str(error)), "ERROR")
        Logme()("", "ERROR")
        Logme()("All entities in the current transaction will be restored.", "ERROR")
        Logme()("------------------------------------", "ERROR")
        for failedEntity in failedEntitiesInBatch:
            Summary().fail(failedEntity, Summary().ARCHIVE, 'Failed to archive {} {}.'.format(self.entityName.lower(), failedEntity.Oid()), failedEntity.Oid())

    def LogStart(self, entityType):
        Logme()("", "INFO")
        Logme()("Start archiving {}".format(entityType), "INFO")

    def LogEnd(self, entityType):
        Logme()("Finished archiving {}".format(entityType), "INFO")


class SettlementArchiver(OperationsArchiver):

    def __init__(self, testmode, args):
        OperationsArchiver.__init__(self, testmode, args)

    def LogActiveSettlements(self, activeSettlements):
        for settlement in activeSettlements:
            Summary().ignore(settlement, Summary().ARCHIVE, 'is within the active settlements window or in the future, hence not archived', settlement.Oid())

    def LogExcludedSettlements(self, excludedSettlements):
        for settlement in excludedSettlements:
            Summary().ignore(settlement, Summary().ARCHIVE, 'Referenced/Referred by settlements that are not archived', settlement.Oid())

    def LogIgnoredEntities(self):
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, Summary().ARCHIVE, "already archived", ignoredEntity.Oid())

class JournalLinkArchiver(OperationsArchiver):

    def __init__(self, testmode, args):
        OperationsArchiver.__init__(self, testmode, args)

    def EntityShouldBeArchived(self, aelEntity):
        acmObj = acm.FJournalLink[aelEntity.seqnbr]
        return not self.IsArchived(aelEntity) and self.IsObjectArchiveApplicable(acmObj)

    def IsObjectArchiveApplicable(self, acmObj):
        isApplicable = True
        for journal in acmObj.Journals():
            aelJournal = ael.Journal[journal.Oid()]
            if not aelJournal.archive_status:
                isApplicable = False
                break
        return isApplicable

    def LogIgnoredEntities(self):
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, Summary().ARCHIVE, 'Referenced by journals that are not archived', ignoredEntity.Oid())

    def LogTestMode(self):
        Logme()("", "INFO")
        Logme()("------------------------------------", "INFO")
        Logme()("Please note that when running this ", "INFO")
        Logme()("script, journal link records", "INFO")
        Logme()("might be archived if all their journals", "INFO")
        Logme()("have been archived, but this will not", "INFO")
        Logme()("be shown when running in testmode.", "INFO")
        Logme()("------------------------------------", "INFO")

class JournalInformationArchiver(JournalLinkArchiver):

    def __init__(self, testmode, args):
        JournalLinkArchiver.__init__(self, testmode, args)

    def EntityShouldBeArchived(self, aelEntity):
        acmObj = acm.FJournalInformation[aelEntity.seqnbr]
        return not self.IsArchived(aelEntity) and self.IsJournalInformationArchiveApplicable(acmObj)

    def IsJournalInformationArchiveApplicable(self, acmObj):
        isApplicable = True
        if self.IsObjectArchiveApplicable(acmObj):
            ai = acmObj.AccountingInstruction()
            if ai:
                isApplicable = not ai.IsPeriodic()
        else:
            isApplicable = False
        return isApplicable

    def LogIgnoredEntities(self):
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, Summary().ARCHIVE, self._GetLogString(ignoredEntity), ignoredEntity.Oid())

    def _GetLogString(self, entity):
        ai = entity.AccountingInstruction()
        return 'Periodic accounting instruction' if ai and ai.IsPeriodic() else 'Referenced by journals that are not archived'

    def LogTestMode(self):
        Logme()("", "INFO")
        Logme()("------------------------------------", "INFO")
        Logme()("Please note that when running this ", "INFO")
        Logme()("script, journal information records", "INFO")
        Logme()("might be archived if all their journals", "INFO")
        Logme()("have been archived, but this will not", "INFO")
        Logme()("be shown when running in testmode.", "INFO")
        Logme()("------------------------------------", "INFO")
