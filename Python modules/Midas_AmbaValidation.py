#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : Fx Swap, Spot and Outright Amaba message validation
#  Department and Desk : Front Arena BTB/TRB
#  Requester           : Front Arena BTB/RTB]
#  CR Number           : CR 587810
#-----------------------------------------------------------------------------------------------------------------

import amb, ael

def modify_sender(m, s):
    
    result = (m, s)
    type_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    type_value = type_obj.mbf_get_value() 

    if type_value in ['INSERT_TRADE', 'UPDATE_TRADE']:
        AmbMsg  = m.mbf_find_object("TRADE", "'MBFE_BEGINNING'")
        t = ael.Trade[int( AmbMsg.mbf_find_object("TRDNBR").mbf_get_value())]
        if t.insaddr.instype == 'Curr':
            if ael.date_from_time(t.creat_time)== ael.date_today(): 
                if AmbMsg.mbf_find_object('STATUS').mbf_get_value() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                    if AmbMsg.mbf_find_object('COUNTERPARTY_PTYNBR.PTYID').mbf_get_value() not in ('NLD DESK', 'AFRICA DESK', 'RAND SPOT DESK'):
                        return (m, s)
    

