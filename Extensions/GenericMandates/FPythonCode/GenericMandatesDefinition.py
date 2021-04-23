"""
This file contains the Mandate class with all the methods related to a mandate object.
---------------------------------------------------------------------------------------------------
28-08-2018      Jaysen Naicker          add new method GetAllMandateQFNamesExcept
28-08-2018      Jaysen Naicker          fix limit commit issue in classs Mandate for ApplyTypeToLimit and ApplyEntityToLimit
"""

import json
import acm

from GenericMandatesConstants import MANDATE_TEXT_OBJECT_SUBTYPE, MANDATE_TEXT_OBJECT_TYPE, MANDATE_ALLOWED_TEXT, \
    MANDATE_NOT_ALLOWED_TEXT, MANDATE_NOT_FOUND_TEXT, MANDATE_LIMIT_BLOCKING, MANDATE_LIMIT_NON_BLOCKING, \
    MANDATE_LIMIT_UNKNOWN, MANDATE_QUERY_FOLDER_NAME, M_TYPE_TRADER, M_DESCR_TRADER, \
    M_TYPE_COUNTERPARTY, M_DESCR_COUNTERPARTY, M_TYPE_PORTFOLIO, M_DESCR_PORTFOLIO, M_METHOD_COUNTERPARTY, \
    M_METHOD_PORTFOLIO, M_METHOD_TRADER
from GenericMandatesLogger import getLogger
from GenericMandatesUtils import CreateLimitFromTemplate, GetMandateSettingsParam


# Mandate types
MANDATE_TYPES = [{"name": M_TYPE_TRADER,       "description": M_DESCR_TRADER,          "method": M_METHOD_TRADER},
                 {"name": M_TYPE_COUNTERPARTY, "description": M_DESCR_COUNTERPARTY,    "method": M_METHOD_COUNTERPARTY},
                 {"name": M_TYPE_PORTFOLIO,    "description": M_DESCR_PORTFOLIO,       "method": M_METHOD_PORTFOLIO}]

# Don't edit below this line
OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}
MANDATE_BLOCK_TYPES = {"Non - Blocking": {"threshold": 0, "warning": 1}, "Blocking": {"threshold": 1, "warning": 1}}

MANDATE_STATUS_INACTIVE = "inactive"
MANDATE_STATUS_ACTIVE = "active"


class Mandate(object):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    # Amount of attributes and public methods in this class is reasonable
    """
    Mandate definition class.
    """
    def __init__(self, limit):
        """
        :param limit: FLimit
        :return: Mandate
        """

        if limit:
            self._limitOid = limit.Oid()

            # Mandate definition
            self._mandateType = None
            self._mandatedEntity = None
            self._linkedQueryFolders = []  # Array of query folder IDs
            self._name = ""
            self._blocking = False
            self._authRequired = True
            self._description = ""

            # Proposed definition
            self._proposedActive = False
            self._proposedType = None
            self._proposedMandatedEntity = None
            self._proposedEntityType = None
            self._proposedLinkedQueryFolders = []
            self._proposedName = ""
            self._proposedBlocking = False
            self._proposedDescription = ""

            self._result = '...init...'
            self._behaviour = {}
            self._simulatedCheckValue = 0
            self._status = MANDATE_STATUS_INACTIVE
            self._protectionLevel = int(GetMandateSettingsParam("TextObjectProtectionLevel"))

            # Mandate Time Stamps
            self._timeCreate = ""
            self._userCreate = ""
            self._timeAmend = ""
            self._userAmend = ""
            self._timeAuthorize = ""
            self._userAuthorize = ""
            self._timeExpire = ""

            # Traders who accepted Mandates
            self._acceptedTraders = []

            # Load mandate from DB
            self.__LoadMandateFromDB()

            # Load Limit from DB
            self._limit = acm.FLimit[self._limitOid]  # pylint: disable=no-member
        else:
            getLogger().error('Invalid limit passed to mandate.')
            raise ValueError("Invalid limit object passed to mandate.")

    def SetProposed(self, active, entityType, entity, folders, name, blocking, description):
        self._proposedActive = active
        self._proposedType = str(entityType)
        self._proposedMandatedEntity = str(entity)
        self._proposedLinkedQueryFolders = str(folders)
        self._proposedName = str(name)
        self._proposedBlocking = str(blocking)
        self._proposedDescription = str(description)

    def SetProposedActive(self, active):
        self._proposedActive = active

    def SetProposedType(self, proposedType):
        self._proposedType = proposedType

    def SetProposedEntity(self, entity):
        self._proposedMandatedEntity = entity

    def SetProposedQueryFolders(self, folders):
        self._proposedLinkedQueryFolders = folders

    def SetProposedName(self, proposedName):
        self._proposedName = proposedName

    def SetProposedBlocking(self, blocking):
        self._proposedBlocking = blocking

    def SetProposedDescription(self, description):
        self._proposedDescription = description

    def ApplyAmendments(self):
        # Mandate definition
        self._mandateType = self._proposedType
        self._mandatedEntity = self._proposedMandatedEntity
        self._linkedQueryFolders = self._proposedLinkedQueryFolders
        self._name = self._proposedName
        self._blocking = self._proposedBlocking
        self._description = self._proposedDescription

        self.SetMandateAsActive() if self._proposedActive is True else self.SetMandateAsInactive()

    def ClearAcceptedTraders(self):
        """
        Clear the list of traders that have accepted the mandate.
        """
        if self.Type() == 'Trader Group':
            getLogger().debug('Clearing all accepted traders from Mandate (%s)' % self.Name())
            self._acceptedTraders = []
        else:
            getLogger().warn('Calling ClearAcceptedTraders() method on a mandate that is not a Trader Group mandate.')

    def AddAcceptedTrader(self, user):
        """
        Add a user to the list of traders that have accepted the mandate.
        :param user: FUser
        :return: bool
        """
        # pylint: disable=no-member
        if self.Type() == 'Trader Group':
            if self.IsAcceptedByTrader(acm.User()) is False:
                self._acceptedTraders.append({'name': str(user.Name()),
                                              'date': str(acm.Time.TimeNow()),
                                              'accepted': True})
        else:
            getLogger().warn('Calling AddAcceptedTrader() method on a mandate that is not a Trader Group mandate.')

    def IsAcceptedByTrader(self, user):
        """
        Check if a specific trader has accepted the mandate.
        :param user: FUser
        :return: date
        """
        if self.Type() == 'Trader Group':
            for record in self._acceptedTraders:
                if record['name'] == user.Name():
                    return True
            return False
        else:
            getLogger().warn('Calling IsAcceptedByTrader() method on a mandate that is not a Trader Group mandate.')

    def GetTraderAcceptDate(self, user):
        """
        Check if a specific trader has accepted the mandate.
        :param user: FUser
        :return: date
        """
        if self.IsAcceptedByTrader(user):
            for record in self._acceptedTraders:
                if record['name'] == user.Name():
                    date = str(record['date'])
                    date = date[:-4]
                    return date

    def RemoveAcceptedTrader(self, user):
        updatedTraders = []
        for trader in self._acceptedTraders:
            if trader['name'] != user.Name():
                updatedTraders.append(trader)
        self._acceptedTraders = updatedTraders

    def __LoadFromJson(self, jsonText):
        try:
            # print jsonText
            self.__dict__ = json.loads(jsonText)
        except TypeError:
            getLogger().error("[ERROR] Converting JSON string to Python dictionary. Detail: %s" % TypeError.message)

    def __LoadMandateFromDB(self):
        textObject = GetTextObject(self._limitOid, subType=MANDATE_TEXT_OBJECT_SUBTYPE)
        if textObject:
            self.__LoadFromJson(textObject.Text())

    def LimitOid(self):
        return self._limitOid

    def Type(self):
        return str(self._mandateType)
        
    def SetType(self, mandateType):
        self._mandateType = mandateType

    def ApplyTypeToLimit(self):
        if self._mandateType in ['Portfolio', 'Counterparty', 'Trader Group']:
            '''
            clone = self._limit.Clone()
            limitSpecName = "Mandate - %s" % self._mandateType
            spec = acm.FLimitSpecification[str(limitSpecName)]  # pylint: disable=no-member

            if spec:
                clone.LimitSpecification(spec)
            else:
                getLogger().error('[ERROR] Could not find Limit Specification (%s)' % limitSpecName)
            self._limit.Apply(clone)
            self._limit.Commit()
            '''
            
            # Fix FIS code to commit limit change
            lim = self._limit
            limitSpecName = "Mandate - %s" % self._mandateType
            spec = acm.FLimitSpecification[str(limitSpecName)]  # pylint: disable=no-member

            if spec:
                lim.LimitSpecification(spec)
            else:
                getLogger().error('[ERROR] Could not find Limit Specification (%s)' % limitSpecName)
            lim.Commit()
        else:
            raise ValueError("Invalid mandate type passed: %s" % self._mandateType)

    def SetEntity(self, entity):
        self._mandatedEntity = entity

    def ApplyEntityToLimit(self):
        try:
            '''
            clone = self._limit.Clone()
            if len(self.Name()) > 1 and self._limit.Name() != self.Name():
                clone.Name(self._name)
            clone.LimitTarget().TemplatePath(self._mandatedEntity)
            clone.LimitTarget().Commit()
            self._limit.Apply(clone)
            self._limit.Commit()
            '''
            
            # Fix FIS code to commit limit change
            lim = self._limit
            if len(self.Name()) > 1 and lim.Name() != self.Name():
                lim.Name(self.Name())
            lim.LimitTarget().TemplatePath(str(self._proposedMandatedEntity))
            lim.Commit()
        except Exception as e:
            getLogger().error('-'*60)
            import sys
            import traceback
            getLogger().error('%s' % e)
            traceback.print_exc(file=sys.stdout)
            getLogger().error('-'*60)

    def Entity(self):
        return str(self._mandatedEntity)

    def Status(self):
        return str(self._status)

    def SetMandateAsActive(self):
        self._status = MANDATE_STATUS_ACTIVE

    def ApplyActiveToLimit(self):
        if self._limit.IsInfant() is True:
            self._limit.Commit()

        clone = self._limit.Clone()
        bpParameters = acm.FDictionary()  # pylint: disable=no-member
        bpParameters.AtPut('Action', 'Toggled mandate activation.')

        if self._limit.BusinessProcess().CanHandleEvent('Activate'):
            self._limit.BusinessProcess().HandleEvent('Activate', bpParameters)
        elif self._limit.BusinessProcess().CanHandleEvent('Monitor Limit'):
            self._limit.BusinessProcess().HandleEvent('Monitor Limit', bpParameters)

        getLogger().debug('Activating limit (Oid: %s)' % self._limitOid)
        self._limit.BusinessProcess().Commit()
        self._limit.Apply(clone)
        self._limit.Commit()

    def SetMandateAsInactive(self):
        getLogger().debug('Deactivate mandate (Oid: %s)' % self._limitOid)
        self._status = MANDATE_STATUS_INACTIVE

    def ApplyInactiveToLimit(self):
        validEvents = self._limit.BusinessProcess().CurrentStep().ValidEvents()
        if 'Deactivate' in '%s' % validEvents:
            self._limit.BusinessProcess().HandleEvent('Deactivate')
            self._limit.BusinessProcess().Commit()
        else:
            getLogger().error('[ERROR] Could not deactivate limit (Oid: %s)' % self._limit.Oid())

    def QueryFolders(self):
        return self._linkedQueryFolders

    def QueryFoldersObj(self):
        queries = []
        for qfId in self._linkedQueryFolders:
            query = acm.FStoredASQLQuery[qfId]  # pylint: disable=no-member
            if query:
                queries.append(query)
        return queries

    def SimulatedCheckValue(self, checkValue):
        self._simulatedCheckValue = checkValue

    def GetSimulatedCheckValue(self):
        return self._simulatedCheckValue

    def ExportToJson(self):
        try:
            return json.dumps(self.__dict__, default=lambda x: None)
        except TypeError:
            getLogger().error("[ERROR] Could not export data to JSON format. Detail: %s" % TypeError.message)

    def LinkQueryFolder(self, queryFolder):
        """
        Add the Oid of a query folder to the mandate.
        :param queryFolder: FASQLQuery
        """
        if not self._linkedQueryFolders:
            self._linkedQueryFolders = []
        if queryFolder.Oid() not in self._linkedQueryFolders:
            self._linkedQueryFolders.append(queryFolder.Oid())

    def UnlinkQueryFolder(self, queryFolder):
        """
        Remove the Oid of a query folder from the mandate.
        :param queryFolder: FASQLQuery
        """
        if queryFolder.Oid() in self._linkedQueryFolders:
            self._linkedQueryFolders.remove(queryFolder.Oid())

    def Commit(self):
        getLogger().debug('Committing Mandate to DB')
        # self._limit.Commit()
        SaveTextObject(self.ExportToJson(), self._limitOid, self._protectionLevel)

    def Delete(self):
        DeleteTextObject(self._limitOid)

    def IsTradeValid(self, trade):
        """
        Check is the trade is valid.
        :param trade: FTrade
        :return: bool
        """
        if len(self._linkedQueryFolders) == 0:
            return False
        for queryFolderOid in self._linkedQueryFolders:
            queryFolder = acm.FStoredASQLQuery[queryFolderOid]  # pylint: disable=no-member
            if queryFolder:
                if not queryFolder.Query().IsSatisfiedBy(trade):
                    return False
            else:
                getLogger().error('[ERROR] Query folder does not exist anymore (%s).' % queryFolderOid)
        return True

    def IsTradeValidGetString(self, trade):
        if len(self._linkedQueryFolders) > 0:
            valid = self.IsTradeValid(trade)
            if valid is True:
                return MANDATE_ALLOWED_TEXT
            else:
                return MANDATE_NOT_ALLOWED_TEXT
        else:
            return MANDATE_NOT_FOUND_TEXT

    def IsBlocking(self):
        return self._blocking

    def SetBlocking(self, enable):
        self._blocking = enable

    def ApplyBlockingToLimit(self):
        # Update threshold & warning value
        if self._blocking is True:
            threshold = MANDATE_BLOCK_TYPES["Blocking"]["threshold"]
            warning = MANDATE_BLOCK_TYPES["Blocking"]["warning"]
        else:
            threshold = MANDATE_BLOCK_TYPES["Non - Blocking"]["threshold"]
            warning = MANDATE_BLOCK_TYPES["Non - Blocking"]["warning"]

        # Update Limit in DB
        clone = self._limit.Clone()
        clone.Threshold(threshold)
        clone.WarningValue(warning)
        self._limit.Apply(clone)
        self._limit.Commit()

    def __BuildNodeArray(self, asqlNodes, returnNodes):
        if type(asqlNodes) is type(acm.FArray()):  # pylint: disable=no-member
            # FArray of asqlNodes
            for asqlNode in asqlNodes:
                self.__BuildNodeArray(asqlNode, returnNodes)
        elif 'AsqlNodes' in dir(asqlNodes):
            # Operation Nodes
            for n in asqlNodes.AsqlNodes():
                self.__BuildNodeArray(n, returnNodes)
        else:
            # Attribute Nodes
            attribute = asqlNodes.AsqlAttribute().AttributeString()
            comparator = ATTR_NODE[asqlNodes.AsqlOperator()]
            if asqlNodes.AsqlValue():
                value = asqlNodes.AsqlValue()
            else:
                value = '-'
            returnNodes.append([['Mandate Component', ], ['%s' % attribute, ], ['%s' % comparator, ], ['%s' % value, ]])

    def __GetNodesFromQuery(self, queryFolder):
        returnNodes = []
        for qn in queryFolder.Query().AsqlNodes():
            nodes = qn.AsqlNodes()
            self.__BuildNodeArray(nodes, returnNodes)
        return returnNodes

    def GetNodes(self):
        nodes = []
        for qfName in self._linkedQueryFolders:
            qf = acm.FStoredASQLQuery[qfName]  # pylint: disable=no-member
            for node in self.__GetNodesFromQuery(qf):
                nodes.append(node)
        return nodes

    def GetBehaviour(self):
        """
        Get the behaviour of the mandate.
        :return: tuple
        """
        failType = self.GetFailType()
        allowed = self._simulatedCheckValue

        behaviour = (1, MANDATE_LIMIT_UNKNOWN)
        if allowed == 'Not Allowed':
            if failType == MANDATE_LIMIT_NON_BLOCKING:
                behaviour = (2, 'Please enter comment, this Mandate allows an override')
            if failType == MANDATE_LIMIT_BLOCKING:
                behaviour = (3, 'Comment not allowed, this Mandate blocks')
        elif allowed == 'Allowed':
            behaviour = (4, 'No comment required, this Mandate passed')
        return behaviour

    def GetFailType(self):
        """
        This checks if a limit is a blocking limit (the trade should not be saved) or a non-blocking limit (the trade
        should be saved with a violation comment).
        :return: string
        """
        warning = self._limit.WarningValue()
        threshold = self._limit.Threshold()

        # Verify that the limit is valid for mandates
        if self._limit.ComparisonOperator() != 'Less':
            msg = "[Warning] The limit comparison operator should be 'Less Than'. Limit Oid: %s" % self._limit.Oid()
            getLogger().warn(msg)
        elif self._limit.PercentageWarning() is True:
            getLogger().warn("[Warning] The limit warning should be absolute. Limit Oid: %s" % self._limit.Oid())
        elif warning not in [0, 1]:
            getLogger().warn("[Warning] The limit warning value should be 0 or 1. Limit Oid: %s" % self._limit.Oid())
        elif threshold not in [0, 1]:
            getLogger().warn("[Warning] The limit threshold value should be 0 or 1. Limit Oid: %s" % self._limit.Oid())

        # Do checks
        if threshold == 1:
            return MANDATE_LIMIT_BLOCKING
        elif threshold == 0:
            return MANDATE_LIMIT_NON_BLOCKING
        return MANDATE_LIMIT_UNKNOWN

    def UnlinkQueryFolders(self):
        self._linkedQueryFolders = []

    def SetCreateTime(self, time):
        self._timeCreate = time

    def GetCreateTime(self):
        return str(self._timeCreate[:19]) if self._timeCreate else ""

    def SetCreateUser(self, name):
        self._userCreate = name

    def GetCreateUser(self):
        return str(self._userCreate) if self._userCreate else ""

    def SetAmendTime(self, time):
        self._timeAmend = time

    def GetAmendTime(self):
        return str(self._timeAmend[:19]) if self._timeAmend else ""

    def SetAmendUser(self, name):
        self._userAmend = name

    def GetAmendUser(self):
        return str(self._userAmend) if self._userAmend else ""

    def SetAuthTime(self, time):
        self. SetExpireTime(acm.Time.DateAddDelta(time, 0, 12, 0))  # pylint: disable=no-member
        self._timeAuthorize = time

    def GetAuthTime(self):
        return str(self._timeAuthorize[:19]) if self._timeAuthorize else ""

    def SetAuthUser(self, name):
        self._userAuthorize = name

    def GetAuthUser(self):
        return str(self._userAuthorize) if self._userAuthorize else ""

    def SetExpireTime(self, time):
        self._timeExpire = time

    def GetExpireTime(self):
        return str(self._timeExpire[:19]) if self._timeExpire else ""

    def SetDescription(self, description):
        self._description = description

    def GetDescription(self):
        return str(self._description) if self._description else str(self._description)

    def SetOwnerAndProtectionOnQueryFoldersAndLimit(self, owner, protection):
        folders = self.QueryFoldersObj()
        limit = acm.FLimit[self._limitOid]  # pylint: disable=no-member

        # Update the ownership and permission on the limit
        if limit:
            limit.Owner(owner)
            limit.Protection(protection)
            limit.Commit()
        
        # Update the ownership and permission on the folders
        for folder in folders:
            if folder.Owner().Name() != owner.Name():
                folder.Owner(owner)
                folder.Protection(protection)
                folder.Commit()

    def Name(self):
        if "_name" in dir(self):
            return str(self._name)

    def SetName(self, inputName):
        self._name = '%s' % inputName

    def ApplyNameToLimit(self):
        if self._limit.Name() != self.Name():
            # Update limit in DB
            clone = self._limit.Clone()
            clone.Name('%s' % self.Name())

            self._limit.Apply(clone)
            self._limit.Clone()

    def GetProductSupervisor(self):
        users = []

        traderGroup = self.Entity()
        productSupervisorProfile = 'PS_%s' % traderGroup[:16]
        profile = acm.FUserProfile[productSupervisorProfile]  # pylint: disable=no-member
        if profile:
            links = profile.Links()
            for link in links:
                user = link.User()
                userName = "%s (%s)" % (user.Name(), user.FullName()) if user.FullName() != "" else "%s" % user.Name()
                users.append(userName)
        return users

    def GetProductSupervisorUsers(self):
        users = []

        traderGroup = self.Entity()
        productSupervisorProfile = 'PS_%s' % traderGroup[:16]
        profile = acm.FUserProfile[productSupervisorProfile]
        if profile:
            links = profile.Links()
            for link in links:
                users.append(link.User())
        return users
        
    def GetMandatedUsers(self):
        """
        Return a list of users that are mandated by this mandate.
        """
        traderGroupName = self.Entity()
        traderGroup = acm.FUserGroup[traderGroupName]  # pylint: disable=no-member
        if traderGroup:
            return traderGroup.Users()
        else:
            return []

    def ApplyMandateToLimit(self):
        self.ApplyActiveToLimit() if self._status == MANDATE_STATUS_ACTIVE else self.ApplyInactiveToLimit()
        self.ApplyBlockingToLimit()
        self.ApplyEntityToLimit()
        self.ApplyNameToLimit()
        self.ApplyTypeToLimit()



"""
Functions required to manipulate the TextObject data in the database.
"""


def GetTextObject(name, textObjectType=MANDATE_TEXT_OBJECT_TYPE, subType=""):
    """
    Return a TextObject from the database.
    :param name: string
    :param textObjectType: string
    :param subType: string
    :return:
    """
    # pylint: disable=no-member
    getLogger().debug('Retrieve Text Object from DB')
    to = acm.FCustomTextObject.Select01('subType="%s" name="%s"' % ("Mandates", name), None)
    if to:
        return to
    else:
        getLogger().debug('Could not find Text Object. Name: %s, SubType: %s' % (name, textObjectType))


def SaveTextObject(jsonText, limitOid, protectionLevel):
    """
    Store a new TextObject in the database. The text object will contain the json string passed to it in the data field.
    :param jsonText: string
    :param limitOid: string
    :param protectionLevel:
    """
    # Check if Mandate has already been stored in the DB
    textObject = GetTextObject(limitOid, MANDATE_TEXT_OBJECT_TYPE, MANDATE_TEXT_OBJECT_SUBTYPE)
    if textObject:
        getLogger().debug("Mandate exists - Updating")
        textObjectClone = textObject.Clone()
        textObjectClone.Text(jsonText)
        textObject.Apply(textObjectClone)
        textObject.Commit()
    else:
        getLogger().debug("Mandate does not exist - Creating")

        newTextObject = acm.FCustomTextObject()  # pylint: disable=no-member
        newTextObject.Name("%s" % limitOid)
        newTextObject.Text(jsonText)
        newTextObject.SubType(MANDATE_TEXT_OBJECT_SUBTYPE)
        newTextObject.Protection(protectionLevel)
        newTextObject.Commit()


def DeleteTextObject(name, type=MANDATE_TEXT_OBJECT_TYPE):
    """
    Delete a specific TextObject from the DB.
    :param name: string
    :param objectType: string
    :return:
    """
    textObject = GetTextObject(name, objectType, "")
    if textObject:
        try:
            textObject.Delete()
        except Exception as e:
            getLogger().error("ERROR. Unable to delete text object.")
            getLogger().error("Detail: %s" % e)


def GetAllMandateLimitOids():
    """
    Retrieve all the mandate names stored in the TextObject table.
    :return: array
    """
    selection = acm.FCustomTextObject.Select('subType="%s"' % MANDATE_TEXT_OBJECT_SUBTYPE)  # pylint: disable=no-member

    result = []
    for to in selection:
        limitId = to.Name()
        result.append(limitId)
    return result


"""
Functions required to create a Mandate and a Limit for a specific mandate type and target.
"""


def CreateMandateAndLimit(mandateName, mandateType, mandateTarget, queryFolders, blocking):
    """
    Create a mandate and a limit for a specific mandate type and target. The function will return the Oid of the limit
    which is also the name of text object containing the mandate data in the text object table.
    :param mandateName: string
    :param mandateType: string
    :param mandateTarget: string
    :param queryFolders: list
    :param blocking: bool
    :return: string
    """
    # pylint: disable=no-member
    # Step 1 - Create Limit on trader group
    if not acm.FLimit[mandateName]:
        getLogger().debug("Create new limit")
        if blocking is True:
            threshold = MANDATE_BLOCK_TYPES["Blocking"]["threshold"]
            warning = MANDATE_BLOCK_TYPES["Blocking"]["warning"]
        else:
            threshold = MANDATE_BLOCK_TYPES["Non - Blocking"]["threshold"]
            warning = MANDATE_BLOCK_TYPES["Non - Blocking"]["warning"]

        templatePath = [mandateTarget, ]
        templateName = "LimitTemplate/%s" % mandateType
        limitProtectionLevel = int(GetMandateSettingsParam("LimitProtectionLevel"))
        
        limitOwnerName = GetMandateSettingsParam("LimitOwnerName")
        limitOwner = acm.FUser[limitOwnerName]
        
        CreateLimitFromTemplate(templateName, MANDATE_QUERY_FOLDER_NAME, templatePath, mandateName, threshold, warning,
                                limitProtectionLevel, limitOwner)
    else:
        if acm.FLimit[mandateName]:
            getLogger().error("[ERROR] Limit with the name (%s) already exists." % mandateName)
        else:
            getLogger().error("[ERROR] Query folder with the name (%s) does not exist." % mandateName)

    # Step 3 - Create mandate text object
    mandate = Mandate(acm.FLimit[mandateName])
    for queryFolder in queryFolders:
        mandate.LinkQueryFolder(queryFolder)
    mandate.SetCreateTime(acm.Time.TimeNow())
    mandate.SetCreateUser("%s" % acm.User().Name())
    mandate.Commit()
    return mandateName


def GetMandateTypes():
    types = []
    for mandateType in MANDATE_TYPES:
        types.append(mandateType["name"])
    return types


def GetAllMandateQFNames():
    """
    Retrieve all the Query Folders used in Mandate definitions.
    :return: list
    """
    limitOids = GetAllMandateLimitOids()
    allFolderNames = []
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]  # pylint: disable=no-member
        if limit:
            mandate = Mandate(limit)
            folders = mandate.QueryFoldersObj()
            names = [folder.Name() for folder in folders]
            allFolderNames += names
    return allFolderNames

def GetAllMandateQFNamesExcept(mandateName):
    """
    Retrieve all the Query Folders used in Mandate definitions except for the mandate name sent to the funtion.
    :return: list
    """
    limitOids = GetAllMandateLimitOids()
    allFolderNames = []
    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]  # pylint: disable=no-member
        if limit:
            mandate = Mandate(limit)
            if mandate.Name() != mandateName:
                folders = mandate.QueryFoldersObj()
                names = [folder.Name() for folder in folders]
                allFolderNames += names
    return allFolderNames
