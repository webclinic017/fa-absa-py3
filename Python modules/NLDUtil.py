# Modified by FA 2009-10-23

import ael, acm, time, string, math

# this function obtains the volatility used by the instrument
def TheVol(instr, expry, strk, *rest): 
    InsName= instr.insid 
    MyVol=instr.used_volatility()
    expiry=ael.date(expry)
    return MyVol.volatility(strk, expiry)

# The function calculates the swap price
def GetFwdCurve(instr):
    for l in instr.legs():
        if l.float_rate:
            return GetFwdCurve(l.float_rate)
    if instr.und_insaddr:
        return GetFwdCurve(instr.und_insaddr)
    return ael.YieldCurve[instr.used_yield_curve().yield_curve_name]
    
def TheFwdRate(instr, Adate1,Adate2,q,*rest):
    yc = GetFwdCurve(instr)
    if not yc:
        return 0
    y=yc.clone()
    y.calculate()
    y.simulate()
    ins=ael.Instrument['ZAR-JIBAR-3M']
    prc=ins.prices()
    for p in prc:
        if p.ptynbr.ptyid == 'SPOT':
            #print p.pp()
            pc=p.clone()
            pc.settle = p.settle + q
            pc.last = p.last + q
            pc.bid = p.bid + q
            pc.ask = p.ask + q
            pc.apply()
    y.calculate()
    y.simulate()
    StartDate=ael.date(Adate1)
    EndDate=ael.date(Adate2)
    yr = y.yc_rate(StartDate, EndDate, 'Quarterly', 'Act/365', 'Par Rate', 0, None, 0)
    pc.revert_apply()
    y.calculate()
    y.simulate()
    return yr
 # the function calculates the delta of cap & floor     
def Blck_Delta(instr,Adate1,Adate2,expry,strk,aFwd,q,*rest):
    vol = TheVol(instr, expry, strk)
    fwd = aFwd+q
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    date1=ael.date(Adate1)
    date2=ael.date(Adate2)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    Mperiod=float(date1.days_between(date2))
    T2=float((Mperiod)/365)
    ERate = float(aFwd/100)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    PV01=-1000000*T2*math.exp(-R*T2)*10**-4
    if T > 0:
           
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T)
            
        if instr.instype == 'Cap':
            D = ael.normal_dist(d1)
            if D>=0.5:
                Reset = PV01
            else:
                Reset = 0
        elif instr.instype == 'Floor':
            D = ael.normal_dist(d1)-1 
            if D<= -0.5:
                Reset = -PV01
            else:
                Reset = 0
        else:
            Fv = 0
            D=0
            Reset = 0
    else:
        if instr.instype == 'Cap':
            s = max(fwd-strk, 0)
            if s >0:
                Reset=PV01
            else:
                Reset = 0
        elif instr.instype == 'Floor':
            s = max(strk-fwd, 0)
            if s>0:
                Reset = -PV01
            else:
                Reset = 0
                
    return Reset
#function calculates the discount factor            
def DiscRate(instr,Adate1,*rest):
    StartDate = ael.date_valueday()
    MyRat = instr.used_yield_curve()
    EndDate = ael.date(Adate1)
    r=MyRat.yc_rate(StartDate, EndDate, 'Continuous', 'Act/365', 'Spot Rate', 0, None, 0)
    Perd = float(StartDate.days_between(EndDate))
    x = float((Perd)/365)
    return math.exp(-r*x)              

def Swaption_Delta(instr,expry,ResStart,ResEnd,EndDate,strk,CallOption,q,*rest):
    vol = TheVol(instr, expry, strk)
    if instr.instype == 'Option':
        fwd = TheFwdRate(instr, expry, EndDate, q)*100
    else:
        pass
    # Black Model parameters    
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    #Reset impact
    
    ERate = TheFwdRate(instr, ResStart, ResEnd, q)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    Start=ael.date(ResStart)
    End = ael.date(ResEnd)
    Dur = float(Start.days_between(End))
    Drtn = float((Dur)/365)
    PV01=-1000000*Drtn*math.exp(-R*Drtn)*10**-4
    
    if T>0:
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T) 
    # Black Delta
        if CallOption == True:
            D = ael.normal_dist(d1) 
            if D >= 0.5:
                Reset=PV01
            else:
                Reset=0
        elif CallOption == False:
            D = ael.normal_dist(d1)-1
            if D <= -0.5:
                Reset=-PV01
            else:
                Reset=0
        else:
            D=0
            Reset=1000000
    else:
        if CallOption == True:
            s = max(fwd-strk, 0)
            if s >0:
                Reset=PV01
            else:
                Reset = 0
        elif CallOption == False:
            s = max(strk-fwd, 0)
            if s>0:
                Reset = -PV01
            else:
                Reset = 0
    return Reset 

def Ex_DeltaCF(instr,Adate1,Adate2,expry,strk,aFwd,q,*rest):
    vol = TheVol(instr, expry, strk)
    fwd = aFwd+q
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    date1=ael.date(Adate1)
    date2=ael.date(Adate2)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    Mperiod=float(date1.days_between(date2))
    T2=float((Mperiod)/365)
    ERate = float(aFwd/100)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    PV01=-1000000*T2*math.exp(-R*T2)*10**-4
    if T > 0:
           
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T)
            
        if instr.instype == 'Cap':
            D = ael.normal_dist(d1)
            Rset = PV01*D            
                
        elif instr.instype == 'Floor':
            D = ael.normal_dist(d1)-1 
            Rset = PV01*D
                            
        else:
            Fv = 0
            D=0
            Rset = 0
    else:
        if instr.instype == 'Cap':
            s = max(fwd-strk, 0)
            if s >0:
                Rset=PV01
            else:
                Rset = 0
        elif instr.instype == 'Floor':
            s = max(strk-fwd, 0)
            if s>0:
                Rset = -PV01
            else:
                Rset = 0
                
    return Rset


'''    
def GetNominal(trd,nom1,nom2,*rest):
    if nom2 == 1:
        result = nom1
    elif nom2 < 1 and nom2 > -1:
        result = (nom1*nom2)
        if result > 1000000 or result < -1000000:
            result=result/1000000
    else:
        result=nom2
        if result > 1000000 or result < -1000000:
            result = nom2/1000000
    return result
'''


def GetNominal(trd,nom1,nom2,*rest):
    result = 0
    if nom2 == 1:
        result = nom1
    elif nom2 < 1 and nom2 > -1:
        result = (nom1*nom2)
        if result > 100000 or result < -100000:
            result=result/1000000
    else:
        if nom2 > 100000 or nom2 < 100000:
            if nom1 < 0 and nom1 > -1:
                result = -1*nom2
            elif nom1 > 0 and nom1 < 1:    
                result = nom2
            else: 
                result = nom2 
            result = result/1000000   
        else: 
            result = nom2
    return result



    
def ExpDelta(instr,expry,ResStart,ResEnd,EndDate,strk,CallOption,q,*rest):
    vol = TheVol(instr, expry, strk)
    if instr.instype == 'Option':
        fwd = TheFwdRate(instr, expry, EndDate, q)*100
    else:
        pass
    # Black Model parameters    
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    
    #Reset impact
    ERate = TheFwdRate(instr, ResStart, ResEnd, q)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    Start=ael.date(ResStart)
    End = ael.date(ResEnd)
    Dur = float(Start.days_between(End))
    Drtn = float((Dur)/365)
    PV01=-1000000*Drtn*math.exp(-R*Drtn)*10**-4
    if T > 0 :
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T)    
        
    # Black Delta
        if CallOption == True:
            D = ael.normal_dist(d1) 
            Reset = PV01*D
               
        elif CallOption == False:
            D = ael.normal_dist(d1)-1
            Reset=PV01*D
        else:
            Reset=0
    else:
        if CallOption == True:
            s = max(fwd-strk, 0)
            if s >0:
                Reset=PV01
            else:
                Reset = 0
        elif CallOption == False:
            s = max(strk-fwd, 0)
            if s>0:
                Reset = -PV01
            else:
                Reset = 0
        
    return Reset     
    
    
    
    
    
def Lin(x):
    r=math.exp(1)
    y=(math.log(x))/(math.log(r))
    return y
    
def FraDelta(instr,ResetStart,ResetEnd,aFwd,payleg,p,*rest):
    Fwd= (aFwd + p)/100
    Start = ael.date(ResetStart)
    End = ael.date(ResetEnd)
    period=float(Start.days_between(End))
    T = float((period)/365)
    e1=math.exp(1)
    R=4*(Lin(1+Fwd/4))/(Lin(e1))
    TPV01=-1000000*T*math.exp(-R*T)*10**-4
    if instr.instype == 'Swap':
        if payleg == True:
            PV01= -TPV01
        else:
            PV01=TPV01        
    else:
        PV01=TPV01        
    return PV01


def Bermudan(instr,expry,ResStart,ResEnd,EndDate,strk,payleg,q,*rest):
    vol = TheVol(instr, expry, strk)
    if instr.instype == 'Option':
        fwd = TheFwdRate(instr, expry, EndDate, q)*100
    else:
        pass
    # Black Model parameters    
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    #Reset impact
    
    ERate = TheFwdRate(instr, ResStart, ResEnd, q)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    Start=ael.date(ResStart)
    End = ael.date(ResEnd)
    Dur = float(Start.days_between(End))
    Drtn = float((Dur)/365)
    PV01=-1000000*Drtn*math.exp(-R*Drtn)*10**-4
    
    if T>0:
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T) 
    # Black Delta
        if payleg == False:
            D = ael.normal_dist(d1) 
            if D >= 0.5:
                Reset=PV01
            else:
                Reset=0
        elif payleg == True:
            D = ael.normal_dist(d1)-1
            if D <= -0.5:
                Reset=-PV01
            else:
                Reset=0
        else:
            D=0
            Reset=1000000
    else:
        if payleg == False:
            s = max(fwd-strk, 0)
            if s >0:
                Reset=PV01
            else:
                Reset = 0
        elif payleg == True:
            s = max(strk-fwd, 0)
            if s>0:
                Reset = -PV01
            else:
                Reset = 0
    return Reset


def ExpBermudan(instr,expry,ResStart,ResEnd,EndDate,strk,payleg,q,*rest):
    vol = TheVol(instr, expry, strk)
    if instr.instype == 'Option':
        fwd = TheFwdRate(instr, expry, EndDate, q)*100
    else:
        pass
    # Black Model parameters    
    t0 = ael.date_valueday()
    expiry=ael.date(expry)
    period=float(t0.days_between(expiry))
    T = float((period)/365)
    
    #Reset impact
    ERate = TheFwdRate(instr, ResStart, ResEnd, q)
    e1=math.exp(1)
    R=4*(Lin(1+ERate/4))/(Lin(e1))
    Start=ael.date(ResStart)
    End = ael.date(ResEnd)
    Dur = float(Start.days_between(End))
    Drtn = float((Dur)/365)
    PV01=-1000000*Drtn*math.exp(-R*Drtn)*10**-4
    if T > 0 :
        d1 = (Lin(fwd/strk)+vol**2*T*0.5)/(vol*math.sqrt(T))
        d2 = d1-vol*math.sqrt(T)    
        
    # Black Delta
        if payleg == False:
            D = ael.normal_dist(d1) 
            Reset = PV01*D
               
        elif payleg == True:
            D = ael.normal_dist(d1)-1
            Reset=PV01*D
        else:
            Reset=0
    else:
        if payleg == False:
            s = max(fwd-strk, 0)
            if s >0:
                Reset=PV01
            else:
                Reset = 0
        elif payleg == True:
            s = max(strk-fwd, 0)
            if s>0:
                Reset = -PV01
            else:
                Reset = 0
        
    return Reset 
        
def get_res(instr,*rest):
    res=[]
    t0 = ael.date_valueday()    
    for l in instr.exercise_events():
        if l.day >=t0:
            res.append(l.day)
    return min(res)
