import uuid

import acm
import FLimitUtils
import FLimitTemplate

from GenericMandatesLogger import getLogger
from GenericMandatesConstants import MANDATE_LIMIT_BLOCKING, MANDATE_LIMIT_NON_BLOCKING, MANDATE_LIMIT_UNKNOWN


def SetAddInfoValue(acmObject, addInfoName, value):
    """
    Set additional info field value.
    :param acmObject: FObject
    :param addInfoName: string
    :param value:
    :return: string
    """
    if not acmObject:
        return None

    addInfos = acm.FAdditionalInfo.Select('recaddr = %i' % acmObject.Oid())
    for addInfo in addInfos:
        if addInfo.AddInf().Name() == addInfoName:
            addInfo.FieldValue(value)
            addInfo.Commit()
            return addInfo

    # addInfo not found, so create:
    objAddInfoSpec = acm.FAdditionalInfoSpec[addInfoName]
    if objAddInfoSpec:
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(acmObject.Oid())
        addInfo.AddInf(objAddInfoSpec)
        addInfo.FieldValue(value)
        addInfo.Commit()
        return addInfo


def GetAddInfoValue(acmObject, addInfoName):
    """
    Get additional info field value.
    :param acmObject: FObject
    :param addInfoName: string
    :return: string
    """
    if not acmObject:
        return None

    addInfos = acm.FAdditionalInfo.Select('recaddr = %i' % acmObject.Oid())
    for addInfo in addInfos:
        if addInfo.AddInf().Name() == addInfoName:
            return addInfo.FieldValue()


def GetLimitsOfTypeQuery(limitType):
    folder = acm.FASQLQueryFolder()
    folder.Name('Limits of type "%s"' % limitType)
    query = acm.CreateFASQLQuery('FLimit', 'AND')
    query.AddAttrNode('LimitSpecification.LimitType.Name', 'RE_LIKE_NOCASE', limitType)
    folder.AsqlQuery(query)
    return folder.Query().Select()

    
def GetLimits(trade):
    """
    Return a FArray containing all limits applicable to the trade. The limitSpec parameter uses a LIKE operator not
    equals.
    :param trade: FTrade
    :return: FArray
    """
    allLimits = GetLimitsOfTypeQuery('Mandate')

    # Set all limits in Ready state to Active so that the limit check will pick them up. Currently the
    # acm.Limits.FindByTrade function exclude all limits in "Ready" state.
    limits = []

    applicableLimits = acm.Limits.FindByTrade(trade, allLimits)

    getLogger().debug('Applicable Limits: %s' % applicableLimits)

    # Filter out limits that do not have a target in it's path yet
    applicableLimits = __FilterForLimitTemplates(trade, applicableLimits)

    # Filter out inactive limits
    applicableLimits = __FilterForActiveLimits(applicableLimits)

    return applicableLimits


def __FilterForActiveLimits(limitList):
    """
    Filter out limits that are not in the Inactive state.
    :param limitList: list
    :return: list
    """
    filteredLimits = []
    for limit in limitList:
        if limit.BusinessProcess().CurrentStep().State().Name() != "Inactive":
            filteredLimits.append(limit)
    return filteredLimits


def __FilterForLimitTemplates(trade, limitList):
    """
    This function will filter out limits that does not have the trade counterparty in it's path. This is a workaround
    for a core limits filter functionality issue that will include limits created from a template for paths/positions
    that did not exist on creation.
    :param trade: FTrade
    :param limitList: list
    :return: list
    """
    filteredLimits = []

    for limit in limitList:
        path = limit.LimitTarget().Path().split('/')[1].strip()

        # Counterparty
        if trade.Counterparty():
            if trade.Counterparty().Name() == str(path):
                filteredLimits.append(limit)

        if trade.Instrument().Issuer():
            if trade.Instrument().Issuer().Name() == str(path):
                filteredLimits.append(limit)

        # Trader - User Group
        if trade.Trader():
            if trade.Trader().UserGroup().Name() ==  str(path):
                filteredLimits.append(limit)

        # Portfolio
        if trade.Portfolio():
            if trade.Portfolio():
                if trade.Portfolio().Name() == str(path):
                    filteredLimits.append(limit)

    return filteredLimits
    
    
def GetDefaultLimitsColumns():
    col = ('Limit Specification Name', 'Limit Current State', 'Mandate Fail Type', 'Limit Path', 'Mandate Fail Comment')
    return col


def GetReadOnlyLimitsColumns():
    col = ('Limit Specification Name', 'Limit Current State', 'Mandate Fail Type', 'Limit Path')
    return col


def ToUnicode(stringInput, encoding='latin-1'):
    return str(stringInput, encoding)


def ToString(unicodeInput, encoding='latin-1'):      
    return unicodeInput.encode(encoding)


def GetColor(colorName):
    extension = acm.GetDefaultContext().GetExtension("FColor", acm.FColor, colorName)
    if extension:
        return extension.Value()


def GetFailType(limit):
    """
    This checks if a limit is a blocking limit (the trade should not be saved) or a non-blocking limit (the trade
    should be saved with a violation comment).
    :param limit: FLimit
    :return: string
    """
    warning = limit.WarningValue()
    threshold = limit.Threshold()

    # Verify that the limit is valid for mandates
    if limit.ComparisonOperator() != 'Less':
        getLogger().warn("[Warning] The limit comparison operator should be 'Less Than'. Limit Oid: %s" % limit.Oid())
    elif limit.PercentageWarning() is True:
        getLogger().warn("[Warning] The limit warning should be absolute. Limit Oid: %s" % limit.Oid())
    elif warning not in [0, 1]:
        getLogger().warn("[Warning] The limit warning value should be 0 or 1. Limit Oid: %s" % limit.Oid())
    elif threshold not in [0, 1]:
        getLogger().warn("[Warning] The limit threshold value should be 0 or 1. Limit Oid: %s" % limit.Oid())

    # Do checks
    if threshold == 1:
        return MANDATE_LIMIT_BLOCKING
    elif warning == 1:
        return MANDATE_LIMIT_NON_BLOCKING
    return MANDATE_LIMIT_UNKNOWN


def GetMandateSettingsParam(parameterName):
    """
    Get a specific parameter config value from LimitsExtensionSettings parameterList.
    :param parameterName: string
    :return: string
    """
    paramValue = None
    parameterName = parameterName.strip()
    params = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'GenericMandatesSettings')
    if params:
        paramValue = params.Value()[parameterName]
    return paramValue.Text()


def GetOptionalKey(modified_object):
    # get optional key as unique id for infant trades as link to business process
    tmpOptionalKey = 'ml_%s' % uuid.uuid4()
    tmpOptionalKey = tmpOptionalKey[0:31]
    
    if modified_object.OptionalKey():
        if modified_object.IsInfant():
            if modified_object.OptionalKey()[0:3] == 'ml_':
                tradeOptionalKey = tmpOptionalKey
            else:
                tradeOptionalKey = modified_object.OptionalKey()
        else:
            tradeOptionalKey = modified_object.OptionalKey()
    else:
        tradeOptionalKey = tmpOptionalKey
    return tradeOptionalKey


def formatViolationNotesForTM(notes):
    # Multiline Notes entries appear only as the first line in TM, this just puts them all on 1 line.
    return ''.join([n.replace('\n', ' | ') for n in notes])


def GetLoggedOnUser(trade):
    del trade
    # To get the mandated entity in case of a Trader we do not want to simply use Trade.Trader since
    # this can be manipulated on the trade GUI, simply returning the logged on ACM user, but want to have
    # n custom method we can call from an acm Trade to fit in with the framework.
    return acm.User()


def CreateLimitFromTemplate(templateName, queryFolderName, templatePath, limitName, threshold, warning,
                            protectionLevel, limitOwner):
    """
    Create a Limit from a template. The templates are stored as FParameters.
    :param protectionLevel:
    :param templateName: string
    :param queryFolderName: string
    :param templatePath: string
    :param limitName: string
    :param threshold: float
    :param warning: float
    :param protectionLevel: int
    :param limitOwner: FUser
    :return: bool
    """
    limit = None
    success = False

    # Load a pre-existing template
    template = FLimitTemplate.FLimitTemplate.CreateFromExtension(templateName)
    # Load query folder
    queryFolder = acm.FStoredASQLQuery[queryFolderName]

    if queryFolder:
        template.Path(templatePath)

        # Apply limit template to limit
        try:
            limit = template.Apply(queryFolder)
        except TypeError as e:
            getLogger().error('Could not apply Template to Limit. Error: %s' % e)
        else:
            assert limit.Threshold() == template.Threshold()
            limit.Threshold(threshold)
            limit.Name(limitName)
            limit.WarningValue(warning)
            limit.Protection(protectionLevel)
            limit.Commit()
            # limit.BusinessProcess().HandleEvent('Monitor Limit')
            success = True
    else:
        getLogger().warn('Query folder (%s) does not exist.' % queryFolderName)
    return success, limit
