""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqAverageAnalytic - Analytic valuation of average options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    The module calculates the theoretical price of an average option, where the 
    average is arithmetic or geometric. Both fix and floating strike are handled.
    The methods are based on moment matching.

NOTE            
    FEqAverageAnalytic does not handle the floating geometric average option. 
    Only European options are handled.

EXTERNAL DEPENDENCIES
    FEqAverage      Main function, Theor().

REFERENCES      
    Levy, Edmond. "Pricing European average currency options", 
    Journal of International Money and Finance, no.11, pg.474-491, 1992.
        
    Nelken, Israel. "The Handbook of Exotic options", 
    Irwin Porfessional Book team, 1996.
    
    Margrabe, William. "The Value of an Option to Exchange One Asset for Another",
    Journal of Finance, vol.33, pg.177-186, March, 1978.
    
    Hull, John. Options. "Futures, and Other Derivatives". Prentice Hall, 
    Third Edition, 1997.

    Kemna, A. and Vorst. A. "A Pricing Method for Options Based on Average Asset 
    Values". Journal of Banking and Finance, no.14, pg.113-29, March, 1990. 

 ----------------------------------------------------------------------------"""
import __builtin__
tmp_imp = __builtin__.__import__
import ael

import sys
import FEqAverage 
import FEqAverageUtils
import math 

eps=2.2204e-016

AVERAGE_PUT=0;AVERAGE_CALL=1
AVERAGE_EUR=0;AVERAGE_AME=1
AVERAGE_FIX=0;AVERAGE_FLOAT=1
AVERAGE_ARITH=0;AVERAGE_GEOM=1;AVERAGE_HARM=2
F_AVERAGE_EXCEPT = 'AverageException' # This exception is thrown by all average routines

class AverageAnalytic:
    def __init__(self, average_params):
        self.ap = average_params
        if self.ap.avg_type==AVERAGE_HARM:
            raise F_AVERAGE_EXCEPT, 'This method only handles arithmetic and geometric averages, not harmonic.'
        if self.ap.price==0: 
            raise F_AVERAGE_EXCEPT, 'No price is set for the underlying instrument.'
        
        # A vector with future sample dates.
        self.Ti=[]                                    
        for avg_date in self.ap.avg_dates:
            if 0 <= avg_date <= self.ap.texp:
                self.Ti.append(avg_date)
            # The expiry date in PRIME is decreasing during the day.
            # The following condition makes sure that also the 
            # avg_date on expiry is taken into account.
            # 0.0027 is approximately 24 hours.
            elif 0 < avg_date - self.ap.texp < 0.0027:
                self.Ti.append(avg_date)
        
        self.check = 0
        if len(self.Ti) == 0: self.check = 1
        
        # Dividend handling
        D_dates=[];D_vals=[]
        self.ap.dividends.sort()
        for dividend in self.ap.dividends:
            if dividend[1]>0: 
                D_dates.append(dividend[1])
                D_vals.append(dividend[0])    
        D=[]
        for avg_date in self.Ti:
            Dt=0
            for i in range(len(D_dates)):
                if avg_date < D_dates[i]:
                    Dt = Dt + D_vals[i]*math.exp(-self.ap.rate*(D_dates[i]-avg_date))
            D.append(Dt)
        
        if D != []:
            self.avg_divs = FEqAverageUtils.average(D, self.ap.avg_type)
        else: self.avg_divs = 0
        
        D0=0
        for i in range(len(D_dates)):
            D0 = D0 + D_vals[i]*math.exp(-self.ap.rate*D_dates[i])

        self.price_arith = self.ap.price - D0
        self.price_geom = self.ap.price
        
        self.ap.avg_dates.sort()
        self.avg_start = self.ap.avg_dates[0]
        
        # Total number of observations during the averaging period.               
        self.N = len(self.ap.avg_dates) 
        self.m = 0
        if self.check == 0:
            while self.ap.avg_dates[self.m] < 0: 
                self.m = self.m+1
                
        if  self.avg_start < 0:
            self.strike = self.N/((self.N - self.m)*1.0)* \
                         (self.ap.strike - self.m/(1.0*self.N)*self.ap.avg_so_far)
        else: self.strike = self.ap.strike
        
              
            
    # The method calculates the discrete first order moment for both periodic 
    # and arbitrary arithmetic average sampling dates.
    def first_moment(self): 
        if len(self.ap.avg_dates) != 1: sum = self.err_sum(self.ap.avg_dates)
        else: sum = [1]

        # NOTE! 0.0013 is the accepted deviation when the period is approximated 
        # to be periodical.This deviation accepts daily averaging even though the 
        # weekends are excluded. The approximation can save time, especially when 
        # the averages are taken on a daily basis.
        # If no deviation is accepted, change 0.0013 to 0.
        if sum[0] < 0.0013: self.dt = sum[1]         
        else: self.dt = 0 
        
        price = self.price_arith
        if self.dt==0:        
            # Calculates the moment for non periodic average sampling.
            P=0
            for avg_time in self.Ti:
                P=P+(math.exp((self.ap.rate-self.ap.cont_div)*avg_time))
            M1 = price/(1.0*(self.N-self.m))*P
            return M1
        else:            
            # Calculates the moment for periodic average sampling.
            if 0 <= self.avg_start:
                if self.ap.cont_div == self.ap.rate:
                    M1 = price
                    return M1
                else:    
                    M1= price/(1.0*self.N)*math.exp((self.ap.rate-self.ap.cont_div) \
                       * self.avg_start)*(1-math.exp((self.ap.rate-self.ap.cont_div) \
                       * self.N * self.dt))/(1-math.exp((self.ap.rate-self.ap.cont_div) * self.dt))
                    return M1    
            else:
                if self.ap.cont_div == self.ap.rate:
                    M1=(self.N-self.m)/(self.N*1.0) * price
                else:
                    tm=self.avg_start+math.floor((-self.avg_start+eps)/(1.0*self.dt))*self.dt
                    shi=(-tm)/(1.0*self.dt)
                    M1 = price/(1.0*(self.N-self.m))*math.exp((self.ap.rate-self.ap.cont_div) \
                       * self.dt*(1-shi))*(1-math.exp((self.ap.rate-self.ap.cont_div)*(self.N-self.m) \
                       * self.dt))/(1.0*(1-math.exp((self.ap.rate-self.ap.cont_div)*self.dt)))
                    return M1


    # second_moment() calculates the discrete second order moment for both periodic and
    # and arbitrary arithmetic average sampling dates.
    def second_moment(self):           
        rate = self.ap.rate
        cont_div = self.ap.cont_div
        vol = self.ap.vol
        price = self.price_arith
        
        if (self.dt == 0) or (rate - cont_div + vol**2 == 0) \
                          or (2*(rate - cont_div) + vol**2 == 0) \
                          or (rate - cont_div == 0):           
            #Calculates the second moment, when the period is not periodic.
            S=0
            for i in range(0, len(self.Ti)):
                for j in range(0, len(self.Ti)):
                    S = S + math.exp((rate - cont_div)*(self.Ti[i] + self.Ti[j]) + \
                        vol**2 * min(self.Ti[i], self.Ti[j]))
            M2 = math.pow(price/((self.N - self.m)*1.0), 2) * S
            return M2
        else:              
            #Calculates the second moment, when the period is periodic.
            if 0 <= self.avg_start:
                a1 =  1 - math.exp((2*(rate - cont_div) + vol**2)*self.N*self.dt)
                b1 = (1 - math.exp((rate - cont_div)*self.dt))* \
                     (1 - math.exp((2*(rate - cont_div) + vol**2)*self.dt))
                B1 = a1/b1

                a2 = math.exp((rate - cont_div)*self.N*self.dt) - \
                     math.exp((2*(rate - cont_div) + vol**2)*self.N*self.dt)
                b2 = (1 - math.exp((rate - cont_div)*self.dt))*\
                     (1 - math.exp((rate - cont_div + vol**2)*self.dt))
                B2 = a2/b2

                a3 = math.exp((rate - cont_div)*self.dt) - \
                     math.exp((rate - cont_div)*self.N*self.dt)
                b3 = (1 - math.exp((rate - cont_div)*self.dt))* \
                     (1 - math.exp((rate - cont_div + vol**2)*self.dt))
                B3 = a3/b3

                a4 = math.exp((2*(rate - cont_div) + vol**2)*self.dt) - \
                     math.exp((2*(rate - cont_div) + vol**2)*self.N*self.dt)
                b4 = (1 - math.exp((rate - cont_div + vol**2)*self.dt))* \
                     (1 - math.exp((2*(rate - cont_div) + vol**2)*self.dt))
                B4 = a4/b4

                B = B1 - B2 + B3 - B4

                M2 = price**2/(1.0*self.N**2)*math.exp((2*(rate - cont_div) + vol**2)*self.avg_start)*B
                return M2

            else:
                tm = self.avg_start + math.floor((-self.avg_start + eps)/(1.0*self.dt))*self.dt
                shi=(-tm)/(1.0*self.dt)

                a1 = math.exp((2*(rate - cont_div) + vol**2)*self.dt) - \
                     math.exp((2*(rate - cont_div) + vol**2)*(self.N - self.m + 1)*self.dt)
                b1 = (1 - math.exp((rate - cont_div)*self.dt))* \
                     (1 - math.exp((2*(rate - cont_div) + vol**2)*self.dt))
                A1 = a1/b1

                a2 = math.exp(((rate - cont_div)*(self.N - self.m + 2) + vol**2)*self.dt) - \
                     math.exp((2*(rate - cont_div) + vol**2)*(self.N - self.m + 1)*self.dt)
                b2 = (1 - math.exp((rate - cont_div)*self.dt))* \
                     (1 - math.exp(((rate - cont_div) + vol**2)*self.dt))
                A2 = a2/b2

                a3 = math.exp((3*(rate - cont_div) + vol**2)*self.dt) - \
                     math.exp(((rate - cont_div)*(self.N - self.m + 2) + vol**2)*self.dt)
                b3 = (1 - math.exp((rate - cont_div)*self.dt))* \
                     (1 - math.exp(((rate - cont_div) + vol**2)*self.dt))
                A3 = a3/b3

                a4 = math.exp(2*self.dt*(2*(rate - cont_div) + vol**2)) - \
                     math.exp((2*(rate - cont_div) + vol**2)*(self.N - self.m + 1)*self.dt)
                b4 = (1 - math.exp(((rate - cont_div) + vol**2)*self.dt))* \
                     (1 - math.exp((2*(rate - cont_div) + vol**2)*self.dt))
                A4 = a4/b4

                A = A1 - A2 + A3 - A4

                M2 = price**2/(1.0*(self.N - self.m)**2)*math.exp(-2*shi*self.dt*(rate - cont_div + 1/2.0*vol**2))*A
                return M2


    # The method performs certain calculations necessary to value the arithmetic
    # average option with fix strike.
    def calculations_fix(self):
        try:
            res = 0
            strike = self.strike - self.avg_divs
            if self.ap.avg_type == AVERAGE_ARITH:  
                # An arithmetic average is chosen.
                
                M1 = self.first_moment()
                # Check if the strike is negative.
                if strike <= 0:            
                    if self.ap.put_call == AVERAGE_PUT: return 0
                    strike = self.ap.strike - (self.N-self.m)/(1.0*self.N)*self.avg_divs
                    res = math.exp(-self.ap.rate*self.ap.texp)* \
                          (self.m/(1.0*self.N)*self.ap.avg_so_far + \
                          (self.N - self.m)/(1.0*self.N)*M1 - strike)
                else:
                    M2 = self.second_moment()
                    diff = math.log(M2) - 2*math.log(M1)
                    if -1e-10 < diff <= 0.0:
                        if self.ap.put_call == AVERAGE_PUT:
                            res = (self.N - self.m)/(1.0*self.N)*\
                                  (math.exp(-self.ap.rate*self.ap.texp)*(M1*(-1) - strike*(-1))) 
                        else:
                            res = (self.N - self.m)/(1.0*self.N)*(math.exp(-self.ap.rate* \
                                   self.ap.texp)*(M1 - strike))
                        return res
                    else: v = math.sqrt(diff)

                    d1 = (0.5*math.log(M2) - math.log(self.strike))/(1.0*v)
                    d2 = d1 - v
                    if self.ap.put_call == AVERAGE_PUT:
                        res = (self.N - self.m)/(1.0*self.N)*(math.exp(-self.ap.rate*self.ap.texp)* \
                              (M1*(ael.normal_dist(d1)-1) - strike*(ael.normal_dist(d2)-1))) 
                    else:
                        res = (self.N - self.m)/(1.0*self.N)*(math.exp(-self.ap.rate*self.ap.texp)* \
                              (M1*ael.normal_dist(d1) - strike*ael.normal_dist(d2)))
            # Geometric average
            else:
                vol_a = self.ap.vol/math.sqrt(3)
                cont_div_a = (self.ap.cont_div+self.ap.vol**2/6.0-self.ap.rate)/2.0
                carry_cost_a = (self.ap.rate - (self.ap.vol**2)/6)/2  
                P=1
                for avg_time in self.Ti:
                    P = P*(math.exp((carry_cost_a-cont_div_a*0.5)*avg_time))

                # Check if the strike is negative.
                if strike <= 0:            
                    strike = self.ap.strike - (self.N-self.m)/(1.0*self.N)*self.avg_divs
                    M1 = self.price_arith* P**(1/(1.0*(self.N - self.m)))
                    if self.ap.put_call == AVERAGE_PUT: return 0
                    res =  math.exp(-self.ap.rate*self.ap.texp)* \
                           (self.m/(1.0*self.N)* self.ap.avg_so_far + \
                           (self.N - self.m)/(1.0*self.N)*M1- strike)
                else:
                    M1 = self.price_geom * P**(1/(1.0*(self.N - self.m)))
                    res = (self.N - self.m)/(1.0*self.N)* \
                          ael.eq_option(M1, self.ap.texp, vol_a, self.ap.rate, carry_cost_a, \
                          self.strike, self.ap.put_call, 0, self.ap.dividends) 
            if res >= 0.0: return res    
            else: 
                print "Average Warning: The result is negative"
                return 0.0
        except F_AVERAGE_EXCEPT, msg:
            print "calculations_fix() ERROR: ", msg
            raise F_AVERAGE_EXCEPT, 'The fix calculations could not be performed.'

    
    # The method performs certain calculations, necessary to value the 
    # arithmetic average option with floating strike.
    def calculations_floating(self):
        try:
            M1 = self.first_moment()
            M2 = self.second_moment()
            # Average at time T.
            AT = (self.m*self.ap.avg_so_far + (self.N - self.m)*M1)/(1.0*self.N)    
            # Squared average at time T.
            AT2 = ((self.m*self.ap.avg_so_far)**2 + M2*(self.N - self.m)**2 + \
                  2*self.m*(self.N - self.m)*self.ap.avg_so_far*M1)/(1.0*self.N**2)
            ST = self.ap.price*math.exp((self.ap.rate - self.ap.cont_div)*self.ap.texp)
            S=0
            for i in range(0, len(self.Ti)):
                S = S + math.exp((self.ap.rate - self.ap.cont_div)* \
                        (self.ap.texp + self.Ti[i]) + self.ap.vol**2*self.Ti[i])

            a = self.m/(1.0*self.N)*self.ap.avg_so_far*ST
            
            # The expectation of S(T)*A(T)
            SA = a + self.ap.price**2/(1.0*self.N)*S        
            
            # Parameters in the Margrabe problem.
            diff = math.log(AT2) - 2*math.log(AT)

            if 0 > diff > - 1e-10:
                u = 0
            else:
                u = math.sqrt(math.log(AT2) - 2*math.log(AT))    
            
            w = self.ap.vol*math.sqrt(self.ap.texp)
            x = 2*math.log(AT) - 0.5*math.log(AT2)

            y = math.log(self.ap.price) + (self.ap.rate - self.ap.cont_div \
                - 0.5*self.ap.vol**2)*self.ap.texp

            if self.ap.put_call == AVERAGE_CALL:
                v1 = u;  v2 = w
                a1 = x;  a2 = y
                x1 = AT; x2 = ST
            else:
                v1 = w;  v2 = u
                a1 = y;  a2 = x
                x1 = ST; x2 = AT

            # v1*v2*rho, the correlation factor
            rho = math.log(SA) - (a1 + a2) - 0.5*(v1**2 + v2**2)    
            v = v1**2 - 2*rho + v2**2

            d1 = (math.log(x1/(1.0*x2)) + 0.5*v)/(1.0*math.sqrt(v))    
            d2 = d1 - math.sqrt(v)

            res = math.exp(-self.ap.rate*self.ap.texp)*(x1*ael.normal_dist(d1) \
                                                      - x2*ael.normal_dist(d2))
            return res
        except F_AVERAGE_EXCEPT, msg:
            print "calculations_floating() ERROR: ", msg
            raise F_AVERAGE_EXCEPT, 'The floating calculations could not be performed.'

    
    # The method returns the smallest difference between vector items in sequence.
    # E.g: [1 2 5 10] => Returns (2-1)= 1, since 1 < (5-2)=3 < (10-5)=5.
    def min_diff_list(self, T):
        return min(map(lambda x, y:x-y, T[1:], T[:len(T)-1]))
    
    # The method returns the total sum of the squared difference between the correct 
    # step size and the approximated periodic timestep. If the sum is small ( -> 0) 
    # the approximation is good.
    def err_sum_calc(self, dt, T):
        i = 0;sum1 = 0
        while i <= (len(T)-2):
            tmp2 = T[i+1]-T[i]
            sum1 = sum1 + (dt - tmp2)*(dt - tmp2)
            i = i + 1
        return 1/(1.0*(T[len(T)-1] - T[0])*(T[len(T)-1] - T[0]))*sum1
        
    # The method checks if an arbitry vector can be considered to be periodic. If so, 
    # the function returns the time step.
    def err_sum(self, T):                         
        # Checks if the averages are taken periodically.
        T.sort()
        dt1 = (T[len(T)-1] - T[0])/(1.0*(len(T)-1))    
        # If the averages are approximated to be taken periodically, this is the error.
        err_sum1 = self.err_sum_calc(dt1, T)    

        dt2 = self.min_diff_list(T[:min(20, len(T))])
        err_sum2 = self.err_sum_calc(dt2, T)
        return min([err_sum1, dt1], [err_sum2, dt2])
    

    # This method values average options analytically. It     
    # returns the price of the average option.                                    
    def eq_average_analytic(self):          
        try:
            if len(self.ap.avg_dates) == 0:
                print 'TimeSeriesWarning: No Time Serie has yet been defined for the instrument.'
                return 0        
            
            # All averages are in the past. 
            if self.check and self.ap.fix_float:
                return ael.eq_option(self.ap.price, self.ap.texp, self.ap.vol, self.ap.rate,
                                    self.ap.carry_cost, self.ap.avg_so_far, 1-self.ap.put_call,
                                    self.ap.eur_ame, self.ap.dividends)
            elif self.check:
                    #The result is no longer stochastic.
                    return math.exp(-self.ap.rate*self.ap.texp)*max(self.ap.avg_so_far - self.strike, 0)

            if self.ap.fix_float:           
                res = self.calculations_floating()
            else: res = self.calculations_fix()
            if res >= 0: return res
            return 0
        except F_AVERAGE_EXCEPT, msg:
            print "eq_average_analytic() ERROR: ", msg
            raise F_AVERAGE_EXCEPT, 'The value of the average option could not be calculated.'
            

    















