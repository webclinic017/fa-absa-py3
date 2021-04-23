'''
Purpose:        [To correct sales credit information on trades supplied within the trade filter or individually]
Department:     [PCG]
Requester:      [Dirk Strauss]
Developer:      [Willie van der Bank]
CR Number:      [28/03/2012, 116445]
'''

import ael, acm
  
def UdateAddInfoMacro(temp,AddInfoVal,trade,AddInfo,*rest):
    try:
        trd = trade     #Should be AEL trade
        found = 0
        for ai in trd.additional_infos():
            if ai.addinf_specnbr.field_name == AddInfo:
                found = 1
                ai_found = ai
        if found == 1:
            aicln = ai_found.clone()
            aicln.value = AddInfoVal
            aicln.commit()
        else:
            tcln = trd.clone()
            ai_new = ael.AdditionalInfo.new(tcln)
            ais = ael.AdditionalInfoSpec[AddInfo]
            ai_new.addinf_specnbr = ais
            ai_new.value = AddInfoVal
            ai_new.commit()
        ael.poll()
        
        return 'Updated'
        
    except:
        return 'Failed'

def UpdateTrades(entity):
    
    if (entity.sales_credit != 0 or entity.add_info('ValueAddCredits') != '') and entity.sales_person_usrnbr == None:
        TRDClone = entity.clone()
        TRDClone.sales_credit = 0
        for ai in TRDClone.additional_infos():
            if ai.addinf_specnbr.field_name == 'ValueAddCredits':
                ai.delete()
        TRDClone.commit()
        print entity.trdnbr, 'fixed Sales_Person1'
        
    counter = 2
    while counter <= 5:
        if (entity.add_info('Sales_Credit' + str(counter)) != '' or entity.add_info('ValueAddCredits' + str(counter)) != '') and entity.add_info('Sales_Person' + str(counter)) == '':
            TRDClone = entity.clone()
            TRDClone.sales_credit = 0
            for ai in TRDClone.additional_infos():
                if ai.addinf_specnbr.field_name == 'ValueAddCredits' + str(counter):
                    ai.delete()
                    continue
                if ai.addinf_specnbr.field_name == 'Sales_Credit' + str(counter):
                    ai.delete()
            TRDClone.commit()
            print entity.trdnbr, 'fixed Sales_Person' + str(counter)
        if (entity.add_info('Sales_Credit' + str(counter)) == '' and entity.add_info('ValueAddCredits' + str(counter)) == '') and entity.add_info('Sales_Person' + str(counter)) != '':
            UdateAddInfoMacro(1, '0', entity, 'Sales_Credit' + str(counter))
            print entity.trdnbr, 'fixed Sales_Person' + str(counter)
        counter = counter + 1
       
def filters():
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    return filters
     
ael_variables = [('Trds', 'Trades', 'string', None, None, 0, 0, 'Multiple trade numbers can be entered, eg: "123,456,789".'),
                 ('tf', 'TradeFilter', 'string', filters())]

def ael_main(dict):

    if dict['Trds'] != '':
        trds = dict['Trds'].split(',')
        for trd in trds:
            try:
                aeltrd = ael.Trade[int(trd)]
                if aeltrd:
                    UpdateTrades(aeltrd)
                else:
                    print 'Invalid trade', trd
            except:
                print 'Invalid trade', trd
            
    elif dict['tf'] != '':
        tf = ael.TradeFilter[dict['tf']]
        for aeltrd in tf.trades():
            try:
                aeltrd = ael.Trade[int(trd)]
                if aeltrd:
                    UpdateTrades(aeltrd)
                else:
                    print 'Invalid trade', trd
            except:
                print 'Invalid trade', trd
                
    return 'Done'
