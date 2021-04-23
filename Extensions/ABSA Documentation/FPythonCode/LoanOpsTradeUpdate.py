import acm

from xlrd import open_workbook


path = 'Y:/Jhb/Secondary Markets IT Deployments/FA/Change Pending/CommFeeTradesAgents20191204.xlsx'


def _get_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('Sheet1')
        data = {}
        error_list = []
        for row in sheet.get_rows():
            trade_no = str(row[0].value).replace('.0', '')
            counter_party = row[1].value
            agent = str(row[2].value)
            sett_cat = str(row[3].value)
            data.update({'%s' % trade_no:[counter_party, agent, sett_cat]})
        return data
    except Exception as Ex:
        print Ex

    return None

def update_trade(trade_no, counter_party, agent, sett_cat):
    try:
        trade = acm.FTrade[trade_no]
        trade = trade.StorageImage()
        trade.AdditionalInfo().PM_FacilityAgent(agent)
        trade.SettleCategoryChlItem(sett_cat)
        trade.Commit()
        return trade.Oid()
    except Exception as ex:
        print ex
    return trade_no, counter_party, agent, sett_cat
            
def upload_data():
    data = _get_data(path)
    error_list = []
    success = []
    
    
    for key, value in data.items():
        try:
            if key == 'Trade No':
                continue
            print update_trade(key, value[0], value[1], value[2])
        except Exception as Ex:
            error_list.append(key)
            print Ex
    return error_list, success


upload_data()
