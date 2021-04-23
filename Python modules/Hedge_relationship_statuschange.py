"""
-----------------------------------------------------------------------------------------------------
MODULE    
    Hedge_relationship_statuschange
    
DESCRIPTION
    Date                    : 2018-05-15
    Purpose                 : Forces a status update of hedge relationships
    Department and Desk     : Treasury
    Requester               : James Moodie

HISTORY
======================================================================================================
    Date              Jira Number        Developer              Description
------------------------------------------------------------------------------------------------------
    2021-03-30        PCGDEV-700         Qaqamba Ntshobane      Only allow MO to run script
------------------------------------------------------------------------------------------------------
"""

import acm
import HedgeRelation
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

TCU_GROUPS = [acm.FUserGroup[639].Name(), acm.FUserGroup[646].Name()]
LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add(
    'dummyRun', 
    label='Dummy Run',
    cls='bool', 
    collection=[True, False],
    default=False,
    alt='Check this to avoid committing changes')
ael_variables.add(
    'listOfHedgesToDiscard',
    label='Hedge Relationships', 
    cls='string',
    default='HR/3800342',
    multiple=True,
    alt='Use a comma as a separator.')
ael_variables.add(
    'beforeStatus',
    label='Before Status',
    cls='string',
    collection=['Proposed'],
    default='Simulated')
ael_variables.add(
    'afterStatus',
    label='After Status',
    cls='string',
    collection=['Discard'],
    default='Active')


def ael_main(dict):
    listOfHedgesToDiscard = dict['listOfHedgesToDiscard']
    dummy_run = dict['dummyRun']

    user_group = acm.User().UserGroup().Name()

    if user_group not in TCU_GROUPS:
        raise RuntimeError('Only {0} can use this script. You belong to {1}'.format(TCU_GROUPS[0], user_group))

    for hedgeName in listOfHedgesToDiscard:
        hedgeRelationship = HedgeRelation.HedgeRelation(hedgeName)
        hedgeRelationship.read()

        beforeStatus = hedgeRelationship.get_status()

        if beforeStatus in ['Simulated', 'Proposed']:
            setStatus = dict['afterStatus']
            hedgeRelationship.set_status(setStatus)

            if dummy_run:
                LOGGER.info('{0}.\tBefore status: {1}\tAfter status: {2}'.format(hedgeName, beforeStatus, hedgeRelationship.get_status()))
            else:
                try:
                    hedgeRelationship.save()
                    LOGGER.info('{0} saved.\tBefore status: {1}\tAfter status: {2}'.format(hedgeName, beforeStatus, hedgeRelationship.get_status()))
                except Exception as ex:
                    LOGGER.exception('ERROR: Failed to discard {0}. Exception: {1}'.format(hedgeName, ex))
    LOGGER.info('Done')
