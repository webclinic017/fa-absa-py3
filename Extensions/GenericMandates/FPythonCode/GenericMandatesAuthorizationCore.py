"""
    Provides the core functionality and helpers for the authorization feature
"""
import acm

from GenericMandatesAuthorizationStateChart import StateChartAuthorizationProcess
from GenericMandatesDefinition import Mandate
from GenericMandatesLogger import getLogger


# Constants
EXTENSION_CONTEXT_NAME = "Standard"
AUTHORIZATION_STAGE_STATE_NAME_PREFIX = "Authorization stage "
STATE_ERROR = "Error"

# Event parameters constants
EVENT_PARAMETER_AUTHORIZER_GROUP_NAME = "Authorizer Group"
EVENT_PARAMETER_AUTHORIZER_USER_NAME = "Authorizer User"
EVENT_PARAMETER_REJECTION_REASON = "Rejection reason"
EVENT_PARAMETER_REJECTION_USER = "Rejected by"

EVENT_PARAMETER_NEW_MANDATE_TARGET = "Mandate target"
EVENT_PARAMETER_NEW_MANDATE_TYPE = "Mandate type"
EVENT_PARAMETER_NEW_MANDATE_QUERY_FOLDERS = "Mandate query folders"
EVENT_PARAMETER_NEW_MANDATE_BLOCKING = "Mandate blocking type"
EVENT_PARAMETER_NEW_MANDATE_STATUS = "Mandate Active"
EVENT_PARAMETER_NEW_MANDATE_REASON = "Mandate Change Reason"

# FParameters constants
FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_GLOBAL = "AuthorizerGroupNameMapGlobal"

# FPARAMETER_MANDATE_AUTHORIZATION_PARAMETERS = "MandateAuthorizationParameters"
FPARAMETER_MANDATE_AUTHORIZATION_PARAMETERS = "GenericMandatesSettings"
FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_STAGE = "AuthorizerGroupNameMapStage"

FPARAMETER_KEY_MODE = "AuthorizationMode"

# Authorization mode constants
AUTHORIZATION_MODE_LOCAL = "sequential"
AUTHORIZATION_MODE_GLOBAL = "nonsequential"


# User resolver functions - Follows the signature (FUser, String) -> Boolean
def isUserPartOfUserProfile(user, userProfileName):
    """
    Checks if a specified user has a user profile that matches the specified user profile name
    :param user: the user to check
    :param userProfileName: the name of the user profile to check against
    :return: True if the user is associated with the user profile else false
    """
    userProfileLinks = acm.FUserProfileLink.Select("user=%s" % user.Oid())  # pylint: disable=no-member

    for userProfileLink in userProfileLinks:
        getLogger().debug('-> %s, %s == %s' %(userProfileLink.UserProfile().Name(), userProfileName, userProfileLink.UserProfile().Name() == userProfileName))
        if userProfileLink.UserProfile().Name() == userProfileName:
            return True
    
    return False


def isUserPartOfUserGroup(user, userGroupName):
    """
    Checks if a specified user is in the user group that matches the specified user group name
    :param user: the user to check
    :param userGroupName: the name of the user group to check against
    :return: True if the user is associated with the user group else false
    """
    return user.UserGroup().Name() == userGroupName


def isUserUser(user, userName):
    """
    Checks if a specified user has the specified user name
    :param user: the user to check
    :param userName: the name of the user user to check against
    :return: True if the user is the specified user else false
    """
    return user.Name() == userName


# Core helper functions
def loadMandateCustomTextObject(limitOid):
    """
    Get the mandate as an ACM text object 
    :param limitOid: Int
    :return: FCustomTextObject
    """
    # pylint: disable=no-member
    getLogger().debug('Load text object from DB (%s)' % limitOid)
    return acm.FCustomTextObject.Select01("name=\"%s\"" % limitOid, "Could not load mandate")


def findFParameters(contextName, name):
    """
    Gets the FExtension object for the specified FParameters in the specified context
    :param contextName: string. the context in which to look for the FParameters
    :param name: string. the name of the FParameters Extension
    :return: FDictionary containing the FParameter's keys and there values if found. Else None
    """
    # pylint: disable=no-member
    extension = acm.FExtensionContext[contextName].GetExtension("FParameters", "FObject", name)
    return extension.Value() if extension else None


def extractParametersDictionaryFromFParameters(contextName, fparameterName):
    """
    Get a FParameters as a dictionary
    :param contextName: string
    :param fparameterName: string
    :return: dictionary containing the FParameter's keys and there values if found. Else None
    """
    fparameters = findFParameters(contextName, fparameterName)
    if fparameters:
        parametersDictionary = {}
        for parameterName in fparameters.Keys():
            parametersDictionary[parameterName.Text()] = fparameters[parameterName].Text()

        return parametersDictionary

    return None


def getNumberOfAuthorizationStages():
    """
    Get the number of authorization stages that the GenericMandatesAuthorization state chart has
    :return: int. the number of authorization stages in the state chart
    """
    # pylint: disable=no-member
    stateNames = acm.FStateChart[StateChartAuthorizationProcess.NAME].StatesByName().Keys()
    return len(filter(lambda x: x.startswith(AUTHORIZATION_STAGE_STATE_NAME_PREFIX), stateNames))


def isStateNameThatOfAuthorisationStage(stateName):
    """
    Checks if the state name is that of a Authorization stage
    :param stateName: the name of the state to check
    :return: boolean
    """
    return stateName.startswith(AUTHORIZATION_STAGE_STATE_NAME_PREFIX)


def extractAuthorisationStageNumber(stateName):
    """
    Extract the number of the authorization stage state's name
    :param stateName: The name of the authorization stage's name
    :return: int else None
    """
    if isStateNameThatOfAuthorisationStage(stateName):
        return int(stateName[len(AUTHORIZATION_STAGE_STATE_NAME_PREFIX):])

    return None


def getCurrentStateName(businessProcess):
    """
    Get the name of the current state that the business process is in
    :param businessProcess: the business process object to interrogate
    :return: the name
    """
    return businessProcess.CurrentStep().State().Name()


def getStartEventIndexForCurrentAuthorizationFlow(businessProcess):
    """
    Get the step index of the event that triggered the current authorization flow. Used for determining if the flow is
    for mandate creation or update
    :param businessProcess: FBusinessProcess
    :return: int if start event was found else None
    """
    steps = list(businessProcess.Steps().SortByProperty('Oid', False))
    stepCount = len(steps)
    eventUpdate = StateChartAuthorizationProcess.EVENT_SUBMIT_UPDATE
    eventCreate = StateChartAuthorizationProcess.EVENT_CREATE

    for i in range(stepCount):
        step = steps[i]
        if step.EventName() in [eventUpdate, eventCreate]:
            return step.Oid()
    return None


def isUpdateAuthorization(businessProcess):
    """
    Checks if the current authorization flow is for a mandate update
    :param businessProcess: FBusinessProcess
    :return: Boolean
    """
    getLogger().debug("isUpdateAuthorization() executing")
    startEventIndex = getStartEventIndexForCurrentAuthorizationFlow(businessProcess)
    getLogger().debug("Start event index: %s" % startEventIndex)

    if startEventIndex:
        previousStep = acm.FBusinessProcessStep[startEventIndex]
        return previousStep.State().Name() == StateChartAuthorizationProcess.STATE_PENDING_UPDATE_APPROVAL
    else:
        return False


def isAuthorizationRejected(businessProcess):
    """
    Checks if the current authorization flow is for a mandate is in rejected state
    :param businessProcess: FBusinessProcess
    :return: Boolean
    """
    return getCurrentStateName(businessProcess) == StateChartAuthorizationProcess.STATE_REJECTED


def isAuthorizationAuthorized(businessProcess):
    """
    Checks if the current authorization flow is for a mandate is in rejected state
    :param businessProcess: FBusinessProcess
    :return: Boolean
    """
    return getCurrentStateName(businessProcess) in [StateChartAuthorizationProcess.STATE_AUTHORIZED,
                                                    StateChartAuthorizationProcess.STATE_APPLY]


def isAuthorizationError(businessProcess):
    """
    Checks if the current authorization flow is for a mandate is in error state
    :param businessProcess: FBusinessProcess
    :return: Boolean
    """
    return getCurrentStateName(businessProcess) == StateChartAuthorizationProcess.STATE_ERROR


def CreateTempName(qf):
    """
    Create temporary query folder name.
    :param qf: FStoredASQLQuery
    :return: string
    """
    qfName = qf.Name()
    if 'Mandate/' in qfName:
        return 'Mandate/TEMP/%s' % qfName[8:]
    else:
        return 'Mandate/TEMP/%s' % qfName


def CopyQueryFolder(qf):
    """
    Create a copy of the query folder. If a query folder with the target name already exists, it will be deleted.
    :param qf: FStoredASQLQuery
    :return: FStoredASQLQuery
    """
    # Check if temp Query Folder already exists
    exists = acm.FStoredASQLQuery.Select('name="%s"' % CreateTempName(qf))  # pylint: disable=no-member
    if exists:
        for queryFolder in exists:
            queryFolder.Delete()

    qfCopy = qf.Clone()
    qfCopy.Name(CreateTempName(qf))
    qfCopy.Commit()
    return qfCopy


def setMandatePropertiesInEventParameters(eventParameters, mandateTarget, mandateType, queryFolders, blocking, active,
                                          reason):
    """
    Set the properties for a mandate in the specified Business process's Event's parameters dictionary
    :param eventParameters: FDictionary
    :param mandateTarget: String
    :param mandateType: String
    :param queryFolders: list
    :param blocking: boolean
    :param active:
    :param reason:
    :return:
    """
    getLogger().debug("setMandatePropertiesInEventParameters()")
    getLogger().debug('Target: %s, Type: %s, QF: %s, Blocking: %s' % (mandateTarget, mandateType, len(queryFolders),
                                                                      blocking))

    # Create temporary copies of query folders
    # tempQueryFolders = [CopyQueryFolder(queryFolder) for queryFolder in queryFolders]
    tempQueryFolders = queryFolders

    # Converting array of FStoredASQLQuery to string
    queriesStr = ""
    for qf in tempQueryFolders:
        queriesStr += qf.Name() + ", "
    queriesStr = queriesStr[:-2]

    # Store string values in FBusinessProcessStep parameters
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_TARGET, mandateTarget)
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_TYPE, mandateType)
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_QUERY_FOLDERS, queriesStr)
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_BLOCKING, blocking)
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_STATUS, active)
    eventParameters.AtPut(EVENT_PARAMETER_NEW_MANDATE_REASON, reason)


def GetAuthGroup():
    """
    Get the authorization group that the logged in user belongs to
    :return: str
    """
    from GenericMandatesAuthorizationLocal import localFindAuthorizationStagesAuthorizerGroupMaps
    from GenericMandatesAuthorizationGlobal import IsUserAuthorized

    authMap = localFindAuthorizationStagesAuthorizerGroupMaps('Standard')
    stages = authMap.keys()
    for stage in stages:
        if IsUserAuthorized(authMap[stage]) is True:
            # pylint: disable=no-member
            getLogger().debug('User %s belongs to authorizer group %s' % (acm.User().Name(), stage))
            return stage
    return None


def getMandatePropertiesFromEventParameters(eventParameters):
    """
    Get the properties of a mandate from a Business process's Event's parameters dictionary
    :param eventParameters: FDictionary
    :return: String, String, List, Boolean. Mandate target, Mandate type, Query folders, Blocking
    """
    getLogger().debug("getMandatePropertiesFromEventParameters() executing")
    queryFoldersObj = []
    
    mandateTarget = eventParameters[EVENT_PARAMETER_NEW_MANDATE_TARGET]
    mandateType = eventParameters[EVENT_PARAMETER_NEW_MANDATE_TYPE]
    queryFolders = eventParameters[EVENT_PARAMETER_NEW_MANDATE_QUERY_FOLDERS].split(', ')
    blocking = eventParameters[EVENT_PARAMETER_NEW_MANDATE_BLOCKING]
    active = eventParameters[EVENT_PARAMETER_NEW_MANDATE_STATUS]
    reason = eventParameters[EVENT_PARAMETER_NEW_MANDATE_REASON]

    for qfName in queryFolders:
        selection = acm.FStoredASQLQuery.Select('name="%s"' % qfName)  # pylint: disable=no-member
        query = selection[0]
        if query:
            queryFoldersObj.append(query)
        else:
            getLogger().error('[ERROR] Query folder does not exist (%s)' % qfName)

    return mandateTarget, mandateType, queryFoldersObj, blocking, active, reason


def validateParameterIsSet(eventParameters, parameterName):
    """
    Validates a parameter in a Business process's Event's parameters dictionary
    :param eventParameters: FDictionary
    :param parameterName: String
    :return: True if the dictionary contains the key and it is not an empty string and not None
    """
    return eventParameters.HasKey(parameterName) and eventParameters[parameterName] is not None and \
        eventParameters[parameterName] != ""


def validateThatMandatePropertiesParametersAreSet(eventParameters):
    """
    Validates that a Business process's Event's parameters dictionary had all the valid parameters for a mandate
    :param eventParameters: FDictionary
    :return: True if Mandate target, Mandate type, Query folders, Blocking parameters are all valid
    """

    return validateParameterIsSet(eventParameters, EVENT_PARAMETER_NEW_MANDATE_TARGET) and \
        validateParameterIsSet(eventParameters, EVENT_PARAMETER_NEW_MANDATE_TYPE) and \
        validateParameterIsSet(eventParameters, EVENT_PARAMETER_NEW_MANDATE_QUERY_FOLDERS) and \
        validateParameterIsSet(eventParameters, EVENT_PARAMETER_NEW_MANDATE_BLOCKING)


def getMandateFromMandateTextObject(mandateTextObject):
    """
    Get a mandate object from the mandates text object
    :param mandateTextObject: FPersistentTextObject
    :return: Mandate object
    """
    limit = acm.FLimit[mandateTextObject.Name()]  # pylint: disable=no-member
    return Mandate(limit)


def areNewMandatePropertiesSetForBusinessProcess(businessProcess):
    """
    Check if the update mandate properties are set and valid for the current flow
    :param businessProcess: the authorization business process
    :return: True if the mandate parameters are set and valid
    """
    getLogger().debug("areNewMandatePropertiesSetForBusinessProcess() executing")

    # Get the start index of the current flow
    startEventIndex = getStartEventIndexForCurrentAuthorizationFlow(businessProcess)

    if startEventIndex:
        # Check if the current flow is an update flow
        if isUpdateAuthorization(businessProcess):
            # Get dictionary entry for the triggering event
            entry = businessProcess.Diary().GetEntry(businessProcess, acm.FBusinessProcessStep[startEventIndex])
            # Validate that the event parameters for the triggering event contain the mandate parameters
            return validateThatMandatePropertiesParametersAreSet(entry.Parameters())
    else:
        return False


def getNewMandatePropertiesFromBusinessProcess(businessProcess):
    """
    Get the mandate properties to update the current mandate with for the current flow
    :param businessProcess: the authorization business process
    :return: String, String, List, Boolean. Mandate target, Mandate type, Query folders, Blocking
    """
    getLogger().debug("getNewMandatePropertiesFromBP() executing")

    updateApprovalState = StateChartAuthorizationProcess.STATE_PENDING_UPDATE_APPROVAL
    activateApprovalState = StateChartAuthorizationProcess.STATE_PENDING_ACTIVATION_APPROVAL

    # Get the start index of the current flow
    startEventIndex = getStartEventIndexForCurrentAuthorizationFlow(businessProcess)
    
    if startEventIndex:
        # Check if the current flow is an update or create flow
        update_or_activation_step = acm.FBusinessProcessStep[startEventIndex]

        if update_or_activation_step.StateName() in [updateApprovalState, activateApprovalState]:
            # Get dictionary entry for the triggering event
            entry = update_or_activation_step.DiaryEntry()
            # Validate that the event parameters for the triggering event contain the mandate parameters
            return getMandatePropertiesFromEventParameters(entry.Parameters())
        else:
            return None
