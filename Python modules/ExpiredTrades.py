import ael
    
def displayTF():
    filterlst = []
    for f in ael.TradeFilter.select():
        filterlst.append(f.fltid)
    filterlst.sort()
    return filterlst
    
def displayPort():
    filterlst = []
    for f in ael.Portfolio.select():
        filterlst.append(f.prfid)
    filterlst.sort()
    return filterlst

	

ael_variables = [('flt', 'Filter', 'string', displayTF(), None, 0, 0), ('Portid', 'Porfolio', 'string', displayPort(), None, 0, 0)]
    
def ael_main(parameter):
    NewPortfolio = parameter.get('Portid')    
    spec = ael.AdditionalInfoSpec["FromPortfolio"]
  
    count = 0
    fail_list = []
    
    for trd in ael.TradeFilter[parameter.get('flt')].trades():
        flag = 'no'
        new_trd = trd.clone()
        new_trd.prfnbr = ael.Portfolio[NewPortfolio].prfnbr
         

        ais = trd.additional_infos()
    	for ai in ais:
            if ai.addinf_specnbr.field_name == 'FromPortfolio':
                flag = 'yes'
		a = ai
		break
		
        if flag == 'no':
            addinf = ael.AdditionalInfo.new(new_trd)
            addinf.addinf_specnbr = spec
            addinf.value = str(trd.prfnbr.prfid)
        else:
            addinf = a.clone()
            addinf.value = str(trd.prfnbr.prfid)
            
        try:
            addinf.commit()
            new_trd.commit()
            print 'Trade ', trd.trdnbr, ' portfolio changed\n'
            count = count + 1
        except:
            print 'Error committing trade ', trd.trdnbr	
            fail_list.append(t.trdnbr)

    print '\nTrades committed : ', count
    print '\nTrades not committed : ', fail_list

    '''
     ai = ael.AdditionalInfo.new(new_trd)
     ai.addinf_specnbr = spec
     ai.value = str(trd.prfnbr.prfid)
     ai.commit()
     new_trd.commit()
    '''

    
