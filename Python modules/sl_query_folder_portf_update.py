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
CR NUMBER               :  280186

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-04-09 280186    Francois Truter    Initial Implementation

-----------------------------------------------------------------------------"""

import acm

def removeAttributes(opNode, removePortfolioAttributes):
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
            node = removeAttributes(node, removePortfolioAttributes)
            if not node.AsqlNodes():
                nodes.Remove(node)
    return opNode

queryFoldersKey = 'QueryFolders'

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [queryFoldersKey, 'Query Folders', 'FStoredASQLQuery', None, None, 0, 1, 'The Query Folders that need to be recreated', None, 1]
]

def ael_main(parameters):
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
                        
                    portfolioQuery = removeAttributes(queryFolder.Query().Clone(), False)
                    portfolioQuery.AsqlQueryClass(acm.FPhysicalPortfolio)

                    newQueryFolderName = queryFolder.Name() + ' Manual'
                    acm.BeginTransaction()
                    try:
                        newQueryFolder = acm.FStoredASQLQuery[newQueryFolderName]
                        if not newQueryFolder:
                            newQueryFolder= acm.FStoredASQLQuery()
                            newQueryFolder.Name(newQueryFolderName)

                        newQuery = removeAttributes(queryFolder.Query().Clone(), True)
                        op = newQuery.AddOpNode('OR')

                        for portfolio in portfolioQuery.Select():
                            op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())

                        newQueryFolder.Query(newQuery)
                        newQueryFolder.Commit()
                        acm.CommitTransaction()
                    except Exception as ex:
                        acm.AbortTransaction()
                        raise ex
                    else:
                        acm.Log('Updated %s' % newQueryFolderName)
                except Exception as ex:
                    acm.Log('Could not recreate %s: %s' % (queryFolder.Name(), str(ex)))
    except Exception as ex:
        acm.Log('Error in sl_query_folder_portf_update: %s' % str(ex))
        

