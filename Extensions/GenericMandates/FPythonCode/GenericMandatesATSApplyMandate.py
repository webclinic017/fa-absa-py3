"""
    ATS that subscribes to the FBusinessProcess table.

"""

import acm
import queue
import smtplib
import string
import json


from GenericMandatesConstants import FPARAM_VIOLATION_EMAIL_ENABLED, FPARAM_VIOLATION_EMAIL_RECIPIENT, \
    FPARAM_VIOLATION_EMAIL_SENDER, FPARAM_VIOLATION_EMAIL_SERVER
from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import GetAllMandateLimitOids, Mandate
from GenericMandatesUtils import GetMandateSettingsParam
from ABSAMailer import SendMailUserGroupChange, GetAfricaSupervisorGroupEmails, SendViolationMail, \
    SendMandateCreatedMail, SendMandateAuthorizedMail, GetMandatedTradersEmails, SendMandateAmendedMail, \
    SendMandateRejectedMail


CHART_VIOLATION = 'GenericMandates_ViolationStates'
CHART_AUTHORIZATION = 'GenericMandatesAuthorization_v3'
TRANSITION = 'Save to DB'
USER_TRACKER_TEXT_OBJECT = 'Mandates_UserTracker'

ENABLE_AUTHORIZATION_SUBSCRIPTION = True
ENABLE_VIOLATION_SUBSCRIPTION = True
ENABLE_USER_SUBSCRIPTION = True
ENABLE_TRADE_SUBSCRIPTION = False


# Queues containing objects subscribed to
authorizationQueue = queue.Queue()
violationQueue = queue.Queue()
userQueue = queue.Queue()
tradeQueue = queue.Queue()


class UserTracker(object):
    """
    Class that enables the tracking users moving in and out of User Groups.
    """
    def __init__(self, textObjectName):
        self._to = acm.FCustomTextObject[textObjectName]  # pylint: disable=no-member
        if not self._to:
            self._to = acm.FCustomTextObject()  # pylint: disable=no-member
            self._to.Name(textObjectName)
            self._to.Text(json.dumps({}))
            self._to.Commit()
        self._userDict = json.loads(self._to.Text())

    def _UpdateTextObject(self):
        try:
            self._to.Text(json.dumps(self._userDict))
            self._to.Commit()
        except Exception as e:
            getLogger().error('Exception occurred. %s' % e)
            getLogger().error('-'*60)
            import sys
            import traceback
            traceback.print_exc(file=sys.stdout)
            getLogger().error('-'*60)

    def InitialSetup(self, users):
        """
        Set up initial users.
        :param users:
        """
        if users:
            for user in users:
                self._userDict[user.Name()] = user.UserGroup().Name()
            self._to.Commit()

    def GetAllUsers(self):
        """
        Return all the users.
        :return: list
        """
        return self._userDict.keys()

    def GetUserGroup(self, user):
        """
        Get all the user groups.
        :param user:
        :return: list
        """
        if user.Name() in self._userDict.keys():
            return self._userDict[user.Name()]

    def SetUserGroup(self, user):
        self._userDict[user.Name()] = user.UserGroup().Name()
        self._UpdateTextObject()

    def RemoveUser(self, user):
        if user.Name() in self._userDict.keys():
            del self._userDict[user.Name()]
            self._UpdateTextObject()


class UpdateHandler(object):
    # pylint: disable=too-few-public-methods

    """
    Handler to handle updates made to FBusinessProcess objects in the database.
    """
    def ServerUpdate(self, subscribed, operation, obj):
        del subscribed
        stateChart = obj.StateChart().Name()

        if str(operation) in ['insert', 'update'] and stateChart == CHART_AUTHORIZATION:
            # Handling Authorization Business Processes
            getLogger().info('[AUTH] Added - FBusinessProcess updated (Oid: %s) State Chart: %s' % (obj.Oid(), stateChart))
            authorizationQueue.put(obj)
        elif str(operation) == 'insert' and stateChart == CHART_VIOLATION:
            # Handling Violation Business Processes
            getLogger().info('[VIOLATION] FBusinessProcess created (Oid: %s) State Chart: %s' % (obj.Oid(), stateChart))
            violationQueue.put(obj)


class UserUpdateHandler(object):
    # pylint: disable=too-few-public-methods
    """
    Handler to handle updates made to FUser objects in the database.
    """
    def ServerUpdate(self, subscribed, operation, obj):
        del subscribed

        if str(operation) in ['insert', 'remove', 'update']:
            getLogger().info('[USERS] User updated / inserted')
            userQueue.put(obj)


def start():
    """
    Executed when the ATS is starting up.
    """
    acm.Log('-' * 48)
    acm.Log('Mandates ATS - FIS Ltd')
    acm.Log('-' * 48)
    acm.Log('Monitor Authorizations                | %s |' % 'Y' if ENABLE_AUTHORIZATION_SUBSCRIPTION else '')
    acm.Log('Monitor Violations                    | %s |' % 'Y' if ENABLE_VIOLATION_SUBSCRIPTION else '')
    acm.Log('Monitor Users (LAM)                   | %s |' % 'Y' if ENABLE_USER_SUBSCRIPTION else '')
    acm.Log('Monitor Trades                        | %s |' % 'Y' if ENABLE_TRADE_SUBSCRIPTION else '')
    acm.Log('-' * 48)

    getLogger().info('Mandates ATS starting ..')

    if acm.User().Name() == GetMandateSettingsParam("LimitOwnerName"):  # pylint: disable=no-member
        getLogger().info('ATS user name is %s' % acm.User().Name())  # pylint: disable=no-member
        getLogger().info('Process any authorizations pending while the ATS was offline')
        ProcessIncompleteAuthorizations()
                
        getLogger().info('Subscribing to all FBusinessProcess data')
        objSubscription = acm.FBusinessProcess.Select('')  # pylint: disable=no-member
        objUpdateHandler = UpdateHandler()
        objSubscription.AddDependent(objUpdateHandler)

        getLogger().info('Subscribing to all FUser data')
        userSubscription = acm.FUser.Select('')  # pylint: disable=no-member
        userUpdateHandler = UserUpdateHandler()
        userSubscription.AddDependent(userUpdateHandler)

        # Print all mandated users
        getLogger().info('MANDATED USERS:')
        mandatedUsers = GetAllMandatedTraders()
        if mandatedUsers:
            for user in mandatedUsers:
                getLogger().info("%s - %s" % (user.UserGroup().Name(), user.Name()))
    else:
        getLogger().info('[WARNING] ATS should be run with the following user - %s' %
                         GetMandateSettingsParam("LimitOwnerName"))


def stop():
    """
    Executed when the ATS stops.
    """
    pass


def status():
    """
    Executed when the status of the ATS is requested.
    """
    pass


def GetAllAuthBusinessProcesses():
    # Create query
    query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')

    field = "StateChart.Name"
    orNode = query.AddOpNode('AND')
    orNode.AddAttrNode(field, 'EQUAL', CHART_AUTHORIZATION)
    storedQuery = acm.FStoredASQLQuery()
    storedQuery.Query = query
    return query.Select()
    
    
def ProcessIncompleteAuthorizations():
    """
    Process any incomplete authorizations that might have occurred while the ATS was offline.
    """
    businessProcesses = GetAllAuthBusinessProcesses()
    if ENABLE_AUTHORIZATION_SUBSCRIPTION is True:
        for businessProcess in businessProcesses:
            stateChartName = businessProcess.StateChart().Name()
            if stateChartName == CHART_AUTHORIZATION and businessProcess.CanHandleEvent(TRANSITION):
                getLogger().info("Transitioning state to 'Active'. Oid (%s)" % businessProcess.Oid())
                businessProcess.HandleEvent(TRANSITION)
                businessProcess.Commit()

                # Check if e-mails need to be sent out for authorization state changes
                ProcessAuthorization(businessProcess)


def work():
    """
    Executed when an update to any of the monitored database tables occurs.
    """
    # Process Authorizations that are currently queued
    while authorizationQueue.qsize() > 0:
        if ENABLE_AUTHORIZATION_SUBSCRIPTION is True:
            businessProcess = authorizationQueue.get(False)
            if businessProcess.CanHandleEvent(TRANSITION):
                getLogger().info("Transitioning state to 'Active'.")
                businessProcess.HandleEvent(TRANSITION)
                businessProcess.Commit()

            # Check if e-mails need to be sent out for authorization state changes
            ProcessAuthorization(businessProcess)

    # Process violations
    while violationQueue.qsize() > 0:
        if ENABLE_VIOLATION_SUBSCRIPTION is True:
            businessProcess = violationQueue.get(False)
            ProcessViolation(businessProcess)

    # Process User changes that are currently queued
    while userQueue.qsize() > 0:
        if ENABLE_USER_SUBSCRIPTION:
            try:
                user = userQueue.get(False)
                ProcessUserChange(user)
            except Exception as e:
                getLogger().error('Exception: %s' % e)

    # Process trades
    while tradeQueue.qsize() > 0:
        if ENABLE_TRADE_SUBSCRIPTION is True:
            trade = tradeQueue.get(False)
            ProcessTrade(trade)


def GetAllMandatedTraders():
    """
    Retrieve a list of all the traders that currently have a mandate linked to their profiles.
    :return: FArray
    """
    limitOids = GetAllMandateLimitOids()
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]  # pylint: disable=no-member
        if limit:
            mandate = Mandate(limit)
            entity = mandate.Entity()
            group = acm.FUserGroup[entity]  # pylint: disable=no-member

            if group:
                return group.Users()


def GetMailFromAddress():
    """
    Retrieve the e-mail address from which e-mails will be sent.
    :return:
    """
    return str(GetMandateSettingsParam(FPARAM_VIOLATION_EMAIL_SENDER)).replace("'", '')


def ProcessViolation(businessProcess):
    """
    Process violation record (Business Process).
    :param businessProcess: FBusinessProcess
    """
    mandate = None
    params = businessProcess.CurrentStep().DiaryEntry().Parameters()
    paramTradeOptKey = params.At('TradeOptionalKey')
    limit = businessProcess.Subject()
    if limit:
        mandate = Mandate(limit)

    if paramTradeOptKey and mandate:
        trade = acm.FTrade.Select01('optionalKey = %s' % paramTradeOptKey, '')  # pylint: disable=no-member
        mailFrom = GetMailFromAddress()
        # Send e-mail to whole Africa Supervisor group
        mailTo = GetAfricaSupervisorGroupEmails()
        SendViolationMail(trade, mandate, mailTo, mailFrom, businessProcess)

        # Send e-mail to trader who breached the mandate
        mailTo = trade.Trader().Email()
        SendViolationMail(trade, mandate, mailTo, mailFrom, businessProcess)
    else:
        getLogger().error('[ERROR] Could not select trade from DB (Optional Key %s)' % paramTradeOptKey)


def ProcessUserChange(user):
    """
    Process any user changes that were made to users with a mandate linked to them.
    :param user: FUser
    """
    mandatedTraders = GetAllMandatedTraders()
    mandatedTraderNames = [userObj.Name() for userObj in mandatedTraders]
    tracker = UserTracker(USER_TRACKER_TEXT_OBJECT)
    storedUsers = tracker.GetAllUsers()

    # User moved out of Mandated Trader list for all mandates
    if user.Name() in storedUsers and user.Name() not in mandatedTraderNames:
        getLogger().debug("User %s moved out of mandated trader list." % user.Name())
        tracker.RemoveUser(user)

    elif user.Name() in mandatedTraderNames:
        oldGroup = tracker.GetUserGroup(user)
        newGroup = user.UserGroup().Name()
        mailTo = GetAfricaSupervisorGroupEmails()

        if user.Name() in storedUsers:
            # User exists in stored list
            if user.UserGroup().Name() != tracker.GetUserGroup(user):
                getLogger().debug("User moved user groups. %s --> %s" % (oldGroup, newGroup))
                getLogger().info("[EMAIL] Sending e-mail notification to %s" % mailTo)
                SendMailUserGroupChange(user, oldGroup, mailTo, GetMailFromAddress())
            else:
                getLogger().debug("User profile changed, but did not move user groups. (%s)" % user.Name())
        else:
            # User does not exist in current stored list
            getLogger().debug("User %s moved into group (%s)." % (user.Name(), user.UserGroup().Name()))
            getLogger().info("[EMAIL] Sending e-mail notification to %s" % mailTo)
            SendMailUserGroupChange(user, oldGroup, mailTo, GetMailFromAddress())

        # Update user group in DB
        tracker.SetUserGroup(user)
    else:
        getLogger().debug("User not mandated (%s)." % user.Name())


def ProcessAuthorization(businessProcess):
    """
    Process any pending mandate update or creation authorizations.
    :param businessProcess: FBusinessProcess
    """
    getLogger().debug('Business Process Updated')
    state = businessProcess.CurrentStep().State().Name()
    to = businessProcess.Subject()
    
    if to:
        limit = acm.FLimit[to.Name()]  # pylint: disable=no-member
        if limit:
            mandate = Mandate(limit)
            mailFrom = GetMandateSettingsParam(FPARAM_VIOLATION_EMAIL_SENDER)
            mailTo = GetAfricaSupervisorGroupEmails() if GetAfricaSupervisorGroupEmails() else 'none@none.com'

            if state == 'Authorization stage 1':
                getLogger().info('Business Process entered Pending activation approval stage - Sending e-mail')
                SendMandateCreatedMail(mandate, mailTo, mailFrom)


def ProcessTrade(trade):
    """
    Handle new trades picked up by the ATS.
    :param trade: FTrade
    """
    getLogger().debug('New trade picked up. Trade No: %s' % trade.Oid())
    from GenericMandatesRunScriptEOD import ProcessTradeForViolations
    ProcessTradeForViolations(trade)
    getLogger().debug('Trade processed.')
