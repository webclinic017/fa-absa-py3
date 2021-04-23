"""---------------------------------------------------------------------------------------------------------------
Purpose                 : Pull rates for BSB and Depo trades
Department and Desk     : Liquidity 
Requester               : Andrew East, Noloyiso Mahlakahlaka-Mhlubulwana, Hendrico Kok, Lawrence Masekoa
Developer               : Edmundo Chissungo
JIRA Number             : ABITFA-1801
------------------------------------------------------------------------------------------------------------------"""



import ael, acm, csv, time
import sys
from pprint import pprint

def TradeFilter():

    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    TradeFilterList.sort()
    
    return TradeFilterList



tradeFilter = TradeFilter()
ael_variables = [('Path', 'OutputDirectory', 'string', 'F:\ '),
                 ('Filename', 'FileName', 'string', '', 'Liquidity_BSB_Repos.txt'),
                 ('Filter', 'Filter', 'string', tradeFilter, 'Liquidity_BSB_Repos'),
                 ('strDate', 'Date', 'string', '', ael.date_today())]


def ael_main(parameter):  
    #print '\t Start\n'
    OutPutFile = parameter['Filename']
    filter = acm.FTradeSelection[parameter['Filter']]
    path = parameter['Path']
    
    date_s = parameter['strDate']    
    if date_s == 'Today':
        d = ael.date_today()
    else:
        try:
            d = ael.date_from_string(date_s, '%Y-%m-%d')
        except:
            d = ael.date_today()

    #print 'Outfile = ','', path+OutPutFile
    bsb_repo_rate_deposit_pull(filter, path, OutPutFile)

    print '\nWrote secondary output to:::', path+OutPutFile
    print '\nCompleted Successfully'
    

    
def bsb_repo_rate_deposit_pull(filter, path, OutPutFile, *rest):

    la_BSB_Repo_trades = filter.Trades() 
    
    if len(la_BSB_Repo_trades) < 0:
        print '\ntrade filter has no trades ...crash imminant...will exit -1 instead\n'
        return 
    
    rates = []
  
    for t in la_BSB_Repo_trades:
        i = t.Instrument()
        Itype = i.InsType()
        if i.InsType() == 'BuySellback':
            rate = i.Rate()
        elif i.InsType() in ('Repo/Reverse', 'Deposit'):
            #repo or deposit
            l = i.Legs()[0]
            if l.LegType() == 'Float':
                rate = l.FirstRate()
            else:
                rate = l.FixedRate()
        else:
            rate = 0.0
                
        temp = [t.Oid(), str(rate), Itype+'\n']
        rates.append(temp)
    

    outfile = open(path+OutPutFile, 'w')
    outfile.write ('TradeNumber\tRate\n')
    outfile.flush()
    
    for r in rates:
        outfile.write ('{0}\t{1}\n'.format(r[0], r[1]))
    
    outfile.close()
  

