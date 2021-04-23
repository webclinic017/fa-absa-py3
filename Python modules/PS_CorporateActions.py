'''----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)
----------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no Developer                  Description
--------------------------------------------------------------------------------
2011-08-17 750738    Rohan van der Walt         isExCouponDay implementation
2011-08-17 750738    Rohan van der Walt         LDT adjustment
2011-11-10 823071    Rohan van der Walt         Bond Coupon LDT changes
2012-02-23           Herman Hoon                ETF Dividend changes
2012-03-19 883716    Phumzile Mgcima           'Iterate' parameter on GetDividend() for multiple dividends
2014-10-09 2344594   Jakub Tomaga               None handling in GetLDT()
2015-08-13 3028161   Ondrej Bahounek            Amend coupon amount calculation.
-----------------------------------------------------------------------------'''

import acm

import  PS_XMLReportingToolsMultRows

from xml.etree import ElementTree as ET


def CalculateExCouponDate(exCouponList, couponDate):
    ''' This function identifies the date in exCouponList that is the ex-coupon-date corresponding to couponDate and converts 
        that date to the correct year.  The dates in the exCouponList have the same year as when the bond was issued.  
        
        The reason for using mod 12 arithmetic in calculating month differences is that we want the difference 
        between December (12th month) and January (1st) month to be 1.
    '''
    couponTuple = acm.Time().DateToYMD(couponDate)
    candidateDate = None
    minMonthDifference = 100
    
    for date in exCouponList:
        dateTuple = acm.Time().DateToYMD(date)
        monthDifference = (couponTuple[1] - dateTuple[1]) % 12
        if monthDifference < minMonthDifference:
            candidateDate = dateTuple
            minMonthDifference = monthDifference
    
    if candidateDate[1] <= couponTuple[1]:
        year = couponTuple[0]
    else:
        year = couponTuple[0] - 1
        
    return acm.Time().DateFromYMD(year, candidateDate[1], candidateDate[2])
    
def GetExCouponDate(bond, couponDate, adjusted = False):
    ''' Calculate the ex-coupon-day (BCD) for a bond, given a coupon date.
    '''
    exCouponMethod = bond.ExCouponMethod()
    # There are some irregular instruments that should be excluded from the report.
    if exCouponMethod not in ('Calendar Days', 'Business Days', 'AdditionalInfo'):
        return None
    calendar = acm.FCalendar['ZAR Johannesburg']

    if exCouponMethod == 'Calendar Days':
        period = period = '-' + str(bond.ExCouponPeriod())
        exCouponDate = acm.Time().DateAdjustPeriod(couponDate, period)
        
    elif exCouponMethod == 'Business Days':
        period = '-' + str(bond.ExCouponPeriod())
        exCouponDate = calendar.AdjustBankingDays(acm.Time().DateAdjustPeriod(couponDate, period), 0)
        
    elif exCouponMethod == 'AdditionalInfo':
        exCouponDateList = []
        exCoupon1 = bond.AdditionalInfo().ExCoup1()
        if exCoupon1:
            exCouponDateList.append(exCoupon1)
        exCoupon2 = bond.AdditionalInfo().ExCoup2()
        if exCoupon2:
            exCouponDateList.append(exCoupon2)
        exCoupon3 = bond.AdditionalInfo().ExCoup3()
        if exCoupon3:
            exCouponDateList.append(exCoupon3)
        exCoupon4 = bond.AdditionalInfo().ExCoup4()
        if exCoupon4:
            exCouponDateList.append(exCoupon4)
        exCouponDate = CalculateExCouponDate(exCouponDateList, couponDate)
    
    if adjusted:
        #print 'adjusting', exCouponDate
        #Adjusts exCouponDate to the next banking date if it was on a nonbanking day.
        exCouponDate = calendar.AdjustBankingDays(exCouponDate, -1)
        exCouponDate = calendar.AdjustBankingDays(exCouponDate, 1)
        #print 'to', exCouponDate            
    return exCouponDate
    
def GetCouponCashFlow(bond, date):
    ''' Return the cashflow corresponding where date corresponds to the pay date if it exists.  The cashflow end date
        is actually the coupon date, but because this can fall on non-business days we use the pay date.
    '''
    leg = bond.Legs().At(0)
    for cashFlow in leg.CashFlows():
        if ((cashFlow.CashFlowType() == 'Fixed Rate' or cashFlow.CashFlowType()== 'Float Rate') and 
            (cashFlow.StartDate() < date <= cashFlow.EndDate())):
            return cashFlow
    return None
    
def IsCouponDay(bond, date):
    ''' Check to see if date is a coupon day for the bond.
    ''' 
    
    coupon = GetCouponCashFlow(bond, date)
    if coupon:
        return True
    else:
        return False
        
def IsExCouponDay(bond, date):
    ''' Check to see if date is a coupon day for the bond.
    ''' 
    coupon = GetCouponCashFlow(bond, date)
    if date == GetExCouponDate(bond, coupon.EndDate(), True):
        return True
    else:
        return False        

def GetPayDay(bond, couponDate):
    coupon = GetCouponCashFlow(bond, couponDate)
    if coupon:
        return coupon.PayDate()
    return None

def GetLDT(bond, couponDate):
    ''' Return LDT (last day to trade) for the bond corresponding to the couponDate.  
        This is just 4 banking days before the ex-coupon-date.
    '''
    calendar = acm.FCalendar['ZAR Johannesburg']
    coupon = GetCouponCashFlow(bond, couponDate)
    if not coupon:
        return None
    exCouponDate = GetExCouponDate(bond, coupon.EndDate(), True)
    if exCouponDate is None:
        return None
    return calendar.AdjustBankingDays(exCouponDate, -4)

def IsCouponSettlementPeriod(bond, date):
    ''' Check to see if the date is between LDT and pay day for the coupon
    '''
    LDT = GetLDT(bond, date)
    payDay = GetPayDay(bond, date)
    if LDT is not None and (LDT <= date <= payDay):
        return True
    else:
        return False

def IsLDT(bond, date):
    ''' Check to see if date is a coupon day for the bond.
    ''' 
    calendar = acm.FCalendar['ZAR Johannesburg']
    coupon = GetCouponCashFlow(bond, date)
    if coupon:
        ecd = GetExCouponDate(bond, coupon.EndDate(), True)
        if ecd is None:
            return False
        if date == calendar.AdjustBankingDays(ecd, -4):
            return True

    return False

def CalculateCouponAmount_RollingPeriod(bond, nominal):
    ''' Calculate the coupon amount of a bond given a nominal.
    This is an old way:
        Value=Position*Factor*(RollingPeriod/12m)/100
    This function is imprecise and should be osbsolete now.
    '''
    couponRate = bond.CouponRate()
    leg = bond.Legs().At(0)
    rollingPeriodUnit = leg.RollingPeriodUnit()
    if rollingPeriodUnit == 'Months':
        annualCouponRate = 12 / leg.RollingPeriodCount()
        couponAmount = (nominal * couponRate) / (annualCouponRate * float(100))
    else:
        couponAmount = (nominal * couponRate) / float(100)
    return couponAmount
    
def CalculateCouponAmount(instr, nominal, value_date, trades=None):
    ''' Calculate the coupon amount of an instrument given a nominal.
    Instrument should be coupon typed.
    This is a new and correct way:
        Value=Position*Factor*(Days/365)/100
    Days are dependent on proper cashflow.
    If no cashlow for given date is found,
    call original function (which is slightly incorrect for some instruments).
    '''
    cf = GetCouponCashFlow(instr, value_date)
    if not cf or not trades:
        return CalculateCouponAmount_RollingPeriod(instr, nominal)
    cfc = cf.Calculation()
    coupon_amount = 0.0
    for trade in trades:
        if trade.Status() not in ['Simulated', 'Void', 'Terminated']:
            proj = cfc.Projected(acm.FStandardCalculationsSpaceCollection(), trade)
            coupon_amount += proj.Value().Number()
    return coupon_amount

def GetDividend(stock, date, exDivPeriod = False, iterate = False):
    '''
    Returns dividend or dividends or none
    date = run date
    exDivPeriod = indicates whether it is ExDivPeriod 
    iterate = indicates wherether to return multiple dividends, this is to accomdate legacy 
    which could be using this script and yet not catering for multiple dividends.
    '''
    dividendsList = []
    
    if not exDivPeriod and stock.InsType() in ('Stock', 'ETF'):
        dividends = stock.Dividends()
        for dividend in dividends.AsArray():
            if dividend.ExDivDay() == date:
                dividendsList.append(dividend)
        
    elif stock.InsType() in ('Stock', 'ETF'):
        dividends = stock.Dividends()
        for dividend in dividends.AsArray():
            
            if dividend.ExDivDay() <= date and dividend.PayDay() >= date:
                    
                    dividendsList.append(dividend)
                    
                    
    if len(dividendsList)>0:
        #Ensure that the list contains more than one entry and iterate is set to true for multiple dividends.
        if iterate and len(dividendsList)>1 :
            return dividendsList
        else:
            return dividendsList[0]
    else:
        return None
    
def IsExDivDay(instrument, date):
    ''' Check to see if date is the ex div day of the instrument 
    '''
    dividend = GetDividend(instrument, date)
    if dividend:
        return True
    else:
        return False
        
def IsInExDivPeriod(instrument, date):
    dividend = GetDividend(instrument, date, exDivPeriod = True)
    if dividend:
        return True
    else:
        return False
        

# Some of the indices in the PS_Corporate_Actions workbook
CLOSING_POSITION = 5
CA_LDT = 7 # LDT = Last Day of Trading
CA_PAY_DAY = 8
CA_LDT_POSITION = 6
CA_FACTOR = 9
CA_VALUE = 11
def PreProcessXML(reportObj, param, xml):
    """
    Remove zero positions, clean compound numbers and expand multivalue rows.
    """

    def CleanCompoundNumbers(rowselement, is_top=False):
        """
        Remove the nonsensical compound numbers in higher-level rows.

        Currently, one column is cleaned in this way:

        - Closing Position (the higher-level figure wouldn't be a sum of the
          lower-level ones because of LDT-Position based filtering.)
        """
        if not is_top and not rowselement.find('./Row/Rows'):
            # Don't remove the closing position figure on the leaf nodes unless
            # they are root nodes at the same time.
            return
        rows = rowselement.findall('Row')
        for row in rows:
            for column in (CLOSING_POSITION, ):
                for data_format in ('FormattedData', 'RawData'):
                    row.findall('Cells/Cell')[column].find(
                        data_format).text = ''
        for element in rowselement.findall('./Row/Rows'):
            CleanCompoundNumbers(element)

    def RemoveZeroPositions(rowselement):
        """Remove zero LDT position rows from the file."""
        rows = rowselement.findall('Row')
        for row in rows:
            ldt_position_str = row.findall('Cells/Cell')[CA_LDT_POSITION].find(
                    'FormattedData').text
            try:
                ldt_position_is_zero = float(ldt_position_str) == 0.0 
            except (ValueError, TypeError):
                ldt_position_is_zero = False
            if (not ldt_position_str or ldt_position_str == '[]' or
                    ldt_position_is_zero):
                rowselement.remove(row)
        for element in rowselement.findall('./Row/Rows'):
            RemoveZeroPositions(element) # Recurse to deeper levels.
    
    xmltree = ET.fromstring(xml)
    RemoveZeroPositions(xmltree.find('.//Table/Rows/Row/Rows')) # Don't remove the top row
    CleanCompoundNumbers(xmltree.find('.//Table/Rows'), is_top=True)
    new_xml = ET.tostring(xmltree)
    # Declare the columns whose values are (or might be) arrays that should be
    # expanded into multiple rows.
    indices_to_expand = (CA_LDT, CA_PAY_DAY, CA_LDT_POSITION, CA_FACTOR,
            CA_VALUE)
    return PS_XMLReportingToolsMultRows.PreProcessXML(reportObj, param, new_xml,
            indices_to_expand)


def TestCalculateExCouponDate():
    ''' Convert to unit test
    '''
    dateList = [acm.Time().DateFromYMD(1999, 6, 20), acm.Time().DateFromYMD(1999, 12, 20)]
    date = acm.Time().DateFromYMD(2011, 1, 05)
    #print 'Expected Date: 2010-12-20'
    print 'Calculated Date:', CalculateExCouponDate(dateList, date)
    print ''
    
    dateList = [acm.Time().DateFromYMD(1999, 3, 10), acm.Time().DateFromYMD(1999, 9, 10)]
    date = acm.Time().DateFromYMD(2011, 3, 20)
    print 'Expected Date: 2011-03-10'
    print 'Calculated Date:', CalculateExCouponDate(dateList, date)
    print ''

    dateList = [acm.Time().DateFromYMD(1999, 4, 25), acm.Time().DateFromYMD(1999, 10, 25)]
    date = acm.Time().DateFromYMD(2011, 5, 5)
    print 'Expected Date: 2011-04-25'
    print 'Calculated Date:', CalculateExCouponDate(dateList, date)
    print ''

def test():
    bond = acm.FInstrument['ZAR/CMH']
    date = acm.Time().DateFromYMD(2014, 3, 14)
    #coupon = GetCouponCashFlow(bond, date)
    print bond.InsType()
    print 'LDT', GetLDT(bond, date)
    print type(bond)
    print 'copoun=', CalculateCouponAmount_RollingPeriod(bond, 10000000)
    print GetCouponCashFlow(bond, date)
    #print 'Div=', GetDividend(bond, date,True,True)
    #print 'GetExCouponDate', GetExCouponDate(bond, coupon.EndDate(), True)
    
    '''leg = bond.Legs().At(0)
    print leg.RollingPeriodUnit()
    print leg.RollingPeriodCount()
    print CalculateCouponAmount(bond, 10000000)
    print IsLDT(bond, date)
    print GetLDT(bond, date)'''
    
#test()

