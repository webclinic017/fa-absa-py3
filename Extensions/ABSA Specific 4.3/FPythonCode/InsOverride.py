import acm

def get_InsOverride(trade):
    addInfo = acm.FAdditionalInfo.Select01('recaddr = %i addInf = %i' % (trade.Oid(), 1011), ' ')
    if addInfo:
        return addInfo.FieldValue()

def objectSatisfiesQueryFolder(object, queryFolderName):
    queryFolder = acm.FStoredASQLQuery[queryFolderName]
    assert queryFolder is not None, 'Cannot find query folder named %s' % queryFolderName
    assert queryFolder.IsKindOf(acm.FStoredASQLQuery), 'Cannot find query folder with name %s' % queryFolderName
    query = queryFolder.Query()
    return query.IsSatisfiedBy(object)
