'''
Purpose                 : Clean up zero Bonds
Department and Desk     :IT
Requester:              :Daniel Simoes
Developer               :Ickin Vural
CR Number               :C000000510284
'''

import ael, acm, time, string


def filters():
    filterList = []
    filters = ael.TradeFilter.select()
    for tf in filters.members():
        filterList.append(tf.fltid)
    return filterList

filters = filters()
today = ael.date_today()
ael_variables = [('StartDate', 'StartDate', 'date', None, today, 1, 0, 'Execution date from which sales credit should be calculated.'),
                ('EndDate', 'EndDate', 'date', None, today, 1, 0, 'Execution date up to which sales credit should be calculated.'),
                ('Filter', 'Filter', 'string', filters, 'SalesCredit', 1, 0, 'Trade filter on which sales credit should be calculated.')]
 
 

   

def createAddInfo(t, name, value):
    '''
Creates the additional info for a trade
    '''
    
    ais = ael.AdditionalInfoSpec[name]
    found = 0
    for ai in t.additional_infos():
        if ai.addinf_specnbr == ais:
                found = 1
                break
                
    if found == 1:
        ai.value = value
    else:
        ai_new = ael.AdditionalInfo.new(t)
        ai_new.addinf_specnbr = ais
        ai_new.value = value
       
    return t      


def ael_main(ael_dict):
    '''
Module to calculate the sales credit
    '''
    
    startDate = ael.date_from_string(ael_dict['StartDate'], '%Y-%m-%d')
    endDate = ael.date_from_string(ael_dict['EndDate'], '%Y-%m-%d')
    tradefilter = ael.TradeFilter[ael_dict['Filter']]
           
    
    t0  = time.time()
    count = 0

    
    
    try:
    
        for trade in tradefilter.trades():
                
                
                createDate = ael.date_from_time(trade.creat_time)
                    
                if createDate <= endDate and createDate >= startDate:
                  
                        if trade.prfnbr.prfid in ('EQ Islamic Liabilities') and trade.add_info('Sales_Person2') == 'ABBS447' and trade.add_info('Sales_Person3') == 'ABTMAHN':
                           
                            count = count + 1
                            
                            value = 0
                                           
                            try:
                                trade_clone = trade.clone()
                                
                                trade_clone = createAddInfo(trade_clone, 'Sales_Credit2', str(value))
                                trade_clone = createAddInfo(trade_clone, 'Sales_Person2', 'ABBS447')
                                
                                trade_clone = createAddInfo(trade_clone, 'Sales_Credit3', str(value))
                                trade_clone = createAddInfo(trade_clone, 'Sales_Person3', 'ABTMAHN')
                                
                                try:
                                    trade_clone.commit()
                                
                                except  Exception, errMsg:
                                    print 'Trade %i have not been updated with the additional info fields : %s' %(trade.trdnbr, errMsg)
                                
                                
                            except Exception, errMsg:
                                print 'Exception in Zero or IndexLinkedBond', errMsg, 'Trade ', trade.trdnbr
                                
                            
                            ael.poll()
         

        print '%i trades have been updated with a Sales Credit additional info in %.0f seconds' % (count, time.time() - t0)

    except Exception, errMsg:
        print 'Exception', errMsg