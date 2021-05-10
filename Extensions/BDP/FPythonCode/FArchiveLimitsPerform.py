""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/limits/bdp/archive/FArchiveLimitsPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FArchiveLimitsPerform - Called from FArchiveLimits

DESCRIPTION
    Main module for archiving limits. 

----------------------------------------------------------------------------"""


import acm, ael
import FBDPCommon
import FArchiveLimits

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import FBDPRollback


BatchSize = 10  # For production purposes set this value to 1000

def perform(dictionary):
    Logme()('Archiving Limits')
    processor = ArchivingLimitsProcessor()
    processor.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')


class ArchivingLimitsProcessor(object):

    def __init__(self):
        self.processedEntitiesCounter = 0
        self.processedEntitiesAfterLastTransaction = 0
        self.processedEntitiesInBatch =[]
        self.ignoredEntitiesInBatch = []
        self.entitiesToBeProcessed = []
        self.descendantLimits = []
        self.entityName = 'Limits'
        self.rollback = None
        self.currentEntity = None

    def readArguments(self, dictionary):
        self.testmode = True
        if 'Testmode' in dictionary:
            self.testmode = dictionary['Testmode']

        self.limits = acm.FArray()
        if 'Limits' in dictionary and dictionary['Limits']:
            for oid in dictionary['Limits']:
                self.limits.Add(ael.Limit[int(str(oid))])

        self.deArchive = 0
        if 'Dearchive' in dictionary and dictionary['Dearchive']:
            self.deArchive = dictionary['Dearchive']

        self.newArchiveStatus = 1 - self.deArchive

    # For a given limit returns corresponding business process
    def _getAssociatedBusinessProcess(self, limit):
        limOid = limit.seqnbr
        constraint = 'subject_seqnbr={}'.format(limOid)
        bpSelection = acm.FBusinessProcess.SqlSelect('oid', constraint)
        bpOid = bpSelection[0].ColumnValues()[0]
        bp = ael.BusinessProcess[bpOid]

        return bp

    # For a given business process returns a list of business process steps
    def _getBusinessProcessSteps(self, bp):
        return bp.reference_in()

    # For a given limit returns a list of its descendants
    def _getDescendantLimits(self, limit):
        chLimits = limit.reference_in()
        if chLimits:
            for chLimit in chLimits:
                self.descendantLimits.append(chLimit)
                self._getDescendantLimits(chLimit)
        else:
            self.descendantLimits.append(limit)

    def processEntity(self, ent):
        entClone = ent.clone()
        entClone.archive_status = self.newArchiveStatus
        entClone.commit()

    def processEntities(self, aelEntitySet):
        for aelEntity in aelEntitySet:
            self.currentEntity = aelEntity
            if self.entityShouldBeProcessed(aelEntity):
                if self.processedEntitiesCounter % BatchSize == 0 or self.processedEntitiesCounter == self.processedEntitiesAfterLastTransaction:
                    if not self.testmode:
                        ael.begin_transaction()

                if not self.testmode:
                    self.processEntity(aelEntity)
                self.processedEntitiesInBatch.append(aelEntity)
                self.processedEntitiesCounter += 1

                if self.processedEntitiesCounter % BatchSize == 0:
                    if not self.testmode:
                        ael.commit_transaction()
                    self.processedEntitiesAfterLastTransaction = self.processedEntitiesCounter
                    self.logProcessedEntities()
                    self.logIgnoredEntities()
                    self.processedEntitiesInBatch =[]
                    self.ignoredEntitiesInBatch = []
            else:
                self.ignoredEntitiesInBatch.append(aelEntity)

        if self.processedEntitiesInBatch:
            if not self.testmode:
                ael.commit_transaction()
            self.processedEntitiesAfterLastTransaction = self.processedEntitiesCounter
            self.logProcessedEntities()

        if self.ignoredEntitiesInBatch:
            self.logIgnoredEntities()

    def entityShouldBeProcessed(self, ent):
        if ent.archive_status == self.newArchiveStatus:
            return False
        else:
            return True

    def performProcess(self, dictionary):
        self.readArguments(dictionary)
        self.logStart()
        action = 'Archive' if not self.deArchive else 'Dearchive'
        self.rollback = FBDPRollback.RollbackWrapper(action + self.entityName)
        limitsForProcessingList = []
        for limit in self.limits:
            self._getDescendantLimits(limit)
            if self.descendantLimits:
                limitsForProcessingList.extend(self.descendantLimits)
            limitsForProcessingList.append(limit)

        limitsForProcessing = set(limitsForProcessingList)

        # Colecting Limits and linked objects 
        for limit in limitsForProcessing:
            bp = self._getAssociatedBusinessProcess(limit)
            if bp:
                self.entitiesToBeProcessed.append(bp)
                bpSteps = self._getBusinessProcessSteps(bp)
                self.entitiesToBeProcessed.extend(bpSteps)
            self.entitiesToBeProcessed.append(limit)
            
        # Processing self.entitiesToBeProcessed
        try:
            self.processEntities(self.entitiesToBeProcessed)
        except Exception as error:
            if not self.testmode:
                ael.abort_transaction()
            self.logFailedCommitTransaction(error, self.processedEntitiesInBatch)

        self.logEnd()

    def logProcessedEntities(self):
        action = 'Archived' if not self.deArchive else 'Dearchived'
        Logme()("{} total {} entities for {}".format(action, self.processedEntitiesCounter, self.entityName))
        for archivedEntity in self.processedEntitiesInBatch:
            Summary().ok(archivedEntity, action, archivedEntity.seqnbr)

    def logIgnoredEntities(self):
        action = 'Archiving' if not self.deArchive else 'Dearchiving'
        for ignoredEntity in self.ignoredEntitiesInBatch:
            Summary().ignore(ignoredEntity, action, "already processed", ignoredEntity.seqnbr)

    def logFailedCommitTransaction(self, error, failedEntitiesInBatch):
        action = 'Archive' if not self.deArchive else 'Dearchive'
        Logme()("------------------------------------", "ERROR")
        Logme()("An exception occurred while processing {} {} which caused the current transaction to be aborted:".format(self.currentEntity.record_type, self.currentEntity.seqnbr), "ERROR")
        Logme()("", "ERROR")
        Logme()("{}".format(str(error)), "ERROR")
        Logme()("", "ERROR")
        Logme()("All entities in the current transaction will be restored.", "ERROR")
        Logme()("------------------------------------", "ERROR")
        for failedEntity in failedEntitiesInBatch:
            Summary().fail(failedEntity, action, 'Failed to {} {} {}.'.format(action, failedEntity.record_type.lower(), failedEntity.seqnbr), failedEntity.seqnbr)

    def logStart(self):
        action = 'Archiving' if not self.deArchive else 'Dearchiving'
        Logme()("", "INFO")
        Logme()("Start {} {}".format(action, self.entityName), "INFO")

    def logEnd(self):
        action = 'Archiving' if not self.deArchive else 'Dearchiving'
        Logme()("Finished {} {}".format(action, self.entityName), "INFO")

