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



ael_variables = [('flt', 'Filter', 'string', displayTF(), None, 0, 0)]
    
def ael_main(parameter):

    spec = ael.AdditionalInfoSpec["FromPortfolio"]
    for trd in ael.TradeFilter[parameter.get('flt')].trades():
        NewPortfolio = trd.add_info('FromPortfolio') 
        new_trd = trd.clone()
         
        new_trd.prfnbr = ael.Portfolio[NewPortfolio].prfnbr
        for ai in trd.additional_infos():
                if ai.addinf_specnbr == spec:
                    ai_c = ai.clone()
                   

                    ai_c.value = str(trd.prfnbr.prfid)
                    ai_c.commit()
        new_trd.commit()
        
    

