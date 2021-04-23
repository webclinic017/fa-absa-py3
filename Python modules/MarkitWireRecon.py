'''----------------------------------------------------------------------------------------------------------
MODULE                  :       MarkitWireRecon
PROJECT                 :       OTC Clearing
PURPOSE                 :       This module serves the purpose of highlighting breaks as a reconciliation between Markit Wire and Front Arena
                                The source file from Markit Wire is in a CSV format and downloaded via the DealExtractor on the production AMWI server
                                Extracted file name from Markit Wire: DEbaseline.csv
DEPARTMENT AND DESK     :       ABSA Capital / IRD Desk and Prime Services Desk
REQUESTER               :       Manus van den Berg
DEVELOPER               :       Arthur Grace
CR NUMBER               :       CHNG0002411366
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2014-11-11    CHNG0002275049    Arthur Grace                    Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module provides a recon between Markit Wire and Front Arena. It displays the results in an output file specific in parameters, 
    and to the log for quick review
'''

import acm
import ael
import csv
import string
import FLogger
from datetime import datetime
logger = FLogger.FLogger('MarkitWireRecon')
expiry = ael.date_today()

'''
Different possible states on Markit Wire
New - Cancelled - Amended - New-Match - New-Novated - PrimeBrokered - New-PrimeBrokered - Novated - Novated-Partial - Clearing
'''

def MarkitWireID(value):
    #the various versions of the concatenated entry for MW deals
    #this method is used to clean out the Markit Wire Trade ID stored on the add info of an IRS and FRA
    value = value.replace('MW', '')
    value = value.replace('S1', '')
    value = value.replace('S2', '')
    value = value.replace('S3', '')
    value = value.replace('S4', '')
    value = value.replace('V1', '')
    value = value.replace('V2', '')
    value = value.replace('V3', '')
    value = value.replace('V4', '')
    value = value.replace('V5', '')
    value = value.replace('V6', '')
    value = value.replace('V7', '')
    value = value.replace('aa', '')
    value = value.replace('ab', '')
    value = value.replace('ac', '')
    value = value.replace('ad', '')
    value = value.replace('ae', '')
    value = value.replace('af', '')
    value = value.replace('ag', '')
    value = value.replace('ah', '')
    value = value.replace('Amended', '')
    value = value.replace('Cancelled', '')
    value = value.replace('New', '')
    value = value.replace('-Novated', '')
    value = value.replace('-PrimeBrokere', '')
    value = value.replace('T', '')
    value = value.replace('d', '')
    value = value.replace('Clearing', '')
    value = value.replace('-Match', '')
    value = value.replace('*', '')
    value = value.replace('**', '')
    value = value.replace('ai', '')
    value = value.replace('V8', '')
    value = value.replace('Novate', '')
    value = value.replace('-Partial', '')
    return value

def IgnoreExpiredTrades(fTrade):
    try:
        if fTrade:
            for leg in fTrade.Instrument().Legs():    
                if str(datetime.strptime(leg.EndDate(), '%Y-%m-%d')) < expiry.to_string('%Y-%m-%d') :
                    return 'Xpired-'
                else:
                    return ''
        return ''
    except StandardError, e:
        print 'Ignore Expired Trades', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def LegsFirstFixing(fTrade, firstFixing):
    try:
        foundFirstFixing=False
        firstFixing=float(firstFixing)*100
        for leg in fTrade.Instrument().Legs():
            for cflows in leg.CashFlows():
                for reset in cflows.Resets():
                    if round(reset.FixingValue(), 3)==round(firstFixing, 3):
                        foundFirstFixing=True
        return foundFirstFixing   
    except StandardError, e:
        print 'Legs First Fixing', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def LegsFirstFixingRate(fTrade): #This function provides the last fixing value
    try:
        fixingValue = 0
        for leg in fTrade.Instrument().Legs():
            for cFlows in leg.CashFlows():
                for reset in cFlows.Resets():
                    fixingValue = reset.FixingValue()
        return fixingValue
    except StandardError, e:
        print 'Legs First Fixing Rate', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetFloatLegSpread(fTrade):
    try:
        for leg in fTrade.Instrument().Legs():
            if leg.LegType()=='Float':
                return leg.Spread()
        return 0
    except StandardError, e:
        print 'Get Float Leg Spread', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetCalendarList(fTrade, calendarSet): #Is duplicated values in the list fine?
    calendarList = ''
    for leg in fTrade.Instrument().Legs():
        if calendarSet=='Pay':
            if leg.PayCalendar():
                calendarList=leg.PayCalendar().BusinessCenter()
            if leg.Pay2Calendar():
                calendarList+=';'+leg.Pay2Calendar().BusinessCenter()
            if leg.Pay3Calendar():
                calendarList+=';'+leg.Pay3Calendar().BusinessCenter()
        elif calendarSet=='Fixing':
            if leg.ResetCalendar():
                calendarList=leg.ResetCalendar().BusinessCenter()
            if leg.Reset2Calendar():
                calendarList+=';'+leg.Reset2Calendar().BusinessCenter()
            if leg.Reset3Calendar():
                calendarList+=';'+leg.Reset3Calendar().BusinessCenter()
    if calendarList == '':
        return 'Target'
    else:
        return calendarList 
    
def GetPayCalendars(fTrade):
    try:
        calendars=[]
        for leg in fTrade.Instrument().Legs():
                if leg.PayCalendar():
                    calendars.append(leg.PayCalendar().BusinessCenter())
                else:
                    calendars.append('') 
                if leg.Pay2Calendar():    
                    calendars.append(leg.Pay2Calendar().BusinessCenter())
                else:
                    calendars.append('')
                if leg.Pay3Calendar():
                    calendars.append(leg.Pay3Calendar().BusinessCenter())
                else:
                    calendars.append('')
        return calendars
    except StandardError, e:
        print 'Get Pay Calendars', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
        
def GetResetCalendars(fTrade):
    try:
        calendars=[]
        for leg in fTrade.Instrument().Legs():
                if leg.ResetCalendar():
                    calendars.append(leg.ResetCalendar().BusinessCenter())
                else:
                    calendars.append('') 
                if leg.Reset2Calendar ():    
                    calendars.append(leg.Reset2Calendar().BusinessCenter())
                else:
                    calendars.append('')
                if leg.Reset3Calendar ():
                    calendars.append(leg.Reset3Calendar().BusinessCenter())
                else:
                    calendars.append('')
        return calendars
    except StandardError, e:
        print 'Get Reset Calendars', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
        
def TradeStatuses(entry, MWOrFront):
    try:
        if MWOrFront == 'MW':
            if entry == 'Cancelled':
                return 'Cancelled'
        if MWOrFront == 'FA':
            if entry == 'Terminated':
                return 'Cancelled'
            elif entry == 'Void':
                return 'Cancelled'
            elif entry == 'BO-BO Confirmed':
                return 'New'
            elif entry == 'BO Confirmed':
                return 'New'
        return ''
    except StandardError, e:
        print 'Trade Statuses', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def GetPublicHolidays():
    try:
        publicHolidays=[]
        days=ael.Calendar['ZAR Johannesburg']
        for day in days.dates():
            publicHolidays.append(str(day.daynbr))
        return publicHolidays
    except StandardError, e:
        print 'Get Public Holidays', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def GetFloatReference(fTrade, frateindex, tenor):
    try:
        for leg in fTrade.Instrument().Legs():
            if leg.LegType()=='Float':
                if leg.FloatRateReference().Name()!=frateindex[0:10]+tenor:
                    return 1
        return 0
    except StandardError, e:
        print 'Get Float Reference', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetTenor(fTrade):
    try:
        for leg in fTrade.Instrument().Legs():
            if leg.LegType()=='Float':
                return leg.FloatRateReference().Name()
        return ''
    except StandardError, e:
        print 'Get Tenor', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def PaymentCheck(fTrade, typePayment): #You only need the first payment that match?
    try:
        for payment in fTrade.Payments():
            if payment.Type()==typePayment:
                return payment.Amount()
        return 0
    except StandardError, e:
        print 'Payment Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetBrokerageCalc(fTrade, mwBrokerage, faBrokerage):
    try:
        brokerage = []
        if faBrokerage<0:
            faBrokerage=faBrokerage*-1
        if round(mwBrokerage, 3)!=round(faBrokerage, 3):
            #FRAs fees on front of trade ticket
            if fTrade.Fee():
                faBrokerage = fTrade.Fee()  #Do you need to check for FRAs?
                if faBrokerage < 0:
                    faBrokerage = faBrokerage * -1
                if round(mwBrokerage, 3)!=round(faBrokerage, 3):
                    return 1
        return 0
    except StandardError, e:
        print 'Brokerage Calc', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetBrokerageResults(fTrade, mwTrade, mwAmount):
    try:
        if mwAmount!='':
            if GetBrokerageCalc(fTrade, float(mwAmount), PaymentCheck(fTrade, 'Broker Fee'))==1:
                return IgnoreExpiredTrades(fTrade)+'Brokerage Mismatch | Brokerage Value| FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Fee: '+str(PaymentCheck(fTrade, 'Broker Fee'))+' | MW Fee: '+str(mwAmount)
        return ''
    except StandardError, e:
        print 'Get Brokerage Results', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetMissingOptionalKey(fTrade, mwTrade, optionalkey, mwfullkey):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if optionalkey=='' and mwfullkey!='':
                return IgnoreExpiredTrades(fTrade)+'Optional Key | No Optional Key | FATrade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | | '
        return ''
    except StandardError, e:
        print 'Get Missing Optional Key', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetRateIndexCheck(fTrade, mwTrade, mwRateIndex, faRateIndex):
    try:
        if GetFloatReference(fTrade, mwRateIndex, faRateIndex)==1:
            if mwRateIndex != 'EUR-EURIBOR-Reuters':
                return IgnoreExpiredTrades(fTrade)+'Index Mismatch | Rate Index | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Index: '+GetTenor(fTrade)+' | MW Index: '+mwRateIndex
        return ''
    except StandardError, e:
        print 'Get Rate Index Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetPaymentCalendarCheck(fTrade, mwTrade, mwPaymentCalendars):
    try:
        calendars = mwPaymentCalendars.split(';')
        for calendar in calendars:
            if calendar not in (GetPayCalendars(fTrade)):
                if mwPaymentCalendars != 'EUTA;':
                    return IgnoreExpiredTrades(fTrade)+'Calendar Mismatch | Pay Calendar Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Calendar: '+GetCalendarList(fTrade, 'Pay')+' | MW Calendar: '+mwPaymentCalendars
        return ''
    except StandardError, e:
        print 'Get Calendar Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
        
def GetResetCalendarCheck(fTrade, mwTrade, mwResetCalendars):
    try:
        calendars = mwResetCalendars.split(';')
        for calendar in calendars:
            if calendar!='':
                if calendar not in (GetResetCalendars(fTrade)):
                    if mwResetCalendars != 'EUTA;':
                        return IgnoreExpiredTrades(fTrade)+'Calendar Mismatch| Reset Calendar Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Calendar: '+GetCalendarList(fTrade, 'Fixing')+' | MW Calendar: '+mwResetCalendars
        return ''
    except StandardError, e:
        print 'Get Calendar Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def GetSpreadCheck(fTrade, mwTrade, mwSpreadFloat):
    try:
        faSpread=GetFloatLegSpread(fTrade)
        if mwSpreadFloat!='':
            if float(mwSpreadFloat) > 0:
                mwSpread = float(mwSpreadFloat) * 100
                if round(faSpread, 2) != round(mwSpread, 2):
                    return IgnoreExpiredTrades(fTrade)+'Spread Mismatch | Float Spread Issue | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Spread: '+str(faSpread)+' | MW Spread: '+str(mwSpreadFloat)
        return ''
    except StandardError, e:
        print 'Get Spread Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetPortfolioCheck(fTrade, mwTrade, mwPortfolio):
    try:
        if fTrade.OptionalKey()!='':
            if mwPortfolio!=fTrade.Portfolio().Name():
                return IgnoreExpiredTrades(fTrade)+'Portfolio Mismatch | Portfolio Match Issue | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Portfolio: '+fTrade.Portfolio().Name()+' | MW Portfolio: '+mwPortfolio
        return ''
    except StandardError, e:
        print 'Get Portfolio Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetFirstFixingCheck(fTrade, mwTrade, mwFirstFixing):
    try:
        if mwFirstFixing!='':
            if LegsFirstFixing(fTrade, mwFirstFixing)==False:
                return IgnoreExpiredTrades(fTrade)+'First Fixing | Issue On First Fixing | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA First Fixing: '+str(LegsFirstFixingRate(fTrade))+' | MW First Fixing: '+str(float(mwFirstFixing)*100)
        return ''
    except StandardError, e:
        print 'Get First Fixing Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetStatusChecks(fTrade, mwTrade, mwStatus):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if mwStatus=='Cancelled':
                if mwStatus!=TradeStatuses(fTrade.Status(), 'FA'):
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch | Cancellation Status | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Status: '+fTrade.Status()+' | MW Status: '+mwStatus
            elif mwStatus in('Amended', 'New-Novated'):
                if fTrade.Status()!='BO-BO Confirmed':
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch | Amended Status | FA Trade: '              +str(fTrade.Oid())+     ' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Status: '+fTrade.Status()+' | MW Status: '+mwStatus
            elif mwStatus in ('New'):
                if mwStatus!=TradeStatuses(fTrade.Status(), 'FA'):
                    if fTrade.Type()=='Closing':
                        return IgnoreExpiredTrades(fTrade)+'Status Mismatch | Closing Trade | FA Trade: '              +str(fTrade.Oid())+     ' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Status: '+fTrade.Status()+' | MW Status: '+mwStatus
            elif mwStatus in ('New-PrimeBrokered'):
                if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch | New-PB Manual Update | FA Trade: '           +str(fTrade.Oid())+     ' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Status: '+fTrade.Status()+' | MW Status: '+mwStatus                
            if fTrade.Status() in ('Simulated', 'BO Confirmed'):
                return IgnoreExpiredTrades(fTrade)+'Status Mismatch | Unexpected FA status | FA Trade: '      +str(fTrade.Oid())+     ' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Status: '+fTrade.Status()+' | MW Status: '+mwStatus 
        return ''
    except StandardError, e:
        print 'Get Status Checks', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetStartDateCheck(MMA, fTrade, mwTrade, faStartDate, mwTradeStatus, mwStartDate):
    try:
        publicHolidays=GetPublicHolidays()
        if fTrade.Status() not in ('Void', 'Terminated') and mwTradeStatus != 'Cancelled':
            dmw = datetime.strptime(mwStartDate, '%Y-%m-%d')
            if str(dmw) != str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')):
                dateobj = mwStartDate.split('-')
                d = datetime(int(dateobj[0]), int(dateobj[1]), int(dateobj[2]))
                if d.weekday() not in (5, 6):
                    if str(mwStartDate) not in publicHolidays:
                        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
                            if MMA == 'A':
                                return IgnoreExpiredTrades(fTrade)+'Start End Date | Start Date Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+ ' | Create user: '+fTrade.CreateUser().Name()+' | Update user: '+fTrade.UpdateUser().Name()+' | FA start date: '+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+' | MW start date: '+str(dmw).replace(' 00:00:00', '')
                            elif MMA == 'B':
                                return IgnoreExpiredTrades(fTrade)+'Start End Date | End Date Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+ ' | Create user: '+fTrade.CreateUser().Name()+' | Update user: '+fTrade.UpdateUser().Name()+' | FA End date: '+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+' | MW End date: '+str(dmw).replace(' 00:00:00', '')
                            return IgnoreExpiredTrades(fTrade)+'Start End Date | OTHER Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+ ' | Create user: '+fTrade.CreateUser().Name()+' | Update user: '+fTrade.UpdateUser().Name()+' | FA start date: '+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+' | MW start date: '+str(dmw).replace(' 00:00:00', '')
        return ''
    except StandardError, e:
        print 'Get Start Date Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetNominalCheck(fTrade, mwTrade, faNominal, mwNominal):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if faNominal < 0:
                faNominal = faNominal * -1
            if round(faNominal, 2)!=round(mwNominal, 2):
                if int(faNominal-mwNominal) == 0:
                    return 'Excluded | Minor Nominal Mismatch | FA Trade:'+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Nominal: '+str(faNominal)+' | MW Nominal: '+str(mwNominal)
                else:
                    return IgnoreExpiredTrades(fTrade)+'Nominal Mismatch | Nominal Mismatch | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Nominal: '+str(faNominal)+' | MW Nominal: '+str(mwNominal)
        return ''
    except StandardError, e:
        print 'Get Nominal Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetRateCheck(fTrade, mwTrade, faRate, mwRate):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if round(float(mwRate)*100, 4)!=round(float(faRate), 4):
                if round(float(faRate), 4)/round(float(mwRate)*100, 4) > 1:
                    return IgnoreExpiredTrades(fTrade)+'Rate Mismatch | Rate Concern | FA Trade: '+str(fTrade.Oid())+' | MW Trade: '+str(mwTrade)+' | Acquirer: '+fTrade.Acquirer().Name()+ ' | Create User: '+fTrade.CreateUser().Name()+' | Update User: '+fTrade.UpdateUser().Name()+' | FA Rate: '+str(faRate)+' | MW Rate: '+str(float(mwRate)*100)
        return ''
    except StandardError, e:
        print 'Get Rate Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetNoTradeMatchesToBeDone(selection, reader, parameters):
    try:
        mwTrades = [] #to match all MW trades between MW and FA
        FATrades = [] #to match all FA trades between MW and FA
        mwTradeDetails = [] #house the MW dictionary objects with keys
        FATradeDetails = [] #house the FA dictionary objects with keys
        MWIndex = 0 #Find the MW record in list
        FAIndex = 0 #Find the Arena record in list
        MWDict = {} #Store the key fields from Markit Wire required for the recon
        FADict = {} #Store the key fiedls from the Front Arena report required for the recon
        MWRecon = [] #capture all the records trapped on actual breaks and run them into a file when done

        #Records from MW
        for read in reader:
            if read[2] not in ('absa_swcancel1', 'absa_swcancel2', 'absa_swcancel3', 'absa_swcancel4', 'absa_swcancel5', 'absa_swcancel6', 'absa_swcancel7', 'absa_swcancel8'): #ignore specific deal bookings from Markit Wire which are not relevant
                if read[2] not in ('Absa Listener 1', 'Absa Listener 2', 'Absa Listener 3', 'Absa Listener 4', 'Absa Listener 5'):
                    mwTrades.append(read[0])
                    #Trade id        #Trader          #Portfolio       #Status          #Trade Date       #Start Date       #End Date         #Direction        #Notional         #Rate             #Additional Amount / Curr             #Payment date      #Payment Type
                    #read[0]         read[2]          read[3]          read[6]          read[7]           read[15]          read[16]          read[10]          read[22]          read[23]          read[163]            read[164]        read[165]          read[166])
                    MWDict = {'TradeId':read[0],'Nominal':read[22],'Status':read[6],'TradeDate':read[7],'Rate':read[23],'Trader':read[2],'StartDate':read[15],'EndDate':read[16],'Portfolio':read[3],'BookingState':read[242],'FirstFixing':read[88],'SpreadFloat':read[89],'PaymentHolidays':read[86],'ValueTenor':read[72],'FixedFrequency':read[74],'FloatFrequency':read[78],'FRateIndex':read[24],'BrokerageAmount':read[19],'FixingHolidays':read[85]}
                    mwTradeDetails.append(MWDict)
        
        #Records from Front Arena as per query
        for selectionFA in selection[1][0]:  
            FATrades.append(MarkitWireID(selectionFA[3]))
            FADict = {'TradeId':MarkitWireID(selectionFA[3]),'Nominal':selectionFA[7],'Status':selectionFA[5],'TrdNbr':selectionFA[0],'TradeDate':selectionFA[6],'InsType':selectionFA[1],'OptionalKey':selectionFA[4],'Quantity':selectionFA[13],'FixedRate':selectionFA[12],'MWKey':selectionFA[3],'StartDate':selectionFA[10],'EndDate':selectionFA[11],'Portfolio':selectionFA[9],'MWFullKey':selectionFA[14],'SpreadFloat':selectionFA[15],'PayCal1':read[16],'PayCal2':read[17],'PayCal3':read[18],'TradeType':read[19]}
            FATradeDetails.append(FADict)

        userCreatedTrade=[]
        
        for mwTrade in mwTrades:
            if mwTrade in FATrades:
                # find the FA trade[s] based on the key location on MW trade ID
                arenaTradesSeriesFind=[item for item in range(len(FATrades)) if FATrades[item] == mwTrade]
                lengthReset=0
                #step through the specific Front Arena trades linked to this MW trade
                for arenaListIndex in arenaTradesSeriesFind:
                    result=''
                    mwInit=0
                    try:
                        #Make sure the MW trade id in FA trade ticket is cleansed properly
                        #This would need to be a valid integer value
                        mwInit=int(mwTradeDetails[MWIndex]['TradeId'])
                    except:
                        print 'Error: Check cleansing of trade id ********************************:', mwTradeDetails[MWIndex]['TradeId']
                        MWRecon.append('Error: Check cleansing of trade id ********************************: '+mwTradeDetails[MWIndex]['TradeId'])
                        
                    #initialize the trade object for overall trade evaluation further than report output
                    fTrade = acm.FTrade[FATradeDetails[arenaListIndex]['TrdNbr']]
                    
                    lengthReset=lengthReset+1
                    
                    #Brokerage Fee
                    if parameters['MWBrokerageCheck']:
                        if lengthReset==len(arenaTradesSeriesFind):
                            result = GetBrokerageResults(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['BrokerageAmount'])
                            if result!='':
                                MWRecon.append(result)
                                
                    #Optionl Key Population Check
                    if parameters['MWOptionalKeyCheck']:
                        if lengthReset ==len(arenaTradesSeriesFind):
                            result = GetMissingOptionalKey(fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['OptionalKey'], FATradeDetails[arenaListIndex]['MWFullKey'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Rate Index Check
                    if parameters['MWIndexCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            if FATradeDetails[arenaListIndex]['InsType']=='FRA':
                                result = GetRateIndexCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FRateIndex'], mwTradeDetails[MWIndex]['ValueTenor'])
                                if result!='':
                                    MWRecon.append(result)
                            elif FATradeDetails[arenaListIndex]['InsType']=='Swap':
                                result = GetRateIndexCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FRateIndex'], mwTradeDetails[MWIndex]['FloatFrequency'])
                                if result!='':
                                    MWRecon.append(result)
                    
                    #Calendar checks
                    if parameters['MWHolidayCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetPaymentCalendarCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['PaymentHolidays'])
                            if result!='':
                                MWRecon.append(result)
                                
                    if parameters['MWFixingCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetResetCalendarCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FixingHolidays'])
                            if result!='':
                                MWRecon.append(result)
                        
                    #Spread check
                    if parameters['MWSpreadCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetSpreadCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['SpreadFloat'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Portfolio check
                    if parameters['MWPortfolioCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetPortfolioCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['Portfolio'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #First fixing
                    if parameters['MWFirstFixCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetFirstFixingCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FirstFixing'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Check for cancelled trades on MW that are not cancelled on Front Arena
                    if parameters['MWStatusCheck']==True:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetStatusChecks(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['Status'])
                            if result!='':
                                MWRecon.append(result)
                            
                    #Start and End Date Check
                    if parameters['MWStartEndDateCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetStartDateCheck('A', fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['StartDate'], mwTradeDetails[MWIndex]['Status'], mwTradeDetails[MWIndex]['StartDate'])
                            if result!='':
                                MWRecon.append(result)
                            result = GetStartDateCheck('B', fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['EndDate'], mwTradeDetails[MWIndex]['Status'], mwTradeDetails[MWIndex]['EndDate'])
                            if result!='':
                                MWRecon.append(result)
                         
                    #Nominal check
                    if parameters['MWNominalCheck']==True:
                        if lengthReset == len(arenaTradesSeriesFind):
                            if FATradeDetails[arenaListIndex]['OptionalKey'] != '':
                                if mwTradeDetails[MWIndex]['Status'] not in ('Cancelled', 'Novated') and FATradeDetails[arenaListIndex]['Status'] not in ('Terminated', 'Void'):
                                    if FATradeDetails[arenaListIndex]['InsType'] == 'FRA':
                                        result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Quantity']), float(mwTradeDetails[MWIndex]['Nominal']))
                                        if result!='':
                                            MWRecon.append(result)
                                    else:
                                        if float(FATradeDetails[arenaListIndex]['Nominal'])!=0:
                                            result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Nominal']), float(mwTradeDetails[MWIndex]['Nominal']))
                                        elif float(FATradeDetails[arenaListIndex]['Quantity'])!=0:
                                            result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Quantity']), float(mwTradeDetails[MWIndex]['Nominal']))
                                        if result!='':
                                            MWRecon.append(result)
                                                
                    #Rate check
                    if parameters['MWRateCheck']==True:                
                        if lengthReset == len(arenaTradesSeriesFind):
                            if float(FATradeDetails[arenaListIndex]['FixedRate']) != 0:
                                result = GetRateCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['FixedRate']), float(mwTradeDetails[MWIndex]['Rate']))                                
                                if result!='':
                                    MWRecon.append(result)
                lengthReset=0
                
            MWIndex+=1
            
        #print 'In this recon ',len(mwTrades),' Markitwire trades and ',len(FATrades),'FA TRADE STATES were analysed.'
        #print len(MWRecon),' breaks were found in this recon.'
        #print 'BreakGroup | BreakType | FATrade | mwTrade | Acquirer | CreateUser | UpdateUser | FrontValue | MarkitWireValue'
        
        MWRecon.append('#1   '+str(len(mwTrades))+' MarkitWire TRADES analysed.')
        MWRecon.append('#2   '+str(len(FATrades))+' Front Arena TRADE STATES trades analysed.')
        MWRecon.append('#3   '+str(len(MWRecon)-2)+' breaks identified.')        
        MWRecon.append('BreakGroup | BreakType | FATrade | mwTrade | Acquirer | CreateUser | UpdateUser | FrontValue | MarkitWireValue')        
        print 'Done adding entries to the Markit Wire Recon ', len(MWRecon)
        MWRecon.sort()
        if parameters['MWUserCreatedTradesCheck']:  
            return userCreatedTrade
        else:
            return MWRecon
    except StandardError, e:
        print 'GetNoTradeMatchesToBeDone', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def LegacyMarkitWire(fromDate, toDate):
    query = """select t.trdnbr,i.instype,ais.field_name,ai.value,t.optional_key,t.status, \
          t.time,nominal_amount(t),t.quantity,port.prfid,l.start_day,l.end_day,l.fixed_rate,t.quantity*1000000 'QuantityMW',ai.value 'MWFullKey',l.spread,l.pay_calnbr,l.pay2_calnbr,l.pay3_calnbr,t.type \
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais,portfolio port,leg l \
          where t.insaddr = i.insaddr \
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
          and ais.field_name = 'MarkitWire' and ai.value like 'MW%' \
          and i.instype in ('FRA','Swap') \
          and l.insaddr = i.insaddr \
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated','Simulated','Void') \
          and t.prfnbr = port.prfnbr \
          and t.time between '"""+fromDate+"""' and '"""+toDate+"""' \
          and l.fixed_rate~=0 \
          order by t.trdnbr asc """
    return query

def AMWI_query(fromDate, toDate):
    query = """select t.trdnbr,i.instype,ais.field_name,ai.value,t.optional_key,t.status, 
          t.time,nominal_amount(t),t.quantity,port.prfid,l.start_day,l.end_day,l.fixed_rate,t.quantity*1000000 'QuantityMW',ai.value 'MWFullKey',l.spread,l.pay_calnbr,l.pay2_calnbr,l.pay3_calnbr 
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais,portfolio port,leg l 
          where t.insaddr = i.insaddr 
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr 
          and ais.field_name = 'CCPmiddleware_id' and ai.value ~=''
          and i.instype in ('FRA','Swap') 
          and l.insaddr = i.insaddr 
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated','Simulated','Void') 
          and t.prfnbr = port.prfnbr 
          and t.time between '"""+fromDate+"""' and '"""+toDate+"""' \
          and l.fixed_rate~=0 
          order by t.trdnbr asc"""
    return query

ael_variables = \
    [
        ['SourceCSVFile', 'Source CSV file', 'string', None, 'Y:\Jhb\FAReports\FA_MarkitWire\DealExtractor\DEbaseline.csv', 1],
        ['OutputCSVFile', 'Output CSV file', 'string', None, 'Y:\Jhb\FAReports\FA_MarkitWire\DealExtractor\DealExtractorOutput.csv', 1],
        ['FromDate', 'From Date', 'string', None, '2014-01-01', 1],
        ['ToDate', 'To Date', 'string', None, ael.date_today().to_string('%Y-%m-%d'), 1],
        ['ToExpiry', 'To Expiry', 'string', None, ael.date_today().add_days(-30), 1],
        ['MWStatusCheck', 'Markit Wire Status Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWOddStatusCheck', 'Front Arena Odd MW Status Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWStartEndDateCheck', 'Front Arena Start Date Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWRateCheck', 'Front Arena Rate Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWNominalCheck', 'Front Arena Nominal Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWFirstFixCheck', 'Front Arena First Fixing Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWPortfolioCheck', 'Front Arena Portfolio Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWSpreadCheck', 'Front Arena Float Spread Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWIndexCheck', 'Front Arena Index Tenor Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWHolidayCheck', 'Front Arena Payment Holiday Calendar Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWFixingCheck', 'Front Arena Fixing Holiday Calendar Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWOptionalKeyCheck', 'Front Arena Optional Key Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWBrokerageCheck', 'Front Arena Brokerage Fee Check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWUserCreatedTradesCheck', 'Front Arena User Created Trades', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWOptionalCCPKeyCheck', 'Front Arena New CCP Key Concern', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWAMWI', 'Front Arena AMWI check', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1]
    ]

def ael_main(parameters):

   #Front Arena records from current Synthesis Adapter
    expiry = parameters['ToExpiry']
    
    q = LegacyMarkitWire(str(parameters['FromDate']), str(parameters['ToDate']))
    
    if parameters['MWAMWI']:
        print 'Generating AMWI query'
        q = AMWI_query(str(parameters['FromDate']), str(parameters['ToDate']))
        print q

    selection = ael.asql(q)
    
    #get the deal extractor details
    try:
        f = open(parameters["SourceCSVFile"], 'rt')
        
        reader = csv.reader(f)
        fResults = open(parameters['OutputCSVFile'], 'w')
        print 'Recon Started'
        fResults.write('#    Reonciliation between MarkitWire and Front Arena.'+'\n')
        fResults.write('#    Date Range: '+str(parameters['FromDate'])+' to '+str(parameters['ToDate'])+'\n')
        for entry in GetNoTradeMatchesToBeDone(selection, reader, parameters):
            print entry
            fResults.write(entry+'\n')
        fResults.close()
        f.close()
    except StandardError, e:
        print str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
