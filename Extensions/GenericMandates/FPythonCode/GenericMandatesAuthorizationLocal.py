"""
    Provides the core functionality and helpers for the authorization feature's local mode
"""
import acm

# Local mode - Set of authorizer groups per authorization stage
from GenericMandatesAuthorizationCore import AUTHORIZATION_STAGE_STATE_NAME_PREFIX, \
    getNumberOfAuthorizationStages, EXTENSION_CONTEXT_NAME, \
    FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_STAGE
from GenericMandatesAuthorizationCore import extractParametersDictionaryFromFParameters, isUserUser, \
    isUserPartOfUserProfile, isUserPartOfUserGroup
from GenericMandatesLogger import getLogger


def localFindAuthorizationStageAuthorizerGroupMap(contextName, stageNumber):
    """
    Get the authorizer group map dictionary for the specified authorization stage
    :param contextName: String
    :param stageNumber: int
    :return: FDictionary
    """
    parameterName = "%s%s" % (FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_STAGE, stageNumber)
    return extractParametersDictionaryFromFParameters(contextName, parameterName)


def localFindAuthorizationStagesAuthorizerGroupMaps(contextName):
    """
    Get a dictionary of all the authorization stage's authorizer group maps
    :param contextName: String
    :return: FDictionary of FDictionary
    """
    numberOfAuthorizationStages = getNumberOfAuthorizationStages()

    authorizationStageAuthorizerGroupMaps = {}
    for i in range(0, numberOfAuthorizationStages):
        stageName = "%s%s" % (AUTHORIZATION_STAGE_STATE_NAME_PREFIX, (i + 1))
        parameterName = "%s%s" % (FPARAMETER_AUTHORIZER_GROUP_NAME_MAP_STAGE, (i + 1))
        paramDict = extractParametersDictionaryFromFParameters(contextName, parameterName)
        authorizationStageAuthorizerGroupMaps[stageName] = paramDict

    return authorizationStageAuthorizerGroupMaps


def localAuthoriseMandateWithCurrentUser(stageNumber):
    """
    Authorize the mandate with the current user. By checking if the current user belongs to an authorization group
    that is associated with current authorization stage
    :param stageNumber: int
    :return: True if the user can authorise else False, the second value is indicates if the has permission to authorize
    """
    authMap = localFindAuthorizationStageAuthorizerGroupMap(EXTENSION_CONTEXT_NAME, stageNumber)
    return IsUserAuthorized(authMap)


def IsUserAuthorized(authMap):
    """
    Check if user is authorized.
    :param authMap: dict
    :return: bool
    """
    user = acm.FACMServer().User()  # pylint: disable=no-member

    for key in list(authMap.keys()):
        if key == 'UserProfiles':
            profiles = authMap[key].split(', ')
            if True in [True for profile in profiles if isUserPartOfUserProfile(user, profile)]:
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
