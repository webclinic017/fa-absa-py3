#    Functions used for Repo fields for BESA
import ael

def sgn(x):
    if x < 0.0:
        sn = -1
    else:
        sn = 1

    return sn

def curr_year(od):
    
    today = ael.date_today()
    d = ael.date(od)
    yb = int(d.years_between(today))
    return d.add_years(yb)
    

def dirty_from_yield_ur(ins, settlement, yld):
    
    mature = ins.exp_day
    coupon = ins.legs()[0].fixed_rate        
              
        
    ins_ex1 = ins.add_info('ExCoup1')
    ins_ex2 = ins.add_info('ExCoup2')
        
    ex1 = curr_year(ins_ex1)
    c1 = ex1.add_days(10)
    ex2 = curr_year(ins_ex2)
    c2 = ex2.add_days(10)
    
    if ex1 > c1:
        ex1 = ex1.add_years(-1)
    
    if (c1 <= settlement):
        c1 = c1.add_years(1)
        ex1 = ex1.add_years(1)
    
    if ex2 > c2:
        ex2 = ex2.add_years(-1)
    
    if (c2 <= settlement):
        c2 = c2.add_years(1)
        ex2 = ex2.add_years(1)
    
    if (settlement.days_between(c1)) < (settlement.days_between(c2)):
        nc = c1
        nex = ex1
        pc = c2.add_years(-1)
    else:
        nc = c2
        nex = ex2
        pc = c1.add_years(-1)
    
    if (settlement.days_between(nex)) <= 0:
        exflag = 0
    else:
        exflag = 1
    
    c2go = round(2*(nc.days_between(mature))/365.25, 0)
    
    coupfrac = (c2go + (float)(settlement.days_between(nc))/(pc.days_between(nc)))
    
      
    if c2go >= 1:
        dfy_ur = 100 / ((1 + yld / 200) ** coupfrac) + coupon / 2 * ((1 + yld / 200) ** (c2go + exflag) - 1) / (yld / 200 * ((1 + yld / 200) ** coupfrac))
    
    else: 
        dfy_ur = (100 + coupon / 2 * exflag) / (1 + (settlement.days_between(nc)) / 36500 * yld)
    
    return dfy_ur


def bond_deriv(ins, settlement, yld):
    
    
    ain_up = dirty_from_yield_ur(ins, settlement, yld + 0.00001)
    ain_down = dirty_from_yield_ur(ins, settlement, yld - 0.00001)
    bd = (ain_up - ain_down)/ (0.00002) 
    return bd
  


def bond_iyl(ins, price, settlement):
    oyld = 12.0
    
    for i in range(4):
       oyld = oyld - (ins.dirty_from_yield(settlement, None, None, oyld) - price) / bond_deriv(ins, settlement, oyld)
       
    return round(oyld, 5)
