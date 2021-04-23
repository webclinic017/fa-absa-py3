
#Date:                   2010-04-07

#Purpose:                Asian Performance Options valuations

#Department and Desk:    FO Equities

#Requester:              Andrey Chechin

#Developer:              Zaakirah kajee, Stephen Zoio, Paul Jacot-Guillarmod, Jan Sinkora

#CR Number:              275496, 517213, 527888, 550450, 1936380



import acm, ael, time, zak_funcs, sys
from math import *
C_P = {1:1, 0:-1}

# ========================================================
#       Asian Performance Options
#                                     Zaakirah Kajee
# ========================================================



class AsianPerformance:
    def __init__(
                self,
                valuationDate,
                instrumentOid,
                instrumentPayDayOffset,
                instrumentAsianInWeight,
                underlyingCurrency,
                underlyingSpotBankingDaysOffset,
                underlyingSpotPrice,
                discountCurve,
                repoCurve,
                volatilityInformation,
                exoticEvents,
                dividends,
                exoticPayDates,
                spotDate,
                payDate,
                isCallPut,
                vola):

        df = self.get_df(valuationDate, discountCurve, payDate)

        try:
            alpha = instrumentAsianInWeight
        except:
            raise Exception('No Weighting factor specified for Asian Performance Option')
        isCall = C_P[isCallPut]

        fixedUnderlyingSpotPrice = self.getFixedUnderlyingSpotPrice(instrumentOid)

        priceDates = self.get_forwards(valuationDate, underlyingSpotPrice, repoCurve, spotDate, exoticPayDates, dividends, exoticEvents, 'Average price', fixedUnderlyingSpotPrice)
        strikeDates = self.get_forwards(valuationDate, underlyingSpotPrice, repoCurve, spotDate, exoticPayDates, dividends, exoticEvents, 'Average strike', fixedUnderlyingSpotPrice)
        obs_S, priceAvgSoFar = self.avg_so_far(priceDates, )
        obs_K, strikeAvgSoFar = self.avg_so_far(strikeDates)
        unobs_S = len(priceDates) - obs_S
        moment1_S = self.moment1(priceDates)
        moment1_K = self.moment1(strikeDates)
        mod_strike, w1_K, w1_S = self.mod_strike(obs_K, obs_S, strikeDates, priceDates, strikeAvgSoFar, moment1_K, alpha)
        self.strike_only=self.mod_strike(obs_K, obs_S, strikeDates, priceDates, strikeAvgSoFar, moment1_K, alpha)
        volmap = self.getVols(valuationDate, instrumentOid, exoticEvents, mod_strike, volatilityInformation)
        volmapStrike = [[x[0], x[1]] for x in volmap['Average strike']]
        volmapStrike.sort()
        volmapPrice = [[x[0], x[1]] for x in volmap['Average price']]
        volmapPrice.sort()
        self.checkVolDates(strikeDates, volmapStrike)
        self.checkVolDates(priceDates, volmapPrice)
        moment2_S = self.moment2(valuationDate, priceDates, volmapPrice)
        moment2_K = self.moment2(valuationDate, strikeDates, volmapStrike)
        aPrime_K = w1_K * strikeAvgSoFar
        aPrime_S = w1_S * priceAvgSoFar
        moment3 = self.moment3(valuationDate, strikeDates, priceDates, volmapStrike)
        m_S =  self.M(moment1_S, moment2_S)
        m_K =  self.M(moment1_K, moment2_K)
        v_K = self.V(moment1_K, moment2_K)
        v_S = self.V(moment1_S, moment2_S)
        rho = self.rho(v_K, v_S, moment3, moment1_S, moment1_K)
        kstar = self.kStar(priceDates, unobs_S, mod_strike, priceAvgSoFar)
        self.result = self.asianTheor(obs_K, strikeDates, kstar, m_S, v_S, isCall, df, strikeAvgSoFar, rho, alpha, aPrime_S, aPrime_K, m_K, v_K)

    def checkVolDates(self, dates, volmap):
        if len(dates) <> len(volmap):
            raise Exception('Volmap has invalid number of dates')
        for i in range(len(dates)):
            if acm.Time.DateDifference(dates[i][0], volmap[i][0]) <> 0:
                raise Exception('Volmap has invalid date')

    def getFixedUnderlyingSpotPrice(self, instrumentOid):
        instrument = acm.FInstrument[instrumentOid]
        underlying = instrument.Underlying()
        underlyingPrice = acm.GetCalculatedValueFromString(underlying, acm.GetDefaultContext(), "marketPrice", None).Value().Number()
        return underlyingPrice

    def pp(self):
        for method in dir(self):
            print method, ' = ', eval('self.'+method)

    def get_df(self, valuationDate, discountCurve, payDate):
        intRate = discountCurve.Rate(valuationDate, payDate)
        timetocarry = acm.Time.DateDifference(payDate, valuationDate) / 365.0
        return exp(-timetocarry * intRate)

    def get_forwards(self, valuationDate, underlyingSpotPrice, repoCurve, spotDate, exoticPayDates, dividends, exoticEvents, type, fixedUnderlyingSpotPrice):
        dates = []
        i = 0

        while i < exoticEvents.Size():
            e = exoticEvents.At(i)
            if e.Type() == type:
                d = e.Date()
                if acm.Time.DateDifference(d, valuationDate) >= 0 or (valuationDate > acm.Time().DateToday() and d >= acm.Time().DateToday()):
                    dividendsForEvent = dividends.At(e)
                    payDate = exoticPayDates.At(e)
                    divpv = repoCurve.DiscountValues(dividendsForEvent, spotDate).Number()
                    carrycost = repoCurve.Rate(spotDate, payDate)
                    timetocarry = acm.Time.DateDifference(payDate, spotDate)/365.0

                    certain = (d == valuationDate) and (e.EventValue() > 0)

                    if valuationDate > acm.Time().DateToday() and d < valuationDate:
                        certain = True
                        underlyingSpotPriceForEvent = fixedUnderlyingSpotPrice
                    else:
                        underlyingSpotPriceForEvent = underlyingSpotPrice

                    if d == acm.Time().DateToday():
                        certain = True

                    val = (underlyingSpotPriceForEvent - divpv)*exp(timetocarry*carrycost)

                    dates.append([d, val, e.EventValue(), certain])
                    if e.EventValue() > 0:
                        ael.log('Future Averaging Date has already been fixed')
                else:
                    if e.EventValue() < 0:
                        dates.append([d, e.EventValue(), e.EventValue(), False])
                        raise Exception('Historical Averaging Date missing a fixing')
                    else:
                        dates.append([d, e.EventValue(), e.EventValue(), True])
            i = i + 1
        dates.sort()
        return dates

    def avg_so_far(self, dates):
        y = [x[1] for x in dates if not self.uncertain(x)]
        n= len(y)
        s = sum(y)
        if n == 0:
            return 0, 0
        else:
            return n, float(s)/n

    def moment1(self, dates):
        y = [x[1] for x in dates if self.uncertain(x)]
        n = len(dates)
        s = sum(y)
        if n == 0:
            return 0
        return float(s)/n

    def moment2(self, valuationDate, dates, volmap):
        n = len(dates)
        s0 = s1 = 0
        for i, x in enumerate(dates):
            if self.uncertain(x):
                T = acm.Time.DateDifference(x[0], valuationDate)/365.0
                vol = volmap[i][1]
                s0 += x[1]*x[1]*exp(pow(vol, 2)*T)
        s0 = (1.0/(n*n))*s0
        for j, datej in enumerate(dates):
            if self.uncertain(datej):
                for i in range(j):
                    if self.uncertain(dates[i]):
                        T = acm.Time.DateDifference(dates[i][0], valuationDate)/365.0
                        vol = volmap[i][1]
                        s1 +=  datej[1]*dates[i][1]*exp(pow(vol, 2)*T)
        s1 = 2.0/(n*n)*s1
        return s1+s0

    def moment3(self, valuationDate, strikeDates, priceDates, volmapStrike):
        s1 = 0
        for i, strikeDates_i  in enumerate(strikeDates):
            if self.uncertain(strikeDates_i):
                for j, priceDates_j in enumerate(priceDates):
                    if self.uncertain(priceDates_j):
                        T = acm.Time.DateDifference(strikeDates_i[0], valuationDate)/365.0
                        vol = volmapStrike[i][1]
                        s1 += strikeDates_i[1]*priceDates_j[1]*exp(pow(vol, 2)*T)
        return (1.0/(len(strikeDates)*len(priceDates)))*s1

    def M(self, m1, m2):
        if m1 == 0.0 or m2 == 0.0:
            return 0.0
        return 2.0*log(m1) - 0.5*log(m2)

    def V(self, m1, m2):
        if m1 == 0.0 or m2 == 0.0:
            return 0.0
        return sqrt(log(m2) - 2.0*log(m1))

    def rho(self, v_K, v_S, moment3, moment1_S, moment1_K):
        if v_K ==0:
            return 0.0
        return log(moment3/(moment1_S*moment1_K))/(v_S*v_K)

    def phi(self, x, aPrime_K, m_K, v_K):
        return aPrime_K + exp(m_K + v_K * x)

    def logarg(self, x, alpha, aPrime_S, aPrime_K, m_K, v_K):
        return alpha*self.phi(x, aPrime_K, m_K, v_K) - aPrime_S

    def d1(self, logargx, m_S, v_S):
        return (log(logargx,) - m_S)/v_S

    def A(self, x, rho, call, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K):
        logargx = self.logarg(x, alpha, aPrime_S, aPrime_K, m_K, v_K)
        if logargx <= 0.0:
            NA = 1
        else:
            rhoCompSq = 1- rho*rho
            NA = ael.normal_dist(call*(rho*x - self.d1(logargx, m_S, v_S)) / sqrt(rhoCompSq) )
        return NA * (alpha - aPrime_S / self.phi(x, aPrime_K, m_K, v_K))

    def B(self, x, rho, call, v_S, m_S, alpha, aPrime_S, aPrime_K, m_K, v_K):
        logargx = self.logarg(x, alpha, aPrime_S, aPrime_K, m_K, v_K)

        rhoCompSq = 1- rho * rho
        if logargx <= 0.0:
            NB = 1
        else:
            NB = ael.normal_dist(call*(rho*x + v_S*rhoCompSq - self.d1(logargx, m_S, v_S)) / sqrt(rhoCompSq) )
        return NB * exp(m_S + v_S * v_S * rhoCompSq * 0.5 + rho * v_S * x) / self.phi(x, aPrime_K, m_K, v_K)

    def f(self, x, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K):
        return df * call* (self.B(x, rho, call, v_S, m_S, alpha, aPrime_S, aPrime_K, m_K, v_K)-self.A(x, rho, call, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K))* exp(-0.5*pow(x, 2))/sqrt(2*pi)

    def theor_DA(self, n, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K):
        s = 0.0
        b = 7.0
        a = -7.0
        for k in range(1, n):
            x = a + k*(b-a)/n
            s = s + self.f(x, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K)
        s = ((b-a)/n)*(0.5*(self.f(a, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K) + self.f(b, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K)) + s)
        return s

    def kStar(self, priceDates, unobs_S, mod_strike, priceAvgSoFar):
        t1 = len(priceDates) - unobs_S
        return mod_strike - float(t1)/len(priceDates)* priceAvgSoFar

    def theor_BA(self, v_S, v_K, rho, m_S, m_K, alpha, call, df):
        VT = sqrt(v_S*v_S + v_K*v_K- 2*rho*v_S*v_K)
        d1 = (m_S - m_K + 0.5*(pow(v_S, 2) -pow(v_K, 2)) + 0.5*pow(VT, 2) - log(alpha))/VT
        d2 = d1 - VT

        return (exp(m_S - m_K + 0.5*pow(VT, 2))*ael.normal_dist(call*d1) - alpha*ael.normal_dist(call*d2))*call*df

    def theor_AA(self, kstar, m_S, v_S, call, df, strikeAvgSoFar):
        kstar = kstar
        if kstar > 0:
            d2 = (m_S - log(kstar))/v_S
            d1 = d2 + v_S
            return df*call*(exp(m_S + 0.5*v_S*v_S)*ael.normal_dist(call*d1) - kstar*ael.normal_dist(call*d2))/strikeAvgSoFar
        else:
            return  df*call*(exp(m_S + 0.5*v_S*v_S) - kstar)/strikeAvgSoFar

    def mod_strike(self, obs_K, obs_S, strikeDates, priceDates, strikeAvgSoFar, moment1_K, alpha):

        wk = obs_K / float(len(strikeDates))
        ws = obs_S / float(len(priceDates))
        k = (wk*strikeAvgSoFar + moment1_K)*alpha

        return k, wk, ws

    def asianTheor(self, obs_K, strikeDates, kstar, m_S, v_S, call, df, strikeAvgSoFar, rho, alpha, aPrime_S, aPrime_K, m_K, v_K):

        if obs_K == 0:
            return self.theor_BA(v_S, v_K, rho, m_S, m_K, alpha, call, df)
        elif obs_K < len(strikeDates):
            return self.theor_DA(1000, df, call, rho, alpha, aPrime_S, m_S, v_S, aPrime_K, m_K, v_K)
        else:
            theor = self.theor_AA(kstar, m_S, v_S, call, df, strikeAvgSoFar)
            return theor
        return Exception('Unable to Value')

    def uncertain(self, x):
            return not(x[3])

    def getVols(self, valuationDate, instrumentOid, exoticEvents, strikePrice, volatilityInformation):
        expiryDate = acm.FInstrument[930054].ExpiryDate()
        v = acm.FDictionary()
        v['Average strike'] = acm.FArray()
        v['Average price'] = acm.FArray()
        #[v[x.Type()].Add([x.Date(), volatilityStructure.GetVolatilityValue(0,  acm.Time.DateDifference(x.Date(), valuationDate)/365.0, strikePrice , 1, instrumentOid, 0.0, 1, 0, [])]) for x in exoticEvents]
        for x in exoticEvents:
       		v[x.Type()].Add([x.Date(), volatilityInformation.Value(0, x.Date(), strikePrice, 1, 0)])


        return v


    def Result(self):
        return self.result


def theor(  valuationDate,
            instrumentOid,
            instrumentPayDayOffset,
            instrumentAsianInWeight,
            instrumentCurrency,
            instrumentSpotOrStartDate,
            underlyingCurrency,
            underlyingSpotBankingDaysOffset,
            underlyingSpotPrice,
            discountCurve,
            repoCurve,
            volatilityInformation,
            exoticEvents,
            dividends,
            exoticPayDates,
            spotDate,
            payDate,
            isCall,
            vola):

    ap = AsianPerformance(
            valuationDate,
            instrumentOid,
            instrumentPayDayOffset,
            instrumentAsianInWeight,
            underlyingCurrency,
            underlyingSpotBankingDaysOffset,
            underlyingSpotPrice.Number(),
            discountCurve,
            repoCurve,
            volatilityInformation,
            exoticEvents,
            dividends,
            exoticPayDates,
            spotDate,
            payDate,
            isCall,
            vola)

    v = ap.Result()

    res = acm.DenominatedValue(v, instrumentCurrency, instrumentSpotOrStartDate)
    return {'result':res}


def get_strike(  valuationDate,
            instrumentOid,
            instrumentPayDayOffset,
            instrumentAsianInWeight,
            underlyingCurrency,
            underlyingSpotBankingDaysOffset,
            underlyingSpotPrice,
            discountCurve,
            repoCurve,
            volatilityInformation,
            exoticEvents,
            dividends,
            exoticPayDates,
            spotDate,
            payDate,
            isCall):
    ap = AsianPerformance(
            valuationDate,
            instrumentOid,
            instrumentPayDayOffset,
            instrumentAsianInWeight,
            underlyingCurrency,
            underlyingSpotBankingDaysOffset,
            underlyingSpotPrice.Number(),
            discountCurve,
            repoCurve,
            volatilityInformation,
            exoticEvents,
            dividends,
            exoticPayDates,
            spotDate,
            payDate,
            isCall,
            0)
    return ap.strike_only[0]


def get_asql_strike(ins, *rest):

    i = acm.FInstrument[ins.insid]
    context = acm.GetDefaultContext()
    sheet_type = 'FOrderBookSheet'
    column_id = 'Average Model Strike'

    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)

    modStrike = calc_space.CreateCalculation(i, column_id)

    return  modStrike.Value()


