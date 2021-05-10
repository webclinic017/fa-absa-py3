"""
RunScript

Script that will run end of day.

The purpose of this script:

(1) To check for mandates that are close to expiring and send an e-mail notification once this occurs.
(2) Check for mandates that are pending authorization and send an e-mail reminder to the authorizers.

This RunScript should be setup to run once a day.
"""

import acm

from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate, GetAllMandateLimitOids
from ABSAMailer import GetAfricaSupervisorGroupEmails, SendMailMandateCloseToExpiry, SendMailMandatePendingAuthorizationReminder


DAYS_TILL_EXPIRY_LIMIT = 7


ael_variables = [
]


def ael_main(ael_variables):
    getLogger().info('Mandates - E-mail reminder script starting ...')
    getLogger().info('Retrieving all Mandates')

    limitOids = GetAllMandateLimitOids()
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]
        if limit:
            mandate = Mandate(limit)

            # Check for any Mandates that are close to expiring and send an e-mail reminder
            mandate.GetExpireTime()
            if mandate and mandate.GetExpireTime():
                daysTillExpiry = acm.Time.DateDifference(mandate.GetExpireTime(), acm.Time.DateToday())
                getLogger().info('%s expires @ %s' % (mandate.Name(), mandate.GetExpireTime()))
                if daysTillExpiry <= DAYS_TILL_EXPIRY_LIMIT:
                    getLogger().debug('Send e-mail notification')
                    supervisorMails = GetAfricaSupervisorGroupEmails()
                    SendMailMandateCloseToExpiry(mandate, supervisorMails, 'Front Arena - Mandates')

            if mandate:
                stateName = getCurrentStateName(mandate)
                if stateName and 'Authorization stage' in stateName:
                    getLogger().info('Send e-mail notification (authorization reminder e-mail)')
                    supervisorMails = GetAfricaSupervisorGroupEmails()
                    SendMailMandatePendingAuthorizationReminder(mandate, supervisorMails, 'Front Arena - Mandates')
        else:
            getLogger().warn('Limit does not exist anymore (Oid: %s)' % limitOid)

    getLogger().info('Mandates - E-mail reminder script finished running.')


def getCurrentStateName(mandate):
    """
    Retrieve the name of the State that the mandate's authorization business process is currently in.
    :param mandate: Mandate
    :return: string
    """
    textObject = acm.FCustomTextObject['%i' % mandate.LimitOid()]
    if textObject:
        bps = acm.FBusinessProcess.Select('subject_seqnbr=%i' % textObject.Oid())
        for bp in bps:
            if bp.StateChart().Name() == "GenericMandatesAuthorization_v3":
                return bp.CurrentStep().State().Name()
    else:
        getLogger().error('[ERROR] Text Object does not exist (%s)' % mandate.LimitOid())
