""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/archive/FArchiveBusinessProcessesPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FArchiveBusinessProcessesPerform - Module to archive business processes

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FBusinessProcessesPerform
import importlib
importlib.reload(FBusinessProcessesPerform)
from FBDPCurrentContext import Summary

def perform(params):
    dearchive = bool(params['Dearchive'])
    params['other_params'] = {
        'task': 'de-archiving' if dearchive else 'archiving',
        'src_archive_status': 1 if dearchive else 0,
        'action': Summary().DEARCHIVE if dearchive else Summary().ARCHIVE,
    }
    FBusinessProcessesPerform.perform(params, ArchiveBusinessProcesses)

class ArchiveBusinessProcesses(
    FBusinessProcessesPerform.BusinessProcessesPerform
):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        super(ArchiveBusinessProcesses, self).__init__(
            testmode, baseParams, otherParams
        )
        self.new_archive_status = int(not bool(self._src_archive_status))

    # override
    def processObj(self, obj):
        if not self.testmode:
            obj = obj.clone()
            obj.archive_status = self.new_archive_status
            obj.commit()

        return obj
