""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/futures_maintenance/FSTIRFuturesMaintenance.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------


#==============================================================================
# mkSTIRFutures
#
# Maintenance of contract strips for '
#  * Futures with underlying RateIndex'
#  * Forwards with underlying FRA'
#  * FRAs
#
# Support 4.0, 4.1 and 3.2 simultaneously
#
# # Bugfix in 2008-02-13
# Fixed problems with changed parameters overidden by the config tab
#
# # Added in 2007-10-03
#
# Support for displaying script names such as
# "FSTIR_my_script" as "my script" in the drop downlist
# Make sure to avoid using a script named
# "FSTIR_my_script" and one named "FSTIR_my script"
# as both will show up as "my script" in the drop down list
#
# # Added in 2007-08-17
# Drop down list that allow quick creation of standard stripes added.
# Each drop down list entry has helpful default values to make it easy to setup
# standard strips.
# If instruments have been correctly setup creating a strip such as euroDollar
# future strip simply select it from the drop down list and click run.
#
# This drop down list displays any script named FSTIR_* to use as a
# configuration template. Each configuration file consist of lines of type
# <key> = <value>
# See FSTIR_EuroDollar python module for a description.
#
#
# There has been an ongoing discussion if instrument definitions should be part
# of the script. See code marked as obsolete.
# =============================================================================


import ael


import datetime
import time
#import FLogger
import logging


import FBDPRollback
import FBDPString
import FBDPCommon
import importlib
logme = FBDPString.logme  # Required for FBDPRollback. Do NOT remove.


#==============================================================================
# Global variables
#==============================================================================

# logger object
logger = logging.getLogger('FContractStrip')

# parameter dictionary
globalParams = {}


verbose = 3


#==============================================================================
# patching the FBDPRollback functionality to make it work with FLOGGER this
# should be fixed in FLogger and not here
#==============================================================================


class LogPatch:
    def DLOG(self, msg):
        #global logme
        #logme(msg, "DEBUG")
        logger.log(3, msg)

    def WLOG(self, msg):
        #logme(msg, "WARNING")
        logger.log(2, msg)

    def ELOG(self, msg):
        logger.log(1, msg)

    def CLOG(self, msg):
        logger.log(1, msg)


flogger = LogPatch()


#==============================================================================


monthL = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
number_string = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
        'sixth': 6, 'seventh': 7, 'eight': 8, 'nineth': 9, 'tenth': 10}
weeks = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4}  # 'last': ???
weekdays = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5,
        'sun': 6}
month_names = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}


def isInt(s):
    ''' Is the given string an integer?    '''
    logger.debug('def isInt(s):')
    ok = 1
    try:
        int(s)
    except ValueError:
        ok = 0
    return ok


def check_ym_format(y, m):
    """
    Check year and month format and return (y, m) as int
    """
    logger.debug('def check_ym_format(y, m):')
    if isInt(y):
        y = int(y)
    else:
        #logger.error('check_ym_format(y, m)::Unknown year format')
        flogger.ELOG('check_ym_format(y, m)::Unknown year format')
        raise TypeError('Unknown year format: {0} {1}'.format(y, type(y)))
    if isInt(m):
        m = int(m)
    elif type(m) == type('string'):
        try:
            m = month_names[m[0:3].lower()]
        except:
            #logger.exception('check_ym_format(y, m)::Unknown month format')
            flogger.CLOG('check_ym_format(y, m)::Unknown month format')
            raise ValueError('Unknown month format: {0} {1}'.format(m,
                    type(m)))
    else:
        logger.error('check_ym_format(y, m)::Unknown month format')
        flogger.ELOG('check_ym_format(y, m)::Unknown month format')
        raise TypeError('Unknown month format: {0} {1}'.format(m, type(m)))
    return (y, m)


def weekdayAfterDays(y=None, m=None, weekday='Wednesday', nrDays=9):
    """
    Return the first specified weekday after a specified number of days,
    e.g. first Wednesday after the nineth day
    """
    logger.debug('def weekdayAfterDays(y, m, weekday, nrDays):')
    (y, m) = check_ym_format(y, m)
    if isInt(weekday):
        weekday = int(weekday)
    elif type(weekday) == type('string'):
        try:
            weekday = weekdays[weekday[0:3].lower()]
        except:
            logger.exception('weekdayAfterDays(...)::Unknown weekday format')
            raise ValueError('Unknown weekday format: {0} {1}'.format(weekday,
                    type(weekday)))
    else:
        flogger.ELOG('weekdayAfterDays(...)::Unknown weekday format')
        raise TypeError('Unknown weekday format: {0} {1}'.format(weekday,
                type(weekday)))
    if isInt(nrDays):
        nrDays = int(nrDays)
    elif type(nrDays) == type('string'):
        try:
            nrDays = number_string[nrDays.lower()]
        except:
            logger.exception('weekdayAfterDays(...):::Unknown format on '
                    'number of days')
            raise ValueError('Unknown format on number of days: {0} '
                    '{1}'.format(nrDays, type(nrDays)))
    else:
        flogger.ELOG('weekdayAfterDays(...)::Unknown format on number of days')
        raise TypeError('Unknown format on number of days: {0} {1}'.format(
                nrDays, type(nrDays)))
    wd = time.localtime(time.mktime((y, m, nrDays, 0, 0, 0, 0, 0, -1)))[6]
    day_diff = wd - weekday
    theDay = nrDays + 7 - (day_diff % 7)
    dayRule = ael.date_from_time(int(
                time.mktime((y, m, theDay, 0, 0, 0, 0, 0, -1))))
    return dayRule


def weekdayInWeek(y=None, m=None, weekday='Wednesday', nrWeeks=3):
    """
    Return a specific weekday of month, e.g. third Wednesday of the month or
    third Friday of the month.
    """
    logger.debug('def weekdayInWeek(y, m, weekday, nrWeeks):')
    (y, m) = check_ym_format(y, m)
    if isInt(weekday):
        weekday = int(weekday)
    elif type(weekday) == type('string'):
        try:
            weekday = weekdays[weekday[0:3].lower()]
        except:
            logger.exception('weekdayInWeek(...)::Unknown weekday format')
            raise ValueError('Unknown weekday format: {0} {1}'.format(weekday,
                    type(weekday)))
    else:
        flogger.ELOG('weekdayInWeek(...)::Unknown weekday format')
        raise TypeError('Unknown weekday format: {0} {1}'.format(weekday,
                type(weekday)))
    if isInt(nrWeeks):
        nrWeeks = int(nrWeeks)
    elif type(nrWeeks) == type('string'):
        try:
            nrWeeks = weeks[nrWeeks.lower()]
        except:
            logger.exception('weekdayInWeek(...)::Unknown format on number '
                    'of weeks')
            raise ValueError('Unknown format on number of weeks: {0} '
                    '{1}'.format(nrWeeks, type(nrWeeks)))
    else:
        flogger.ELOG('weekdayInWeek(...):::Unknown format on number of weeks')
        raise TypeError('Unknown format on number of weeks: {0} '
                '{1}'.format(nrWeeks, type(nrWeeks)))
    nrDays = (nrWeeks - 1) * 7 + (7 - weekday)
    # Weekday
    wd = time.localtime(time.mktime((y, m, nrDays, 0, 0, 0, 0, 0, -1)))[6]
    theDay = nrWeeks * 7 - wd
    dayRule = ael.date_from_time(int(
            time.mktime((y, m, theDay, 0, 0, 0, 0, 0, -1))))
    return dayRule


def thirdWednesday(dat):
    """
    Return 3rd Wednesday in a month
    """
    logger.debug('def thirdWednesday(dat):')
    dts = dat.to_string(ael.DATE_ISO).split('-')
    y = int(dts[0])
    m = int(dts[1])
    wed3 = weekdayInWeek(y, m, 'Wednesday', 3)
    return wed3


def thirdFriday(dat):
    """
    Return 3rd Friday in a month
    """
    logger.debug('def thirdFriday(dat):')
    dts = dat.to_string(ael.DATE_ISO).split('-')
    y = int(dts[0])
    m = int(dts[1])
    fri3 = weekdayInWeek(y, m, 'Friday', 3)
    return fri3


def firstWednesdayAfter9Days(dat):
    """
    Return 1st Wednesday after the ninth day in a month
    """
    logger.debug('def firstWednesdayAfter9Days(dat):')
    dts = dat.to_string(ael.DATE_ISO).split('-')
    y = int(dts[0])
    m = int(dts[1])
    wed3 = weekdayAfterDays(y, m, 'Wednesday', 9)
    return wed3


def nextIMM(dat, roll='3m'):
    """
    Return the next IMM date
    """
    logger.debug('def nextIMM(dat, roll):')
    dts = dat.to_string(ael.DATE_ISO).split('-')
    y = int(dts[0])
    m = int(dts[1])
    # IMM month: March (3), June (6), September (9), December (12)
    imm_m = m + 3 - ((m - 1) % 3 + 1)
    immDay = weekdayInWeek(y, imm_m, 'Wednesday', 3)
    return immDay


def insOf(ins):
    """
    Return ins as a instrument
    """
    logger.debug('def insOf(ins):')
    if type(ins) == type('string'):
        ins = ael.Instrument[ins]
    elif FBDPCommon.is_acm_object(ins):
        ins = ael.Instrument[ins.Oid()]
    return ins  # Is now instrument entity


#
#isin is set from the advanced tab
#
def getISIN(ref, exp, isin=None):
    """
    Create ISIN, i.e., "COMMODITY + M + YY" where COMMODITY either comes from
    ref instrument or the in parameter script
    """
    logger.debug('def getISIN(ref, exp, isin):')
    if isin:
        commodity = isin
    else:
        if type(ref) == type('string') and ael.Instrument[ref]:
            ref = ael.Instrument[ref]
        if type(ref) == type('string'):
            flogger.ELOG('insOf::Instrument not found')
            raise RuntimeError('Instrument not found {0}'.format(ref))
        commodity = ref.isin
    if type(exp) == type('string'):
        try:
            exp = ael.date(exp)
        except:
            exp = ael.date_today().add_period(exp)
    dts = exp.to_string(ael.DATE_ISO).split('-')
    ys, m = dts[0][-2:], int(dts[1])
    if commodity:
        # commodity
        #print "getISIN ", commodity, monthL[m - 1], ys
        isin = commodity + monthL[m - 1] + ys
    else:
        isin = commodity
    return isin


def getINSID(fut, ref, exp, insid=None):
    """
    Generate an INSID
    """
    flogger.DLOG("getINSID " + insid)
    if insid == None or insid == "":
        insid = fut.suggest_id()
    else:
        if type(exp) == type('string'):
            try:
                exp = ael.date(exp)
            except:
                exp = ael.date_today().add_period(exp)
        dts = exp.to_string(ael.DATE_ISO).split('-')
        m = int(dts[1])
        # should clean the date code here someday
        insid = insid + ("%02d" % int(m)) + monthL[m - 1]
    flogger.DLOG("getINSID after " + insid)
    return insid


def mkSTIRFutures(ref, expDay, startDay=ael.date_today(), isin=None,
        doCommit=0, tag=None, qtype="Pct of Nominal", insid=None):
    """
    SPR 258684 Maintenance of contract strips
    """
    flogger.DLOG('def mkSTIRFutures()')
    ref = insOf(ref)
    if type(startDay) == type('string'):
        try:
            startDay = ael.date(startDay)
        except:
            startDay = ael.date_today().add_period(startDay)
    if type(expDay) == type('string'):
        try:
            expDay = ael.date(expDay)
        except:
            expDay = ael.date_today().add_period(expDay)

    logMsg = ("  Reference :: ref.insid=%s, ref.instype=%s, expDay=%s, "
            "startDay=%s" % (ref.insid, ref.instype, expDay.to_string(),
            startDay.to_string()))
    flogger.DLOG(logMsg)
    # copy from reference instrument
    fut = ref.new()
    fut.archive_status = 0
    fut.generic = 0
    fut.creat_time = ael.date_today().to_time()
    fut.issue_day = ael.date_today()
    fut.updat_time = fut.creat_time
    fut.exp_day = expDay
    fut.exp_time = expDay.to_time()
    fut.extern_id1 = ''
    fut.extern_id2 = ''
    # Note: Instrument of type FRA...
    #   Generic FRA: quote_type = Coupon
    #   Non Generic: quote_type = Pct of Nominal
    #   start_day is needed
    if ref.instype == 'FRA':
        if qtype:
            try:
                fut.quote_type = qtype
            except TypeError:
                flogger.ELOG("Type Error (Invalid Quote Type)")
                return []
        else:
            fut.quote_type = "Pct of Nominal"
        for leg in fut.legs():
            leg.start_day = startDay
            leg.end_day = expDay
            leg.archive_status = 0
            leg.creat_time = fut.creat_time
            leg.updat_time = fut.creat_time
            #                     ael.date('0001-01-01').add_years(-1)
            leg.amort_start_day = startDay
            #                   ael.date('0001-01-01').add_years(-1)
            leg.amort_end_day = expDay
            leg.regenerate()
    # like isin
    #insid = fut.suggest_id()
    insid = getINSID(fut, ref, expDay, insid)
    flogger.DLOG("Insid is " + insid)

    #print 'insid from suggestname is %s' %insid
    isin = getISIN(ref, expDay, isin)
    if insid:
        i = ael.Instrument[insid]
        if not i:
            i = ael.Instrument.read("insid='%s'" % insid)
        if i:
            logMsg = 'Instrument insid %s already exists' % insid
            logger.warning(logMsg)
            return i
    if isin:
        i = ael.Instrument[isin]
        if not i:
            i = ael.Instrument.read("isin='%s'" % isin)
        if i:
            logMsg = 'Instrument ISIN %s already exists' % isin
            logger.warning(logMsg)
            return i
    fut.isin = isin
    fut.insid = insid
    # Set Free Text field
    if tag:
        fut.free_text = tag
    if doCommit:
        '''
        try:
            fut.commit()
            msg0 = 'Created'
        except:
            msg0 = 'Failed to Create'
        '''
        if rollback.add(fut):
            msg0 = 'Created'
        else:
            msg0 = 'Failed to Create'
    else:
        #flogger.DLOG( 'Created (TRIAL)', fut.insid)
        msg0 = 'Created (TRIAL)'
    if verbose:
        flogger.DLOG(fut.pp())
    logMsg = ('%s %s Instrument "%s" ISIN "%s" with EXP DAY "%s"' %
            (ael.date_today().to_string(), msg0, fut.insid, fut.isin,
            expDay.to_string()))
    flogger.DLOG(logMsg)
    if doCommit:
        fut = ael.Instrument[fut.insid]
    # To get database value, to later link to OB
    # SPR-252304 says that it is not possible to link to a temporary entity
    return fut


def getRefDay(refDay):
    """ Calculate refDay
    """
    # If refDay is a string it may be a date or datePeriod
    #ogger.debug("refDay " + str(refDay)
    #               +" type(" + str(type(refDay)) + ")")
    if type(refDay) == type('string'):
        # only works from the automatic scripts ?
        try:
            refDay = ael.date(refDay)  # refDay as date string
        except TypeError:
            try:
                refDay = ael.date_today().add_period(refDay)
            except TypeError:
                flogger.ELOG("Type Error (Invalid date/period) in Reference "
                        "Day field")
                raise TypeError("Type Error (Invalid date/period) in "
                        "Reference Day field")
    flogger.DLOG("RefDay was set by getRefDay to " + str(refDay))
    return refDay


def getExpSet(ref, refDay, stripLen, expRule=None, rollPer=None):
    ''' Return the list of expiry dates... '''
    # this function is too long fo its own good
    flogger.DLOG('def getExpSet()')
    # get the rolling period and cal from ref instrument
    ref = insOf(ref)
    while ref.und_insaddr:
        ref = ref.und_insaddr
    roll = None
    cal = ref.curr
    if ref.legs():
        leg = ref.legs()[0]
        while leg.float_rate:
            leg = leg.float_rate.legs()[0]
        roll = leg.end_period
        cal = leg.pay_calnbr
    # override default rolling period?
    if rollPer:
        roll = rollPer
    if expRule == 'IMM':
        roll = '3m'

    # Check Rolling Period
    if not roll:
        flogger.ELOG("Invalid Rolling Period")
        return []

    # If refDay is a string it may be a date or datePeriod
    #if type(refDay) == type('string'):
    #    try:
    #        refDay = ael.date(refDay) # refDay as date string
    #    except TypeError, eMsg:
    #        try:
    #            refDay = ael.date_today().add_period(refDay)
    #        except TypeError, eMsg:
    #            flogger.ELOG("Type Error (Invalid date/period) in Reference "
    #                    "Day field")
    #            return []

    refDay = getRefDay(refDay)

    # override default reference day, e.g. IMM?
    if expRule == 'IMM':
        immDay = nextIMM(refDay)
        if immDay < refDay:
            immDay = nextIMM(immDay.add_period(roll))
        refDay = immDay
    elif expRule == '3rdWednesday':
        wed3 = thirdWednesday(refDay)
        if wed3 < refDay:
            wed3 = thirdWednesday(wed3.add_period(roll))
        refDay = wed3
    elif expRule == '3rdFriday':
        fri3 = thirdFriday(refDay)
        if fri3 < refDay:
            fri3 = thirdFriday(fri3.add_period(roll))
        refDay = fri3
    elif expRule == '1stWednesdayAfter9D':
        wed9 = firstWednesdayAfter9Days(refDay)
        if wed9 < refDay:
            wed9 = firstWednesdayAfter9Days(wed9.add_period(roll))
        refDay = wed9
    else:
        pass  # Default use reference day as is....

    # adjust for banking day
    refDay = refDay.adjust_to_banking_day(cal)
    # find the last expiry day from stripLen
    # endDay = refDay.add_period(stripLen)
    endDay = stripLen
    if isInt(stripLen):
        endDay = refDay
        for i in range(int(stripLen)):
            endDay = endDay.add_period(roll)
    else:
        try:
            endDay = ael.date(stripLen)  # refDay as date string
        except TypeError:
            try:
                endDay = refDay.add_period(stripLen)
            except TypeError:
                flogger.ELOG("Type Error (Invalid date/period) in Strip "
                        "Length field")
                return []
    if expRule == 'IMM':
        endDay = nextIMM(endDay)
    elif expRule == '3rdWednesday':
        endDay = thirdWednesday(endDay)
    elif expRule == '3rdFriday':
        endDay = thirdFriday(endDay)
    elif expRule == '1stWednesdayAfter9D':
        endDay = firstWednesdayAfter9Days(endDay)
    else:
        pass  # Default use as is....
    endDay = endDay.adjust_to_banking_day(cal)

    # find the set of expiry days
    expSet = []
    expDay = refDay

    while expDay < endDay:
        try:
            expDay = expDay.add_period(roll)
        except TypeError:
            flogger.ELOG("Type Error (Invalid date/period) in Rolling "
                    "Period field")
            return []

        if expRule == 'IMM':
            expDay = nextIMM(expDay)
        elif expRule == '3rdWednesday':
            expDay = thirdWednesday(expDay)
        elif expRule == '3rdFriday':
            expDay = thirdFriday(expDay)
        elif expRule == '1stWednesdayAfter9D':
            expDay = firstWednesdayAfter9Days(expDay)
        else:
            pass  # Default use as is....
        expDay = expDay.adjust_to_banking_day(cal)

        if expDay <= refDay:
            flogger.ELOG("Invalid Reference Day/Strip Length/Rolling "
                    "Period/Expiry Day Rule")
            return []

        expSet.append((refDay, expDay))
        refDay = expDay

    return expSet


def mkSTIRFuturesSet(ref, refDay='0d', stripLen='2y', expDayRule=None,
        rollPer=None, isin=None, doCommit=0, tag=None, qtype="Pct of Nominal",
        insid=None):
    flogger.DLOG("mkSTIRFutureSet processing " + str(ref) + " insid=" + insid)
    ref = insOf(ref)
    flogger.DLOG('mkSTIRFuturesSet::REF InsType=%s InsId=%s ISIN=%s' % (
            ref.instype, ref.insid, ref.isin))
    expSet = getExpSet(ref, refDay, stripLen, expDayRule, rollPer)
    for (startDay, expDay) in expSet:
        fut = mkSTIRFutures(ref, expDay, startDay, isin, doCommit, tag, qtype,
                insid)
        if fut:
            flogger.DLOG('mkSTIRFuturesSet::FUT InsId=%s ISIN=%s InsAddr=%s' %
                    (fut.insid, fut.isin, fut.insaddr))


#==============================================================================
# Log Set Up function
#==============================================================================


logmode = 0


def LogSetup():
    '''
        Set up the logging environment. If logging not enabled,
        just return the logger with no handlers. This will trigger
        a warning message but do not affect the functionality
        of the script.
            in:    - params (list)
                     [loggingEnabled (bool),
                      loggingPath (string),
                      loggingLevel (string)]
    '''
    global logger
    global logmode
    # set the debug level
    level = globalParams['LogLevel']
    if level == 'Info':
        logger.setLevel(logging.INFO)
        logmode = 2
    if level == 'Debug':
        logger.setLevel(logging.DEBUG)
        logmode = 3
    if level == 'Error':
        logger.setLevel(logging.ERROR)
        logmode = 1
    logToFile = False
    if (globalParams['LogFile'] != ""
        and globalParams['LogFile'] is not None
        and (globalParams['LogEnabled'] == 1
        or globalParams['LogEnabled'] == "1")):
        logToFile = True
    #FBDPRollback, Required call logme.setLogmeVar(8args).  Do NOT remove.
    ScriptName = "FContractStript"
    #logme.setLogmeVar(ScriptName,
    setLogmeVar(logme,
            ScriptName,
            logmode,
            not logToFile,
            logToFile,
            globalParams['LogFile'], 0, "", "")
    # set up loggers
    logger.handlers = []

    # if not enabled, do not create handlers

    if (not globalParams['LogEnabled']):
        #create handlers to file and console
        hdlrConsole = logging.StreamHandler()

        if hdlrConsole:
            cformatter = logging.Formatter('%(asctime)s %(levelname)s '
                    '%(message)s')
            hdlrConsole.setFormatter(cformatter)
            logger.addHandler(hdlrConsole)
#    if not globalParams['LogEnabled']:
#        return
    else:
        try:
            hdlrFile = logging.FileHandler(globalParams['LogFile'])
        except:
            print 'Error: Could not create log file:', globalParams['LogFile']
            # bind this file to nothing!! (added 2007-08-20)
            hdlrFile = None

        if hdlrFile:
            formatter = logging.Formatter('%(asctime)s %(levelname)s '
                    '%(message)s')
            hdlrFile.setFormatter(formatter)
            logger.addHandler(hdlrFile)

#==============================================================================
# AEL Menu
#==============================================================================

#------------------------------------------------------------------------------
# AEL Help functions
#------------------------------------------------------------------------------

quote_types = [ael.enum_to_string("QuoteType", i) for i in range(1, 20)]


pdn_list = [pd.id for pd in ael.ListNode.select() if not pd.father_nodnbr]
pdn_list.sort()


def PageDefRec(node):
    if  len(node.leafs()):
        leafList = [leaf.insaddr.insid for leaf in node.leafs()]
        return leafList
    elif len(node.reference_in()):
        pageList = []
        for ref in node.reference_in():
            refList = PageDefRec(ref)
            pageList.extend(refList)
        return pageList
    else:
        return []


def refIns(listNames=""):
    'List all relevant reference instruments'
    # changed to search for items
    if listNames == "":
        insList = []  # [ins.insid for ins in ael.Instrument.select()]
        #insList = [ins.insid for ins in ael.Instrument.select()]
        return insList
    insList = []
    for node in ael.ListNode.select():
        if not node.father_nodnbr and node.id in listNames:  # page_base_name:
            insList.extend(PageDefRec(node))
    insList.sort()
    return insList


refInsList = refIns()


def refDay():
    days = ['0d', '1d', '2d', '1w', '2w', '1m', '']
    return days


def stripLen():
    strips = ['1m', '3m', '6m', '12m', '18m', '24m', '1y', '2y', '3y', '4y']
    return strips


def rollPeriod():
    roll = ['1m', '3m', '6m', '9m', '12m']
    return roll


def expDayRule():
    rule = ['RefDay', 'IMM', '3rdWednesday', '3rdFriday',
            '1stWednesdayAfter9D']
    return rule

#-----------------------------------------------------------------------------
# AEL Variables Hooks
#-----------------------------------------------------------------------------

#These hooks should use
#pguiList2param and pguiParam2List to skip dependencies on the field numbers
#ignoring this problem for now


def RefInsHook(index, fieldValues):
    return fieldValues


def PageDefinitionHook(index, fieldValues):
    global refInsList
    while refInsList:
        refInsList.pop()
    refInsList.extend(refIns(fieldValues[8]))
    return fieldValues


def DisableLoggingHook(index, fieldValues):
    if fieldValues[10] == '0':
        # changed to 12 from 13
        for i in range(11, 12):
            ael_variables[i][9] = 0
    if fieldValues[10] != '0':
        # changed to 12 from 13
        for i in range(11, 12):
            ael_variables[i][9] = 1
    return fieldValues


#-----------------------------------------------------------------------------
# AEL Variables
#-----------------------------------------------------------------------------


ttReferenceInstrument = ("instrument that will be used as a template for "
        "creating new instruments")
ttReferenceDay = "relative day to create a strip against"
ttINSID = "Name of the instruments as <field text><date> or suggested id"
ttStripLenght = "length of the complete strip"
ttExpiryDayRule = "how to find the expiration day"
ttRollingPeriod = "period between instruments"
ttQuoteType = "set the quote type used"
ttFreeText = "free text to add in the instruments"
ttISINID = "ISIN will be <field text><date month code><date>"
ttPageDefBase = ("from which page definition a list of instrument will be "
        "selected from")
ttTestMode = "run but do not make any changes to the database"
ttLogEnabled = "enable/disable logging to file"
ttLogFile = "path to the logfile"
ttLogLevel = "amount of output"


ael_variables_main = [
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Reference Instrument',
                'Reference Instrument_generic',
                'FInstrument', refInsList, None,
                1, 1, ttReferenceInstrument, 0, None, 0],
        ['Reference Day',
                'Reference Day_override', 'string', refDay(), None,
                1, None, ttReferenceDay, None, 0],
        ['Strip Length',
                'Strip Length_override',
                'string', stripLen(), None,
                1, None, ttStripLenght, None, 0],
        ['Rolling Period',
                'Rolling Period_override',
                'string', rollPeriod(), None, None,
                None, ttRollingPeriod, None, 0],
        ['Expiry Day Rule',
                'Expiry Day Rule_override',
                'string', expDayRule(), None, None,
                None, ttExpiryDayRule, None, 0],
        # Advancede - tab
        ['Quote Type',
                'Quote Type (FRA)_Advanced',
                'string', quote_types, None,
                0, None, ttQuoteType, None, 0],
        ['Free Text',
                'Free Text_Advanced',
                'string', None, None,
                0, None, ttFreeText, None, 0],
        ['ISIN ID',
                'ISIN String_Advanced',
                'string', None, None,
                None, None, ttISINID, None, 0],
        ['PageDefBase',
                'Page Definition Name_Advanced',
                'string', pdn_list, None,
                0, 1, ttPageDefBase, PageDefinitionHook, 0],
        # Loggin - tab
        ['Test Mode',
                'Test Mode_Logging',
                'int', [1, 0], 0,
                0, 0, ttTestMode, None, 1],
        ['LogEnabled',
                'Log to File_Logging',
                'int', [1, 0], 0,
                0, 0, ttLogEnabled, DisableLoggingHook, 1],
        # was string
        ['LogFile',
                'Log File_Logging',
                'string', None, 'c:\TEMP\FContractStrips.log',
                0, 0, ttLogFile, None, 0],
        ['LogLevel',
                'Log Level_Logging',
                'string', ['Error', 'Info', 'Debug'], 'Info',
                0, 0, ttLogLevel, None, 1],
        #['Special',
        #        'Log Level_special',
        #        'string',['Error', 'Info', 'Debug'], 'Info',
        #        0, 0, None, None, None],
        # has to be here in order not to break a few callbacks
        ['INSID',
                'INSID String_Advanced',
                'string', None, None,
                None, None, ttINSID, None, 0],

   ]


#=============================================================================
#PRIME 3 compatibility code
#=============================================================================


class RollbackWrapper(FBDPRollback.RollbackInfo):
    def __init__(self, rollbackName=None, Testmode=0, param={}):
        importlib.reload(FBDPCommon)
        FBDPRollback.Rollback.Testmode = Testmode
        self.ael_variables_dict = param
        dTime = datetime.datetime.today()
        self.initializeSpecification((rollbackName[0:21] + ' ' +
                str(dTime)[2:19]))

    def end(self):
        FBDPCommon.Summary().log(self.ael_variables_dict)
        logme(None, 'FINISH')


def RollbackVersion(keyargs):

    if hasattr(FBDPRollback, "RollbackWrapper"):
        rollback = FBDPRollback.RollbackWrapper('mkSTIRFutures', **keyargs)
    else:
        rollback = RollbackWrapper('mkSTIRFutures', **keyargs)
    return rollback


# since logMeVar appearws different from 4.0 and 2.-0 veriosns we need
# a second version to solve it.
###setLogmeVar


def setLogmeVar(selfObj, ScriptName, LogMode, LogToConsole, LogToFile,
        Logfile, SendReportByMail, MailList, ReportMessageType):
    try:
        # version 4+
        selfObj.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile,
                Logfile, SendReportByMail, MailList, ReportMessageType)
    except Exception:
        # version 3+
        selfObj.setLogmeVar(ScriptName, LogMode, LogToConsole, LogToFile,
                Logfile)


#=============================================================================
# Main program
#=============================================================================

def ael_main_main(vdict):

    global logger
    # first the initalization of FLogger must be done
    #global flogger
    #logToConsole = True
    #fpath = False
    #if ((vdict['LogEnabled'] == "1" or vdict['LogEnabled'] == 1) \
    #        and vdict['LogFile']!= "" \
    #        and vdict['LogFile']!= None):
    #    logToConsole = False
    #    fpath = vdict['LogFile']
    #dLevels = {'Info': 1, 'Debug': 2 , 'Error': 4}
    #level = dLevels[vdict['LogLevel']]
    #flogger = flogger.Reinitialize(
    #                   logToPrime = False,
    #                   logToConsole = logToConsole,
    #                   logToFileAtSpecifiedPath = fpath,
    #                   level = level
    #               )
    referenceDay = vdict['Reference Day']
    stripLength = vdict['Strip Length']
    rollingPeriod = vdict['Rolling Period']
    expiryDayRule = vdict['Expiry Day Rule']
    insid = vdict['INSID']
    isinID = vdict['ISIN ID']
    tag = vdict['Free Text']
    qtype = vdict['Quote Type']

    # Start Rollback
    global rollback
    testmode = vdict['Test Mode']
    keyargs = {'Testmode': testmode, 'param': vdict}  # 'param': {}}
    # wrap the call for version 3 versions
    #rollback = FBDPRollback.RollbackWrapper('mkSTIRFutures', **keyargs)
    rollback = RollbackVersion(keyargs)
    # rollback = FBDPRollback.RollbackWrapper('mkSTIRFutures')
    # Set up logging
    global globalParams
    globalParams = vdict
    LogSetup()
    flogger.DLOG('Logger set up')
    commit = not vdict['Test Mode']
    logme(55 * '-')
    logme(' ')
    logme(' ')
    logme('Contract Strip Maintenance Start')  # flogger.DLOG('C Start')
    logme(' ')
    logme(' ')
    logme(55 * '-')
    for ri in vdict['Reference Instrument']:
        ins = insOf(ri)
        logMsg = 'Now handling Reference Instrument %s' % id
        if not globalParams['LogEnabled'] or logmode < 2:
            flogger.DLOG(logMsg)
        else:
            flogger.WLOG(logMsg)
        if not ins:
            logMsg = 'Reference Instrument %s not found' % id  # ERROR:
            flogger.ELOG(logMsg)
            FBDPCommon.Summary().fail(' ', 'mkSTIRFutures', logMsg, id)
        else:
            mkSTIRFuturesSet(ins, referenceDay, stripLength, expiryDayRule,
                    rollingPeriod, isinID, commit, tag, qtype, insid=insid)
            FBDPCommon.Summary().ok(ins, 'mkSTIRFutures')
    rollback.end()


#=============================================================================
# Specific instrument support
#
# will support euorDollar contracts and similar
#
#=============================================================================


def getSQLVal(query):
    """ Convenienve function to reterieve values from the database.
    Useful to retrieve elemnts by attributes
    """
    res = ael.asql(query)
    val = res[1][0][0][0]
    return val


def getSQLList(query):
    res = ael.asql(query)
    val = res[1][0]
    lst = [v[0] for v in val]
    return lst


def getBody(name):
    s = "select seqnbr from textobject where name = 'FSTIR_"
    s += name + "'"
    #x = getSQLVal(str)
    x = getSQLVal(s)
    z = ael.TextObject[x]
    text = z.get_text()
    return text


def filterHash(l):
    p = l.find("#")
    r = l
    if p >= 0:
        r = l[0:p]
    return r


def parseBody(name):
    getB = getBody(name)
    lines = getB.split("\n")
    lines = [filterHash(l) for l in lines if l.find("=") > 0]
    cmds = [(t[0:t.find("=")].strip(), t[t.find("=") + 1:].strip())
                for t in lines]
    cmds2 = [t for t in cmds if t[0] != ""]
    flogger.DLOG("got from python file ")
    flogger.DLOG(cmds2)
    return cmds2


#=============================================================================
#Instrument types, these are proxy objects to access other scripts
#=============================================================================

class generic:
    """
    the generic class , this will be subclassed to create the other classes
    """
    def __init__(self, params):
        self.params = params

    def copyParam(self, setw, tow):
        if tow in self.params:
            self.params[setw] = self.params[tow]

    def getParameters(self):
        """
        return the parameters formated as before
        """
        #self.copyParam('Reference Instrument','Reference Instrument_generic')
        #self.copyParam('Reference Day','Reference Day_override')
        #self.copyParam('Strip Length','Strip Length_override')
        #self.copyParam('Rolling Period','Rolling Period_override')
        #self.copyParam('Expiry Day Rule','Expiry Day Rule_override')

        return self.params

    def getStoredParams(self):
        """
        return the parameters with defaults set to the instrument defaults
        """
        return self.params

#
#This class has now become obsolete
#
#class euroDollar(generic):
#    """
#    This class will implement the euroDollar instrument, should be implemented
#    to be generated by something else, a generic euroDollar
#    """
#
#    def instrumentName(self):
#        #return "INTERNAL_MKTSTIR_EURODOLLAR" # does not work as name why ?
#        return "BDP_MKTSTIR_EURODOLLAR"
#
#
#    def build(self):
#        """ Build the instrument """
#
#
#        # will delete the old entry here, this is important if
#        # we start to load data from a database entry
#        oins = ael.Instrument[self.instrumentName()]
#        print oins
#        if oins:
#            oins.delete()
#
#        ins = ael.Instrument.new("Future/Forward")
#        ins.four_eye_on = 0 #No
#        ins.authorizer_usrnbr = 0
#        ins.insid = self.instrumentName()
#        ins.generic = 0 #No
#        ins.notional = 0 #No
#        ins.curr = "USD" # 8
#        ins.quote_type = "100-rate"
#        ins.otc = 0 #No
#        ins.mtm_from_feed = 1 #Yes
#        ins.spot_banking_days_offset = 2 # was 2 days
#        ins.suspended = 0 #No
#        ins.product_chlnbr = getSQLVal("select seqnbr from choicelist where "
#                 "entry = 'Swap' and list = 'ValGroup'")
#        ins.contr_size = 1.000000E+006
#        ins.phys_contr_size = 0
#        ins.und_insaddr = "USD/LIBOR/3M"
#        ins.und_instype = "RateIndex"
#        ins.settlement = "Cash"
#        ins.paytype = "Future"
#        setattr(ins, "exp_period.unit", "Days")
#        setattr(ins, "exp_period.count", 291)
#        ins.pay_day_offset = 1 # settle day
#        setattr(ins, "pay_period.unit", "Days")
#        setattr(ins, "pay_period.count", 0)
#        ins.call_option = 0 #No
#        ins.strike_price = 0
#        ins.strike_curr = 3
#        ins.digital = 0 #No
#        ins.barrier = 0 #0
#        ins.payout = 0
#        ins.callable = 0 #No
#        ins.putable = 0 #No
#        ins.index_factor = 0
#        ins.index_type = "Capital weighted"
#        ins.round_clean = 11
#        ins.round_premium = 11
#        ins.beta = 0
#        ins.coupons = 0
#        ins.coup_rate = 0
#        ins.face_value = 0
#        ins.accrued_arrear =0 #No
#        ins.settle_calnbr = 0
#        ins.category_chlnbr = getSQLVal(         #196
#                "select seqnbr from choicelist where entry = 'none' and "
#                "list = 'Category'")
#        setattr(ins, "ex_coup_period.unit", "Days")
#        setattr(ins, "ex_coup_period.count", 0)
#        ins.rate =0
#        ins.ref_price =0
#        ins.ref_value =0
#        ins.rating1_chlnbr =0
#        ins.rating2_chlnbr =0
#        ins.rating3_chlnbr = 0
#        ins.archive_status = 0
#        ins.total_issued = 0
#        ins.minimum_piece = 0
#        ins.minimum_incremental = 0
#        ins.price_diff_limit_abs = 0
#        ins.price_diff_limit_rel = 0
#        ins.short_sell = "Allowed"
#        ins.pay_offset_method = "Business Days"
#        ins.settle_category_chlnbr = getSQLVal( #197
#                "select seqnbr from choicelist where entry = 'none' and "
#                "list = 'Settle Category'")
#        ins.conversion_ratio = 0
#        ins.original_curr = "USD" # 8
#        ins.comb_category_chlnbr =0
#        ins.price_finding_chlnbr = 0
#        #isin
#        ins.dividend_factor = 0
#        ins.fix_fx_rate =0
#        ins.rebate =0
#        ins.exp_time =0
#        ins.fix_fx = 0 #No
#        ins.round_accrued =11
#        ins.bond_future_market = "DTB"
#        ins.seniority_chlnbr =0
#        ins.original_insaddr = 0
#        setattr(ins, "notice_period.unit", "Days")
#        setattr(ins, "notice_period.count", 0)
#
#        ins.fund_prfnbr = 0
#        ins.product_type_chlnbr = 0
#        ins.short_dividend_factor = 0
#        ins.quotation_seqnbr = getSQLVal( #15
#            "select seqnbr from quotation where name = '100-rate'")
#        ins.strike_quotation_seqnbr = 0
#        ins.rounding_spec_seqnbr = 0
#        ins.fixed_end_day = 0 #No
#
#        ins.commit()
#
#
#    def __init__(self, params):
#        """ create an instrument called INTERNAL_MKTSTIR_EURODOLLAR"""
#        self.params = params
#        self.build()
#
#
#    def setParam(self, what, val):
#        if not what in self.params \
#            or self.params[what].strip() == "":
#                self.params[what] = val
#
#    def getParameters(self):
#
#        # also needs to be flexible enough
#        #
#        self.params["Reference Instrument"] = (self.instrumentName(),)
#        self.setParam("ISIN ID", "ED")
#        self.setParam('Strip Length', "10y")
#        self.setParam('Rolling Period', "3m")
#        self.setParam('Expiry Day Rule','IMM') #3rdWednesday')
#        self.setParam('Reference Day', "0d")
#        print "Self params before sending ", self.params
#        #vals = generic.getParameters(self)
#        print "Params after ", self.params
#        return self.params


class fromObject(generic):

    def __init__(self, params, objname, mapping):
        """
        create an instrument called INTERNAL_MKTSTIR_EURODOLLAR
        """
        self.params = params
        #self.objname = objname
        self.inObjname = objname
        self.mapping = mapping
        # fetch the name by mapping
        # this is required as
        # module with names A_B
        # and A B can exist
        self.objname = mapping[objname]

    #
    #Obsolete
    #
    #def clear(self):
    #    # will delete the old entry here, this is important if
    #    # we start to load data from a database entry
    #    oins = ael.Instrument[self.instrumentName()]
    #    print oins
    #    if oins:
    #        oins.delete()

    def tr(self, val):
        if isInt(val):
            return int(val)
        else:
            try:
                return float(val)
            except:
                return val

    #
    #this has become an obsolete method
    #
    #def build(self):
    #
    #    self.clear()
    #
    #    # parse each line a very simple manner
    #    # the format is (<key>,<val>)
    #    items = parseBody(self.objname)
    #
    #    # for easy access
    #    dict = {}
    #    for d in items:
    #        dict[d[0]]=d[1]
    #
    #    #print dict
    #    #print "Instrument is ", dict['instype']
    #    ins = ael.Instrument.new(dict['instype'])
    #    ins.insid = self.instrumentName()
    #
    #
    #    # now for a very long interpretor loop
    #    for i in items:
    #
    #      key = i[0]
    #      val = i[1]
    #      print "Setting ",key, "=", val
    #
    #
    #      if key == "instype":
    #        pass
    #      elif key == "product_chlnbr":
    #        res = getSQLVal(
    #            "select seqnbr from choicelist where entry = '"
    #                +val+"' and list = 'ValGroup'")
    #        ins.product_chlnbr = res
    #      elif key == "category_chlnbr":
    #        res = getSQLVal(
    #          "select seqnbr from choicelist where entry = '"
    #              +val+"' and list = 'Category'")
    #        ins.category_chlnbr = res
    #      elif key == "settle_category_chlnbr":
    #        res = getSQLVal( #197
    #            "select seqnbr from choicelist where entry = '"
    #                +val+"' and list = 'Settle Category'")
    #        ins.category_chlnbr = res
    #      elif key == "quotation_seqnbr":
    #        res = getSQLVal(
    #            "select seqnbr from quotation where name = '"+val+"'")
    #        ins.quotation_seqnbr = res
    #      elif key in ["Reference Instrument" , \
    #                    "ISIN ID", \
    #                    'Strip Length', \
    #                    'Rolling Period', \
    #                    'Expiry Day Rule', \
    #                    'Reference Day', \
    #                    'Quote Type']:
    #        pass
    #      else:
    #        setattr(ins,key, self.tr(val))
    #
    #    ins.commit()
    #
    #    # set all the params
    #
    #    self.params["Reference Instrument"] = (self.instrumentName(),)
    #    self.setParam('Strip Length', dict["Strip Length"])
    #    self.setParam('Rolling Period', dict["Rolling Period"])
    #    self.setParam('Expiry Day Rule', dict['Expiry Day Rule'])  # 3rd Wed
    #    self.setParam('Reference Day', dict["Reference Day"])
    #
    #    # optional variables
    #    self.setParamFD('Quote Type', dict)
    #    self.setParamFD('Free Text', dict)
    #    print "The dictionary!!", dict
    #    self.setParamFD("ISIN ID", dict)

    # is this in the GUI control ??
    # 100-rate

    def getStoredParams(self):
        """
        Return the parameters with defaults set to the instrument defaults
        """
        items = parseBody(self.objname)
        # convert the list of format [(K,V),..]
        # to { K:V, ...}
        D = {}
        for T in items:
            D[T[0]] = T[1]
        D['StdContract'] = self.objname.replace("_", " ")
        return D

    def setParamFD(self, what, dct):
        if what in dct:
            self.setParam(what, dct[what])

    def setParam(self, what, val):
        if not what in self.params \
            or self.params[what].strip() == "":
                # special handling for StdContract
                self.params[what] = val

    #
    #Obsolete
    #
    #def instrumentName(self):
    #    #return "INTERNAL_MKTSTIR_EURODOLLAR" # does not work as name why ?
    #    return "BDP_MKTSTIR_"+self.objname


#=============================================================================
#Generator of new instruments
#=============================================================================


class genIns:

    def  __init__(self, kind=None, params=None):
        self.kind = kind
        self.params = params

    def makeProxyInstrument(self):

        #print "~"*5, "params", "~"*5
        #print self.params
        #print "~"*18

        if self.kind == "Custom":
            return generic(self.params)
        else:
            # best effort _<word>_<bword> mapping
            if not hasattr(self, "textobjects"):
                self.getList()
            return fromObject(self.params, self.kind, self.textobjects)
            #raise NotImplementedError("Not yet implemented")
        #if self.kind == "EuroDollar":
        #    return euroDollar(self.params)
        #else:
        #    return generic(self.params)

    def getList(self):
        """
        generate list of available elements
        """
        lst = getSQLList("select name from textobject where type = "
                "'AEL Module' and name like 'FSTIR_%'")
        # reformat the strings to be visible
        dictL = [((s[6:]).replace("_", " "), s[6:]) for s in lst]
        self.textobjects = dict(dictL)
        lst = [((s[6:]).replace("_", " ")) for s in lst]
        lst.append("Custom")
        #return ["EuroDollar", "Generic"]
        return lst

#=============================================================================
#Menu input elements
#=============================================================================

#=========================================================
# Functions to change the values in the parameter GUI
#=========================================================


def pguiList2param(fvals):
    dct = {}
    for i in range(len(fvals)):
        if (fvals[i] != ''):
            dct[ael_variables[i][0]] = fvals[i]
    return dct


def pguiParam2List(params):

    lst = []
    for i in range(len(ael_variables)):
        e = ael_variables[i][0]
        if e in params:
            lst.append(params[e])
        else:
            lst.append('')
    return lst


def getMenuHook(Name, lst=None, itr=0):

    if (lst == None):
        lst = ael_variables
    if (lst == []):
        return
    if (lst[0][0] == Name):
        return (lst[0][8], itr)
    return getMenuHook(Name, lst[1:], itr + 1)


#
#Lockdown/Unlock all menu items that are part of an instrument
#
def lockdown(direction):
    for i in range(len(ael_variables)):
        # exclude the instrument and the logging
        if (ael_variables[i][0] != "StdContract" and \
            ael_variables[i][1][-8:] != "_Logging"):
            ael_variables[i][9] = direction


#
#Read ael_variables and replace the values of the logger variables
#
def noLoggingDefaults(nparam, param):
    for i in range(len(ael_variables)):
        # exclude the instrument and the logging
        if (ael_variables[i][1][-8:] == "_Logging"):

            nparam[ael_variables[i][0]] = param[ael_variables[i][0]]
    return nparam


def MenuManager(Index, fvals):
    #
    #This should change the whole table using the generic instrument
    #

    flogger.DLOG("=" * 10 + "fvals" + "=" * 10)
    flogger.DLOG(fvals)
    flogger.DLOG("~" * 20)
    param = pguiList2param(fvals)
    flogger.DLOG(param)

    # the custom criteria doesn't have defaults
    if param['StdContract'] == 'Custom':
        # all options should be none locked if custom
        lockdown(1)
        return fvals
    # values should be locked if anything else is selected
    lockdown(0)

    factory = genIns(param['StdContract'], param)
    pins = factory.makeProxyInstrument()
    nparam = pins.getStoredParams()
    flogger.DLOG("~" * 5 + "MenuManager param list" + "~" * 5)
    flogger.DLOG(nparam)
    noLoggingDefaults(nparam, param)
    nfvals = pguiParam2List(nparam)
    flogger.DLOG(nfvals)

    # switch this to amother function

    # adjust the referenceInstrument list by calling
    # appropriate call back
    (hook, indexI) = getMenuHook("PageDefBase")
    if (nfvals[indexI] != ''):
        nres = hook(indexI, nfvals)
    else:
        nres = nfvals

    #Should be moved into another function together
    #with above statmeent
    (hook, indexI) = getMenuHook("LogEnabled")
    if (nfvals[indexI] != ''):
        nres = hook(indexI, nres)

    # select an instrument if there is only one available in
    # the refInsList ..
    if len(refInsList) == 1:
        flist = pguiList2param(nres)
        flist['Reference Instrument'] = refInsList[0]
        fres = pguiParam2List(flist)
    else:
        fres = nres
    return fres


#==========================================================

def ael_main_extra(vdict):
    """
    The purpose of this function is to add reference instrument to the
    database to support the script, and modify vdict to suit the indata
    in the previous script

    It should support alternative user interfaces that have been simplified
    """
    #print "Vdict", ">"*10, "\n", vdict, "\n", ">"*10, "\n"
    #factory = genIns(vdict['StdContract'], vdict)
    #pins = factory.makeProxyInstrument()
    #xdict = pins.getParameters()
    #print "Created the parameters ", xdict, " not yet sending to next stage"
    #ael_main_main(xdict)
    ael_main_main(vdict)
    #print "Ignoring requests since GUI is set elsewhere!"


def extraList():
    """ Create a list of options, the word generic is special in this case.."""
    return genIns().getList()


#
#Useful if mixing both generic and none generic in the same input menu
#
def makeNoneMandatory(List):
    """ remove any required fields """
    for i in range(len(List)):
        if len(List[i]) > 5:
            List[i][5] = 0
    return List


def ael_variables_fun():
    #global ael_variables_main
    ex = [
            ['StdContract',
                    'Standard Contract Instrument',
                    'string', extraList(), "Custom",
                    1, 0, "Standard Contract Instrument", MenuManager, 1]
    ]
    # need to be done like this because other hook changes ael_variables_main
    # directly and hence uses how python creates list
    #makeNoneMandatory(ael_variables_main).extend(ex)
    ael_variables_main.extend(ex)
    return ael_variables_main

ael_variables_extra = ael_variables_fun()


#=============================================================================
# Hooks into the module for PRIME
#=============================================================================


def ael_main(vdict):
    return ael_main_extra(vdict)


ael_variables = ael_variables_extra
