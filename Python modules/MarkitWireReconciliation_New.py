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
2015-05-04    CHNG0002783243    Arthur Grace                    Amendments and new features

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
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
DATEFORMAT = '%Y-%m-%d'

import xml.dom.minidom as xml
configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'AMWI_Mappings')
config = xml.parseString(configuration)

mappings = config.getElementsByTagName("Mappings")

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
    value = value.replace('V8', '')
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
    value = value.replace('Novated', '')
    value = value.replace('-PrimeBrokere', '')
    value = value.replace('-PrimeBrokered', '')
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

def CurrentNominal(fTrade, date, curr):
    cashflows = []
    currentNominal = 0
    
    date = datetime.strptime(date, DATEFORMAT)
    sdate = datetime.strptime('0001-01-01', DATEFORMAT)
    edate = datetime.strptime('0001-01-01', DATEFORMAT)
    
    legs = fTrade.Instrument().Legs()
    from_curr = fTrade.Instrument().Currency()
    
    for l in legs:
        for c in l.CashFlows():
            if ((c.CashFlowType() != 'Fixed Amount') and (c.CashFlowType() != 'Redemption Amount') and 
                (c.CashFlowType() != 'Interest Reinvestment')):
                cashflows.append(c)
    
    for cf in cashflows:
        cf_end = datetime.strptime(cf.EndDate(), DATEFORMAT)
        cf_start = datetime.strptime(cf.StartDate(), DATEFORMAT)
        if cf.CashFlowType()=='Float Rate':
            
            if (date >= cf_start) and (date < cf_end) and (sdate != cf_start) and (edate != cf_end):
                calc = cf.Calculation()
                sdate = cf.StartDate()
                edate = cf.EndDate()
                
                if fTrade.RecordType() == 'Trade':
                    currentNominal = currentNominal + (calc.Nominal(cs, fTrade, from_curr).Value().Number())
                
    return currentNominal
    
def NominalDirectionChangeCheck(fTrade, mwTrade):
    nominalReporting = ''
    if not fTrade.IsInfant():
        if fTrade.Oid() > 0:
            if fTrade.Contract():
                if fTrade.Oid()!= fTrade.Contract().Oid():
                    currentNominal = CurrentNominal(fTrade, acm.Time.DateToday(), fTrade.Instrument().Currency())
                    newNominal = CurrentNominal(fTrade.Contract(), acm.Time.DateToday(), fTrade.Instrument().Currency())
                    if fTrade.Status() not in ('Terminated', 'Void') and fTrade.Contract().Status() not in ('Terminated', 'Void'):
                        if currentNominal < 0 and newNominal > 0:
                            nominalReporting = 'Nominal direction mismatch|Nominal direction|Current FA Trade: '+str(fTrade.Contract().Oid())+'|'+mwTrade+'||||Current nominal '+str(currentNominal)+'|||||New FA Trade: '+str(fTrade.Oid())+'|New nominal: '+str(newNominal)+'\n'
                        elif currentNominal > 0 and newNominal < 0:
                            nominalReporting = nominalReporting + 'Nominal direction mismatch | Nominal direction |'+str(fTrade.Contract().Oid())+' | MW Trade '+mwTrade+'||||Current nominal '+str(currentNominal)+'|||||New FA Trade '+str(fTrade.Oid())+' | New nominal '+str(newNominal)
                        elif currentNominal != newNominal:
                            nominalReporting = nominalReporting+ 'Nominal mismatch | Nominal mismatch | FA Trade '+str(fTrade.Contract().Oid())+' | MW Trade '+mwTrade+'||||Current nominal '+str(currentNominal)+'|||||New FA Trade '+str(fTrade.Oid())+' | New nominal '+str(newNominal)
    return nominalReporting

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

def GetMissingMarkitWireTrades(mwTradeID, Status, StartDate, EndDate, TradeDate, UserID, OurBIC, CptyBIC):
    if EndDate > expiry.to_string('%Y-%m-%d'):
        return 'MW Only Trades|Trade Not On Front||'+str(mwTradeID)+'|||||'+Status+'|'+StartDate+'|'+EndDate+'|'+TradeDate[0:10]+'|||'+UserID+'|'+OurBIC+'|'+CptyBIC        
    if EndDate <= expiry.to_string('%Y-%m-%d'):
        return 'Xpired-MW Only Trades|Trade Not On Front||'+str(mwTradeID)+'|||||'+Status+'|'+StartDate+'|'+EndDate+'|'+TradeDate[0:10]+'|||'+UserID+'|'+OurBIC+'|'+CptyBIC                

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
            elif entry == 'FO Confirmed':
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
        if fTrade.Fee() > 0 or fTrade.Fee() < 0:
            return 1
        return 0
    except StandardError, e:
        print 'Brokerage Calc', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetBrokerageResults(fTrade, mwTrade, mwAmount, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if mwAmount!='':
            if GetBrokerageCalc(fTrade, float(mwAmount), PaymentCheck(fTrade, 'Broker Fee'))==1:
                return IgnoreExpiredTrades(fTrade)+'Brokerage On Face of Ticket|Brokerage Value| FA Trade|'+str(fTrade.Oid())+'| MW Trade|'+str(mwTrade)+'|'+str(fTrade.Fee())+'|'+str(fTrade.TradeTime())
        return ''
    except StandardError, e:
        print 'Get Brokerage Results', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetMissingOptionalKey(fTrade, mwTrade, optionalkey, mwfullkey, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if optionalkey=='' and mwfullkey!='':
                return IgnoreExpiredTrades(fTrade)+'Optional Key|No Optional Key|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'||'+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Missing Optional Key', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetRateIndexCheck(fTrade, mwTrade, mwRateIndex, faRateIndex, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if GetFloatReference(fTrade, mwRateIndex, faRateIndex)==1:
            if mwRateIndex != 'EUR-EURIBOR-Reuters':
                return IgnoreExpiredTrades(fTrade)+'Index Mismatch|Rate Index|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Index: '+GetTenor(fTrade)+'|MW Index: '+mwRateIndex+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Rate Index Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetPaymentCalendarCheck(fTrade, mwTrade, mwPaymentCalendars, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        calendars = mwPaymentCalendars.split(';')
        for calendar in calendars:
            if calendar not in (GetPayCalendars(fTrade)):
                if mwPaymentCalendars != 'EUTA;':
                    return IgnoreExpiredTrades(fTrade)+'Calendar Mismatch|Pay Calendar Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+GetCalendarList(fTrade, 'Pay')+'|'+mwPaymentCalendars+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Calendar Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
        
def GetResetCalendarCheck(fTrade, mwTrade, mwResetCalendars, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        calendars = mwResetCalendars.split(';')
        for calendar in calendars:
            if calendar!='':
                if calendar not in (GetResetCalendars(fTrade)):
                    if mwResetCalendars != 'EUTA;':
                        return IgnoreExpiredTrades(fTrade)+'Calendar Mismatch|Reset Calendar Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Calendar: '+GetCalendarList(fTrade, 'Fixing')+'|MW Calendar: '+mwResetCalendars+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Calendar Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def GetSpreadCheck(fTrade, mwTrade, mwSpreadFloat, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        faSpread=GetFloatLegSpread(fTrade)
        if mwSpreadFloat!='':
            if float(mwSpreadFloat) > 0:
                mwSpread = float(mwSpreadFloat) * 100
                if round(faSpread, 2) != round(mwSpread, 2):
                    return IgnoreExpiredTrades(fTrade)+'Spread Mismatch|Float Spread Issue|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Spread: '+str(faSpread)+'|MW Spread: '+str(mwSpreadFloat)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Spread Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetPortfolioCheck(fTrade, mwTrade, mwPortfolio, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if fTrade.OptionalKey()!='':
            if mwPortfolio!=fTrade.Portfolio().Name():
                return IgnoreExpiredTrades(fTrade)+'Portfolio Mismatch|Portfolio Match Issue|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+fTrade.Portfolio().Name()+'|'+mwPortfolio +'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Portfolio Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetFirstFixingCheck(fTrade, mwTrade, mwFirstFixing, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if mwFirstFixing!='':
            if LegsFirstFixing(fTrade, mwFirstFixing)==False:
                return IgnoreExpiredTrades(fTrade)+'First Fixing|Issue On First Fixing|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(LegsFirstFixingRate(fTrade))+'|'+str(float(mwFirstFixing)*100)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get First Fixing Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetFO_BO_StatusCheck(fTrade, mwTrade):
#,mwStartDate,mwEndDate,mwTradeDate,mwUserID,mwOurBIC,mwTheirBIC
    try:
        if fTrade:
            if fTrade.Status() in ('FO Confirmed', 'BO Confirmed'):
                return IgnoreExpiredTrades(fTrade)+'Status Mismatch|FO or BO Confirmed FA Trade|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|||| Status '+fTrade.Status()
            else:
                return ''
    except StandardError, e:
        print 'Get FO BO Status Checks', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetStatusChecks(fTrade, mwTrade, mwStatus, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS', 'ATS_AMWI_TST', 'ATS_AMWI_PRD'):
            if mwStatus=='Cancelled':
                if mwStatus!=TradeStatuses(fTrade.Status(), 'FA'):
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch|Cancellation Status|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
            elif mwStatus in('Amended', 'New-Novated'):
                if fTrade.Status()!='BO-BO Confirmed':
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch|Amended Status|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
            elif mwStatus in ('New'):
                if mwStatus!=TradeStatuses(fTrade.Status(), 'FA'):
                    if fTrade.Type()=='Closing':
                        return IgnoreExpiredTrades(fTrade)+'Status Mismatch|Closing Trade|'              +str(fTrade.Oid())+     '|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
                    else:
                        return IgnoreExpiredTrades(fTrade)+'Status Mismatch|New MW Trade Status Incorrect|'              +str(fTrade.Oid())+     '|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
            elif mwStatus in ('New-PrimeBrokered'):
                if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
                    return IgnoreExpiredTrades(fTrade)+'Status Mismatch|New-PB Manual Update|'           +str(fTrade.Oid())+     '|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC                
            if fTrade.Status() in ('Simulated', 'BO Confirmed', 'FO Confirmed'):
                return IgnoreExpiredTrades(fTrade)+'Status Mismatch|Unexpected FA status|'      +str(fTrade.Oid())+     '|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA Status: '+fTrade.Status()+'|MW Status: '+mwStatus+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC 
            if fTrade.Status() in ('FO Confirmed'):
                return IgnoreExpiredTrades(fTrade)+'Status Mismatch|FO Confirmed FA status|'+str(fTrade.Oid())
        return ''
    except StandardError, e:
        print 'Get Status Checks', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetStartDateCheck(MMA, fTrade, mwTrade, faStartDate, mwTradeStatus, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
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
                                return IgnoreExpiredTrades(fTrade)+'Start End Date|Start Date Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+'|'+str(dmw).replace(' 00:00:00', '')+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
                            elif MMA == 'B':
                                return IgnoreExpiredTrades(fTrade)+'Start End Date|End Date Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+'|'+str(dmw).replace(' 00:00:00', '')+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
                            return IgnoreExpiredTrades(fTrade)+'Start End Date|OTHER Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|FA start date: '+str(faStartDate.to_string('%Y-%m-%d %H:%M:%S')).replace(' 00:00:00', '')+'|MW start date: '+str(dmw).replace(' 00:00:00', '')+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Start Date Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetNominalCheck(fTrade, mwTrade, faNominal, mwNominal, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if faNominal < 0:
                faNominal = faNominal * -1
            if round(faNominal, 2)!=round(mwNominal, 2):
                if int(faNominal-mwNominal) == 0:
                    return 'Excluded|Minor Nominal Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(faNominal)+'|'+str(mwNominal)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
                else:
                    return IgnoreExpiredTrades(fTrade)+'Nominal Mismatch|Nominal Mismatch|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(faNominal)+'|'+str(mwNominal)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Nominal Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
    
def GetRateCheck(fTrade, mwTrade, faRate, mwRate, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        if fTrade.CreateUser().Name() in ('AMBA', 'ATS'):
            if round(float(mwRate)*100, 4)!=round(float(faRate), 4):
                if round(float(faRate), 4)/round(float(mwRate)*100, 4) > 1:
                    return IgnoreExpiredTrades(fTrade)+'Rate Mismatch|Rate Concern|'+str(fTrade.Oid())+'|'+str(mwTrade)+'|'+fTrade.Acquirer().Name()+'|'+fTrade.CreateUser().Name()+'|'+fTrade.UpdateUser().Name()+'|'+str(faRate)+'|'+str(float(mwRate)*100)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|||'+mwUserID+'|'+mwOurBIC+'|'+mwTheirBIC
        return ''
    except StandardError, e:
        print 'Get Rate Check', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def ReturnBrokerCodeMapping(entry, typeofentry):
    try:
        for mapping in mappings:
            if mapping.getAttribute("MappingName") == typeofentry:
                map = mapping.getElementsByTagName("Mapping")
                for mappedentries in map:
                    if mappedentries.getAttribute("key") == entry:
                        return mappedentries.childNodes[0].nodeValue  
    except StandardError, e:
        print 'Get Mapping of Brokers', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))

def GetBrokerCodeCheck(fTrade, mwTradeId, mwBrokerCode, mwStartDate, mwEndDate, mwTradeDate, mwUserID, mwOurBIC, mwTheirBIC):
    try:
        brokerMappings = []
        if mwBrokerCode != '':
            brokerMap = ReturnBrokerCodeMapping(mwBrokerCode, 'Brokers')
            broker = acm.FBroker[str(brokerMap)]
            if not broker:
                if mwBrokerCode not in brokerMappings:
                    brokerMappings.append(mwBrokerCode)
                    print 'Check if these are actually mapped correctly between mappings and Front Arena', mwBrokerCode
            else:
                if fTrade.Broker():
                    if fTrade.Broker().Name() != broker.Name():
                        return 'Broker Code Check|Broker Code Mismatch|'+str(fTrade.Oid())+'|'+ mwTradeId +'||||'+str(fTrade.Broker().Name()) + '|'+str(mwBrokerCode)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|Mapped broker in Arena '+str(broker.Name())+'|Broker InMappingFile'+str(brokerMap)+'|'+mwUserID+ '|'+mwOurBIC+ '|'+mwTheirBIC
                if fTrade.Broker() == None:
                    return 'Broker Code Check|Broker Code Missing on FA Ticket|'+str(fTrade.Oid())+ '|'+ mwTradeId +'|||||'+str(mwBrokerCode)+'|'+mwStartDate+'|'+mwEndDate+'|'+mwTradeDate+'|Check the mapping file||'+mwUserID+ '|'+mwOurBIC+ '|'+mwTheirBIC
    except StandardError, e:
        print 'Get Brokers', str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))    
            
def AMWITradeMissingInAlignment(mwTrade):
    query = """select t.trdnbr \
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais \
          where t.insaddr = i.insaddr \
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
          and (ais.field_name = 'CCPmiddleware_id' or ais.field_name = 'MarkitWire') and ai.value ~='' \
          and i.instype in ('FRA','Swap') \
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated','Simulated','Void') \
          and (ai.value = '"""+mwTrade+"""' or t.optional_key like '%"""+mwTrade+"""%') \
          order by t.trdnbr asc"""
          
    selection = ael.asql(query)
    for selectionFA in selection[1][0]:
        if selectionFA[0] > 0:
            return True
        else:
            return False
    
def SynthesisTradeMissingInAlignment(mwTrade):
    query = """select t.trdnbr 
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais 
          where t.insaddr = i.insaddr 
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr 
          and ais.field_name = 'MarkitWire' and ai.value ~='' 
          and i.instype in ('FRA','Swap') 
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated','Simulated','Void') 
          and (ai.value like '%"""+mwTrade+"""%' or t.optional_key like '%"""+mwTrade+"""%')
          order by t.trdnbr asc"""
    selection = ael.asql(query)
    for selectionFA in selection[1][0]:
        if selectionFA[0] > 0:
            return True
        else:
            return False
    
def PriorMiddleWareIDClearing(mwTrade):
    query = """select t.trdnbr
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais
          where t.insaddr = i.insaddr \
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
          and ais.field_name = 'prior_middleware' and ai.value ~= '' \
          and i.instype in ('FRA','Swap') \
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated','Simulated','Void') \
          and ai.value like '%"""+mwTrade+"""%' \
          """
    selection = ael.asql(query)
    for selectionFA in selection[1][0]:
        if selectionFA[0] > 0:
            print 'Trade number found as part of prior middleware clearing id is', selectionFA[0]
            return True
        else:
            return False
            
def ErrorStatusOnTransitions(fTrade):
    if fTrade.AdditionalInfo().CCPclearing_status()=='Error':
        if fTrade.Status() not in ('BO-BO Confirmed', 'Terminated', 'Void'):
            return 'Clearing Status Error | Status of trade is in Error |'+str(fTrade.Oid())+' ! Status '+fTrade.Status()
    else:
        return ''

def getInterdeskChecks(fTrade):
    traderWrongAcquirer=''
    if (fTrade.Acquirer().Name()=='IRD DESK' and fTrade.Counterparty().Name()=='PRIME SERVICES DESK') or (fTrade.Acquirer().Name()=='PRIME SERVICES DESK' and fTrade.Counterparty().Name()=='IRD DESK'):
        if fTrade.Acquirer().Name()=='IRD DESK' and fTrade.Trader().Name() in ('MOTLOUNN', 'NAIDOOEV') and fTrade.Status() not in ('Terminated', 'Void'):
            traderWrongAcquirer+='Trader Acquirer Check | This Trader '+fTrade.Trader().Name() + ' | FA Trade | '+str(fTrade.Oid()) + ' | Wrong Acquirer | '+fTrade.Acquirer().Name()+' | '
        elif fTrade.Acquirer().Name()=='PRIME SERVICES DESK' and fTrade.Trader().Name() in ('OELOFSED', 'CHABUDAR') and fTrade.Status() not in ('Terminated', 'Void'):
            traderWrongAcquirer+='Trader Acquirer Check | This Trader '+fTrade.Trader().Name() + ' | FA Trade | '+str(fTrade.Oid()) + ' | Wrong Acquirer | '+fTrade.Acquirer().Name()+' | '
    return traderWrongAcquirer
            
def getDuplicatePayments():
    businessProcesses= acm.FBusinessProcess.Select('')
    duplicatePaymentList = ''
    for bp in businessProcesses:
        if bp.Subject() and bp.Subject().AdditionalInfo().CCPclearing_process() == 'Amend/CancelDirectDeal' and \
           bp.Subject().Contract().Oid() != bp.Subject().Oid():
            for payment in bp.Subject().Payments():
                for origPay in bp.Subject().Contract().Payments():
                    if payment.Amount() == origPay.Amount() and payment.Type() == origPay.Type():
                        if bp.Subject().Contract().Status() not in ('Terminated', 'Void'):
                            duplicatePaymentList+='Payment Duplication Check | Possible duplicate payment type | '+payment.Type() + ' | for amount | ' +str(payment.Amount()) +' | Contract trade | '+ str(bp.Subject().Contract().Oid())
                            duplicatePaymentList+=' | is in status | '+bp.Subject().Contract().Status()+' | for Trade | ' + str(bp.Subject().Oid())+' | in status | '+bp.Subject().Status()+'\n'
    return duplicatePaymentList
    
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
        recordCount = 1
        for read in reader:
            if read[0]=='':
                continue
            if read[2] not in ('absa_swcancel1', 'absa_swcancel2', 'absa_swcancel3', 'absa_swcancel4', 'absa_swcancel5', 'absa_swcancel6', 'absa_swcancel7', 'absa_swcancel8'): #ignore specific deal bookings from Markit Wire which are not relevant
                if read[2] not in ('Absa Listener 1', 'Absa Listener 2', 'Absa Listener 3', 'Absa Listener 4', 'Absa Listener 5'):
                    string_date = read[8][0:10]
                    if string_date != 'DealDate':
                        if datetime.strptime(string_date, "%Y-%m-%d") > datetime.strptime(parameters['FromDate'], "%Y-%m-%d"):
                            mwTrades.append(read[0])
                            #Trade id        #Trader          #Portfolio       #Status          #Trade Date       #Start Date       #End Date         #Direction        #Notional         #Rate             #Additional Amount / Curr             #Payment date      #Payment Type
                            #read[0]         read[2]          read[3]          read[6]          read[7]           read[15]          read[16]          read[10]          read[22]          read[23]          read[163]            read[164]        read[165]          read[166])
                            #if datetime.datetime(read[7][0:10]) > datetime.datetime('2015-03-22')
                            MWDict = {'TradeId':read[0],'Nominal':read[23],'Status':read[8],'TradeDate':read[9],'Rate':read[24],'Trader':read[2],'StartDate':read[16],'EndDate':read[17],'Portfolio':read[3],'BookingState':read[244],'FirstFixing':read[89],'SpreadFloat':read[90],'PaymentHolidays':read[88],'ValueTenor':read[74],'FixedFrequency':read[76],'FloatFrequency':read[80],'FRateIndex':read[26],'BrokerageAmount':read[20],'FixingHolidays':read[87],'BIC':read[15],'CptyBIC':read[11],'UserID':read[117],'BrokerCode':read[5]}
                            mwTradeDetails.append(MWDict)
            recordCount+=1
        #Records from Front Arena as per query
       
        for selectionFA in selection[1][0]:  
            if parameters['MWAMWI']:
                FATrades.append(selectionFA[3])
                FADict = {'TradeId':selectionFA[3],'Nominal':selectionFA[7],'Status':selectionFA[5],'TrdNbr':selectionFA[0],'TradeDate':selectionFA[6],'InsType':selectionFA[1],'OptionalKey':selectionFA[4],'Quantity':selectionFA[13],'FixedRate':selectionFA[12],'MWKey':selectionFA[3],'StartDate':selectionFA[10],'EndDate':selectionFA[11],'Portfolio':selectionFA[9],'MWFullKey':selectionFA[14],'SpreadFloat':selectionFA[15],'PayCal1':read[16],'PayCal2':read[17],'PayCal3':read[18],'TradeType':read[19]}
                FATradeDetails.append(FADict)
            else:
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

                    #Check if the wrong acquirer is allocated to the wrong trader
                    if parameters['MWWrongTrader']:
                        result = getInterdeskChecks(fTrade)
                        if result != '' and result != None:
                            MWRecon.append(result)
                    
                    #Error on the clearing status additional info field - this is a transition issue on the workflows in AMWI
                    if parameters['MWErrorStatus']:
                        result = ErrorStatusOnTransitions(fTrade)
                        if result != '' and result != None:
                            MWRecon.append(result)
                        
                    #Nominal Direction Check / Change
                    if parameters['MWNominalDirection']:
                        result = NominalDirectionChangeCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'])
                        if result != '' and result != None:
                            MWRecon.append(result)
                    
                    #Broker Code
                    if parameters['MWBrokerCode']:
                        if mwTradeDetails[MWIndex]['BrokerCode'] != 'BrokerCode':
                            result = GetBrokerCodeCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['BrokerCode'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result != '' and result!= None:
                                MWRecon.append(result)
                    
                    #Brokerage Fee
                    if parameters['MWBrokerageCheck']:
                        if lengthReset==len(arenaTradesSeriesFind):
                            result = GetBrokerageResults(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['BrokerageAmount'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='' and result != None:
                                MWRecon.append(result)
                                
                    #Optionl Key Population Check
                    if parameters['MWOptionalKeyCheck']:
                        if lengthReset ==len(arenaTradesSeriesFind):
                            result = GetMissingOptionalKey(fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['OptionalKey'], FATradeDetails[arenaListIndex]['MWFullKey'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Rate Index Check
                    if parameters['MWIndexCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            if FATradeDetails[arenaListIndex]['InsType']=='FRA':
                                result = GetRateIndexCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FRateIndex'], mwTradeDetails[MWIndex]['ValueTenor'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                                if result!='':
                                    MWRecon.append(result)
                            elif FATradeDetails[arenaListIndex]['InsType']=='Swap':
                                result = GetRateIndexCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FRateIndex'], mwTradeDetails[MWIndex]['FloatFrequency'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                                if result!='':
                                    MWRecon.append(result)
                    
                    #Calendar checks
                    if parameters['MWHolidayCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetPaymentCalendarCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['PaymentHolidays'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                                
                    if parameters['MWFixingCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetResetCalendarCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FixingHolidays'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                        
                    #Spread check
                    if parameters['MWSpreadCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetSpreadCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['SpreadFloat'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Portfolio check
                    if parameters['MWPortfolioCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetPortfolioCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['Portfolio'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #First fixing
                    if parameters['MWFirstFixCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetFirstFixingCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['FirstFixing'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                    
                    #Check for cancelled trades on MW that are not cancelled on Front Arena
                    if parameters['MWStatusCheck']==True:
                        if lengthReset == len(arenaTradesSeriesFind):
                            #result = GetStatusChecks(fTrade,mwTradeDetails[MWIndex]['TradeId'],mwTradeDetails[MWIndex]['Status'],mwTradeDetails[MWIndex]['StartDate'],mwTradeDetails[MWIndex]['EndDate'],mwTradeDetails[MWIndex]['TradeDate'],mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'],mwTradeDetails[MWIndex]['CptyBIC'])
                            result = GetFO_BO_StatusCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'])                                           
                                #,[MWIndex]['StartDate'],mwTradeDetails[MWIndex]['EndDate'],mwTradeDetails[MWIndex]['TradeDate'],mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'],mwTradeDetails[MWIndex]['CptyBIC']
                            if result!='':
                                MWRecon.append(result)
                            
                    #Start and End Date Check
                    if parameters['MWStartEndDateCheck']:
                        if lengthReset == len(arenaTradesSeriesFind):
                            result = GetStartDateCheck('A', fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['StartDate'], mwTradeDetails[MWIndex]['Status'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                            result = GetStartDateCheck('B', fTrade, mwTradeDetails[MWIndex]['TradeId'], FATradeDetails[arenaListIndex]['EndDate'], mwTradeDetails[MWIndex]['Status'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                            if result!='':
                                MWRecon.append(result)
                         
                    #Nominal check
                    if parameters['MWNominalCheck']==True:
                        if lengthReset == len(arenaTradesSeriesFind):
                            if FATradeDetails[arenaListIndex]['OptionalKey'] != '':
                                if mwTradeDetails[MWIndex]['Status'] not in ('Cancelled', 'Novated') and FATradeDetails[arenaListIndex]['Status'] not in ('Terminated', 'Void'):
                                    if FATradeDetails[arenaListIndex]['InsType'] == 'FRA':
                                        result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Quantity']), float(mwTradeDetails[MWIndex]['Nominal']), mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                                        if result!='':
                                            MWRecon.append(result)
                                    else:
                                        if float(FATradeDetails[arenaListIndex]['Nominal'])!=0:
                                            result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Nominal']), float(mwTradeDetails[MWIndex]['Nominal']), mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                                        elif float(FATradeDetails[arenaListIndex]['Quantity'])!=0:
                                            result = GetNominalCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['Quantity']), float(mwTradeDetails[MWIndex]['Nominal']), mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])
                                        if result!='':
                                            MWRecon.append(result)
                                                
                    #Rate check
                    if parameters['MWRateCheck']==True:                
                        if lengthReset == len(arenaTradesSeriesFind):
                            if float(FATradeDetails[arenaListIndex]['FixedRate']) != 0:
                                result = GetRateCheck(fTrade, mwTradeDetails[MWIndex]['TradeId'], float(FATradeDetails[arenaListIndex]['FixedRate']), float(mwTradeDetails[MWIndex]['Rate']), mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])                                
                                if result!='':
                                    MWRecon.append(result)
                lengthReset=0
                
            MWIndex+=1
        MWIndex = 0

        if parameters['MWDuplicatePayments']:
            result = getDuplicatePayments()
            if result != '' and result != None:
                MWRecon.append(result)
        
        if parameters["MWMissingTrades"]==True:
            for mwTrade in mwTrades:
                if mwTrade not in FATrades:
                    #perform another check because of misaligned result sets
                    if AMWITradeMissingInAlignment(mwTrade):
                        print 'Trade does actually exist on Front Arena', mwTrade
                    else:   
                        if PriorMiddleWareIDClearing(mwTrade) == True:
                            print 'Trade does actually exist on Front Arena as prior middle ware ID', mwTrade
                        else:
                            result = GetMissingMarkitWireTrades(mwTradeDetails[MWIndex]['TradeId'], mwTradeDetails[MWIndex]['Status'], mwTradeDetails[MWIndex]['StartDate'], mwTradeDetails[MWIndex]['EndDate'], mwTradeDetails[MWIndex]['TradeDate'], mwTradeDetails[MWIndex]['UserID'], mwTradeDetails[MWIndex]['BIC'], mwTradeDetails[MWIndex]['CptyBIC'])       
                            if result != '' and result != None:
                                MWRecon.append(result)
                    '''if SynthesisTradeMissingInAlignment(mwTrade) == True:
                        print 'Synthesis trade does actually exist on Front Arena',mwTrade
                    else:
                        print 'Synthesis trade does not actually exist on Front Arena',mwTrade
                        result = GetMissingMarkitWireTrades(mwTradeDetails[MWIndex]['TradeId'],mwTradeDetails[MWIndex]['Status'],mwTradeDetails[MWIndex]['StartDate'],mwTradeDetails[MWIndex]['EndDate'],mwTradeDetails[MWIndex]['TradeDate'],mwTradeDetails[MWIndex]['UserID'],mwTradeDetails[MWIndex]['BIC'],mwTradeDetails[MWIndex]['CptyBIC'])       
                        if result != '' and result != None:
                            MWRecon.append(result)'''
                MWIndex+=1
                    
        MWRecon.append('#1   '+str(len(mwTrades))+' MarkitWire TRADES analysed.')
        MWRecon.append('#2   '+str(len(FATrades))+' Front Arena TRADE STATES trades analysed.')
        MWRecon.append('#3   '+str(len(MWRecon)-2)+' breaks identified.')   
        MWRecon.append('BreakGroup|BreakType|FATrade|MWTrade|Acquirer|CreateUser|UpdateUser|FrontValue|MarkitWireValue|MarkitWireStartDate|MarkitWireEndDate|MarkitWireTradeDate|Info_1|Info_2|MarkitWire Update User|Our BIC|Cpty BIC')        
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
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Simulated','Void') 
          and t.prfnbr = port.prfnbr 
          and t.time between '"""+fromDate+"""' and '"""+toDate+"""' \
          and l.fixed_rate~=0 \
          order by t.trdnbr asc"""
    return query

ael_variables = \
    [
        ['SourceCSVFile', 'Source CSV file', 'string', None, 'Y:\Jhb\FALanding\Dev\MarkitWire\DEbaseline.csv', 1],
        ['OutputCSVFile', 'Output CSV file', 'string', None, 'Y:\Jhb\FALanding\Dev\MarkitWire\DealExtractorOutput_'+ael.date_today().to_string('%Y-%m-%d')+'.csv', 1],
        ['FromDate', 'From Date', 'string', None, '2005-03-22', 1],
        ['ToDate', 'To Date', 'string', None, ael.date_today().to_string('%Y-%m-%d'), 1],
        ['ToExpiry', 'To Expiry', 'string', None, '2014-11-21', 1],
        ['MWStatusCheck', 'Markit Wire Status Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWOddStatusCheck', 'Front Arena Odd MW Status Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWStartEndDateCheck', 'Front Arena Start Date Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWRateCheck', 'Front Arena Rate Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWNominalCheck', 'Front Arena Nominal Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWFirstFixCheck', 'Front Arena First Fixing Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWPortfolioCheck', 'Front Arena Portfolio Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWSpreadCheck', 'Front Arena Float Spread Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWIndexCheck', 'Front Arena Index Tenor Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWHolidayCheck', 'Front Arena Payment Holiday Calendar Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWFixingCheck', 'Front Arena Fixing Holiday Calendar Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWOptionalKeyCheck', 'Front Arena Optional Key Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWBrokerageCheck', 'Front Arena Brokerage Fee Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWBrokerCode', 'Front Arena Broker Code Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWUserCreatedTradesCheck', 'Front Arena User Created Trades', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWOptionalCCPKeyCheck', 'Front Arena New CCP Key Concern', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1],
        ['MWMissingTrades', 'Front Arena Missing Trades', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWNominalDirection', 'Front Arena Nominal Direction Check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWErrorStatus', 'Front Arena Error Clearing Status', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWWrongTrader', 'Front Arena Wrong Trading Desk', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWDuplicatePayments', 'Front Arena Duplicate Payments', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1],
        ['MWAMWI', 'Front Arena AMWI check', 'bool', [True, False], True, 0, 0, 'Roll back', None, 1]
    ]

def ael_main(parameters):

   #Front Arena records from current Synthesis Adapter
    expiry = parameters['ToExpiry']
    
    q = LegacyMarkitWire(str(parameters['FromDate']), str(parameters['ToDate']))
    
    if parameters['MWAMWI']:
        print 'Generating AMWI query'
        q = AMWI_query(str(parameters['FromDate']), str(parameters['ToDate']))

    selection = ael.asql(q)
    
    #get the deal extractor details
    try:
        f = open(parameters["SourceCSVFile"], 'rt')
        
        reader = csv.reader(f)
        fResults = open(parameters['OutputCSVFile'], 'w')
        print 'Recon Started...'
        fResults.write('#    Reconciliation between MarkitWire and Front Arena.'+'\n')
        fResults.write('#    Date Range: '+str(parameters['FromDate'])+' to '+str(parameters['ToDate'])+'\n')
        fResults.write('#    Expiry After: '+str(parameters['ToExpiry'])+'\n')
        for entry in GetNoTradeMatchesToBeDone(selection, reader, parameters):
            print entry
            fResults.write(entry+'\n')
        fResults.close()
        f.close()
    except StandardError, e:
        print str(e)
        logger.ELOG('Markit Wire Recon %s < ', str(e))
        
        print 'completed succesfully'
