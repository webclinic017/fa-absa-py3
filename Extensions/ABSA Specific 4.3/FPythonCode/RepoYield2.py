


import ael
import acm
from SAFI_BONDS_BESA import bond_iyl

def get_repo_yield2(obj):


    #code as defined in MessageAdaptations
    trd = ael.Trade[obj.Oid()]
    ins = trd.insaddr
    leg = ins.legs()[0]
    start_day = leg.start_day
    end_day = ins.exp_day
    end_cash = leg.projected_cf(start_day, end_day)*trd.quantity
    val = end_cash*100/(ins.ref_value*trd.quantity)
    price2 = bond_iyl(ins.und_insaddr, val, end_day)
    
    return price2
