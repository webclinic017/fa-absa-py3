"""-----------------------------------------------------------------------------
MODULE
    PS_Provision

DESCRIPTION
    Date                : 2011-12-08
    Purpose             : Calculates the provision per trade. Based on the SAIRD_ShortEndCurve_Management python module.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 850928
ENDDESCRIPTION

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-12-08 850928       Herman Hoon        Initial implementation
2014-03-11 abcdef       Peter Fabian       Calculate live provision only for current day
2015-01-14 2562289      Hynek Urban        Use sum_over_multiple where appropriate.
-----------------------------------------------------------------------------"""
import acm, ael
import datetime

import PS_FundingSweeper
from at_decorators import sum_over_multiple
import at_logging


LOGGER = at_logging.getLogger()


class ProvReport:

    def __init__(self, data):

        self.InputData = data['InputType']
        self.DataParam = data['Trade']
        self.ReportType = data['ReportType']
        self.Currency = data['Currency'][0].Name()
        self.FwdCurve = data['Curve'][0]
        self.FwdCurveName = self.FwdCurve.Name()
        self._ValidateData()
        self.StartDate = ael.date_today()
        self.EndDate = ael.date_today().add_months(9)
        self.TradePop = self.ValidTradeCollection()
        self.calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self.FXRate = self._FXRate()
        self.PSign = {1:-1, 0: 1}


    def _ValidateData(self):
        if self.FwdCurveName not in ['ZAR-SWAP', 'USD-SWAP'] and self.ReportType == 'Provision':
            raise Exception('Provision Report not available for selected curve, run risk report')


    def ValidTradeCollection(self):
        tradecol = []
        t = self.DataParam

        if t:
            if t.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
                ins = t.Instrument()
                if ins.InsType() not in  ['Combination', 'Curr']:
                    if ael.date_from_string(ins.ExpiryDateOnly()) > self.StartDate:
                        if self.ReportType != 'Reset Risk':
                            if self._FindBasisTrades(t) < 2 and ins.InsType() in ('Swap', 'FRA'):
                                tradecol.append(t)
                        else:
                            tradecol.append(t)

                elif ins.InsType() in ['Curr']:
                    if ael.date_from_string(t.ValueDay()) > self.StartDate:
                        if self.ReportType == 'Reset Risk':
                            tradecol.append(t)

                else:
                    comb_ins = ins.Instruments()
                    for i_c in comb_ins:
                        trds_comb = i_c.Trades()
                        if len(trds_comb) > 0:
                            t = trds_comb[0]
                            if t.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
                                if self.ReportType != 'Reset Risk':
                                    if self._FindBasisTrades(t) < 2 and t.Instrument().Instype() in ('Swap', 'FRA'):
                                        tradecol.append(t)
                                else:
                                    tradecol.append(t)
        return tradecol


    def _FindBasisTrades(self, trade):
        flag = 0
        ins_legs = trade.Instrument().Legs()

        if len(ins_legs) > 1:
            for l in ins_legs:
                if l.IsFloatLeg():
                    flag += 1
                else:
                    flag -= 1
        return flag


    def _FXRate(self):
        curr_base = ael.Instrument['ZAR']
        curr = ael.Instrument[self.Currency]
        d = 1.0 / curr_base.used_price(self.StartDate, curr.insid)

        return d

def PickUpMPC(TSspec_Name, acmdate):

    date_list = []
    tsspec = acm.FTimeSeriesSpec[TSspec_Name]
    ts = tsspec.TimeSeries()

    for t in ts:
        if acm.Time().AsDate(t.Day()) > acmdate:
            date_list.append(t.Day())

    date_list.sort(lambda x, y: cmp(acm.Time().AsDate(x), acm.Time().AsDate(y)))
    return date_list

def SE_Curve(d1, mpc, ins_ccy):

    mkt_dte_lst = []
    mkt_rt_lst = []
    done_mpc = 0

    if ins_ccy == 'ZAR':
        ccy = ael.Instrument[ins_ccy]
        mkt_dte_lst.append(d1)
        ins = ael.Instrument['ZAR-JIBAR-3M']
        mkt_rt_lst.append(ins.used_price())
        
        
        for k in range(1, 10):
            ins = ael.Instrument['ZAR/FRA/JI/' + str(k) + 'X' + str(k + 3)]
            dte = d1.add_months(k).adjust_to_banking_day(ccy)
            rt = ins.used_price()
            
            if len(mpc) > 0 and ael.date(dte) > ael.date(mpc[0]):
                
                mpc_date = ael.date(mpc[0])
                mpc_string = mpc_date.to_string('%b%y').upper()
                preIns = "ZAR/FRA/JI/PRE_%s_MPC" % (mpc_string)                
                postIns = "ZAR/FRA/JI/POST_%s_MPC" % (mpc_string)
                
                try:
                    ins = ael.Instrument[preIns]
                    if ins:
                        mkt_dte_lst.append(ael.date(mpc_date))                
                        mkt_rt_lst.append(ins.used_price())
                        
                        
                except:
                    pass

                try:
                    ins = ael.Instrument[postIns]
                    if ins:
                        mkt_dte_lst.append(ael.date(mpc_date).add_days(1).adjust_to_banking_day(ccy))
                        mkt_rt_lst.append(ins.used_price())
                        
                        
                except:
                    pass
                del mpc[0]
            
            mkt_dte_lst.append(dte)
            mkt_rt_lst.append(rt)

    if ins_ccy == 'USD':
        ccy = ael.Instrument[ins_ccy]
        mkt_dte_lst.append(d1)
        ins = ael.Instrument['USD-LIBOR-3M']
        mkt_rt_lst.append(ins.used_price())

        for k in range(1, 10):
            ins = ael.Instrument['USD/FRA/LI/' + str(k) + 'X' + str(k + 3) ]
            dte = d1.add_months(k).adjust_to_banking_day(ccy)
            rt = ins.used_price()


            if ael.date(dte) > mpc and done_mpc == 0:
                mkt_dte_lst.append(mpc)
                mkt_rt_lst.append(mkt_rt_lst[len(mkt_rt_lst) - 1])
                mkt_dte_lst.append(mpc.add_days(1))
                mkt_rt_lst.append(rt)

                done_mpc = -1

            mkt_dte_lst.append(dte)
            mkt_rt_lst.append(rt)

    return mkt_dte_lst, mkt_rt_lst

#=====================================================================================

def lin_interp(x, y, val):

    if val <= x[0]:
        return y[0]

    for k in range(1, len(x)):

        if x[k] > val:
            n = x[k - 1].days_between(x[k]) * 1.0
            n1 = x[k - 1].days_between(val) * 1.0
            n2 = n - n1
            interp = ((n1 * y[k] + n2 * y[k - 1]) / n)
            return interp
    return y[ len(y) - 1 ]


#=====================================================================================

def CalculateBucket(resterm, nominal):

    if resterm < 0.2:
        return [nominal, 0, 0, 0, 0]
    elif resterm >= 0.2 and resterm < 0.45:
        return [0, nominal, 0, 0, 0]
    elif resterm >= 0.45 and resterm < 0.7:
        return [0, 0, nominal, 0, 0]
    elif resterm >= 0.7 and resterm < 1:
        return [0, 0, 0, nominal, 0]
    else:
        return [0, 0, 0, 0, nominal]


def calculateProvision(trade):
    '''Calculate the provision for the difference between the ZAR-SWAP and the MPC Curve
    '''

    data = {'Curve':        [acm.FYieldCurve['ZAR-SWAP']],
            'Trade':        trade,
            'Currency':     [acm.FCurrency['ZAR']],
            'ReportType':   'Provision Per Reset',
            'Portfolio':    [],
            'InputType':    'Filter'}

    report = ProvReport(data)
    acmtoday = acm.Time().DateToday()

    timeseries = 'MO_MPC' + '_' + report.Currency
    next_mpc = PickUpMPC(timeseries, acmtoday)
    mkt_dte, mkt_rt = SE_Curve(report.StartDate, next_mpc, report.Currency)
    zar = ael.Instrument['ZAR']
    yc = ael.YieldCurve[report.FwdCurve.Name()]
    TotalProv = 0
    All_Resets = {}
    reset_day_dict = {}

    for t in report.TradePop:
        ins = t.Instrument()
        try:
            l = ins.FirstFloatLeg()
        except:
            LOGGER.warning('No Float Leg %s %s', ins.Name(), ins.InsType())

        if l:
            if l.Currency().Name() == report.Currency:
                if l.FloatRateReference() <> None:
                    fwd_curve = None
                    if 'FYCAttribute' in str(l.MappedForwardLink().Link().YieldCurveComponent().Class()):
                        fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent().Curve()
                    else:
                        fwd_curve = l.MappedForwardLink().Link().YieldCurveComponent()
                    if fwd_curve.Name() in ('ZAR-SWAP-SPREAD-1m', 'ZAR-SWAP-SPREAD-6m', 'ZAR-SWAP-SPREAD-12m'):
                        fwd_curve = acm.FYieldCurve['ZAR-SWAP']

                    if fwd_curve == report.FwdCurve:
                        for cf in l.CashFlows():
                            if (cf.EndDate() and ael.date(cf.EndDate()) >= report.StartDate) and (cf.StartDate() and ael.date(cf.StartDate()) <= report.EndDate):
                                for r in cf.Resets():
                                    if r <> None :
                                        if r.ResetType() in ('Single', 'Compound', 'Weighted'):
                                            if ael.date(r.Day()) >= report.StartDate and ael.date(r.Day()) <= report.EndDate:
                                                if (r.Day(), l.DayCountMethod()) in All_Resets.keys():
                                                    fwd_rt = All_Resets[r.Day(), l.DayCountMethod()][1]
                                                    se_rt = All_Resets[r.Day(), l.DayCountMethod()][0]
                                                else:
                                                    start = ael.date(r.Day())
                                                    se_rt = lin_interp(mkt_dte, mkt_rt, start) / 100
                                                    end = start.add_months(3).adjust_to_banking_day(zar)
                                                    fwd_rt = yc.yc_rate(start, end, 'Quarterly', l.DayCountMethod(), 'Forward Rate')
                                                    All_Resets[start.to_string('%Y-%m-%d'), l.DayCountMethod() ] = [se_rt, fwd_rt ]

                                                reset_period = acm.Time().DateDifference(r.EndDate(), r.StartDate()) / 365.0
                                                sign = report.PSign[l.PayLeg()]
                                                nominal = cf.Calculation().Nominal(report.calcSpace, t).Number() * report._FXRate()
                                                provision = nominal / 100 * reset_period * 96 * (se_rt - fwd_rt)
                                                buckets = CalculateBucket(reset_period, nominal)
                                                TotalProv += provision


    return TotalProv


@sum_over_multiple('portfolioSwap')
def GetProvision(instrument, portfolioSwap, date):
    '''Calculate the provision that is stored down for a specific date.
    '''
    LOGGER.debug("Calculating provision for instrument: '%s'", instrument.Name())
    provision = 0.0
    leg = PS_FundingSweeper.GetLeg(portfolioSwap, 'Total Return', instrument)
    if leg:
        cashFlow = PS_FundingSweeper.GetReturnCashFlow(leg, 'Provision')
        if cashFlow:
            for reset in cashFlow.Resets():
                LOGGER.debug("Checking reset '%s' (day: '%s', type: '%s'), for: leg '%s', cashflow '%s'",
                             reset.Oid(), reset.Day(), reset.ResetType(), leg.Oid(), cashFlow.Oid())
                if reset.Day() == date and reset.ResetType() == 'Return':
                    provision = reset.FixingValue()
                    break
    return provision

def hist_valuation():
    ''' Heuristics to find out whether the calc runs for past date.
        (if it does, we don't want to calculate intraday provision from current yield curve)
    '''
    [acm_y, acm_m, acm_d] = acm.Time.DateToYMD(acm.Time.DateToday())
    real_today = datetime.date.today()
    year = real_today.year
    month = real_today.month
    day = real_today.day
    return not (acm_y == year and acm_m == month and acm_d == day)

def CalculateProvisionStartEnd(trades, instrument, portfolioSwap, startDate, endDate, warehousingType='Daily'):
    ''' Historical Provision is stored on the Total Return leg of a portfolioswap at a instrument level.  This returns
        the sum of all provision resets for a given date for a particular instrument type

        For intraday it should calculate the provision from the Yield Curve
    '''
    startProvision = GetProvision(instrument, portfolioSwap, startDate)
    endProvision = 0.0
    today = acm.Time.DateToday()

    if today == endDate and not hist_valuation():
        for trade in trades.AsList():
            endProvision += calculateProvision(trade)
    else:
        endProvision = GetProvision(instrument, portfolioSwap, endDate)

    provision = endProvision - startProvision
    return provision

