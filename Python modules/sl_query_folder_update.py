"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Updates a list of Query Folders. The Query Folders 
                           should select trades from portfolios based on the 
                           values of additional info fields on the portfolios.
                           The Query Folders are much faster if the portfolios 
                           are specified explicitly as opposed to filterring
                           on the additional info field values. This script 
                           sets the portfolios on the Query Folders.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  500708

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-06-08 332137    Francois Truter    Initial Implementation
2010-11-20 500708    Francois Truter    Added _getNewQueryFolderName to
                                        prevent errors when the new query 
                                        folder name is trunacted
2017-08-15 4820291   Ondrej Bahounek    Exclude graveyarded portfolios.
-----------------------------------------------------------------------------"""

import acm


def is_graveyarded(portf):
    if not portf:
        return False
    if portf.Name() == "GRAVEYARD":
        return True
    for link in portf.MemberLinks():
        return is_graveyarded(link.OwnerPortfolio())
    return False


def _removeAttributes(opNode, removePortfolioAttributes):
    nodes = opNode.AsqlNodes()
    clones = nodes.Clone()
    for node in clones:
        if node.IsKindOf(acm.FASQLAttrNode):
            attrString = node.AsqlAttribute().AttributeString().Text()
            if attrString.startswith('Portfolio.') == removePortfolioAttributes:
                nodes.Remove(node)
            elif not removePortfolioAttributes:
                node.AsqlAttribute().AttributeString(attrString.replace('Portfolio.', '', 1))
        elif node.IsKindOf(acm.FASQLOpNode):
            node = _removeAttributes(node, removePortfolioAttributes)
            if not node.AsqlNodes():
                nodes.Remove(node)
    return opNode


def _getNewQueryFolderName(original):
    maxLen = 31
    if len(original) >= (maxLen - 1):
        raise Exception('The original name of the query folder [%s] is too long - it cannot be modified to create a name for the new query folder.' % original)
    
    new = original + ' Manual'
    length = len(new)
    if length > maxLen:
        new = new[:(length - maxLen) * -1]
        
    return new

queryFoldersKey = 'QueryFolders'

def updateQueryFolders(parameters):
    succcessful = True
    try:
        queryFolders = parameters[queryFoldersKey]
        if not queryFolders or len(queryFolders) == 0:
            defaultQueryFolderList = acm.FStoredASQLQuery['SL_Query_Folder_Portf_Update']
            if defaultQueryFolderList and defaultQueryFolderList.Query() and defaultQueryFolderList.QueryClass() == acm.FStoredASQLQuery:
                queryFolders = defaultQueryFolderList.Query().Select()
        
        if not queryFolders or len(queryFolders) == 0:
            acm.Log('No query folders to update')
        else:
            for queryFolder in queryFolders:
                try:
                    if queryFolder.QueryClass() != acm.FTrade:
                        raise Exception('This process is only implemented for Query Folders on Trades.')
                        
                    portfolioQuery = _removeAttributes(queryFolder.Query().Clone(), False)
                    portfolioQuery.AsqlQueryClass(acm.FPhysicalPortfolio)

                    user = queryFolder.User()
                    newQueryFolderName = _getNewQueryFolderName(queryFolder.Name())
                    acm.BeginTransaction()
                    try:
                        newQueryFolder = acm.FStoredASQLQuery.Select01("name = '%(name)s' and user = %(user)s" % {'name': newQueryFolderName, 'user': str(user.Oid()) if user else 'null'}, "More than one object returned with unique id")
                        if not newQueryFolder:
                            newQueryFolder = acm.FStoredASQLQuery()
                            newQueryFolder.Name(newQueryFolderName)

                        newQuery = _removeAttributes(queryFolder.Query().Clone(), True)
                        op = newQuery.AddOpNode('OR')

                        for portfolio in portfolioQuery.Select():
                            if not is_graveyarded(portfolio):
                                op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())

                        newQueryFolder.Query(newQuery)
                        newQueryFolder.AutoUser(False)
                        newQueryFolder.User(user)
                        newQueryFolder.Commit()
                        acm.CommitTransaction()
                    except Exception as ex:
                        acm.AbortTransaction()
                        raise ex
                    else:
                        acm.Log('Updated %s' % newQueryFolderName)
                except Exception as ex:
                    acm.Log('Could not recreate %s: %s' % (queryFolder.Name(), str(ex)))
                    succcessful = False
    except Exception as ex:
        acm.Log('Error in sl_query_folder_update: %s' % str(ex))
        return False
    else:
        return succcessful
