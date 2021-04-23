#-----------------------------------------------------------------------------------------------------
# Name                : CurrSwap_MtM_Fixings
# Purpose             : This script fixes the reset dates on Fx rate to avoid unnecessary cash breaks.
# Developer           : Tshepo Mabena
# Department and Desk : Derivatives - PCG Operations
# Requester           : Julie Ellis
# Date                : 15/07/2010
# CR Number           : 371486
#------------------------------------------------------------------------------------------------------

import ael, acm
from FBDPCommon import is_acm_object, acm_to_ael

def get_addinfo(entity, ai_name):
    
    if is_acm_object(entity):
        entity = acm_to_ael(entity)
  
    val = None
    for ai in entity.additional_infos():       
        if ai.addinf_specnbr.field_name == ai_name:
            val = ai.value
            break
    return val

def Reset_Date_Fixing(temp,t,*rest):
    
    Cal_List = []
    ins = acm.FInstrument[t.insaddr.insid]
    
    if t.insaddr.instype == 'CurrSwap':  
        for l in t.insaddr.legs():
            if l.nominal_scaling == 'FX':
                Cal1 = get_addinfo(ins, 'FX Reset Calendar1')
                Cal2 = get_addinfo(ins, 'FX Reset Calendar2')
                Cal3 = get_addinfo(ins, 'FX Reset Calendar3')
                             
                Cal_List.append(Cal1)
                Cal_List.append(Cal2)
                Cal_List.append(Cal3)
       
    for cf in t.insaddr.legs()[0].cash_flows():
        
        if cf.type == 'Return' and cf.start_day >= ael.date_today():
            for r in cf.resets():
                if r.type in ('Nominal Scaling', 'Return'):

                    all_dates = []
                    for cal in Cal_List:
                        if str(cal) != 'None':
                            date = r.start_day.add_banking_day(ael.Calendar[cal], -1)
                            Reset_Date = date.adjust_to_banking_day(ael.Calendar[cal], 'Preceding')
                            all_dates.append(Reset_Date)
                            
                    if not(max(all_dates) == min(all_dates) and r.day == max(all_dates)) :   
                    # reset dates do not match    
                        if max(all_dates) == min(all_dates):
                        # current reset day does not equal calculated reset day
                            nday = min(all_dates)
                        else:
                            while max(all_dates) <> min(all_dates):
                                mdate = min(all_dates)
                                all_dates = []
                                    
                                for cal in Cal_List:
                                    all_dates.append(mdate.adjust_to_banking_day(ael.Calendar[cal], 'Preceding'))
                                if min(all_dates) == max(all_dates):
                                    nday = min(all_dates)   
                                else:
                                    all_dates = []
                                    for cal in Cal_List:
                                        date = mdate.add_banking_day(ael.Calendar[cal], -1)
                                        all_dates.append(date.adjust_to_banking_day(ael.Calendar[cal], 'Preceding'))
                                    if min(all_dates) == max(all_dates):
                                        nday = min(all_dates)
                    else:
                        nday = min(all_dates)
        
                    all_dates = []
                    for cal in Cal_List:
                        if str(cal) != 'None':
                            date = nday.add_banking_day(ael.Calendar[cal], -1)
                            Reset_Date = date.adjust_to_banking_day(ael.Calendar[cal], 'Preceding')
                            all_dates.append(Reset_Date)
                                    
                    if not(max(all_dates) == min(all_dates) and r.day == max(all_dates)) :   
                    # reset dates do not match    
                        if max(all_dates) == min(all_dates):
                        # current reset day does not equal calculated reset day
                            r = r.clone()
                            r.day = max(all_dates)
                            try:
                                r.commit()
                            except:
                                print 'Commit failed'   
                        else:
                            while max(all_dates) <> min(all_dates):
                                mdate = min(all_dates)
                                all_dates = []
                                    
                                for cal in Cal_List:
                                    if str(cal) != 'None':
                                        all_dates.append(mdate.adjust_to_banking_day(ael.Calendar[cal], 'Preceding'))
                                if min(all_dates) == max(all_dates):
                                    r = r.clone()
                                    r.day = min(all_dates)
                                    try:
                                        r.commit()
                                    except:
                                        print 'Commit failed'   
                                else:
                                    all_dates = []
                                    for cal in Cal_List:
                                        if str(cal) != 'None':
                                            date = mdate.add_banking_day(ael.Calendar[cal], -1)
                                            all_dates.append(date.adjust_to_banking_day(ael.Calendar[cal], 'Preceding'))
                                    if min(all_dates) == max(all_dates):
                                        r = r.clone()
                                        r.day = min(all_dates)
                                        try:
                                            r.commit()
                                        except:
                                            print 'Commit failed'                
                                
def Filter():
    
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
        
    return filters  
        
def ASQL(*rest):
    acm.RunModuleWithParameters('CurrSwap_MtM_Fixings', 'Standard' )
    return 'SUCCESS'
    
ael_variables = [('tf', 'TradeFilter:', 'string', Filter(), 'ALL'),
                ('trdnbr', 'Trade Number:', 'string', None, '0')]
                
def ael_main(dict):
    
    if dict['trdnbr'] == '0' and dict['tf'] == 'ALL':
        tf = ael.TradeFilter['CurrSwap_MtM_Fixings']
        for t in tf.trades():
            Reset_Date_Fixing(1, t)
                
    if dict['trdnbr'] == '0' and dict['tf'] != 'ALL':
        tf = ael.TradeFilter[dict['tf']]
        for t in tf.trades():
            Reset_Date_Fixing(1, t)                
                               
    if dict['trdnbr'] != '0' and dict['tf'] == 'ALL':
        t = ael.Trade[int(dict['trdnbr'])]
        Reset_Date_Fixing(1, t)                
