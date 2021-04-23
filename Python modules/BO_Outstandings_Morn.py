'''HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2015-09-08  Paseka Motsoeneng           Abitfa3738:Added the logic to calculate aging from trade update time and remove the previous execution time.
2016-01-27  Faize Adams                 ABITFA-4035: Added update time field in output.
'''

import ael
from datetime import datetime

def gen_head(headers, delimiter, breaker):
    return delimiter.join(map(str, headers)) + breaker 
    
def get_outstanding(outfile, trade_filter):
    tb = '\t'
    nl = '\n'
    trades = ael.TradeFilter[trade_filter].trades()
    
    days = []
    
    data_file = open(outfile, 'w')
    
    print 'Create file:%s'%outfile
    
    head = ['Area', 'Trade', 'Days', 'Portfolio', 'Portfolio Code', 'Type',
            'Instrument', 'Execution Time', 'Trader', 'Create User',
            'Update User', 'Maturity', 'Counterparty', 'Party Type',
            'Aggregated', 'Status', 'MirrorTrade', 'Otc', 'EconomicAmend',
            'ApproxLoad', 'BondNutronBooked', 'Currency', 'MarkitWire',
            'EconoAmendOPSConf', 'Acquirer', 'Trade type', 'Update Time']
    data_file.write(gen_head(head, tb, '\n'))
    
    print 'Populating records...'
    
    for trade in trades:
        data = []
        
        #Area
        data.append(trade.prfnbr.add_info('Parent_Portfolio'))
        
        #Trade
        data.append(trade.trdnbr)
        
        #Days
        data.append(ael.date_today().bankingdays_between(ael.date(datetime.fromtimestamp(trade.updat_time).strftime('%Y-%m-%d')), ael.Instrument['ZAR']))
        
        #Portfolio
        data.append(trade.prfnbr.prfid)
        
        #Portfolio Code
        data.append(trade.prfnbr.prfnbr)
        
        #Type
        data.append(trade.insaddr.instype)
        
        #Instrument
        data.append(trade.insaddr.insid)
        
        #Execution Time
        data.append(datetime.fromtimestamp(trade.execution_time).strftime('%Y-%m-%d %H:%M:%S'))
        
        #Trader
        try:
            data.append(trade.trader_usrnbr.name)
        except:
            data.append('None')
        
        #Create User
        data.append(trade.creat_usrnbr.name)
        
        #Update User
        data.append(trade.updat_usrnbr.name)
        
        #Maturity
        data.append(trade.maturity_date())
        
        #Counterparty
        data.append(trade.counterparty_ptynbr.display_id())
        
        #Party Type
        data.append(trade.counterparty_ptynbr.type)
        
        #Aggregated
        if trade.aggregate:
            data.append('Yes')
        else:
            data.append('No')
        
        #Status    
        data.append(trade.status)
        
        #MirrorTrade
        if trade.mirror_trdnbr:
            data.append(trade.mirror_trdnbr.trdnbr)
        else:
            data.append('None') 
        
        #Otc
        if trade.insaddr.otc:
            data.append('OTC')
        else:
            data.append('')
        
        #EconomicAmend
        if trade.add_info('EconomicAmend'):
            data.append(trade.add_info('EconomicAmend'))
        else:
            data.append('None')
        
        #ApproxLoad
        if trade.add_info('Approx. load'):
            data.append(trade.add_info('Approx. load'))
        else:
            data.append('None')
        
        #BondNutronBooked
        if trade.insaddr.instype == 'Bond':
            data.append(trade.insaddr.add_info('Exchange'))
        else:
            data.append('')
        
        #Currency
        data.append(trade.curr.insid)
        
        #MarkitWire
        if trade.add_info('CCPmiddleware_id'):
            data.append(trade.add_info('CCPmiddleware_id'))
        else:
            data.append('None') 
        
        #EconoAmendOPSConf
        if trade.add_info('EconoAmendOPSConf'):
            data.append(trade.add_info('EconoAmendOPSConf'))
        else:
            data.append('None')
            
        #Acquirer
        if trade.acquirer_ptynbr:
            data.append(trade.acquirer_ptynbr.ptyid)
        else:
            data.append('None')

        #Trade type
        if trade.type:
            data.append(trade.type)
        
        #Update time
        data.append(datetime.fromtimestamp(trade.updat_time).strftime('%Y-%m-%d %H:%M:%S'))
        
        line = gen_head(data, tb, nl)
        data_file.write(line)
    print 'Process complete...'
    data_file.close()


tfs = [
    'FO_Outstanding_JRJ_Edit',
    'FO_Outstanding_JRJ_Edit_AC'
]

ael_variables = [
    ['FilePath', 'File Path', 'string', None, '/services/frontnt/Task/', 0],
    ['FileName', 'File Name', 'string', None, 'BO_Outstandings.xls', 0],
    ['TradeFilter', 'Trade Filter', 'string', tfs, tfs[0], 1, 0,
        'Choose the trade filters (virtual portfolios) to report', None]
]


def ael_main(ael_variables):
    print 'FO_Outstandings process starts...'

    trade_filter = ael_variables['TradeFilter']
    outfile = '%s%s'%(ael_variables['FilePath'], ael_variables['FileName'])

    try:
        results = get_outstanding(outfile, trade_filter)
    except Exception, e:
        print str(e)
