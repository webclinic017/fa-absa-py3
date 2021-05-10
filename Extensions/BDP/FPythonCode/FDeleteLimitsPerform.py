""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/limits/bdp/delete/FDeleteLimitsPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDeleteLimitsPerform - Called from FDeleteLimits

DESCRIPTION
    Main module for deleting limits. 

----------------------------------------------------------------------------"""


import acm, ael
import FBDPCommon
import FDeleteLimits

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import FBDPRollback

def perform(dictionary):
    Logme()('Deleting Limits')
    processor = DeletingLimitsProcessor()
    processor.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')


class DeletingLimitsProcessor(object):

    def __init__(self):
        self.deletedEntitiesCounter = 0
        self.deletedEntitiesAfterLastTransaction = 0
        self.deletedEntitiesInBatch =[]
        self.ignoredEntitiesInBatch = []
        self.entitiesToBeDeleted = {'lim': [], 'bp': [], 'bps': []}
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
        if 'NonArchived' in dictionary and dictionary['NonArchived']:
            self.nonArchive = dictionary['NonArchived']

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

    def performProcess(self, dictionary):
        Logme()('Deleting limits', 'INFO')
        self.readArguments(dictionary)
        action = 'Delete'
        self.rollback = FBDPRollback.RollbackWrapper(action + self.entityName)
        limitsForProcessingList = []
        for limit in self.limits:
            self._getDescendantLimits(limit)
            if self.descendantLimits:
                limitsForProcessingList.extend(self.descendantLimits)
            limitsForProcessingList.append(limit)

        limitsForProcessing = set(limitsForProcessingList)
        
        # Collecting entities for deletion
        for limit in limitsForProcessing:            
            bp = self._getAssociatedBusinessProcess(limit)
            if bp:
                self.entitiesToBeDeleted['bp'].append(bp)
                bpSteps = self._getBusinessProcessSteps(bp)
                self.entitiesToBeDeleted['bps'].extend(bpSteps)
            self.entitiesToBeDeleted['lim'].append(limit)

        for bp in self.entitiesToBeDeleted['bp']:
            try:
                bp.delete()
                self.deletedEntitiesInBatch.append(bp)
                Summary().ok(bp, action)
            except Exception as e:
                self.ignoredEntitiesInBatch.append(bp)
                Summary().fail(bp, action, e, bp.seqnbr)

        for lim in self.entitiesToBeDeleted['lim']:
            try:
                lim.delete()
                self.deletedEntitiesInBatch.append(lim)
                Summary().ok(lim, action)
            except Exception as e:
                self.ignoredEntitiesInBatch.append(lim)
                Summary().fail(lim, action, e, limit.seqnbr)

