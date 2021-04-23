""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/delete/FDeleteBusinessProcessesPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FDeleteBusinessProcessesPerform - Module to delete business processes

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FBusinessProcessesPerform
import importlib
importlib.reload(FBusinessProcessesPerform)
from FBDPCurrentContext import Summary

def perform(params):
    params['other_params'] = {
        'task': 'deleting',
        'src_archive_status': int(not params['NonArchived']),
        'action': Summary().DELETE,
    }
    FBusinessProcessesPerform.perform(params, DeleteBusinessProcesses)

class DeleteBusinessProcesses(
        FBusinessProcessesPerform.BusinessProcessesPerform
):
    # override
    def processObj(self, obj):
        if (not self.testmode and
            obj.record_type != 'BusinessProcessStep'):
            obj.delete()

        return
