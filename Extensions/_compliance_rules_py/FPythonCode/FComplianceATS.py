""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceATS.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceATS

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
        
-----------------------------------------------------------------------------"""
import acm
import FAppliedRuleServer
from FCalculationSpaceUtils import SpaceCollection
from FComplianceRulesUtils import logger


class TaskParamsReader(object):

    def __init__(self, taskParams):
        self._param = taskParams
        if not self._param:
            raise ValueError('Option task_parameters not found')
        
    def GetFolder(self, validator=None):
        queryId = self._param.At('Query', None)
        if queryId is None:
            raise ValueError('Parameter Query not found in task_parameters')
        folder = acm.FStoredASQLQuery[queryId]
        if folder is None:
            raise ValueError('Query {0} not found'.format(queryId))
        if validator is not None:
            validator(folder)
        return folder
        
        
class NoQuery(object):

    def Select(self):
        return []
        
    def IsSatisfiedBy(self, anObject):
        return False

        
def validate(folder):
    if folder.QueryClass() is not acm.FAppliedRule:
        raise ValueError('Query {0} must have QueryClass set to FAppliedRule '
            'instead of {1}'.format(folder.Name(), folder.QueryClass().Name()))

def getQuery(params):
    try:
        reader = TaskParamsReader(params)
        return reader.GetFolder(validate).Query()
    except ValueError as err:
        logger.error(err)
        return NoQuery()
        
        
params = acm.TaskParameters().At('taskParameters')
server = FAppliedRuleServer.Server(getQuery(params))

def start():
    server.Start()

def work():
    server.Run()
    SpaceCollection.Refresh()

def stop():
    server.Stop()