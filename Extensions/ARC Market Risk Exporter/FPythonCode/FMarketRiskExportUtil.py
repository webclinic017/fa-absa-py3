""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportUtil.py"
import acm
import re
import functools
import FBDPCommon

_ISO_DATE_MATCHER = re.compile('([0-9]{4})-([0-9]{2})-([0-9]{2})')
_PERIOD_MATCHER = re.compile(r"""([\d ]+(?:m|y|d|w)) # match 11m, -1d """, re.I + re.VERBOSE)


def ConvertToDays(value, period):
    if period == 'w':
        return value*7
    
    if period == 'm':
        return value*30
    
    if period == 'y':
        return value*365
    
    return value
    
def Compare(value1, value2):
    a = value1
    b = value2
    if ":" in value1:
        a = value1.split(":")[0]
        b = value2.split(":")[0]
    if a == '':
        return -1
    if b == '':
        return 1

    if a in ['rest']:
        return 1
    if b in ['rest']:
        return -1

    bucketsStr = 'dwmy'
    if a[-1] not in bucketsStr:
        return -1
    if b[-1] not in bucketsStr:
        return -1

    value1 = ConvertToDays(int(value1[:-1]), a[-1])
    value2 = ConvertToDays(int(value2[:-1]), b[-1])
    
    if value1 < value2:
        return -1
    else:
        return 1

def DateDiffToPeriod(endDate, startDate):
        
    if re.match(_ISO_DATE_MATCHER, startDate) and re.match(_ISO_DATE_MATCHER, endDate):
        startYMD = [int(i) for i in startDate.split('-')]
        endYMD = [int(i) for i in endDate.split('-')]
        result = [e-s for e, s in zip (endYMD, startYMD)]
        if result[0] > 0:
            return '{0}y'.format(result[0])
        if result[1] > 0:
            return '{0}m'.format(result[1])
        if result[2] > 0:
            return '{0}d'.format(result[2])

    diff = acm.Time.DateDifference(endDate, startDate)
    monthUnit = int(diff / 30)
    mReminder = diff % 30
    yearUnit = int(diff / 365)
    yReminder = diff % 365

    if mReminder == 0 and yReminder != 0:
        convertY = abs(monthUnit)%12 == 0
        if convertY:
            return '{0}y'.format(int(monthUnit/12))
        return '{0}m'.format(monthUnit)

    if abs(yearUnit) > 1:
        return '{0}y'.format(yearUnit)
    
    if abs(monthUnit) > 1:
        return '{0}m'.format(monthUnit)

    return '{0}d'.format(diff)


def ParseDateStrToPeriod(inputStr, logger):
    explictPeriod = re.findall(_PERIOD_MATCHER, inputStr)
    if len(explictPeriod) > 0:
        dateStr= explictPeriod[0].strip()
        period = dateStr.replace(' ', "").lower()
        return dateStr, period
    
    explictDate = re.findall(_ISO_DATE_MATCHER, inputStr)
    if len(explictDate) > 0:
        dateStr = "-".join(explictDate[0]).strip()
        period = DateDiffToPeriod(FBDPCommon.toDate(dateStr), acm.Time.DateToday())
        return dateStr, period
    
    if inputStr.lower() =='rest':
        return "rest", "rest"

    logger.logError('unexpected string {0} for date or period.'.format(inputStr))
    return "", ""
    
def TimebucketInPeriod(timebucket, logger):
    if not timebucket:
        return None
        
    buckets = [t.Name().lower() for t in timebucket.AsList()]
    buckets = [ParseDateStrToPeriod(b, logger)[1] for b in buckets if b.lower() !='rest'] 
    buckets = sorted(buckets, key=functools.cmp_to_key(Compare))
    return buckets

def createTBbasedOnPoints(points, onPointDate):
    sortedPoints = sorted(points, key=lambda p: p.ActualDate())
    pDateList = []
    buckets = acm.FArray()
    for point in sortedPoints:
        bucketDef = acm.FFixedDateTimeBucketDefinition()
        pDate = point.ActualDate() if onPointDate \
            else acm.Time.DateAddDelta(point.ActualDate(), None, 4, 2) #adjust for 
                # inflation Curve Seasonality.  
                #point.Instrument().ExpiryDateOnly()
        if pDate in pDateList:
            continue
            
        pDateList.append(pDate)
        bucketDef.FixedDate( pDate )
        bucketDef.DateAsName(False)
        bucketDef.Name(point.Name())
        bucketDef.Adjust( True )
        buckets.Add(bucketDef)

    if buckets.Size():
        tbs = acm.Time().CreateTimeBucketsFromDefinitions( acm.Time().DateToday(),
            buckets, None, 0, False, False, False, False, False )
        return tbs
    else:
        return None

def createTBbasedOnDates(dates, logger):
    sortedDates = sorted(list(set(dates)))
    periods = [ParseDateStrToPeriod(d, logger) for d in sortedDates]
    createdBucketPeriod=[]
    buckets = acm.FArray()
    for item in periods:
        if item[1] not in createdBucketPeriod:
            createdBucketPeriod.append(item[1])
            bucketDef = acm.FFixedDateTimeBucketDefinition()
            bucketDef.FixedDate(item[0] )
            bucketDef.DateAsName(False)
            bucketDef.Name(item[1])
            bucketDef.Adjust( False )
            buckets.Add(bucketDef)

    if buckets.Size():
        tbs = acm.Time().CreateTimeBucketsFromDefinitions( acm.Time().DateToday(),
            buckets, None, 0, False, False, False, False, False )
        return tbs
    else:
        return None


def CreateYcTimeBucket(ycName, logger):
    yc = acm.FYieldCurve[ycName]
    if not yc:
        logger._logError("{0} is not a valid yield curve.".format(ycName))
        return []
    
    timeBucket = None
    if yc.Type() == "Instrument Spread":
        dates=[]
        spreads = yc.InstrumentSpreads()
        for s in spreads:
            dates.append(s.Instrument().EndDate())
        timeBucket = createTBbasedOnDates(dates, logger)
    else:
        points = [p for p in yc.Points()]
        if yc.Type() == "Composite":
            for p in yc.YieldCurveLinks():
                conCurv = p.ConstituentCurve()
                points.extend(conCurv.Points())
        if yc.Type() == "Inflation":
            timeBucket = createTBbasedOnPoints(points, False)
        else:
            timeBucket = createTBbasedOnPoints(points, True)
    return timeBucket

def getTBbasedOnDates(dates, logger):
    periods = list({ParseDateStrToPeriod(d, logger)[1] for d in dates})
    return sorted(periods, key=functools.cmp_to_key(Compare))
    
def getTBbasedOnPoints(points, logger, onPointDate):
    pDateList = []
    ycValidPoints = []
    for point in points:
        if onPointDate:
            pDate = point.ActualDate()
            if pDate in pDateList:
                continue
        else:
            #adjust for inflation Curve Seasonality.  
            pDate = acm.Time.DateAddDelta(point.ActualDate(), None, 4, 2)
        
        pDateList.append(pDate)
        ycValidPoints.append(point)
   
    buckets = [(p.Name().lower(), p.Instrument().Name() if p.Instrument() else "") for p in ycValidPoints]

    if len(buckets) == 0:
        buckets.append("0d", "")

    buckets = list({ParseDateStrToPeriod(b[0], logger)[1] for b in buckets if b[0].lower() != 'rest'})
    buckets = sorted(buckets, key=functools.cmp_to_key(Compare))
    return buckets

def GetYcTimeBucket(ycName, logger):
    yc = acm.FYieldCurve[ycName]
    if not yc:
        logger._logError("{0} is not a valid yield curve.".format(ycName))
        return []
    
    timeBucket = []
    if yc.Type() == "Instrument Spread":
        dates=[]
        spreads = yc.InstrumentSpreads()
        for s in spreads:
            dates.append(s.Instrument().EndDate())
        timeBucket = getTBbasedOnDates(dates, logger)
    else:
        points = [p for p in yc.Points()]
        if yc.Type() == "Composite":
            for p in yc.YieldCurveLinks():
                conCurv = p.ConstituentCurve()
                points.extend(conCurv.Points())
        if yc.Type() == "Inflation":
            timeBucket = getTBbasedOnPoints(points, logger, False)
        else:
            timeBucket = getTBbasedOnPoints(points, logger, True)
    return timeBucket
