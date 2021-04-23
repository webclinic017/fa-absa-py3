
import ael, FCreditLimit

def calc_credit_util_ins(ins,*rest):
    ret = 0
    trades = ins.trades()
    for trade in trades:
        ret += FCreditLimit.calc_credit_util_cp(trade)
    ret = max(ret, 0) 
    return ret

def calc_credit_util_cp_A(ins,*rest):
    ret = 0
    trade = ins.trades()[0]
    party =  trade.counterparty_ptynbr
        
    ret = FCreditLimit.credit_tot_cp(party)
    return ret            


