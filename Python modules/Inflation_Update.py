import ael


inflationCurvesDict = {}
yieldCurves = ael.YieldCurve.select()
print yieldCurves 
for yieldCurve in yieldCurves:
    if yieldCurve.add_info('InflationCurve') == 'Yes':
        print yieldCurve.yield_curve_name, yieldCurve.add_info('InflationCurve'), '<<<<<<<<<'
        nominalCurve = yieldCurve.add_info('NominalCurve')
        realCurve = yieldCurve.add_info('RealCurve')
        inflationCurvesDict[yieldCurve] = (nominalCurve, realCurve)

print inflationCurvesDict

inflationCurvesDictKeys = inflationCurvesDict.keys()
if len(inflationCurvesDictKeys) > 0:
    for cpiOffName in inflationCurvesDictKeys:
        cpiOff = cpiOffName
        cpiNom = ael.YieldCurve[inflationCurvesDict[cpiOffName][0]]
        cpiReal= ael.YieldCurve[inflationCurvesDict[cpiOffName][1]]
    
        print cpiOff.yield_curve_name, cpiNom.yield_curve_name, cpiReal.yield_curve_name
        
    
    """
    
    cpiOff = ael.YieldCurve['ZAR/CPI/OFFICIAL']
    cpiNom = ael.YieldCurve['ZAR/SWAP']
    cpiReal= ael.YieldCurve['ZZ_REAL']
    """
    
    bMarkPoints = []
    cpiOffDict = {}
    
    cpiNomPts= cpiNom.points()
    cpiNomBmks = cpiNom.benchmarks()
    
          
    for y in cpiNomBmks: 
        inst = y.instrument
        datePeriod = y.instrument.legs()[0].end_period
        tpl = (inst, datePeriod)
        bMarkPoints.append(tpl)
     
    print bMarkPoints
    
    for bMP in bMarkPoints:
        period = bMP[1]
        today = ael.date_today()
        endDay = ael.date_today().add_period(period).adjust_to_banking_day(ael.Calendar['ZAR Johannesburg'])
    
        df1 = cpiNom.yc_rate(today, endDay, None, 'Act/365', 'Discount')
        df2 = cpiReal.yc_rate(today, endDay, None, 'Act/365', 'Discount')
        
        print today, endDay, df1, df2, today.years_between(endDay, 'Act/365')
        print period, ((df1/df2)**(1.0/(-1.0*today.years_between(endDay, 'Act/365')))-1)*100.0
        cpiOffNACS = ((df1/df2)**(1.0/(-1.0*today.years_between(endDay, 'Act/365')))-1)*100.0
        cpiOffDict[period] = cpiOffNACS/100.0
    
    cpiOffPts= cpiOff.points()
    
    print  cpiOffDict
    for cpiOffPt in cpiOffPts:
        print cpiOffPt.date_period, cpiOffDict[cpiOffPt.date_period]
        cpiOffPtClone = cpiOffPt.clone()
        cpiOffPtClone.value = cpiOffDict[cpiOffPt.date_period]
        cpiOffPtClone.commit()
