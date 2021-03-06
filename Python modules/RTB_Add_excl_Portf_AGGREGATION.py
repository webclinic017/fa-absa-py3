import acm

listOfQueryFolders = ['AGG_BILL_CASH_POSTING',
'AGG_BILL_EXP',
'AGG_BILL_INTERN_EXP',
'AGG_BILL_INTERN_TERM',
'AGG_BILL_SIM',
'AGG_BILL_TERM',
'AGG_BILL_VOID',
'AGG_BOND_CORP_CASH_POSTING',
'AGG_BOND_CORP_EXP',
'AGG_BOND_CORP_INTERN_EXP',
'AGG_BOND_CORP_INTERN_TERM',
'AGG_BOND_CORP_SIM',
'AGG_BOND_CORP_TERM',
'AGG_BOND_CORP_VOID',
'AGG_BOND_GOVI_CASH_POSTING',
'AGG_BOND_GOVI_EXP',
'AGG_BOND_GOVI_INTERN_EXP',
'AGG_BOND_GOVI_INTERN_TERM',
'AGG_BOND_GOVI_SIM',
'AGG_BOND_GOVI_TERM',
'AGG_BOND_GOVI_VOID',
'AGG_DEPOSIT_OTCF_CASH_POSTING',
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
'AGG_DEPOSIT_OTCT_VOID',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_CASH_POSTING',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_EXP',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_INT_EXP',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_INT_TERM',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_SIM',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_TERM',
'AGG_FF_CMDTY_INDEX_OTCF_FUT_VOID',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_CASH_POSTING',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_EXP',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_INT_EXP',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_INT_TERM',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_SIM',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_TERM',
'AGG_FF_CMDTY_INDEX_OTCF_FWD_VOID',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_CASH_POSTING',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_EXP',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_INT_EXP',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_INT_TERM',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_SIM',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_TERM',
'AGG_FF_CMDTY_INDEX_OTCT_FUT_VOID',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_CASH_POSTING',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_EXP',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_INT_EXP',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_INT_TERM',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_SIM',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_TERM',
'AGG_FF_CMDTY_INDEX_OTCT_FWD_VOID',
'AGG_FF_CMDTY_OTCF_FUT_CASH_POSTING',
'AGG_FF_CMDTY_OTCF_FUT_EXP',
'AGG_FF_CMDTY_OTCF_FUT_INT_EXP',
'AGG_FF_CMDTY_OTCF_FUT_INT_TERM',
'AGG_FF_CMDTY_OTCF_FUT_SIM',
'AGG_FF_CMDTY_OTCF_FUT_TERM',
'AGG_FF_CMDTY_OTCF_FUT_VOID',
'AGG_FF_CMDTY_OTCF_FWD_CASH_POSTING',
'AGG_FF_CMDTY_OTCF_FWD_EXP',
'AGG_FF_CMDTY_OTCF_FWD_INT_EXP',
'AGG_FF_CMDTY_OTCF_FWD_INT_TERM',
'AGG_FF_CMDTY_OTCF_FWD_SIM',
'AGG_FF_CMDTY_OTCF_FWD_TERM',
'AGG_FF_CMDTY_OTCF_FWD_VOID',
'AGG_FF_CMDTY_OTCT_FUT_CASH_POSTING',
'AGG_FF_CMDTY_OTCT_FUT_EXP',
'AGG_FF_CMDTY_OTCT_FUT_INT_EXP',
'AGG_FF_CMDTY_OTCT_FUT_INT_TERM',
'AGG_FF_CMDTY_OTCT_FUT_SIM',
'AGG_FF_CMDTY_OTCT_FUT_TERM',
'AGG_FF_CMDTY_OTCT_FUT_VOID',
'AGG_FF_CMDTY_OTCT_FWD_CASH_POSTING',
'AGG_FF_CMDTY_OTCT_FWD_EXP',
'AGG_FF_CMDTY_OTCT_FWD_INT_EXP',
'AGG_FF_CMDTY_OTCT_FWD_INT_TERM',
'AGG_FF_CMDTY_OTCT_FWD_SIM',
'AGG_FF_CMDTY_OTCT_FWD_TERM',
'AGG_FF_CMDTY_OTCT_FWD_VOID',
'AGG_FRN_OTCF_CASH_POSTING',
'AGG_FRN_OTCF_EXP',
'AGG_FRN_OTCF_INTERN_EXP',
'AGG_FRN_OTCF_INTERN_TERM',
'AGG_FRN_OTCF_SIM',
'AGG_FRN_OTCF_TERM',
'AGG_FRN_OTCF_VOID',
'AGG_FRN_OTCT_CASH_POSTING',
'AGG_FRN_OTCT_EXP',
'AGG_FRN_OTCT_INTERN_EXP',
'AGG_FRN_OTCT_INTERN_TERM',
'AGG_FRN_OTCT_SIM',
'AGG_FRN_OTCT_TERM',
'AGG_FRN_OTCT_VOID',
'AGG_SWAP_CASH_POSTING',
'AGG_SWAP_CASH_POSTING_SIM',
'AGG_SWAP_CASH_POSTING_VOID',
'AGG_SWAP_EXP',
'AGG_SWAP_SIM',
'AGG_SWAP_TERM',
'AGG_SWAP_VOID']

listOfPortfoliosToAdd = ['42721 ACS_Flow 2', '40741 ACS_FLOW', '40725 ACS EQ_Cash_Facilitation', '40709 Cash Equity Misdeals']

print('processing a list of %i query folders' %len(listOfQueryFolders))
count = 0
for queryFolderName in listOfQueryFolders:
    count = count + 1
    print('%i or %i : %s' %(count, len(listOfQueryFolders), queryFolderName))
    queryFolder = acm.FStoredASQLQuery[queryFolderName]
    originalPortfolioNode = []
    query = queryFolder.Query().Clone()
    for node in query.AsqlNodes():
        if node.IsKindOf(acm.FASQLOpNode):
            try:
                if node.AsqlNodes()[0].AsqlAttribute().AttributeString().Text() == 'Portfolio.Name':
                    originalPortfolioNode = node

                    for newPortfolio in listOfPortfoliosToAdd:
                        fAsqlAttributeNodeClone = originalPortfolioNode.AsqlNodes()[0].Clone()
                        fAsqlAttributeNodeClone.AsqlValue(newPortfolio)
                        originalPortfolioNode.AsqlNodes().Add(fAsqlAttributeNodeClone)
            except Exception, e:
                print('%s has no portfolio attribute.' %queryFolderName)
                
    queryFolder.Query(query)
    try:
        queryFolder.Commit()
    except Exception, e:
        print('ERROR: Cannot process Query Folder : %s : %s' %(queryFolderName, str(e)))
