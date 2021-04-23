'''
Purpose:    AEL module for daily updates of stock value total to broker ABCAP SECURITIES addinfo

Department: Middle Office, Middle Office
Requester:  Herman Levin, Khunal Ramesar
Developer:  Jaysen Naicker, Jaysen Naicker
CR Number:  466364(18/10/2010), 481152 (04/11/2010)
'''

import ael, string

def setAddInfo(object, specName, value):
    """
    Sets an additional info on a cloned object.
    If addinfo already exist, it is updated. Otherwise
    it is created.
    Returns FALSE if any error occurs. Otherwise TRUE.
    """
    if not type(object) == ael.ael_entity and not object.original():
        eMsg = "Object must be a cloned ael entity"
        raise ValueError(eMsg)
    try:
        found = False
        addInfoSpec = ael.AdditionalInfoSpec[str(specName)]
        for addInfo in object.additional_infos():
            if addInfo.addinf_specnbr == addInfoSpec:
                found = True
                break
        if found:
            addInfo.value          = value
        else:
            addInfo                = ael.AdditionalInfo.new(object)
            addInfo.addinf_specnbr = addInfoSpec
            addInfo.value          = value
    except Exception, msg:
        print "Failed to set addinfo on object", msg, specName, value
        return False
    return True
        
    
    
'''
Select the value (qty*price) for all stocks fulfilling the below criteria for a particular day
and update the additional info Broker_Fee_Amount and Broker_Fee_Date.
'''
def Update_Broker_Fee(temp, rdate, *rest):
    rdate = ael.date(rdate)
    val = ael.asql(""" select sum(i.quote_type = 'Per 100 Units' ? abs(t.quantity*t.price/100) : abs(t.quantity*t.price))
                from 
                    trade t,
                    instrument i,
                    portfolio port,
                    party p
                where
                    t.insaddr = i.insaddr
                    and t.prfnbr = port.prfnbr
                    and t.counterparty_ptynbr = p.ptynbr
                    and i.instype in ('Stock','ETF')
                    and t.status in ('FO Confirmed','BO Confirmed','BO-BO Confirmed')
                    and to_date(t.time) = to_date(@date)
                    and p.ptyid = 'JSE'
                    and port.prfid not in ('248179','BSE NewGold','Note Platinum','Note Silver','OTC Platinum','OTC Silver','Index Issuance','Platinum Issuance','Silver Issuance') 
                    and add_info(t, 'Broker_Fee_Exclude') ~= 'Yes' """, 1, ['@date'], ["'" + str(rdate) + "'"])[1][0]              
    
    if val:
        value = val[0][0]
    else:
        value = 0
  
    broker = ael.Party['ABCAP SECURITIES']
    bclone = broker.clone()
  
    if broker.add_info('Broker_Fee_Amount') == '':
        if setAddInfo(bclone, 'Broker_Fee_Amount', '0.0'):
            bclone.commit()
            
    if  broker.add_info('Broker_Fee_Date') == '':
        if setAddInfo(bclone, 'Broker_Fee_Date', '1900-01-01'):
            bclone.commit()
    ael.poll()
    
    obal = broker.add_info('Broker_Fee_Amount')
    ldate = broker.add_info('Broker_Fee_Date').replace('/', '-')

    if ael.date(ldate).to_ymd()[1] == ael.date(rdate).to_ymd()[1]:
        cbal = float(obal) + value
    else:
        cbal = value
            
    if setAddInfo(bclone, 'Broker_Fee_Amount', str(cbal)):
        bclone.commit()
    else:
        return 'Broker_Fee_Amount update fail'
        
    if setAddInfo(bclone, 'Broker_Fee_Date', str(rdate)):
        bclone.commit()
    else:
        return 'Broker_Fee_Date update fail'
    ael.poll()
    
    return 'Done'
 


ael_variables = [('Rdate', 'Run Date', 'string', ['today'], 'today')]

def ael_main(ael_dict):
    rdate = ael_dict['Rdate']
    if ael_dict['Rdate'].upper() == 'TODAY':
        rdate = ael.date_today()
    Update_Broker_Fee('', rdate)
    
    print "Completed Successfully ::"
