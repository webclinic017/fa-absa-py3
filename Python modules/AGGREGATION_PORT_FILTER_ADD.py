import PS_Functions
import acm

queryfolders = ['AGG_DEPOSIT_OTCF_CASH_POSTING',
'AGG_DEPOSIT_OTCF_EXP',
'AGG_DEPOSIT_OTCF_INTERN_EXP',
'AGG_DEPOSIT_OTCF_INTERN_TERM',
'AGG_DEPOSIT_OTCF_SIM',
'AGG_DEPOSIT_OTCF_TERM',
'AGG_DEPOSIT_OTCF_VOID',
'AGG_DEPOSIT_OTCT_CASH_POSTING',
'AGG_DEPOSIT_OTCT_EXP',
'AGG_DEPOSIT_OTCT_INTERN_EXP',
'AGG_DEPOSIT_OTCT_INTERN_TERM',
'AGG_DEPOSIT_OTCT_SIM',
'AGG_DEPOSIT_OTCT_TERM',
'AGG_DEPOSIT_OTCT_VOID']

baseQueryFolderName = 'AGG_DEPOSIT_ALL_REPORT'
basePortfolio = []
baseQueryFolder = acm.FStoredASQLQuery[baseQueryFolderName]
query = baseQueryFolder.Query()
for node in query.AsqlNodes():
    if node.IsKindOf(acm.FASQLOpNode):
        if node.AsqlNodes()[0].AsqlAttribute().AttributeString().Text() == 'Portfolio.Name':
            basePortfolio = node.AsqlNodes()



for queryFolderName in queryfolders:
    print('Query Folder %s' %queryFolderName)
    queryFolder = acm.FStoredASQLQuery[queryFolderName]

    query = queryFolder.Query().Clone()
    for node in query.AsqlNodes():
        if node.IsKindOf(acm.FASQLOpNode):
            try:
                if node.AsqlNodes()[0].AsqlAttribute().AttributeString().Text() == 'Portfolio.Name':
                    node.AsqlNodes(basePortfolio)
                    node.Not(True)
            except:
                print('No ASQL Attribute. Moving on...')
    queryFolder.Query(query)
    queryFolder.Commit()
