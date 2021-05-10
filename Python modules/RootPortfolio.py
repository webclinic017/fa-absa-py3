import ael
def getroot(prf,*rest):
    par = getparent(prf)
    '''
    if par.prfid != '9806':
        return getroot(par)
    else:
        if prf:
            return prf.prfid
        else:
            return '1'
    '''
        
        
    if par:
        if par.prfid != '9806':
            return getroot(par)
        else:
            if prf:
                return prf.prfid
            else:
                return '1'
    else:
        return '1'

        
def getparent(prf):        
    p = ael.PortfolioLink.select('member_prfnbr = %d' %(prf.prfnbr))
    return p[0].owner_prfnbr

'''
print ael.Portfolio['4440798'].prfid
print 'Fin - ', getroot(ael.Portfolio['4440798'],None)
'''

mapd = {'43034': 'DELTA_ONE','47076': 'DELTA_ONE','Delta One 1 47464': 'DELTA_ONE','Delta One 2 47605': 'DELTA_ONE','Delta One 3 47613': 'DELTA_ONE','Delta One 4 47621': 'DELTA_ONE','47035': 'DELTA_ONE',
'47159': 'ALSI_TRADING','47001 STRADDLES': 'ALSI_TRADING',
'44404': 'Single Stock Trading','44255': 'Single Stock Trading','47209 Book Build': 'Single Stock Trading','47696': 'Single Stock Trading',
'47670': 'Single Stock Trading','47688': 'Single Stock Trading', '47662 EQ_SA_PairsOption': 'Single Stock Trading',
'47506 NRD': 'Linear Trading','47589': 'Linear Trading','47324': 'Linear Trading','42945 CFD Misdeals': 'Linear Trading','47043':'Linear Trading',
'47738': 'Linear Trading','47472': 'Single Stock Trading', '47787_RAFRES': 'Linear Trading',
'42846': 'Client Trading','47597 Client Trades': 'Client Trading',
'43042': 'SMALL_CAP','47167': 'SMALL_CAP','47373': 'SMALL_CAP',
'47415': 'Structured Note Products',
'44263':'Structured Transactions','44271 Telkom Delta':'Structured Transactions','47142':'Structured Transactions','47233':'Structured Transactions',
'49007 EQ_SA_Opportunity':'Arbitrage Baskets','49015 EQ_SA_Pairs':'Arbitrage Baskets','49031 Eq_SA_TrendA':'Arbitrage Baskets',
'49072':'Arbitrage Baskets','49114 EQ_SA_StockVol':'Arbitrage Baskets','49023 EQ_SA_RelativeVol':'Arbitrage Baskets',
'EQ_SA_PairsOption':'Arbitrage Baskets', '47654 EQ_SA_PairsAuction':'Arbitrage Baskets','47795_RAFIND':'Linear Trading', '47803_RAFFIN':'Linear Trading',
'BRADS':'DELTA_ONE', '47720 EQ-SA-DELTA1':'Arbitrage Baskets','49023':'GRAVEYARD', '49007':'GRAVEYARD', '49015':'GRAVEYARD', 
'47233 OML':'Structured Transactions', '49114':'GRAVEYARD', '47811 Pairs Trading':'DELTA_ONE','47829 USD Equity Swaps':'DELTA_ONE',
'Delta One 1 45062':'DELTA_ONE','Delta One 2 45070':'DELTA_ONE','Delta One 4 45096':'DELTA_ONE' }

plist = ['Structured Note Products', 'Structured Transactions', 'Single Stock Trading', 'Alsi Trading', 'DELTA_ONE', 'Linear Trading']

def mapping(port, *rest):
    try:
        return mapd[(port.prfid)]
    except:
        ael.log(port.prfid)
        return port.prfid
