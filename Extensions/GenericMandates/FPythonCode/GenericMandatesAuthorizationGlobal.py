"""
    MODULE
     Provides the core functionality and helpers for the authorization feature's global mode
    
    AUTHOR
    
    
    DATE CREATED
        
"""
import acm

from GenericMandatesAuthorizationCore import extractParametersDictionaryFromFParameters, \
    FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_GLOBAL, EXTENSION_CONTEXT_NAME, \
    getNumberOfAuthorizationStages, extractAuthorisationStageNumber, \
    EVENT_PARAMETER_AUTHORIZER_GROUP_NAME, getStartEventIndexForCurrentAuthorizationFlow, STATE_ERROR, \
    isUserPartOfUserProfile, isUserPartOfUserGroup, isUserUser
from GenericMandatesAuthorizationStateChart import StateChartAuthorizationProcess
from GenericMandatesAuthorizationLocal import localFindAuthorizationStagesAuthorizerGroupMaps
from GenericMandatesDefinition import Mandate
from GenericMandatesLogger import getLogger


# Enable / Disable Product Supervisor workaround
ENABLE_SUPERVISOR_WORKAROUND = True


def globalCompileAuthorizerGroupNameList(businessProcess):
    """
    Compiles the latest list of authorizer group names of authorizer groups that have approved during the lifetime of
    the current flow in the business process. Note that the entries correspond to each authorization stage in ascending
    sequential order.
    :param businessProcess: The business process to analysis
    :return: The sequential list of authorizer group names that authorized the change.
    """
    maxApproveEvents = getNumberOfAuthorizationStages()
    authorizerGroupNamePerStage = []

    for i in range(0, maxApproveEvents):
        authorizerGroupNamePerStage.append(None)

    # Get current flows starting events index
    startEventIndex = getStartEventIndexForCurrentAuthorizationFlow(businessProcess)

    if not startEventIndex:
        return authorizerGroupNamePerStage

    # Extract steps in last cycle of authorizations. Reverse order the list so that the steps start from first to last
    steps = reversed(list(businessProcess.Steps().SortByProperty('Oid', False))[:startEventIndex])

    for step in steps:
        # Approve events represent addition of 1 approval
        if step.EventName() == StateChartAuthorizationProcess.EVENT_APPROVE:

            stateName = step.State().Name()
            # If the step's resulting state is not an error
            if stateName != STATE_ERROR:
                # If step's resulting state is authorized
                if stateName == StateChartAuthorizationProcess.STATE_AUTHORIZED:
                    stepStageNumber = maxApproveEvents
                else:
                    stepStageNumber = extractAuthorisationStageNumber(stateName) - 1

                # Since the state name is the resulting state the actual stage number is the one before
                authorizerGroupNamePerStage[stepStageNumber - 1] = step.DiaryEntry().Parameters()[EVENT_PARAMETER_AUTHORIZER_GROUP_NAME]

    return authorizerGroupNamePerStage


def IsUserAuthorized(authMap, entity=None):
    user = acm.FACMServer().User()

    for key in authMap.keys():
        if key == 'UserProfiles':
            profiles = authMap[key].split(', ')
            if True in [True for profile in profiles if isUserPartOfUserProfile(user, profile)]:

                if ENABLE_SUPERVISOR_WORKAROUND is True:
                    # ADDITIONAL FUNCTIONALITY for Product Supervisor approvals
                    if entity:
                        """
                        Mandate is of type Trader Group                        
                        Check if trader group exists and PS_<GrpName> profile is linked to user
                        """
                        traderGroup = acm.FUserGroup[entity].Name()
                        productSupervisorProfile = 'PS_%s' % traderGroup[:16]
                        supervisorProfileLinked = isUserPartOfUserProfile(user, productSupervisorProfile)

                        getLogger().debug('Supervisor Profile: %s' % productSupervisorProfile)
                        getLogger().debug('Trader Group: %s' % traderGroup)
                        getLogger().debug('SP Linked: %s' % supervisorProfileLinked)

                        if supervisorProfileLinked is True:
                            return True
                        else:
                            return False
                    else:
                        return True
                    # End of ADDITIONAL FUNCTIONALITY
                else:
                    return True

        elif key == 'UserGroups':
            groups = authMap[key].split(', ')
            if True in [True for group in groups if isUserPartOfUserGroup(user, group)]:
                return True
        elif key == 'Users':
            users = authMap[key].split(', ')
            if True in [True for userName in users if isUserUser(user, userName)]:
                return True
        else:
            getLogger().error('[ERROR] Invalid key used in FParameter. Key: %s' % key)
    return False


def IsUserAllowedToAuthorise(businessProcess):
    """
    Checks if a user is allowed to authorise a Mandate.
    :param businessProcess: FBusinessProcess
    :return: bool
    """
    stages = localFindAuthorizationStagesAuthorizerGroupMaps('Standard')
    authorizedGroups = globalCompileAuthorizerGroupNameList(businessProcess)

    # Get mandate from business process
    limitOid = businessProcess.Subject().Name()
    limit = acm.FLimit[limitOid]
    mandate = Mandate(limit)

    unauthorizedStages = []
    for group in stages:
        # stageName = group.replace('stage', 'Group')

        stageName = group
        if stageName not in authorizedGroups:
            authMap = stages[group]
            if mandate.Type() == "Trader Group":
                if IsUserAuthorized(authMap, mandate.Entity()) is True:
                    return True, [authMap, ]
            else:
                if IsUserAuthorized(authMap) is True:
                    return True, [authMap, ]

            unauthorizedStages.append(authMap)
    return False, unauthorizedStages
