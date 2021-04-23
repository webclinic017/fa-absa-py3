
from __future__ import print_function
import acm
from at_time import *
import ael
from at_time import *
from datetime import datetime, date
import math
from collections import defaultdict
from dateutil.parser import parse
from FCalcUtil import *
import locale
reload(locale)
locale.setlocale(locale.LC_TIME, '')

createDictionary = acm.GetFunction('createDictionary', 2)
shiftBenchmarkPriceTimeBucket=acm.GetFunction('shiftBenchmarkPriceTimeBucket', 5)

zar_swap_instr  = acm.FYieldCurve['ZAR-SWAP'].BenchmarkInstruments()
zar_swap_instr_names = [i.Name() for i in zar_swap_instr]

curves = [acm.FYieldCurve['ZAR-SWAP'], acm.FYieldCurve['ZAR.DISC.CSA_ZAR'], acm.FYieldCurve['ZAR-SWAP-SE']]
for i in range(3):
    for y in curves:
        y.Calculate()


def get_short_end_curve(prices, curve):
    filtered_curve = defaultdict(list)
    for c, p in zip(curve, prices):
        instr = acm.FInstrument[c]
            
        filtered_curve[instr.StartDate()].append((c, instr.Generic(), p))
        if instr.Name() == 'ZAR/FRA/JI/12X15':
            break
    #print('Benchmarks1', filtered_curve)
    curve = []
    for start_date in sorted(filtered_curve.keys()):
        element = filtered_curve[start_date]
        if len(element) == 1:
            curve.append(element[0])
        else:
            non_generic = filter(lambda x: x[1] is True, element)
            curve.append(non_generic[0])
    interpolated = {}
    idx = 0
    while idx < len(curve) - 1:
        benchmark1 = acm.FInstrument[curve[idx][0]]
        benchmark2 = acm.FInstrument[curve[idx+1][0]]
        start_date = benchmark1.StartDate()
        end_date = benchmark2.StartDate()
        rate1 = curve[idx][2]
        rate2 = curve[idx+1][2]
        
        number_of_days = (to_date(end_date) - to_date(start_date)).days
        if number_of_days == 0:
            idx += 1 
            continue
            
        counter = 0
        while counter <= number_of_days:
            date = to_date('%s+%sd' % (start_date, counter))
            interpolated[acm_date(date)] = rate1 + counter * (rate2-rate1)/number_of_days
            counter += 1
        idx += 1
    return interpolated

def Short_End_Spread_Calibration( dates, prices, instruments, yieldCurveName, base_curve_ir, old_ir):
    d = createDictionary(instruments, prices)
    queried_dates = [parse(e).date() for e in dates]
    short_curve = get_short_end_curve(prices, instruments)
    short_end_curve = acm.FYieldCurve[yieldCurveName]
    instr = short_end_curve.AdditionalInfo().Short_End_Cutoff()

    zar_swap=base_curve_ir
    
    start_date = instr.StartDate()
    end_date = instr.EndDate()
    last_shortend = start_date
    
    dates = short_end_curve.Points()
    dates = [p.ActualDate() for p in dates]
    dates = filter(lambda x: x <= last_shortend, dates)
    dates = sorted(dates, reverse=True)
        
    zar_swap_df = {}
    zar_swap_aer = {}
    
    date_idx = to_date(start_date)
    while date_idx <= to_date(end_date):
        zar_swap_df[acm_date(date_idx)] = zar_swap.Discount(acm_date('0d'), acm_date(date_idx))
        date_idx = to_date('%s+1d' % date_idx)

    date_idx = to_date('0d')
    while date_idx <= to_date(end_date):
        zar_swap_aer[acm_date(date_idx)] = zar_swap.Rate(acm_date('0d'), acm_date(date_idx), 'Annual Comp', 'Act/365', 'Spot Rate')
        date_idx = to_date('%s+1d' % date_idx)
    discount_factors_short_end = {}
    aer = {}
    for d in dates:
        end_date = ael_date(d).add_period('3m').adjust_to_banking_day(ael.Instrument[short_end_curve.Currency().Name()], 'Mod. Following')
        start_date = ael_date(d)
        period = (to_date(end_date) - to_date(start_date)).days
        discount_period = (to_date(start_date) - to_date('0d')).days
        short_end_factor = (1+short_curve[d]/100*period/365)
        short_end_factor = math.log(short_end_factor)
        
        if acm_date(end_date) in discount_factors_short_end:
            discount_factors_short_end[acm_date(d)] = discount_factors_short_end[acm_date(end_date)]*math.exp(short_end_factor)
            line = 'A;%s;%s;%s;%s;%s;%s;%s' % (start_date, end_date, period, discount_period, discount_factors_short_end[acm_date(d)], short_end_factor, short_curve[d])
        else:
            discount_factors_short_end[acm_date(d)] = zar_swap_df[acm_date(end_date)]*math.exp(short_end_factor)
            line = 'B;%s;%s;%s;%s;%s;%s;%s' % (start_date, end_date, period, discount_period, zar_swap_df[acm_date(end_date)], short_end_factor, short_curve[d])
        cont_rate = math.log(1/discount_factors_short_end[acm_date(d)])/discount_period*365
        annual = math.pow(math.exp(cont_rate*discount_period/365.0), 365.0/discount_period) -1
        aer[acm_date(d)] = annual
    l = []
    for d in queried_dates:
        if acm_date(d) in aer:
            l.append(round(aer[acm_date(d)]-zar_swap_aer[acm_date(d)], 12))
        else:
            l.append(0.0)
    return l
    
def _is_shortend(instr):
    if instr.InsType() == 'FRA' and instr.StartDate() <= acm.FFra['ZAR/FRA/JI/9X12'].StartDate():
        return True
    elif instr.InsType() == 'FRA' and instr.StartDate() > acm.FFra['ZAR/FRA/JI/9X12'].StartDate():
        return False
    elif instr.InsType() == 'RateIndex':
        return True
    else: 
        return False
        
def bump_curve(ir_curve_info, prices):
    ir_curve_info.Calculate(ir_curve_info.OriginalCurve(), prices)
    return ir_curve_info
    
def bump_swap_curve(curve, prices):
    csc = acm.Calculations().CreateStandardCalculationsSpaceCollection()       
    for i in prices.Keys():
        if prices.At(i):
            curve=shiftBenchmarkPriceTimeBucket(curve, prices.At(i)*100.0, None, i, None)
    benchmarks = curve.BenchmarkInstruments()
    prices = [acm.DenominatedValue(i.Calculation().BenchmarkPrice(csc), 'ZAR', 'Price', acm.Time().DateToday()) for i in benchmarks]
    d = createDictionary(benchmarks, prices)
    ir = curve.IrCurveInformationCacheKey(acm_date('0d'), None, None, acm.FBenchmarkCurve['ZAR.DISC.CSA_ZAR']).IrCurveInformation(d, None)
    return ir

def get_curve_clone(yc, ir):
    ycc = yc.CloneAndSimulateRecursive()
    points = ycc.Points().Clear()
    ycc.RealTimeUpdated(False)
    ycc.UseBenchmarkDates(False)
    
    ir_points = createDictionary([acm_date(to_datetime(e)) for e in ir.PointDates()], ir.PointValues())
    new_points = []
    
    for p in yc.Points():
        pc = p.CloneAndSimulateRecursive()
        pc.PointValue(ir_points.At(p.ActualDate()))
        pc.Curve(ycc)
        new_points.append(pc)
    
    points.AddAll(new_points)
    points.Apply(points)
    
    return ycc

def get_curve_clone_from_values(yc, values):
    ycc = yc.CloneAndSimulateRecursive()
    points = ycc.Points().Clear()
    ycc.RealTimeUpdated(False)
    ycc.UseBenchmarkDates(False)
    ir = ycc.IrCurveInformation()
    ir_points = createDictionary([acm_date(to_datetime(e)) for e in ir.PointDates()], ir.PointValues())
    new_points = []
    
    instr = acm.FInstrument['ZAR/FRA/JI/9X12']
    
    for p, v in zip(yc.Points(), values):
        pc = p.CloneAndSimulateRecursive()
        #if p.ActualDate() <= instr.EndDate():
        pc.PointValue(v)
        pc.Curve(ycc)
        new_points.append(pc)
    
    points.AddAll(new_points)
    points.Apply(points)
    
    return ycc
    
def get_curve_long(yc, ir):
    ycc = yc.CloneAndSimulateRecursive()
    ycc.Calculate()
    old_points = createDictionary([acm_date(to_datetime(e)) for e in yc.IrCurveInformation().PointDates()], yc.IrCurveInformation().PointValues())
    points = ycc.Points().Clear()
    ycc.RealTimeUpdated(False)
    ycc.UseBenchmarkDates(False)
    
    ir_points = createDictionary([acm_date(to_datetime(e)) for e in ir.PointDates()], ir.PointValues())
    new_points = []
    
    instr = acm.FInstrument['ZAR/FRA/JI/9X12']
    
    for p in yc.Points():
    
        pc = p.CloneAndSimulateRecursive()
        if p.ActualDate() >= instr.EndDate():
            pc.PointValue(ir_points.At(p.ActualDate()))
        else:
            pc.PointValue(old_points.At(p.ActualDate()))
        pc.Curve(ycc)
        new_points.append(pc)
    
    points.AddAll(new_points)
    points.Apply(points)
    
    return ycc

def bump_benchmark(curve, benchmarkTickStepShift, timeBucket, specificBenchmark, benchmarksSource):
    if curve.Name() in ('ZAR-SWAP-SE', 'ZAR-SWAP-SE-SPREAD') and _is_shortend(specificBenchmark):
        csc = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        benchmarks = curve.BenchmarkInstruments()
        if specificBenchmark not in benchmarks:
            return curve
        prices = [acm.DenominatedValue(i.Calculation().BenchmarkPrice(csc), 'ZAR', 'Price', acm.Time().DateToday()) for i in benchmarks]
        dates=[p.ActualDate() for p in curve.Points()]
        benchmarks = curve.BenchmarkInstruments()
        prices = [i.Calculation().BenchmarkPrice(csc).Number() for i in benchmarks]

        b = sorted(zip(benchmarks, prices), key=lambda x: x[0].LastIRSensDay())
        b = list(zip(*b))
        benchmarks = b[0]
        prices = b[1]
        benchmarks = [b.Name() for b in benchmarks]
        prices = [p for p in prices]
        idx = benchmarks.index(specificBenchmark.Name())
        prices[idx]+=benchmarkTickStepShift/100.0
        print(specificBenchmark.Name())
        if specificBenchmark.Name() != 'ZAR-JIBAR-ON-DEP':
            ir = bump_swap_curve(acm.FYieldCurve['ZAR-SWAP'], createDictionary([specificBenchmark], [benchmarkTickStepShift/100.0]))
        if curve.Name() in ('ZAR-SWAP-SE'):
            point_values = Short_End_Spread_Calibration( dates, prices, benchmarks, curve.Name(), ir, curve.IrCurveInformation())
        elif curve.Name() in ('ZAR-SWAP-SE-SPREAD'):
            point_values = Short_End_Spread_Calibration( dates, prices, benchmarks, curve.Name(), ir, curve.IrCurveInformation())
        return get_curve_clone_from_values(curve, point_values)
    elif curve.Name() == 'ZAR-SWAP' and specificBenchmark.Name() == 'ZAR-JIBAR-ON-DEP':
        return curve
    elif curve.Name() == 'ZAR-SWAP' and _is_shortend(specificBenchmark):
        return shiftBenchmarkPriceTimeBucket(curve, benchmarkTickStepShift, timeBucket, specificBenchmark, benchmarksSource)
    else:
        return shiftBenchmarkPriceTimeBucket(curve, benchmarkTickStepShift, timeBucket, specificBenchmark, benchmarksSource)
