from ChoicesExprCommon import listChoicesWithEmpty


def get_all_settle_categories(obj):
    chl_lst = listChoicesWithEmpty('TradeSettleCategory')
    modified_chl_lst = []
    for each in chl_lst:
        if not each:
            modified_chl_lst.append(each)
        elif not each.Name().startswith('Euroclear'):
            modified_chl_lst.append(each)
        elif each.Name() == 'Euroclear':
            modified_chl_lst.append(each)
    return modified_chl_lst
