import acm
import math

def BankingDayPeriodToDateFromStartDate(calendars, startDate, period, deliveryCalendar = None):
    if deliveryCalendar is not None:
        calendars.append(deliveryCalendar)
    if acm.Time().DatePeriodUnit(period) == 'Days':
        #if period is days it should add banking days
        date = AdjustBankingDaysFromMultiCalendars(startDate, acm.Time().DatePeriodCount(period), calendars)
    else:
        # If period is not days, simply add the period and adjust to next banking day
        nonAdjustedDate = acm.Time().DateTimeAdjustPeriod(startDate, period, None, 'Following')
        date = AdjustBankingDaysFromMultiCalendars(nonAdjustedDate, 0, calendars)
    return date
    
def AdjustBankingDaysFromMultiCalendars(date, nbrDays, calendars):
    if hasattr(calendars, 'IsKindOf') and calendars.IsKindOf(acm.FCalendar):
        movedDate = calendars.AdjustBankingDays(date, nbrDays)
        #Must do modify as well to handle case with nbrDays = 0
        return calendars.ModifyDate(None, None, movedDate)
    else:
        # Max three calendars because that is all method ModifyDate allows
        if len(calendars) > 3:
            raise RuntimeError('Method "AdjustBankingDaysFromMultiCalendars" can take a maximum of three calendars')

        if len(calendars) == 0:
            return date

        cal2 = None
        cal3 = None
        baseDate = calendars[0].AdjustBankingDays(date, nbrDays)
        if len(calendars) >= 2:
            compDate = calendars[1].AdjustBankingDays(date, nbrDays)
            baseDate = compDate if acm.Time.DateDifference(compDate, baseDate) > 0 else baseDate
            cal2 = calendars[1]
        if len(calendars) == 3:
            compDate = calendars[2].AdjustBankingDays(date, nbrDays)
            baseDate = compDate if acm.Time.DateDifference(compDate, baseDate) > 0 else baseDate
            cal3 = calendars[2]        
        return calendars[0].ModifyDate(cal2, cal3, baseDate)

def GetRelevantFixingCalendar(ins):
    und = ins.Underlying()
    cal = None
    if und:
        cal = und.SettlementCalendar()
        if not cal and und.Currency():
            cal = und.Currency().Calendar()
    if not cal and ins.Currency():
        cal = ins.Currency().calendar()
    return cal

def GeneratePeriodEndDates(start, end, method, freq, calendars, settleDays, settleCalendars):
    if hasattr(calendars, 'IsKindOf') and calendars.IsKindOf(acm.FCalendar):
        calendars = [calendars]

    periodEndDates = acm.FArray()    
    periods = acm.DealCapturing().GenerateStripOfOptionDates(start, end, freq, 
                                                   end, method, calendars, 
                                                   False)
    if periods.Size() > 0:
        periodExpiries = periods[1:]
    else:
        periodExpiries = periods
    
    for expiry in periodExpiries:
        ped = acm.FDictionary()
        ped['endDate'] = expiry
        ped['settlementDate'] = AdjustBankingDaysFromMultiCalendars(expiry, settleDays, settleCalendars)
        periodEndDates.Add(ped)

    return periodEndDates

def GenerateFXPeriodDates(startDate, rolling, dayMethod, currencyPair, deliveryCalendar, nbrOfPeriods, settleDays = None):
    def ModifyDate(date):
        if not deliveryCalendar:
            return date
        return deliveryCalendar.ModifyDate(currencyPair.Currency1().Calendar(), currencyPair.Currency2().Calendar(), date, dayMethod)

    # When deleting a trade, add info values are empty
    if not (rolling and dayMethod):
        return []

    dates = acm.FArray()
    period = '0%s' % acm.Time.DatePeriodUnit(rolling)
    
    previousExpiry = None
    generatedPeriods = 0
    multiplicationPeriods = 0

    while generatedPeriods < nbrOfPeriods:
        period = '%i%s' % (multiplicationPeriods * acm.Time.DatePeriodCount(rolling), acm.Time.DatePeriodUnit(rolling))
        multiplicationPeriods += 1
        expiry = currencyPair.ExpiryDate(startDate, period)
        if previousExpiry and acm.Time.DateDifference(previousExpiry, expiry) == 0:
            # If using period 1D, every saturday and sundag will end up on MOnday and there will
            # be three expiries on every Monday.
            continue
        if settleDays is None or deliveryCalendar is None:
            delivery = currencyPair.SpotDate(expiry)
        else:
            delivery = deliveryCalendar.AdjustBankingDays(expiry, settleDays)
        dates.Add({'endDate':expiry, "settlementDate":ModifyDate(delivery)})
        previousExpiry = expiry
        generatedPeriods += 1
    
    return dates

def GenerateMonthlyPeriodDates(startDate, fixingCalendar, settlementCalendar, deliveryCalendar, nbrOfPeriods, settleDays, dayMethod = 'Following'):
    def ModifyDate(date):
        if not deliveryCalendar:
            return date
        return deliveryCalendar.ModifyDate(settlementCalendar, None, date, dayMethod)

    dates = acm.FArray()
    generatedPeriods = 0
    month = acm.Time.FirstDayOfMonth(startDate)

    while generatedPeriods < nbrOfPeriods:
        month = acm.Time.DateAdjustPeriod(month, '1M')
        lastOfMonth = acm.Time.DateAdjustPeriod(month, "-1d")
        expiry = fixingCalendar.ModifyDate(None, None, lastOfMonth, "Preceding")
        delivery = settlementCalendar.AdjustBankingDays(expiry, settleDays)
        dates.Add({'endDate':expiry, "settlementDate":ModifyDate(delivery)})
        generatedPeriods += 1
    return dates

def GenerateExpiryTableDates(startDate, calendars, periodEndDates, frequency):
    allObservationDates     = acm.FArray()
    currentPeriod           = 0
    currentObservationDate  = startDate
    finalPeriodEndDate      = periodEndDates.Last()['endDate']
    
    while acm.Time().DateDifference(finalPeriodEndDate, currentObservationDate) >= 0:
        if acm.Time().DateDifference(currentObservationDate, periodEndDates[currentPeriod]['endDate']) > 0:
            currentPeriod += 1

        if frequency == 'Daily' or acm.Time().DateDifference(currentObservationDate, periodEndDates[currentPeriod]['endDate']) == 0:
            od = acm.FDictionary()
            od.AddAll( periodEndDates[currentPeriod] )
            od['observationDate'] = currentObservationDate
            allObservationDates.Add(od)
        
        currentObservationDate = AdjustBankingDaysFromMultiCalendars(currentObservationDate, 1, calendars)
        
    return allObservationDates

def GenerateAverageDates(fixingEvents, fixingCalendar):
    dates = acm.FArray()
    for fixing in fixingEvents:
        firstOfMonth = acm.Time.FirstDayOfMonth(fixing.Date())
        currentAvgDate = fixingCalendar.ModifyDate(None, None, firstOfMonth, 'Following')
        while acm.Time.DateDifference(currentAvgDate, fixing.Date()) <= 0:
            dates.Add(currentAvgDate)
            nextCalendarDate = acm.Time.DateAdjustPeriod(currentAvgDate, '1d')
            currentAvgDate = fixingCalendar.ModifyDate(None, None, nextCalendarDate, 'Following')
    return dates
        

def GetHistoricalFxRate(curr1, curr2, date):
    histFxRate = curr1.MtMPrice(date, curr2)
    if histFxRate and (not math.isnan(histFxRate)):
        return histFxRate
    else:
        raise RuntimeError("ERROR: No MtM %s/%s rate available for %s" % (curr2.Name(), curr1.Name(), str(date)))
