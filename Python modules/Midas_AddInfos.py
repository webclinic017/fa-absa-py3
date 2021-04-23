#-----------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module updates additional info's for Fx Swap.
#  Department and Desk : Fx Desk
#  Requester           : Justin Nichols
#  CR Number           : CR 431665, CR 458129
#------------------------------------------------------------------------------

import acm, amb, ael
from FBDPCommon import is_acm_object, acm_to_ael

def setAdditionalInfo(entity, addInfo_fieldName, value):
    
    if entity.trade_process in (16384, 32768): 
        other_entity = otherTrade(entity)
        
        if other_entity:
            
            trd1 = entity.clone()
            trd2 = other_entity.clone()
                     
            for ai in entity.additional_infos():
                if ai.addinf_specnbr.field_name == addInfo_fieldName:
                    trd1_ai = ai.clone()
                    break      
            
            else:
                trd1_ai = ael.AdditionalInfo.new(trd1)
                trd1_ai.addinf_specnbr = ael.AdditionalInfoSpec[addInfo_fieldName] 
            
            trd1_ai.value = value
            
            try:
                ael.begin_transaction()
                trd1.commit()
                trd2.commit()
                trd1_ai.commit()
                ael.commit_transaction()
                ael.poll()
            except:
                ael.abort_transaction()
            
    else:
    
        for ai in entity.additional_infos():
            if ai.addinf_specnbr.field_name == addInfo_fieldName:
                trd1_ai = ai.clone()
                break      

        else:
            trd1_ai = ael.AdditionalInfo.new(entity.clone())
            trd1_ai.addinf_specnbr = ael.AdditionalInfoSpec[addInfo_fieldName]
        
        trd1_ai.value = value
        
        try:
            trd1_ai.commit()
            ael.poll()
        except Exception, e:
            print e
            
def otherTrade(trade):

    if trade:
        acmTrade = acm.FTrade[trade.trdnbr]
        if acmTrade.TradeProcess() == 16384:
            trd_far_leg = acm.FTrade.Select01("connectedTrdnbr=%i and oid<>%i" % (acmTrade.Oid(), acmTrade.Oid()), "")
            if trd_far_leg:
                return acm_to_ael(trd_far_leg)
                
        elif acmTrade.TradeProcess() == 32768:
            trd_near_leg_nbr = acmTrade.ConnectedTrdnbr()
            if trd_near_leg_nbr:
                trd_near_leg = acm.FTrade[trd_near_leg_nbr]
            if trd_near_leg:
                return acm_to_ael(trd_near_leg)
