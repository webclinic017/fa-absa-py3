""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FEntitiesArchiver.py"
"""----------------------------------------------------------------------------
MODULE
    FEntitiesArchiver - Archiver classes for objects.

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm, ael

#operations

#BDP
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
import FBDPRollback


BATCH_SIZE = 1000

class entitiesArchiver():

    def __init__(self, testmode, args):
        self.__args = args
        self.__testmode = testmode
        self.archivedEntitiesCounter = 0
        self.archivedEntitiesAfterLastTransaction = 0
        self.archivedEntitiesInBatch = []
        self.ignoredEntitiesInBatch = []
        self.entityName = ""
        self.rollback = None
        self.currentEntity = None

    def Archive(self, entityName, entitiesToArchive):

        self.entityName = entityName
        self.rollback = FBDPRollback.RollbackWrapper("Archive " + self.entityName, 0, self.Arguments())
        self.archivedEntitiesCounter = 0
        self.archivedEntitiesAfterLastTransaction = self.archivedEntitiesCounter
        self.archivedEntitiesInBatch = []
        self.ignoredEntitiesInBatch = []
        self.currentEntity = None
        try:
            self.ArchiveEntities(entitiesToArchive)
        except Exception as error:
            if not self.InTestmode():
                self.rollback.abortTransaction()
            self.LogFailedCommitTransaction(error, self.archivedEntitiesInBatch)
            return

    def ArchiveEntities(self, acmObjects):
        for acmEntity in acmObjects:
            self.currentEntity = acmEntity
            aelEntity = self.GetAelEntity(acmEntity)
            if self.EntityShouldBeArchived(aelEntity):
                if self.archivedEntitiesCounter % BATCH_SIZE == 0 or self.archivedEntitiesCounter == self.archivedEntitiesAfterLastTransaction:
                    if not self.InTestmode():
                        self.rollback.beginTransaction()

                aelEntityClone = aelEntity.clone()
                if not self.InTestmode():
                    aelEntityClone.archive_status = 1
                    self.rollback.add(aelEntityClone, ['archive_status'], 'Update')
                self.archivedEntitiesInBatch.append(acmEntity)
                self.archivedEntitiesCounter += 1

                if self.archivedEntitiesCounter % BATCH_SIZE == 0:
                    if not self.InTestmode():
                        self.rollback.commitTransaction()
                    self.archivedEntitiesAfterLastTransaction = self.archivedEntitiesCounter
                    self.LogArchivedEntities()
                    self.LogIgnoredEntities()
                    self.archivedEntitiesInBatch = []
                    self.ignoredEntitiesInBatch = []
            else:
                self.ignoredEntitiesInBatch.append(acmEntity)

        if self.archivedEntitiesInBatch:
            if not self.InTestmode():
                self.rollback.commitTransaction()
            self.archivedEntitiesAfterLastTransaction = self.archivedEntitiesCounter
            self.LogArchivedEntities()

        if self.ignoredEntitiesInBatch:
            self.LogIgnoredEntities()

    def InTestmode(self):
        return self.__testmode

    def Arguments(self):
        return self.__args

    def GetAelEntity(self, entity):
        e = None
        exec("e = ael.%s[entity.Oid()]" % entity.RecordType())
        return e

    def IsArchived(self, aelEntity):
        return True if aelEntity and aelEntity.archive_status else False

    def EntityShouldBeArchived(self, aelEntity):
        return not self.IsArchived(aelEntity)

    def LogArchivedEntities(self):
        Logme()("Archived total {} entities for {}".format(self.archivedEntitiesCounter, self.entityName))
        for archivedEntity in self.archivedEntitiesInBatch:
            Summary().ok(archivedEntity, Summary().ARCHIVE, archivedEntity.Oid())

    def LogIgnoredEntities(self):
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, Summary().ARCHIVE, "already archived", ignoredEntity.Oid())

    def LogFailedCommitTransaction(self, error, failedEntitiesInBatch):
        Logme()("------------------------------------", "ERROR")
        Logme()("An exception occurred while processing {} {} which caused the current transaction to be aborted:".format(self.entityName, self.currentEntity.Oid()), "ERROR")
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
