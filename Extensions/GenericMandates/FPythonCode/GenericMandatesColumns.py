import acm

from GenericMandatesAuthorizationGlobal import globalCompileAuthorizerGroupNameList
from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate


STAGE_TO_GROUP_MAP = {'Product Support': 'Authorization stage 1',
                      'Compliance': 'Authorization stage 2',
                      'Product Control': 'Authorization stage 3',
                      'Risk': 'Authorization stage 4'}


def GetGroupStatus(bp, name):
    if name in list(STAGE_TO_GROUP_MAP.keys()):
        if STAGE_TO_GROUP_MAP[name] in globalCompileAuthorizerGroupNameList(bp):
            return 1
        else:
            return 0
    else:
        getLogger().error('[ERROR] Invalid group name passed to custom column (%s).' % name)


# Limit Sheet columns
def GetMandateCreateDate(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetCreateTime():
        return mandate.GetCreateTime()
    else:
        return " - "


def GetMandateAuthorizedDate(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetAuthTime():
        return mandate.GetAuthTime()
    else:
        return " - "


def GetMandateAmendedDate(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetAmendTime():
        return mandate.GetAmendTime()
    else:
        return " - "


def GetMandateExpiryDate(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetExpireTime():
        return mandate.GetExpireTime()
    else:
        return " - "


def GetMandateDaysLeft(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetExpireTime():
        return acm.Time.DateDifference(mandate.GetExpireTime(), acm.Time.DateToday())  # pylint: disable=no-member
    else:
        return " - "


def GetMandateQueryFolders(limit):
    folders = []
    mandate = Mandate(limit)
    if mandate:
        qfIds = mandate.QueryFolders()
        for qfOid in qfIds:
            folders.append(acm.FStoredASQLQuery[qfOid])  # pylint: disable=no-member
        return folders
    else:
        return " - "


def GetMandateDescription(limit):
    mandate = Mandate(limit)
    if mandate and mandate.GetDescription():
        return mandate.GetDescription()
    else:
        return " - "


def GetMandateName(limit):
    mandate = Mandate(limit)
    if mandate and mandate.Name():
        return mandate.Name()
    else:
        return " - "


def GetMandateQF(limit):
    from GenericMandatesTreeView import GetNodeInfo

    returnTxt = ""
    mandate = Mandate(limit)
    folders = mandate.QueryFolders()
    for folder in folders:
        text = []
        criteria = {}
        qf = acm.FStoredASQLQuery[folder]  # pylint: disable=no-member
        nodes = qf.Query()
        GetNodeInfo(nodes, 0, text, criteria)

        for line in text:
            returnTxt += "%s\n" % line

    return returnTxt


def GetMandateTraders(limit):
    mandate = Mandate(limit)
    entity = mandate.Entity()
    group = acm.FUserGroup[entity]  # pylint: disable=no-member
    if group:
        users = group.Users()
        usernames = []
        for user in users:
            userName = user.FullName() if len(user.FullName()) > 1 else user.Name()
            usernames.append(userName)
        return usernames
    else:
        return ' - '


def GetMandateCurrency(limit):
    """
    Get the currencies specified for a mandate.
    :param limit: FLimit
    :return: list
    """
    currencies = []
    qfData = _GetMandateNodeInfo(limit)
    for qf in qfData:
        criteria = qf[1]
        if 'Currency.Name' in list(criteria.keys()):
            currencies.append(criteria['Currency.Name'])
        else:
            currencies.append(' - ')
    return ", ".join(currencies)


def GetMandateInsType(limit):
    """
    Get the instrument types specified for a mandate.
    :param limit: FLimit
    :return: list
    """
    insTypes = []
    qfData = _GetMandateNodeInfo(limit)
    for qf in qfData:
        criteria = qf[1]
        if 'Instrument.InsType' in list(criteria.keys()):
            insTypes.append(criteria['Instrument.InsType'])
        else:
            insTypes.append(' - ')
    return ", ".join(insTypes)


def GetMandateUnderlyingInsType(limit):
    """
    Get the underlying instrument type specified for a mandate.
    :param limit: FLimit
    :return: list
    """
    underlyingInsTypes = []
    qfData = _GetMandateNodeInfo(limit)
    for qf in qfData:
        criteria = qf[1]
        if 'Instrument.Underlying.InsType' in list(criteria.keys()):
            underlyingInsTypes.append(criteria['Instrument.Underlying.InsType'])
        else:
            underlyingInsTypes.append(' - ')
    return ", ".join(underlyingInsTypes)


# Business Process Sheet columns
def GetMandateNameFromBP(businessProcess):
    mandate = _GetMandateFromBusinessProcess(businessProcess)
    if mandate:
        return mandate.Name()
    else:
        return " - "


def GetMandateDescriptionFromBP(businessProcess):
    mandate = _GetMandateFromBusinessProcess(businessProcess)
    if mandate:
        return mandate.GetDescription()
    else:
        return " - "


def GetMandateCreateDateFromBP(businessProcess):
    mandate = _GetMandateFromBusinessProcess(businessProcess)
    if mandate:
        return mandate.GetCreateTime()
    else:
        return " - "


def GetMandateAuthorizedDateFromBP(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate:
        return mandate.GetAuthTime()
    else:
        return " - "


def GetMandateAmendedDateFromBP(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate:
        return mandate.GetAmendTime()
    else:
        return " - "


def GetMandateExpiryDateFromBP(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate:
        return mandate.GetExpireTime()
    else:
        return " - "


def GetMandateDaysLeftFromBP(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate and mandate.GetExpireTime():
        return acm.Time.DateDifference(mandate.GetExpireTime(), acm.Time.DateToday())  # pylint: disable=no-member
    else:
        return " - "


def GetMandateQueryFoldersFromBP(bp):
    folders = []
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate:
        qfIds = mandate.QueryFolders()
        for qfOid in qfIds:
            folders.append(acm.FStoredASQLQuery[qfOid])  # pylint: disable=no-member
        return folders
    else:
        return " - "


def GetMandateDescriptionFromBP(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    if mandate:
        return mandate.GetDescription()
    else:
        return " - "


def GetMandateElapsedDays(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    authTime = mandate.GetAuthTime()
    amendTime = mandate.GetAmendTime()
    if mandate and authTime:
        # pylint: disable=no-member
        if amendTime:
            return acm.Time.DateDifference(acm.Time.DateToday(), amendTime)
        else:
            return acm.Time.DateDifference(acm.Time.DateToday(), mandate.GetCreateTime())
    else:
        return 0


def GetMandateSubmitUser(bp):
    mandate = _GetMandateFromBusinessProcess(bp)
    amendUser = mandate.GetAmendUser()
    username = ""
    if len(amendUser) > 1:
        username = amendUser
    else:
        username = mandate.GetCreateUser()
    user = acm.FUser[username]  # pylint: disable=no-member
    return user.FullName()


def _GetMandateFromBusinessProcess(bp):
    if bp.Subject():
        subject = bp.Subject()

        if bp.Subject_type() == "Limit":
            # Load mandate from Limit
            return Mandate(subject)
        elif bp.Subject_type() == "TextObject":
            # Load mandate from Text Object
            limit = acm.FLimit[subject.Name()]  # pylint: disable=no-member
            if limit:
                return Mandate(limit)
            else:
                getLogger().error('[ERROR] Could not load limit (%s)' % subject.Name())


def _GetMandateNodeInfo(limit):
    from GenericMandatesTreeView import GetNodeInfo
    returnValue = []
    mandate = Mandate(limit)
    folders = mandate.QueryFolders()
    for folder in folders:
        text = []
        criteria = {}
        qf = acm.FStoredASQLQuery[folder]  # pylint: disable=no-member
        nodes = qf.Query()
        GetNodeInfo(nodes, 0, text, criteria)
        returnValue.append((text, criteria))
    return returnValue
