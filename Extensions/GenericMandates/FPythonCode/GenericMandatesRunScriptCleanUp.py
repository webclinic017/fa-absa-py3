"""
RunScript - Maintenance script

The purpose of this script is to remove selected mandates from the database. It will delete the following objects
linked to the mandate:
 (i) FLimit
 (ii) Text Object
 (iii) Business Processes linked to the FLimit
 (iv) Business Processes linked to the Text Object

"""

import acm

from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import GetAllMandateLimitOids, DeleteTextObject, GetTextObject


def __GetAllMandateNames():
    """
    Function to retrieve the names of all the mandates stored in the database.
    :return: FArray
    """
    mandateNames = acm.FArray()
    limitOids = GetAllMandateLimitOids()
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]
        if limit:
            mandateNames.Add(limit.Name())
    return mandateNames


ael_variables = [
    ['Mandates', 'Mandate Name', 'string', __GetAllMandateNames(), None, 1, 1, 'Choose Mandate to delete', None, 1]]


def ael_main(ael_variables):
    getLogger().info('Mandates clean up script started.')
    mandateNames = ael_variables['Mandates']

    for mandateName in mandateNames:
        getLogger().info('Mandate: %s' % mandateName)
        limit = acm.FLimit[mandateName]

        # Step 1 - Delete business processes linked to limit
        if limit:
            bps = acm.FBusinessProcess.Select('subject_seqnbr=%s' % limit.Oid())
            for bp in bps:
                bp.Delete()

        # Step 2 - Delete Business Processes linked to text object
        textObject = GetTextObject(limit.Oid())
        bps = acm.FBusinessProcess.Select('subject_seqnbr=%s' % textObject.Oid())
        for bp in bps:
            bp.Delete()

        # Step 2 - Delete Text Object linked to mandate
        DeleteTextObject(mandateName)

        # Step 3 - Delete Limit
        limit.Delete()

    getLogger().info('Mandates clean up script completed.')
