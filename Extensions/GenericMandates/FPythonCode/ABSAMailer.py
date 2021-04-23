"""
---------------------------------------------------------------------------------------------------
28-08-2018      Jaysen Naicker          add enviornment name to the subject of all emails
"""
import ael
import acm
import sys
import os

from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate
from GenericMandatesConstants import SUPERVISOR_GROUP_NAME

# Check if the server is a production server before sending emails
CHECK_PRODUCTION = False


def IsProduction():
    """
    Check if the code is run from an environment with the name 'Production'.
    :return: bool
    """
    if CHECK_PRODUCTION is True:
        for item in ael.ServerData.select():
            if item.customer_name == 'Production':
                return True
        return False
    else:
        return True
        

def _GetEnvironmentName():
    """
    Get the name of current environment that the code is running on.
    :return: string
    """
    for item in ael.ServerData.select():
        if item.customer_name:
            return item.customer_name


def _SendMail(subject, body, mailTo, mailFrom):
    from threading import Thread
    thread = Thread(target=_SendMailThreaded, args=(subject, body, mailTo, mailFrom))
    thread.start()


def _SendMailThreaded(subject, body, mailTo, mailFrom):
    mailFrom = "ABCapITRTBAMFrontAre@absa.africa"
    
    if IsProduction() is False:
        subject = "[TEST MAIL] %s" % subject

    try:
        from at_email import EmailHelper

        if IsProduction() is True or CHECK_PRODUCTION is False:
            email = EmailHelper(body, subject, mailTo, mailFrom)
            email.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email.host = EmailHelper.get_acm_host()

            try:
                email.send()
            except Exception as e:
                print(("!!! Exception: {0}\n".format(e)))
                exc_type, _exc_obj, exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print((exc_type, filename, exc_tb.tb_lineno))
            finally:
                getLogger().debug('Thread sending e-mail finished executing')
        else:
            _PrintMail(subject, body, mailTo, mailFrom)

    except Exception as e:
        getLogger().info('Could not import at_email library')
        # getLogger().info('%s' % e)
        _PrintMail(subject, body, mailTo, mailFrom)


def _PrintMail(subject, body, mailTo, mailFrom):
    getLogger().debug('-' * 100)
    getLogger().debug('From: %s' % mailFrom)
    getLogger().debug('To: %s' % mailTo)
    getLogger().debug('Subject: %s' % subject)
    getLogger().debug('Message: %s' % body)
    getLogger().debug('-' * 100)


def SendViolationMail(trade, mandate, mailTo, mailFrom, bp):
    subject = _GetEnvironmentName() + " - Front Arena - Trade breaching mandate (%s)" % mandate.Entity()
    body = "Front Arena - Trade breaching mandate <br><br>" \
           "<b>The following trade has breached a mandate and been blocked:</b><br>" \
           "Trade No: %s<br>" \
           "Mandate Name: %s<br>" \
           "Trader: %s<br>" % (trade.Oid(), mandate.Name(), trade.Trader().Name())
    if trade.Trader().FullName():
        body += "Trader Name: %s<br><br>" % trade.Trader().FullName()
    else:
        body += "<br>"
        
    limit = acm.FLimit['%s' % mandate.LimitOid()]
    if limit:
        body += "<b>Violation process details:</b><br>%s" % GetBusinessProcessFromViolation(bp)

    _SendMail(subject, body, mailTo, mailFrom)


def SendMandateCreatedMail(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate Pending Approval (%s)" % mandate.Entity()
    body = "Front Arena - Mandate authorization process pending approval <br><br>" \
           "<b>The following mandate approval is pending:</b><br>" \
           "Mandate Name: %s<br>" \
           "Mandate Entity Type: %s<br>" \
           "Mandated Entity: %s<br>" \
           "Create Time: %s<br>" \
           "Created By: %s<br><br>" % (mandate.Name(), mandate.Type(), mandate.Entity(), mandate.GetCreateTime(),
                                       mandate.GetCreateUser())
    body += "<b>Authorization process details:</b><br>%s" % GetBusinessProcessParams(mandate)

    if mailTo and mandate and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        _PrintMail(subject, body, mailTo, mailFrom)
        getLogger().warn('Cannot send e-mail.')


def SendMandateAmendedMail(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate Authorization Process Completed (%s)" % mandate.Entity()
    body = "Front Arena - Mandate authorization process completed <br><br>" \
           "<b>The following mandate's approval process has been completed:</b><br>" \
           "Name: %s<br>" \
           "Description: %s<br>" \
           "Mandated Entity Type: %s<br>" \
           "Mandated Entity: %s<br>" \
           "Create Time: %s<br>" \
           "Created By: %s<br><br>" % (mandate.Name(), mandate.GetDescription(), mandate.Type(), mandate.Entity(),
                                       mandate.GetCreateTime(), mandate.GetCreateUser())

    body += "<b>Authorization process details:</b><br>%s" % GetBusinessProcessParams(mandate)

    if mailTo and mandate and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        _PrintMail(subject, body, mailTo, mailFrom)
        getLogger().warn('Cannot send e-mail.')


def SendMandateRejectedMail(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate Authorization Process Rejected (%s)" % mandate.Entity()
    body = "Front Arena - Mandate authorization process rejected <br><br>" \
           "<b>The following mandate's authorization process was rejected:</b><br>" \
           "Name: %s<br>" \
           "Description: %s<br>" \
           "Mandated Entity Type: %s<br>" \
           "Mandated Entity: %s<br>" \
           "Create Time: %s<br>" \
           "Created By: %s<br><br>" % (mandate.Name(), mandate.GetDescription(), mandate.Type(), mandate.Entity(),
                                   mandate.GetCreateTime(), mandate.GetCreateUser())
    body += "<b>Authorization process details:</b><br>%s" % GetBusinessProcessParams(mandate)

    if mailTo and mandate and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        _PrintMail(subject, body, mailTo, mailFrom)
        getLogger().warn('Cannot send e-mail.')


def SendMandateAuthorizedMail(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate Authorized (%s)" % mandate.Entity()
    body = "Front Arena - Mandate Authorized <br><br>" \
           "<b>The following mandate was authorized:</b><br>" \
           "Name: %s<br>" \
           "Description: %s <br>" \
           "Mandate Entity Type: %s<br>" \
           "Mandated Entity: %s<br>" \
           "Create Time: %s<br>" \
           "Created By: %s<br>" \
           "Authorize Time: %s<br>" \
           "Authorized By: %s<br><br>" % (mandate.Name(), mandate.GetDescription(), mandate.Type(), mandate.Entity(),
                                          mandate.GetCreateTime(), mandate.GetCreateUser(), mandate.GetAuthTime(),
                                          mandate.GetAuthTime())
    body += "<b>Authorization process details:</b><br>%s" % GetBusinessProcessParams(mandate)

    if mailTo and mandate and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        _PrintMail(subject, body, mailTo, mailFrom)
        getLogger().warn('Cannot send e-mail.')


def SendMailUserGroupChange(user, oldGroupName, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - User Changed User Group (Mandates)"
    body = "Front Arena - Notification: User changed user group <br><br>" \
           "This message was generated due to a user that moved into a user group " \
           "that is mandated. <br><br>" \
           "Details of user that changed User Groups:<br>" \
           "Username %s <br>" \
           "Full name: %s <br>" \
           "Previous user group: %s<br>" \
           "New user group: %s<br>" % (user.Name(), user.FullName(), oldGroupName, user.UserGroup().Name())

    if mailTo and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        getLogger().warn('Cannot send e-mail.')


def SendMailMandateCloseToExpiry(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate close to expiring (Reminder)"
    body = "Front Arena - Mandate close to expiry <br><br>" \
           "This is a reminder that the following mandate is close to expiring:<br>" \
           "Name: %s <br>" \
           "Description: %s <br>" \
           "Expiry Date: %s <br><br>" \
           "Please renew this mandate before it expires." % (mandate.Name(), mandate.GetDescription(),
                                                             mandate.GetExpireTime())
    if mailTo and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        getLogger().warn('Cannot send e-mail')


def SendMailMandatePendingAuthorizationReminder(mandate, mailTo, mailFrom):
    subject = _GetEnvironmentName() + " - Front Arena - Mandate is pending authorization (Reminder)"
    body = "Front Arena - Mandate is pending authorization <br><br>" \
           "This is a reminder that the following mandate is pending authorization:<br>" \
           "Name: %s <br>" \
           "Description: %s <br>" \
           "Please authorize this mandate." % (mandate.Name(), mandate.GetDescription())
    if mailTo and mailFrom:
        _SendMail(subject, body, mailTo, mailFrom)
    else:
        getLogger().warn('Cannot send e-mail')


def GetProductSupervisorsEmails(mandate):
    """
    Return the e-mail information of Product Supervisor(s) for a specific mandate.
    :param mandate: Mandate
    :return: string
    """
    users = mandate.GetProductSupervisorUsers()    
    addresses = [user.Email() for user in users]
    addresses = filter(None, addresses)
    return addresses


def GetMandatedTradersEmails(mandate):
    """
    Return a list containing the e-mail addresses of all the mandated traders for a specific mandate.
    :param mandate: Mandate
    :return: string
    """
    users = mandate.GetMandatedUsers()
    addresses = [trader.Email() for trader in users]
    addresses = filter(None, addresses)
    return addresses


def GetAfricaSupervisorGroupEmails():
    """
    Return a list containing the e-mail addresses of all the users in the "Africa Supervisor" user group.
    :return: string
    """
    userGroup = acm.FUserGroup[SUPERVISOR_GROUP_NAME]
    if userGroup:
        users = userGroup.Users()
        addresses = [user.Email() for user in users]
        addresses = filter(None, addresses)
        return addresses
    else:
       getLogger().error('The %s user group does not exist.' % SUPERVISOR_GROUP_NAME)
       return []


def GetBusinessProcessParams(mandate):
    returnString = ""
    mandateTextObject = acm.FCustomTextObject['%s' % mandate.LimitOid()]
    subjectSequenceNbr = mandateTextObject.Oid()

    selection = acm.FBusinessProcess.Select('subject_seqnbr=%i' % subjectSequenceNbr)
    bp = selection[0]
    bpParams = bp.CurrentStep().DiaryEntry().Parameters()
    for key in bpParams.Keys():
        returnString += '%s: %s <br>' % (key, bpParams[key])
    return returnString


def GetBusinessProcessFromViolation(bp):
    returnString = ""
    bpParams = bp.CurrentStep().DiaryEntry().Parameters()
    for key in bpParams.Keys():
        returnString += '%s: %s <br>' % (key, bpParams[key])

    returnString += "<br><b>Violation comment:</b><br>"
    returnString += "<br>".join(bp.CurrentStep().DiaryEntry().Notes())
    return returnString
