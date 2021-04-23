import acm, ael, time, zak_funcs
from math import *
from FSEQUtils import *
 	
# ========================================================
#       Asian Performance Options
#                                     Zaakirah Kajee
# ========================================================

global today
today = ael.date_today()
callput = {0: -1, 1:1}

class AsianPerformance:
    def __init__(self,i,undspot,sigma,volmap,flag=1):
        
        ins = ael.Instrument[i.Name()]
        self.Ins = ins
        self.acmIns = i
        self.undSpot = undspot
        self.underlying = ins.und_insaddr
        self.undCurr = ins.und_insaddr.curr
        
        self.call = callput[ins.call_option]
        offset = ins.und_insaddr.spot_banking_days_offset
        spotd = today.add_banking_day(ins.curr, offset)
        self.Offset = offset
        self.spotDays = spotd
        self.POffset =ins.pay_day_offset
        self.df = self.get_df()
        
        try: 
            self.alpha = float(ins.add_info('AsianInWeight'))
        except:
            raise AsianError('No Weighting factor specified for Asian Performance Option')
            
        self.PriceDates = self.get_forwards('Average price') 
        self.StrikeDates = self.get_forwards('Average strike') 
        self.obs_S, self.PriceAvgSoFar = self.avg_so_far('PriceDates')
        self.obs_K, self.StrikeAvgSoFar = self.avg_so_far('StrikeDates')
        self.unobs_S, self.Moment1_S = self.moment1('PriceDates')
        self.unobs_K, self.Moment1_K = self.moment1('StrikeDates')
        self.mod_strike, self.w1_K, self.w1_S = self.mod_strike()
        if flag != 1:
            self.sigma = sigma
            self.volmapStrike = [[x[0], x[1]] for x in volmap['Average strike']]
            self.volmapStrike.sort()
            self.volmapPrice = [[x[0], x[1]] for x in volmap['Average price']]
            self.volmapPrice.sort()
            self.checkVolDates(self.StrikeDates, self.volmapStrike)
            self.checkVolDates(self.PriceDates, self.volmapPrice)
            self.Moment2_S = self.moment2(self.PriceDates, self.volmapPrice, self.unobs_S)
            self.Moment2_K = self.moment2(self.StrikeDates, self.volmapStrike, self.unobs_K)
            self.APrime_K = self.w1_K*self.StrikeAvgSoFar
            self.APrime_S = self.w1_S*self.PriceAvgSoFar
            self.Moment3 = self.moment3()
            self.M_S=  self.M(self.Moment1_S, self.Moment2_S)
            self.M_K=  self.M(self.Moment1_K, self.Moment2_K)
            self.V_K = self.V(self.Moment1_K, self.Moment2_K)
            self.V_S = self.V(self.Moment1_S, self.Moment2_S)
            self.rho = self.rho()
            self.kstar = self.KStar()
           
    def checkVolDates(self, dates, volmap):
        
        if len(dates) <> len(volmap):
            raise AsianError('Volmap has invalid number of dates')
        for i in range(len(dates)):
            if dates[i][0] <> volmap[i][0]:
                raise AsianError('Volmap has invalid date')
            
    def pp(self):
        for method in dir(self):
            print method, ' = ', eval('self.'+method)
        
    def get_df(ap):
        discountCurve = ap.acmIns.MappedDiscountCurve().Parameter()
        payd = ael.date(ap.acmIns.ExpiryDateOnly()).add_banking_day(ap.Ins.curr, ap.POffset)
        intRate = discountCurve.Rate(today, payd)
        timetocarry = today.days_between(payd)/365.0
        return exp(-timetocarry*intRate)        
        
    def get_forwards(ap, type):
        dates = []        
        repo = ap.acmIns.MappedRepoCurve().Parameter()

        for e in ap.acmIns.ExoticEvents():
            if e.Type() == type:
                d = ael.date(e.Date())
                if d >= today:
                    payd = ael.date(e.Date()).add_banking_day(ap.Ins.curr, ap.Offset)
                    divo= ap.acmIns.Underlying().DividendTable(e.Date())
                    divpv = ap.acmIns.Underlying().DividendPV(divo, today, ap.spotDays, e.Date(), repo, 1)
                    carrycost = repo.Rate(ap.spotDays, payd)
                    timetocarry = ap.spotDays.days_between(payd)/365.0
                    val = (ap.undSpot - divpv)*exp(timetocarry*carrycost)
                    certain = (d == today) and (e.EventValue() > 0)
                    dates.append([d, val, e.EventValue(), certain])
                    if e.EventValue() > 0:
                        ael.log('Future Averaging Date has already been fixed')
                else:
                    if e.EventValue() < 0:
                        dates.append([d, e.EventValue(), e.EventValue(), False])
                        raise AsianError('Historical Averaging Date missing a fixing')
                    else:
                        dates.append([d, e.EventValue(), e.EventValue(), True])
        dates.sort()
        return dates
    
       
    def avg_so_far(ap, type):
        dates = eval('ap.' + type)
        y = [x[1] for x in dates if not ap.uncertain(x)]
        n= len(y)
        s = sum(y)
            
        if n == 0: 
            return 0, 0
        else:       
            return n, float(s)/n
        
    
    def moment1(ap, type):
        dates = eval('ap.' + type)
        y = [x[1] for x in dates if ap.uncertain(x)]
        n = len(dates)
        s = sum(y)
        if n == 0:
            return 0, 0
        return n, float(s)/n
        
      
    def moment2(ap, dates, volmap, n):
        if n == 0:
            return 0
        
        s0 = s1 = 0
        for i, x in enumerate(dates):
            if ap.uncertain(x):
                T = today.days_between(x[0])/365.0
                vol = volmap[i][1] 
                s0 += x[1]*x[1]*exp(pow(vol, 2)*T)
        
        s0 = (1.0/(n*n))*s0
               
        for j, datej in enumerate(dates):
            if ap.uncertain(datej):
                for i in range(j):
                    if ap.uncertain(dates[i]):
                        T = today.days_between(dates[i][0])/365.0
                        vol = volmap[i][1] 
                        s1 +=  datej[1]*dates[i][1]*exp(pow(vol, 2)*T)
              
        s1 = 2.0/(n*n)*s1
        return s1+s0
    
        
    def moment3(ap):
        if ap.unobs_K == 0:
            return 0
        
        s1 = 0
        for i, StrikeDates_i  in enumerate(ap.StrikeDates):
            if ap.uncertain(StrikeDates_i):
                for j, PriceDates_j in enumerate(ap.PriceDates):
                    if ap.uncertain(PriceDates_j):
                        T = today.years_between(StrikeDates_i[0])
                        vol = ap.volmapStrike[i][1] 
                        s1 += StrikeDates_i[1]*PriceDates_j[1]*exp(pow(vol, 2)*T)
                        
        return (1.0/(ap.unobs_K*ap.unobs_S))*s1
    
    
    def M(ap, m1, m2):
        
        if m1 == 0.0 or m2 == 0.0:
            return 0.0
        return 2.0*log(m1) - 0.5*log(m2)
        
    def V(ap, m1, m2):
        if m1 == 0.0 or m2 == 0.0:
            return 0.0
        return sqrt(log(m2) - 2.0*log(m1))
    
    def rho(ap):
        if ap.V_K ==0:
            return 0.0
        return log(ap.Moment3/(ap.Moment1_S*ap.Moment1_K))/(ap.V_S*ap.V_K)

   
    def phi(ap, x):
        return ap.APrime_K + exp(ap.M_K + ap.V_K*x)
    
    def logarg(ap, x):
        return ap.alpha*ap.phi(x) - ap.APrime_S
        
    def d1(ap, x):
        return (log(ap.logarg(x)) - ap.M_S)/ap.V_S
    
    def A(self, x):
        logargx = self.logarg(x)
        if logargx <= 0.0:
            NA = 1 
        else:
            rhoCompSq = 1- self.rho*self.rho
            NA = ael.normal_dist(self.call*(self.rho*x - self.d1(x)) / sqrt(rhoCompSq) )
        return NA * (self.alpha - self.APrime_S / self.phi(x))
        
    def B(self, x):
        logargx = self.logarg(x)
        
        rhoCompSq = 1- self.rho*self.rho
        if logargx <= 0.0:
            NB = 1 
        else:
            NB = ael.normal_dist(self.call*(self.rho*x + self.V_S*rhoCompSq - self.d1(x)) / sqrt(rhoCompSq) )
        return NB * exp(self.M_S + self.V_S * self.V_S * rhoCompSq * 0.5 + self.rho * self.V_S * x) / self.phi(x)
        
    def f(self, x):
        return self.df * self.call* (self.B(x)-self.A(x))* exp(-0.5*pow(x, 2))/sqrt(2*pi)
        
    # Theoretical price during averaging
    def theor_DA(self, n):
        s = 0.0
        b = 7.0
        a = -7.0
        for k in range(1, n):
            x = a + k*(b-a)/n
            s = s + self.f(x)
        s = ((b-a)/n)*(0.5*(self.f(a) + self.f(b)) + s)
        return s
     
    def KStar(ap):
        
        t1 = len(ap.PriceDates) - ap.unobs_S
        return (( ap.unobs_S + t1)/ ap.unobs_S)*ap.mod_strike - (t1/ ap.unobs_S)*ap.PriceAvgSoFar
    
    def theor_BA(ap):
        VT = sqrt(ap.V_S*ap.V_S + ap.V_K*ap.V_K- 2*ap.rho*ap.V_S*ap.V_K)
        d1 = (ap.M_S - ap.M_K + 0.5*(pow(ap.V_S, 2) -pow(ap.V_K, 2)) + 0.5*pow(VT, 2) - log(ap.alpha))/VT
        d2 = d1 - VT
        return (exp(ap.M_S - ap.M_K + 0.5*pow(VT, 2))*ael.normal_dist(ap.call*d1) - ap.alpha*ael.normal_dist(ap.call*d2))*ap.call*ap.df
    
    def theor_AA(ap):
        kstar = ap.kstar
        if kstar > 0:
            d1 = (log(exp(ap.M_S + 0.5*ap.V_S*ap.V_S)/kstar))/ap.V_S  + 0.5*ap.V_S
            d2 = d1 - ap.V_S
            return ap.df*ap.call*(exp(ap.M_S + 0.5*ap.V_S*ap.V_S)*ael.normal_dist(ap.call*d1) - kstar*ael.normal_dist(ap.call*d2))/ap.StrikeAvgSoFar
        else:
            return  ap.df*ap.call*(exp(ap.M_S + 0.5*ap.V_S*ap.V_S) - kstar)/ap.StrikeAvgSoFar
    
    def mod_strike(ap):
        
        wk =ap.obs_K / float(len(ap.StrikeDates))
        ws = ap.obs_S / float(len(ap.PriceDates))
        k = (wk*ap.StrikeAvgSoFar + ap.Moment1_K)*ap.alpha
        
        return k, wk, ws
        
    def AsianTheor(ap):
        if ap.obs_K == 0:
            return ap.theor_BA()
        elif ap.obs_K < len(ap.StrikeDates):
            return ap.theor_DA(1000)
        else:
            return ap.theor_AA()
        return AsianError('Unable to Value')
        
    def uncertain(ap, x):
            return not(x[3])
        
       
def get_vols(ins, undspot, strike,bump=0):
    volstr = ins.MappedVolatilityStructure().Parameter()
    v = acm.FDictionary()
    v.AtPut('Average strike', acm.FArray().Add([]))
    v.AtPut('Average price', acm.FArray().Add([]))
    [v[x.Type()].Add([ael.date(x.Date()), bump + volstr.GetVolatilityValue(0, today.days_between(ael.date(x.Date())) / 365.0, strike, 1, ins.Oid(), 0.0, 1)]) for x in ins.ExoticEvents()]
    return v

        
def theor(i2, undspot, sigma, vol_map):
   
    ap = AsianPerformance(i2, undspot, sigma, vol_map, 0)
    v = ap.AsianTheor()
    
    delta = "AsianPDelta"
    gamma = "AsianPGamma"
    theta = "numericalTheta"
    vega      = "asianPVega"
    return {"PV": v, "Delta":delta, "Gamma":gamma, "Theta":theta, "Vega":vega}

   
def get_mod_strike(ins, undspot):
    ap = AsianPerformance(ins, undspot, 0, [[], []])
    return ap.mod_strike

def get_asql_strike(i, *rest):
    ins = acm.FInstrument[i.insid]
    undspot= zak_funcs.get_undspot(i)
    return get_mod_strike(ins, undspot)
