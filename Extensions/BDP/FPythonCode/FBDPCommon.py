""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPCommon.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
Module
    FBDPCommon - Module with commonly used code only.

DESCRIPTION
    Includes code to perform common actions.
----------------------------------------------------------------------------"""
import time
import string
import copy
import sys
import traceback
import types
import collections
import inspect


import ael
import acm


import FBDPCurrentContext
from __builtin__ import getattr

DoProfile = 0
_Name = 'Name'
_ExternalId1 = 'ExternalId1'
_ExternalId2 = 'ExternalId2'
_Isin = 'Isin'

def getMaxNameLength(o, default=39):
    return getMaxFStringFieldLength(o, _Name, default)

def getMaxExternalId1Length(o, default=29):
    return getMaxFStringFieldLength(o, _ExternalId1, default)

def getMaxExternalId2Length(o, default=29):
    return getMaxFStringFieldLength(o, _ExternalId2, default)

def getMaxIsinLength(o, default=20):
    return getMaxFStringFieldLength(o, _Isin, default)

def getMaxFStringFieldLength(o, name, default):
    try:
        cls = None
        if hasattr(o, 'IsClass') and o.IsClass():
            cls = o
        else:
            cls = o.GetClass()

        return cls.GetMethod(name, 0).Attribute().Domain().Size()
    except:
        pass

    return default


def convertEntityList(l, d):
    l = l and [i.Oid() for i in l] or []
    return l


def selectionHook(selection, hook, d):
    try:
        import FBDPHook
        reload(FBDPHook)
    except ImportError:
        return selection
    try:
        hook = getattr(FBDPHook, hook)
    except AttributeError:
        return selection
    return hook(selection, d)


def callSelectionHook(d, selId, hook):
    selection = d.get(selId)
    if selection:
        d[selId] = selectionHook(selection, hook, d)


def getPrimaryKey(o):
    try:
        return o.Oid()
    except AttributeError:
        for i in eval('ael.%s.keys()' % o.record_type):
            if i[1] == 'primary':
                return getattr(o, i[0])
    raise TypeError('No primary key for' + o)


def record_type(entity):
    if is_acm_object(entity):
        return entity.RecordType()
    else:
        return entity.record_type


def is_acm_object(o):
    try:
        o.Oid()
        return True
    except Exception:
        return False

def acm_to_ael(o):
    e = None
    exec "e = ael.%s[o.Oid()]" % o.RecordType()
    return e


def ael_to_acm(e):
    return acm.Ael.AelToFObject(e)


def children(obj):
    lst = acm.FArray()
    for typ in obj.Parts():
        for c in typ:
            lst.Add(c)
    return lst


def commit(clone, entity=None):
    if is_acm_object(clone):
        if entity:
            entity.Apply(clone)
        else:
            entity = clone
        entity.Commit()
        return True
    else:
        clone.commit()
        return True


def clone(entity):
    if is_acm_object(entity):
        return entity.Clone()
    else:
        return entity.clone()


def delete(entity):
    if is_acm_object(entity):
        return entity.Delete()
    else:
        return entity.delete()


def get_attr(entity, a):
    if is_acm_object(entity):
        if not a in dir(entity):
            return 0
        return entity.GetProperty(a)
    else:
        return getattr(entity, a)


def set_attr(entity, field, value):
    if is_acm_object(entity):
        entity.SetProperty(field, value)
    else:
        setattr(entity, field, value)


def has_attr(entity, a):
    if is_acm_object(entity):
        try:
            entity.GetProperty(a)
            return True
        except AttributeError:
            False
    else:
        return hasattr(entity, a)

spaceCollection = acm.FStandardCalculationsSpaceCollection()
getObject = acm.GetFunction("getObject", 2)
perUnitQuotation = getObject(acm.FQuotation, "Per Unit")

def trade_premium_from_quote(trade, price, date):
    trade = trade if is_acm_object(trade) else ael_to_acm(trade.clone())
    return trade.Calculation().PriceToPremium(spaceCollection, date, price)

def sendMail(TO, SUBJECT, MSG):

    import smtplib

    HOST = None
    try:
        HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
            'mailServerAddress').Value()
    except:
        pass

    if not HOST:
        FBDPCurrentContext.Logme()('No mail server address specified!\n '
                'Please specify your mail server name or IP address in the '
                'extension attribute mailServerAddress!')

    FROM = "PRIME client"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", MSG), "\r\n")

    try:
        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, TO.split(','), BODY)
        server.quit()
        FBDPCurrentContext.Logme()('Mail sent to: %s' % TO)
    except:
        FBDPCurrentContext.Logme()('Failed sending mail.')


def execute_script(fn, *rest):
    """
    Simple operation for executing a script(procedure) that can be profiled.
    ReturnValue: None
    """
    FBDPCurrentContext.Logme()(None, 'START')
    FBDPCurrentContext.Summary().setStartTime(time.time())

    import __main__
    __main__.__dict__[fn.__name__] = fn
    try:
        if DoProfile:
            import profile
            s = "%s%s" % (fn.__name__, str(rest))
            profile.run(s)
        else:
            fn(*rest)
        acm.PollDbEvents()
    except AttributeError:
        FBDPCurrentContext.Logme()(get_exception(), 'ERROR')
    except RuntimeError:
        FBDPCurrentContext.Logme()(get_exception(), 'ERROR')
    except Exception:
        FBDPCurrentContext.Logme()(get_exception(), 'ERROR')

def eps_compare(a, b=0.0, eps=1e-10):
    """Predicate for checking if a value (float) is zero """
    if abs(a - b) < eps:
        return 1
    return 0


def create_quotetype_price(ins, price):
    """------------------------------------------------------------------------
    FUNCTION
        create_quotetype_price(ins, price):

    DESCRIPTION
        Returns a price based on the Quote Type of an instrument.

    ARGUMENTS
        ins    ael_entity     Instrument
        price  integer/float  Price to convert, given as 'Per Unit' or
                              'Per Contract'
    ------------------------------------------------------------------------"""
    if not is_acm_object(ins):
        ins = ael_to_acm(ins)
    today = acm.Time.DateToday()
    priceDv = ins.DenominatedValueSpot(price, today)
    return ins.UnitValueToQuote(priceDv, today, today, True, None, None,
            ins.Quotation(), 1.0, 0.0).Number()

def create_price(ins, quotetype_price):
    """------------------------------------------------------------------------
    FUNCTION
        create_price(ins, quotetype_price):

        Returns the price in 'Per Unit' or 'Per Contract'

    ARGUMENTS
        ins              ael_entity     Instrument
        quotetype_price  integer/float  Price to convert, given in the Quote
                                        Type of the instrument.
    ------------------------------------------------------------------------"""
    if not is_acm_object(ins):
        ins = ael_to_acm(ins)
    return ins.Calculation().PriceConvert(spaceCollection,
        quotetype_price, ins.Quotation(), perUnitQuotation)


def get_exception():
    """Returns last exception as string"""
    excInfo = sys.exc_info()
    d = traceback.format_exception_only(excInfo[0], excInfo[1])
    msg = string.join(d, '')
    return msg


def toDateAEL(strDate, calOrCurr=None):
    """
    Accepts 'Today', a date or an integer as input. Converts to a date
    (ael.date)
    """
    if strDate and type(strDate) == type(''):
        if type(calOrCurr) == type(''):
            calOrCurr = ael.Party[calOrCurr]
        if calOrCurr == None:
            calOrCurr = ael.Instrument[acm.UsedValuationParameters(
                        ).AccountingCurrency().Name()]
        strDate = strDate.strip()
        firstLetter = strDate[0].upper()
        if firstLetter == 'Today'[0]:
            return ael.date_today()
        elif strDate == 'Never':
            return ael.date('1970-01-01')
        elif firstLetter == 'Previous banking day'[0]:
            return ael.date_today().add_banking_day(calOrCurr, -1)
        elif firstLetter == 'Next banking day'[0]:
            return ael.date_today().add_banking_day(calOrCurr, 1)
        else:
            try:
                day = ael.date(strDate[:10])
            except TypeError:
                try:
                    diff = abs(int(strDate))
                except ValueError:
                    try:
                        day = ael.date_today().add_period(strDate[:10])
                    except TypeError:
                        raise Exception("Invalid date (%s). Format is: %%Y-%%m"
                                "-%%d, a period, 'Today' or 'Never', \n "
                                "e.g. 2001-01-01, -1y, -3m, 'Today', 'Never' "
                                "etc." % strDate)
                else:
                    day = ael.date_today().add_banking_day(calOrCurr, -diff)
            return day
    return strDate


def toDate(strDate, calOrCurr=None):
    """
    Accepts 'Today', a date or an integer as input. Converts to a date
    """
    if strDate and type(strDate) == type(''):
        if type(calOrCurr) == type(''):
            calOrCurr = acm.FCurrency[calOrCurr].Calendar()
        elif calOrCurr == None:
            calOrCurr = acm.FCurrency[
                    str(acm.UsedAccountingCurrency())].Calendar()
        elif (calOrCurr.RecordType() == 'Instrument' and
                calOrCurr.Category() == 'Currency'):
            calOrCurr = calOrCurr.Calendar()
        if not calOrCurr.RecordType() == 'Calendar':
            raise Exception("Second parameter must specify a existing "
                    "FCurrency or FCalendar.")

        strDate = strDate.strip().upper()
        if strDate == 'TODAY':
            return acm.Time.DateToday()
        elif strDate in ('NEVER', 'INCEPTION'):
            return "1970-01-01"
        elif strDate == 'PREVIOUS BANKING DAY':
            return calOrCurr.AdjustBankingDays(acm.Time.DateToday(), -1)
        elif strDate == 'NEXT BANKING DAY':
            return calOrCurr.AdjustBankingDays(acm.Time.DateToday(), 1)
        elif strDate == 'FIRST OF MONTH':
            return acm.Time.FirstDayOfMonth(acm.Time.DateToday())
        elif strDate == 'FIRST OF QUARTER':
            return acm.Time.FirstDayOfQuarter(acm.Time.DateToday())
        elif strDate == 'FIRST OF YEAR':
            return acm.Time.FirstDayOfYear(acm.Time.DateToday())
        else:
            day = acm.Get('formats/DateTimeDefault').Parse(strDate)
            isDate = True
            try:
                d = int(strDate)
                if d <= 100:
                    isDate = False
            except:
                pass

            if not day or not isDate:
                try:
                    d = int(strDate)
                    if d > 0:
                        raise ValueError()
                except ValueError:
                    raise Exception("Invalid date (%s). Format is: "
                            "%%Y-%%m-%%d, a period, a negative integer, "
                            "'Today' or 'Never', \n e.g. 2001-01-01, -1y, "
                            "-3m, -20, 'Today', 'Never' etc." % strDate)
                else:
                    day = calOrCurr.AdjustBankingDays(acm.Time.DateToday(), d)
            return acm.Time.AsDate(day)
    return strDate


def toDateTime(date_time_str, calOrCurr=None):
    if date_time_str.upper() == 'TODAY':
        return toDate(date_time_str, calOrCurr)
    dt = acm.Get('formats/DateTimeDefault').Parse(date_time_str)
    if not dt:
        dt = toDate(date_time_str, calOrCurr)
    return dt


def businessDaySpot(instrument, orgDate):
    """Calculates the business day spot for the AEL date based on the
    instrument's currency. Instrument is expected to be an ael.Instrument or an
    acm.FInstrument; orgDate an ael.date"""
    currInst = None
    instID = ''
    spotOffset = 0
    if type(instrument) == ael.ael_entity:
        currency = instrument.curr
        currInst = acm.FInstrument[currency.insaddr]
        instID = instrument.insid
        spotOffset = instrument.spot_banking_days_offset
    else:
        currInst = acm.FInstrument[instrument.Currency().Name()]
        instID = instrument.Name()
        spotOffset = instrument.SpotBankingDaysOffset()
    if not currInst:
        raise RuntimeError('No currency calendar for %s' % instID)
    cal = currInst.Calendar()
    return cal.AdjustBankingDays(orgDate, spotOffset)

def get_result_in_list(sql_result):
    result = []
    for rset in sql_result:
        for column in rset:
            result.append(column[0])
    return result


def createNewNameByAddingDate(
        oldName, date, nameExistCB, maxLen=30, nameExistList=None):
    """ Create a new name for a historical entity
    The new name is on the format: oldName<underscore>historicalDate """
    if nameExistList is None:
        nameExistList = []
    historicalDate = str(date)
    # Suffix will be of form "_historicalDate"
    suffixLen = 1 + len(historicalDate)
    nameLen = len(oldName)
    if nameLen + suffixLen > maxLen:
        nameLen = maxLen - suffixLen
    newName = oldName[0:nameLen] + '_' + historicalDate
    exist = nameExistCB(newName) or (newName in nameExistList)
    i = 0
    while exist:
        nr = '%d' % (i)
        # Suffix will be of form "_nr_historicalDate"
        suffixLen = 1 + len(nr) + 1 + len(historicalDate)
        nameLen = len(oldName)
        if nameLen + suffixLen > maxLen:
            nameLen = maxLen - suffixLen
        newName = oldName[0:nameLen] + '_' + str(nr) + '_' + historicalDate

        exist = nameExistCB(newName) or (newName in nameExistList)
        i = i + 1

    return newName


def calculate_premium(t):
    isAcm = is_acm_object(t)
    ins = t.Instrument() if isAcm else t.insaddr
    typ = t.Type() if isAcm else t.type
    instype = ins.InsType() if isAcm else ins.instype
    premium = t.Premium() if isAcm else t.premium

    if typ not in ['Cash Posting', 'Clear PL', 'PL Sweep', 'Spot Roll']:
        attr = 'Premium' if isAcm else 'premium'
        price = t.Price() if isAcm else t.price
        # fx cash
        if instype == 'Curr':
            if isAcm:
                t.UpdatePremium(1)
                premium = t.Premium()
            else:
                t.fx_update_non_dealt_amount(t.price)
                premium = t.premium
            # UpdatePremium will call fx_util_update_amounts and update
            # premium OR quantity
        else:
            acc_day = t.AcquireDay() if isAcm else t.acquire_day
            premium = trade_premium_from_quote(t, price, acc_day)
            set_attr(t, attr, premium)
        set_attr(t, 'AggregatePl' if isAcm else 'aggregate_pl', 0.0)
    return premium

def calculate_price_acm(trade):
    return trade.Calculation().PremiumToPrice(spaceCollection,\
                    trade.AcquireDay(), trade.Premium())

def calculate_premium_amc(trade):
    return trade.Calculation().PriceToPremium(spaceCollection, \
                    trade.AcquireDay(), trade.Price()).Number()

def convertDurationInSecondsToHoursMinutesSeconds(timeInSeconds):
    timeInSeconds = int(timeInSeconds)
    mins = timeInSeconds // 60
    hrs = mins // 60
    return '{0:02d}:{1:02d}:{2:02d}'.format(hrs, mins % 60, timeInSeconds % 60)

def dateAddDatePeriod(date, period):
    period = acm.Time.AddDatePeriods(period, '0d')
    period = str(period).strip()
    unit = period[-1].lower()
    period = period[:-1]
    if unit == 'd':
        return acm.Time.DateAddDelta(date, 0, 0, period)

    if unit == 'm':
        return acm.Time.DateAddDelta(date, 0, period, 0)

    if unit == 'y':
        return acm.Time.DateAddDelta(date, period, 0, 0)

    raise Exception('Cannot shift date %s by period: %s' % (date, period))

def reloadModule(name):
    ctx = acm.GetDefaultContext()
    if name in ctx.ModuleNames():
        ctx.RemoveModule(name)
        if name in ctx.ModuleNames():
            raise Exception('Failed to remove module: %s' % name)

    if name not in ctx.ModuleNames():
        ctx.AddModule(name)

    if name not in ctx.ModuleNames():
        raise Exception('Failed to add module: %s' % name)

#--------- Classes

class CalculationSpaceManager:
    Result = collections.namedtuple('Result', 'object_name value')

    def __init__(self, use_distributed_calc):
        self._distribute = bool(use_distributed_calc)
        self._space = None
        self._calcs = {}

    def init(self, asql_query, column_names):
        assert not self._calcs, 'CalculationSpaceManager already initialized'
        collection = acm.Calculations().CreateCalculationSpaceCollection()
        self._space = collection.GetSpace(
            acm.FPortfolioSheet, acm.GetDefaultContext().Name(),
            None, self._distribute
        )
        node = self._space.InsertItem(asql_query)
        self._space.Refresh()
        it = node.Iterator().FirstChild()
        while it:
            tree = it.Tree()
            name = tree.Item().StringKey()
            for column_name in column_names:
                calc = self._space.CreateCalculation(tree, column_name)
                self._calcs.setdefault(column_name, []).append((name, calc))

            it = it.NextSibling()

        return

    def run(self):
        assert self._calcs, 'CalculationSpaceManager not initialized'
        self._space.Refresh()
        results = {}
        for column_name, calcs in self._calcs.items():
            lst = []
            for name, calc in calcs:
                lst.append(self.Result(
                    object_name=name, value=calc.FormattedValue()
                ))

            results[column_name] = tuple(lst)

        return results


class FBDPQuerySelection:
    def __init__(self, name, query_expr, num_results_per_row=1,
            result_types=[]):
        if result_types:
            assert len(result_types) == num_results_per_row, \
            'Size of result_type must match num_results_per_row'

        self._name = name
        self._query_expr = query_expr
        self._num_results_per_row = num_results_per_row
        self._result_types = result_types

    def Name(self):
        return self._name

    def Run(self, time_execution=False):
        """
        Executes the rpc and returns the results list.
        """
        def typeCast(value, result_type):
            if isinstance(result_type, type):
                # is builtin type and requires casting
                return result_type(value)

            # is custom type and require retrieval
            return result_type[value]

        def run():
            queryResult = ael.dbsql(self._query_expr)
            if self._num_results_per_row == 1:
                rows = [row[0] for row in queryResult[0]]
                if self._result_types:
                    result_type = self._result_types[0]
                    return [typeCast(r, result_type) for r in rows]

                return rows

            rows = [row[:self._num_results_per_row] for row in queryResult[0]]
            if self._result_types:
                for col_idx, result_type in enumerate(self._result_types):
                    for row in rows:
                        row[col_idx] = typeCast(row[col_idx], result_type)

            return rows

        if time_execution:
            start_time = time.time()
            results = run()
            end_time = time.time()
            ms_duration = int((end_time - start_time) * 1000.0)
            return results, ms_duration

        return run()


class ListDict(dict):
    """ Extension of ordinary dictionary to be used when value is a list"""
    def __deepcopy__(self, x):
        return ListDict(copy.deepcopy(dict(self)))

    def add(self, key, value):
        """ Appends on value to key """
        if key in self and self[key] is not None:
            if type(self[key]) != type([]):
                raise RuntimeError('Invalid use, values should be a list not '
                        '%s:%s' % (key, value))
            values = self[key]
        else:
            values = []
        values.append(value)
        self[key] = values

    def items(self, cmp_fn=None):
        """ Redefined items operator that can return items sorted. The cmp_fn
            is applied in the keys i.e. keys=D.keys(); keys.sort(cmp_fn) """
        if not cmp_fn:
            return dict.items(self)
        else:
            keys = self.keys()
            keys.sort(cmp_fn)
            tmp = []
            for k in keys:
                tmp.append((k, self[k]))
            return tmp

    def sort(self, cmp_fn=None):
        if not cmp_fn:
            cmp_fn = cmp
        for (k, v) in self.items():
            v.sort(cmp_fn)
            self[k] = v

    def __getitem__(self, i):
        return self.get(i) or []


class SummaryStatics:
    tables = {}
    finalTables = {}
    singleton = None
    startTime = time.time()

class SummaryLocal:
    EXCLUDE = 'excluded'
    DELETE = 'deleted'
    UPDATE = 'updated'
    CREATE = 'created'
    AGGREGATE = 'aggregated'
    DEAGGREGATE = 'deaggregated'
    ARCHIVE = 'archived'
    DEARCHIVE = 'dearchived'
    CLEAR = 'cleared'
    ADJUST = 'adjusted'
    ABANDON = 'abandoned'
    CLOSE = 'closed'
    EXERCISE = 'exercised'
    ASSIGN = 'assigned'
    CASHPOST = 'cashposted'
    PROCESS = 'processed'
    RENAME = 'renamed'
    SWEEP = 'sweeped'

    POSITION = 'Position'

    SWEEP = 'swept'
    ROLL = 'rolled over'

    IGNORE = 'ignored'
    WARNING = 'warning'
    FAIL = 'failed'
    OK = 'ok'

    OK_IDS = 'okIds'

    action = 'n/a'
    EMPTY = ' '

    def __init__(self, tables=None, finalTables=None, startTime=None):
        self.tables = tables if tables else {}
        self.finalTables = finalTables if finalTables else {}
        self.startTime = startTime if startTime else time.time()

    def tableInit(self, entity, action):
        if type(entity) == type(' '):
            self.key = (entity, action)
        else:
            try:
                self.key = (entity.RecordType(), action)
            except (AttributeError):
                self.key = (entity.record_type, action)
        if self.key not in self.tables:
            self.tables[self.key] = ListDict()
            self.tables[self.key].add(self.OK, 0)

    def notOk(self, result, entity, action, reason, objectId):
        self.tableInit(entity, action)
        self.tables[self.key].add(result, (objectId, reason))

    def ignore_action(self, entity, reason, objectId):
        self.notOk(self.IGNORE, entity, SummaryLocal.action, reason, objectId)

    def ignore(self, *arg):
        self.notOk(self.IGNORE, *arg)

    def warning(self, *arg):
        self.notOk(self.WARNING, *arg)

    def fail_update(self, entity, reason, objectId):
        self.notOk(self.FAIL, entity, SummaryLocal.UPDATE, reason, objectId)

    def fail(self, *arg):
        self.notOk(self.FAIL, *arg)

    def ok_update(self, entity, identity=None, n=1):
        self.ok(entity, SummaryLocal.UPDATE, identity, n)

    def ok(self, entity, action, identity=None, n=1):
        self.tableInit(entity, action)
        self.tables[self.key][self.OK][0] += n
        if identity:
            self.tables[self.key].add(self.OK_IDS, identity)

    def removeOk(self, entity, action, identity=None, n=1):
        self.tableInit(entity, action)
        if self.tables[self.key][self.OK][0] != 0:
            self.tables[self.key][self.OK][0] -= n
        if identity:
            if self.tables[self.key][self.OK_IDS].count(identity) > 0:
                self.tables[self.key][self.OK_IDS].remove(identity)

    def commitEntries(self):
        if self.tables:
            self.finalTables = copy.deepcopy(self.tables)

    def abortEntries(self):
        if self.finalTables:
            self.tables = self.finalTables.copy()
        else:
            # We only abort the OK entry, but still leave the errors and
            # warnings there.
            for (table, action) in self.tables.keys():
                self.removeOk(table, action)

    def log(self, args):
        self.commitEntries()
        FBDPCurrentContext.Logme()(self.buildHeader(), 'NOTIME')
        FBDPCurrentContext.Logme()(self.buildExecutionParametersStr(args),
                'NOTIME')
        FBDPCurrentContext.Logme()(self.buildErrorsAndWarningsStr(), 'NOTIME')
        FBDPCurrentContext.Logme()(self.buildActionStr(), 'NOTIME')

    def buildHeader(self):
        s = "\n%s S U M M A R Y %s\n" % ('-' * 30, '-' * 30)
        s += '\nReport date: %s' % str(ael.date_today())
        s += '\nExecution time (hh:mm:ss): {0}\n'.format(
                convertDurationInSecondsToHoursMinutesSeconds(time.time() -
                self.startTime))
        return s

    def buildExecutionParametersStr(self, args):
        s = 'Execution parameters:'
        keys = args.keys()
        keys = [(x.upper(), x) for x in keys]
        keys.sort()
        for k in keys:
            x = args[k[1]]
            if is_acm_object(x):
                v = x.Name()
            else:
                v = str(args[k[1]])
            if len(v) > 60:
                v = v[0:60] + '...'
            s += '\n   %s: %s' % (k[1], v)
            if (k[0] == 'LOGFILE' and
                    'LogPath' in dir(FBDPCurrentContext.Logme())):
                s += '\n   %s: %s' % ('Logpath',
                        FBDPCurrentContext.Logme().LogPath)
        return s

    def buildErrorsAndWarningsStr(self):
        s = '\nErrors and warnings:'
        noFailed = True
        for (table, action) in self.finalTables.keys():
            listDict = self.finalTables[(table, action)]
            for mode in ((self.FAIL, 'ERROR: Failed'),
                         (self.IGNORE, 'NOTICE: Ignored'),
                         (self.WARNING, 'WARNING:')):
                for (eid, reason) in listDict[mode[0]]:
                    noFailed = False
                    s += '\n   %s %s %s: %s' % (mode[1], table, eid, reason)
        if noFailed:
            s += '\n   None'
        return s

    def buildActionStr(self):
        s = '\n%-25s%-14s%-7s%-9s%-6s\n%-s\n' % (
                                                               'ENTITY',
                                                               'ACTION',
                                                               'OK',
                                                               'FAILED',
                                                               'IGNORED',
                                                               '-' * 75)
        keys = self.finalTables.keys()
        keys.sort()
        for (table, action) in keys:
            if table == self.EMPTY:
                continue
            listDict = self.finalTables[(table, action)]
            n_ignored = len(listDict[self.IGNORE])
            n_failed = len(listDict[self.FAIL])
            n_ok = listDict.get(self.OK)[0] or 0
            s2 = '%-25s%-15s%-9d%-9d%-9d\n' % (table, action, n_ok, n_failed,
                    n_ignored)
            s = s + s2
        s += "\n%s\n" % ('-' * 75)
        return s

    def buildOkIdsStr(self, logTables=[]):
        s = ''
        for (table, action) in self.finalTables.keys():
            if logTables and table not in logTables:
                continue
            sHeader = '\nThe following %s(s) were %s:' % (table, action)
            listDict = self.finalTables[(table, action)]
            sNames = ''
            for name in listDict[self.OK_IDS]:
                sNames += '\n   %s' % name
            if sNames:
                s += sHeader
                s += sNames
                s += '\n'
        return s

    def setStartTime(self, startTime):
        self.startTime = startTime

    def clear(self):
        self.tables = {}
        self.finalTables = {}
        self.startTime = time.time()


def Summary():
    if not SummaryStatics.singleton:
        SummaryStatics.singleton = SummaryLocal(SummaryStatics.tables,
                SummaryStatics.finalTables)
    return SummaryStatics.singleton


def CreateSummary():
    return SummaryLocal(None, None)


def display_id(ref):
    if is_acm_object(ref):
        if 'Name' in dir(ref):
            return ref.Name()
        else:
            return ref.Oid()
    else:
        try:
            return ref.display_id()
        except:
            if ref.record_type == 'Price':
                return ref.prinbr
            return None


def is_mandatory_child(ref):
    return record_type(ref) == 'Leg'


def find_references_recursive(obj, references=()):
    children = obj.children()
    references = references or obj.reference_in(1)
    for index in range(len(references)):
        ref = references[index]
        if is_mandatory_child(ref) and ref.parent():
            references[index] = ref.parent()
    for child in children:
        references = references + find_references_recursive(child)
    return references


def find_references(obj, ref_dict, references=()):
    if obj and obj not in ref_dict:
        ref_list = find_references_recursive(obj, references)
        ref_dict[obj] = ref_list
        for ref in ref_list:
            find_references(ref, ref_dict)


def has_excluded_references(obj, excludeList):
    ref_dict = {}
    find_references(obj, ref_dict)
    collect_list = _collect_references(obj, ref_dict)
    record_types = [record_type(r) for r in collect_list]
    if any([r in excludeList for r in record_types]):
        FBDPCurrentContext.Logme()(
            'External references found to these excluded objects: {0}'.format(
            ', '.join(set([r for r in record_types if r in excludeList]))))
        return True, set([r for r in record_types if r in excludeList])

    return False, []


def _validate_own_order(aelTrade):
    """
    Return if illegality detected.  Check if trade has a own order whose
    instrument is different.
    """
    trdOdr = aelTrade.ordnbr
    if not trdOdr:
        return False
    trdOdrIns = trdOdr.insaddr
    if not trdOdrIns:
        return False
    trdIns = aelTrade.insaddr
    if aelTrade.insaddr.insaddr == trdOdrIns.insaddr:
        return False
    FBDPCurrentContext.Logme()('Illegal entity relationship. The own order '
            '[{0}] linked to instrument \'{1}\' is referenced by a trade '
            '[{2}] on a different instrument \'{3}\'.'.format(trdOdr.ordnbr,
            trdOdrIns.insid, aelTrade.trdnbr, trdIns.insid), 'WARNING')
    return True


def collect_references(obj, includeTrade, action, ignoreExtRef):

    ref_dict = {}
    find_references(obj, ref_dict)
    collect_list = _collect_references(obj, ref_dict)
    # Filtering out illegal case
    for aelEntity in collect_list:
        if aelEntity.record_type == 'Trade':
            if _validate_own_order(aelEntity):
                return False, collect_list
    # Figuring out the include list
    includeList = ['IntradayPrice', 'ListLeaf', 'MtmValue',
       'OrderBook', 'OwnOrder', 'OwnOrderLink', 'PriceDefinition',
       'PriceLinkDefinition', 'MatchLot', 'TradeAlias',
       'QuoteParameter', 'CombinationLink',
       'BusinessEventTrdLink']

    try:
        import FBDPHook
        hook = getattr(FBDPHook, 'objects_to_be_deleted_or_archived')
        includeList = hook()
    except ImportError:
        pass
    except AttributeError:
        pass

    # The trades could be handled separately, we need to add or remove
    # them from the List.based on includeTrade flag.
    if includeTrade:
        if 'Trade' not in includeList:
            includeList.append('Trade')
    else:
        if 'Trade' in includeList:
            includeList.remove('Trade')

    if record_type(obj) not in includeList:
        includeList.append(record_type(obj))

    exceptionList = []
    exceptionListType = []
    for ref in collect_list:
        if record_type(ref) not in includeList:
            exceptionList.append(ref)
            if record_type(ref) != 'Trade':
                exceptionListType.append(record_type(ref))

    if exceptionList:
        if exceptionListType:
            FBDPCurrentContext.Logme()('External reference %s found,'
                ' from the collect_references for object %s, but'
                ' not listed in FBDPHook.objects_to_be_deleted_or_archived.'
                 % (exceptionListType, display_id(obj)), 'WARNING')

        for entity in exceptionList:
            if record_type(entity) != 'Trade':
                FBDPCurrentContext.Summary().ignore(record_type(entity),
                    action,
                    'Unexpected external reference',
                    display_id(entity))

            remove_entity_from_list(entity, collect_list)

        if not ignoreExtRef:
            return False, collect_list

    return True, collect_list


def _collect_references(obj, ref_dict):
    collect_list = []
    if obj in ref_dict:
        ref_list = ref_dict[obj]
        del ref_dict[obj]
        for ref in ref_list:
            collect_list = collect_list + _collect_references(ref, ref_dict)
        collect_list.append(obj)
    return collect_list


def delete_child(clone, obj):
    if clone.original() == obj:
        FBDPCurrentContext.Summary().ok(obj,
                FBDPCurrentContext.Summary().DELETE, display_id(obj))
        clone.delete()
    else:
        for child in clone.children():
            delete_child(child, obj)


def create_clones_for_children(collect_list):
    clone_list = []
    handled_list = []
    delete_list = []
    for index in range(len(collect_list)):
        obj = collect_list[index]
        if obj.parent():
            top = obj.parent()
            while top.parent():
                top = top.parent()
            if not top in handled_list:
                found = None
                for clone in clone_list:
                    if clone.original() == top:
                        found = clone
                if not found:
                    clone = top.clone()
                    clone_list.append(clone)
                    collect_list[index] = clone
                else:
                    clone = found
                    delete_list.append(index)
                delete_child(clone, obj)
            else:
                delete_list.append(index)
        else:
            handled_list.append(obj)

    delete_list.reverse()
    for index in delete_list:
        del collect_list[index]


def remove_entity_from_list(entity, entityList):
    removeIndexList = []
    for index in range(len(entityList)):
        if entity == entityList[index]:
            removeIndexList.append(index)
    for index in removeIndexList:
        del entityList[index]


def remove_entities(removeList, entityList):
    for entity in removeList:
        remove_entity_from_list(entity, entityList)


def collect_references_out(entity, removeList):
    if entity in removeList:
        return
    else:
        removeList.append(entity)
        for ref in entity.reference_out():
            collect_references_out(ref, removeList)


def remove_exceptions(entityList, exceptionList):
    removeList = []
    for entity in entityList:
        if entity.record_type in exceptionList:
            collect_references_out(entity, removeList)
    remove_entities(removeList, entityList)


def disconnect_underlying_trades_from_exercised_ins(obj, entityList):
    removeList = []
    disconnected_list = []
    if record_type(obj) == "Instrument":
        for entity in entityList:
            if record_type(entity) == "Trade" and entity.insaddr != obj:
                if (entity.type in ("Exercise", "Assign")
                        and entity.connected_trdnbr.insaddr == obj):
                    removeList.append(entity)
                    clone = entity.clone()
                    clone.connected_trdnbr = entity.trdnbr
                    contract_trd = ael.Trade[entity.contract_trdnbr]
                    if contract_trd and contract_trd.insaddr == obj:
                        clone.contract_trdnbr = entity.trdnbr
                    disconnected_list.append(clone)
    remove_entities(removeList, entityList)
    return disconnected_list


def _delete_object(obj, Testmode, exceptionList=[]):
    acm.PollDbEvents()  # to prevent update collision
    if is_acm_object(obj):
        obj = acm_to_ael(obj)
    do_commit = 0
    action = FBDPCurrentContext.Summary().DELETE
    FBDPCurrentContext.Summary().commitEntries()
    try:
        ok, collect_list = collect_references(obj, True, action, True)
        if not ok:
            FBDPCurrentContext.Logme()('Failed to collect references for %s %s'
                % (obj.record_type, display_id(obj)), 'ERROR')
            return
        if exceptionList:
            exceptionList.append(obj.record_type)
        remove_exceptions(collect_list, exceptionList)
        create_clones_for_children(collect_list)
        disconnected_list = (obj and
                disconnect_underlying_trades_from_exercised_ins(obj,
                collect_list) or [])

        if disconnected_list:
            try:
                FBDPCurrentContext.Logme()('Disconnecting underlying trades '
                        'to instrument %s:' % (display_id(obj)), 'DEBUG')
                for d in disconnected_list:
                    if not Testmode:
                        d.commit()
                    FBDPCurrentContext.Logme()('Disconnected underlying Trade '
                            '%s.' % (display_id(d)), 'DEBUG')
                    FBDPCurrentContext.Summary().ok(d,
                            FBDPCurrentContext.Summary().UPDATE, display_id(d))
            except:
                FBDPCurrentContext.Logme()('Failed to disconnecting all '
                        'underlying trades to instrument %s.' %
                        (display_id(obj)), 'ERROR')
        try:
            ael.begin_transaction()
        except RuntimeError:
            pass
        else:
            do_commit = 1
        for ref in collect_list:
            if ref.original():
                FBDPCurrentContext.Summary().ok(ref,
                            FBDPCurrentContext.Summary().UPDATE,
                            display_id(ref))
                if not Testmode:
                    ref.commit()
                else:
                    FBDPCurrentContext.Logme()('Child Delete %s %s' %
                            (ref.record_type, display_id(ref)), 'DEBUG')
            else:
                if not Testmode:
                    try:
                        ref.delete()
                    except RuntimeError as msg:
                        error_msg = msg
                        if str(msg) == 'Attempt to modify original entity':
                            error_msg = ('Failed to delete %s with id %s '
                                    '(Parent object could not be found)' %
                                    (ref.record_type, display_id(ref)))
                        else:
                            error_msg = 'Failed to delete %s with id %s' % (
                                    ref.record_type, display_id(ref))
                        FBDPCurrentContext.Logme()(error_msg, 'ERROR')
                        FBDPCurrentContext.Summary().fail(ref, action,
                                error_msg, display_id(ref))
                    else:
                        FBDPCurrentContext.Logme()('Delete %s %s' %
                                (ref.record_type, display_id(ref)), 'DEBUG')
                        FBDPCurrentContext.Summary().ok(ref,
                                FBDPCurrentContext.Summary().DELETE,
                                display_id(ref))
                else:
                    FBDPCurrentContext.Logme()('Delete %s %s' %
                            (ref.record_type, display_id(ref)), 'DEBUG')
                    FBDPCurrentContext.Summary().ok(ref,
                            FBDPCurrentContext.Summary().DELETE,
                            display_id(ref))

    except RuntimeError as e:
        if do_commit:
            ael.abort_transaction()
        if str(e) == 'entity is deleted':
            return 1
        FBDPCurrentContext.Logme()(e, 'ERROR')
        FBDPCurrentContext.Summary().abortEntries()
        FBDPCurrentContext.Summary().fail(obj, action, 'Failed to %s '
                'instrument (%s)' % (action[:-1], e), display_id(obj))
        return 0

    if do_commit:
        try:
            ael.commit_transaction()
        except RuntimeError as e:
            ael.abort_transaction()
            FBDPCurrentContext.Logme()(e, 'ERROR')
            FBDPCurrentContext.Summary().abortEntries()
            FBDPCurrentContext.Summary().fail(obj, action, 'Failed to %s '
                    'instrument (%s)' % (action[:-1], e), display_id(obj))
            return 0
    FBDPCurrentContext.Summary().commitEntries()
    acm.PollDbEvents()  # to update acm with deleted entities
    return 1


def delete_object(obj, Testmode):
    return _delete_object(obj, Testmode)


def delete_obsolete_data(obj, Testmode, exceptionList=['Trade']):
    return _delete_object(obj, Testmode, exceptionList)


# Gets the useSelectedFundingDay extension attribute. If true, funding period
# is the same as the P&L period, with both end dates determined by the "Report
# Date" setting in the Valuation Parameters (which may or may not include a
# spot offset). If false, funding period is always calculated until the report
# end date, ignoring spot offset.
def getUseSelectedFundingDay():
    return 1
    # This funding attribute cannot be used until a solution can be found for
    # how to handle trades whose settlement periods (between trade and spot
    # days) cross month or year ends.
    extensionName = 'useSelectedFundingDay'
    context = acm.GetDefaultContext()
    extension = context.GetExtension('FExtensionAttribute', 'FObject',
            extensionName)
    attribute = acm.GetCalculatedValue(extension, '', extensionName)
    val = int(attribute.Value())
    if val not in (0, 1):
        FBDPCurrentContext.Logme()("Invalid value found for "
                "useSelectedFunding extension attribute. Defaulting to true.",
                'WARNING')
        val = 1
    return val


def getPremiumRounding(instrument):
    if instrument is None:
        raise TypeError("Parameter 'instrument' must not be null")
    roundingSpec = instrument.RoundingSpecification()
    if roundingSpec is None:
        return None
    roundings = acm.FRounding.Select("attribute='Premium'")
    rounding = next((r for r in roundings if
            r.RoundingSpec().Name() == roundingSpec.Name()), None)
    return rounding


def getPnLRounding(instrument):
    if instrument is None:
        raise TypeError("Parameter 'instrument' must not be null")
    roundingSpec = instrument.RoundingSpecification()
    if roundingSpec is None:
        return None
    roundings = acm.FRounding.Select("attribute='Profit And Loss'")
    rounding = next((r for r in roundings if
            r.RoundingSpec().Name() == roundingSpec.Name()), None)
    return rounding


def roundValueForInstrument(value, rounding):
    if not isinstance(value, float) and not isinstance(value, int):
        raise TypeError("Parameter 'value' should be of type float or int")
    value = float(value)
    if rounding is None:
        return value
    if type(rounding) != type(acm.FRounding()):
        raise TypeError("Parameter 'rounding' should be of type FRounding not "
                "of type " + str(type(rounding)))
    roundingFunction = acm.GetFunction('round', 3)
    return roundingFunction(value, rounding.Decimals(), rounding.Type())

def calibrateVolatility(vol):
    calibrationResults = acm.FCalibrationResults()
    vol.Calibrate(calibrationResults)
    calcRtn = 0
    errMsg = ''
    for result in calibrationResults.Results().Values():
        rtn = result.SolverResult().Success()
        if not rtn:
            errMsg = errMsg + result.SolverResult().ErrorMessage() + '  '
        calcRtn = calcRtn | (rtn == True)

    return calcRtn == 1, errMsg

def useNewCalibrationFramework(parameterName):
    param = acm.GetDefaultContext().GetExtension(
        'FParameters', 'FParameter', parameterName)
    useLegacyVolCalcFrame = param.Value()['UseLegacyVolCalibration']
    if type(useLegacyVolCalcFrame) == type(acm.FSymbol("")):
        return int(useLegacyVolCalcFrame.Text()) != 1
    else:
        return int(useLegacyVolCalcFrame) != 1

def supportNewCalibrationFramework(vol):
    framework = vol.Framework()
    structure_type = vol.StructureType()
    if structure_type == 'Benchmark' and \
       framework in ('Ho & Lee', 'Hull & White'):
        FBDPCurrentContext.Logme()(
            'New Calibration framework is not supported for '\
            'volatility %s with type %s and framework %s' \
            % (vol.Name(), structure_type, framework), 'DEBUG')
        return False
    return True

def getAttributesOfObject(obj):
    retVal = {}
    for attrNameOrFunc in dir(obj):
        func = getattr(obj, attrNameOrFunc)
        try:
            retVal[attrNameOrFunc] = func()
        except:
            pass
    return retVal

def printAttributesOfObject(obj, header=''):
    if (header == ''):
        print(('type of object = ' + str(type(obj))))
    else:
        print (header)
    print((getAttributesOfObject(obj)))


def AdditionalInfoMethod(entity, recType, additionalInfoName):
    query = 'name="{0}" and recType="{1}"'.format(
                         additionalInfoName, recType)
    infoSpecs = acm.FAdditionalInfoSpec.Select(query)
    if not infoSpecs:
        msg = 'Additional Spec "{0}" is missing'.format(
                            additionalInfoName)
        FBDPCurrentContext.Logme()(msg, 'WARNING')
        return None

    addinfos = entity.AdditionalInfo()
    method = getattr(addinfos, additionalInfoName)
    return method


def SetAdditionalInfoValue(entity, recType, additionalInfoName, value):
    method = AdditionalInfoMethod(entity, recType, additionalInfoName)
    if method:
        method(value)
        addinfos = entity.AddInfos()
        for i in addinfos:
            spec = i.AddInf()
            name = spec.FieldName()
            if name == additionalInfoName:
                return i
    return None


def GetAdditionalInfoValue(entity, recType, additionalInfoName):
    method = AdditionalInfoMethod(entity, recType, additionalInfoName)
    if method:
        return method()
    return None


def BusinessProcessQuery(subject_seqnbr, subject_type):
    return "subject_seqnbr={0} and subject_type={1}".format(
                        subject_seqnbr, subject_type)


def GetBusinessProcess(subjectId, subjectType):

    condition = BusinessProcessQuery(subjectId,
                subjectType)
    bps = acm.FBusinessProcess.Select(condition)
    if bps:
        return bps[0]
    else:
        return None


def getAdditionalInfoNames(recType):
    query = "recType={}".format(recType)
    infoSpecs = acm.FAdditionalInfoSpec.Select(query)
    return [i.Name() for i in infoSpecs]


def convert_stringlike(input):
    str_value = str(input)

    if isinstance(str_value, basestring):
        if str_value.lower() in ['false', 'no', '']:
            return False
        if str_value.lower() in ['true', 'yes']:
            return True

    try:
        return int(str_value)
    except ValueError:
        try:
            return float(str_value)
        except ValueError:
            pass

    return str_value


class FParamsParser(object):

    def __init__(self, value_converter=str):
        self.conv_func = value_converter

    def get_dict(self, param_group, verbose=True):
        values = {}
        p = acm.GetDefaultContext().GetExtension('FParameters',\
                                                 'FObject', param_group)
        try:
            template = p.Value()
        except AttributeError as e:
            if verbose:
                msg = 'Error getting parameters "{0}": {1}'.format(
                    param_group, str(e))
                FBDPCurrentContext.Logme()(msg, 'WARNING')
            return None
        else:
            for k in template.Keys():
                k = str(k)
                values[k] = self.conv_func(template.At(k))
        return values


def TradeGrouperForPositionSpecification(position_spec,
                        context=acm.GetDefaultContext()):
    context_name = context.Name()
    grouping_attrs = []
    for attr_def in position_spec.AttributeDefinitions():
        method_chain = attr_def.Definition()
        display_name = acm.Sheet.Column().MethodDisplayName(
            acm.FTrade, method_chain, context_name
        )
        grouping_attrs.append([display_name, method_chain, False])

    grouper = acm.Risk().CreateChainedGrouperDefinition(
        acm.FTrade, 'Portfolio', False, 'Instrument', True, grouping_attrs
    )
    return grouper

def valueFromFParameter(parameterGroup, specKey):
    value = None
    fParamDict = FParamsParser().get_dict(parameterGroup)
    if fParamDict and specKey in fParamDict:
        value = fParamDict[specKey]
    return value

def positionSpecFromFParameter(parameterGroup, specKey):
    positionSpec = None
    positionSpecName = valueFromFParameter(parameterGroup, specKey)
    if positionSpecName:
        positionSpec = acm.FPositionSpecification[positionSpecName]

    return positionSpec

def buildGrouperFromPositionSpec(positionSpec):
    grouperDefinition = TradeGrouperForPositionSpecification(positionSpec)
    grouper = grouperDefinition.AsPortfolioSheetGrouper()
    #for ag in grouper.Groupers():
    #    print ag
    return grouper

def CreateAdditionalInfo(name, recType, dataTypeGroup, dataTypeType, description='', subTypes=[], defaultValue=None, mandatory=0):
    # pylint: disable-msg=W0102
    addInfoSpec = acm.FAdditionalInfoSpec[name]
    if addInfoSpec:
        FBDPCurrentContext.Logme()('AdditionalInfoSpec with name "%s" already exists' % name)
        return addInfoSpec

    enumNameForDataTypes = 'B92StandardType' if dataTypeGroup == 'Standard' else 'B92RecordType'
    try:
        dataTypeTypeAsInt = acm.FEnumeration['enum(' + enumNameForDataTypes + ')'].Enumeration(dataTypeType)
    except RuntimeError as err:
        FBDPCurrentContext.Logme()('Failed to translate %s to data type for AdditionalInfoSpec "%s" on %s: %s'
                     % (dataTypeType, name, recType, err), 'ERROR')
        raise

    addInfoSpec = acm.FAdditionalInfoSpec(name=name,
                                          recType=recType,
                                          dataTypeGroup=dataTypeGroup,
                                          description=description,
                                          dataTypeType=dataTypeTypeAsInt,
                                          defaultValue=defaultValue,
                                          mandatory=mandatory )
    for subType in subTypes:
        addInfoSpec.AddSubType(subType)
    try:
        addInfoSpec.Commit()
    except StandardError as err:
        FBDPCurrentContext.Logme()('Failed commit AdditionalInfoSpec "%s" on %s: %s' % (name, recType, err), 'ERROR')
        raise

    FBDPCurrentContext.Logme()('Created AdditionalInfoSpec "%s" on %s' % (name, recType))
    return addInfoSpec

def TransitionExists(fromState, toStateName, eventName):
    existingTransitions = fromState.Transitions()
    for t in existingTransitions:
        if t.EventName() in (eventName) and t.ToState().Name() in (toStateName):
            return True
    return False

def DeleteObsoleteTransitions(fromState, newTransitions):
    existingTransitions = fromState.Transitions()
    for t in existingTransitions:
        found = False
        tranEventName = t.EventName()
        tranToStateName = t.ToState().Name()
        for eventName, toStateName in newTransitions.items():
            if tranEventName in (eventName) and tranToStateName in (toStateName):
                found = True
                break
        if not found:
            t.Delete()
            FBDPCurrentContext.Logme()('Deleted event %s from state %s to %s' \
                % (tranEventName, fromState.Name(), tranToStateName))


def CreateStateTransition(stateChart, fromStateName, toStateName, eventName):
    event = acm.FStateChartEvent(eventName)
    states = stateChart.StatesByName()
    fromState = states.At(fromStateName)
    toState = states.At(toStateName)
    fromState.CreateTransition(event, toState)
    stateChart.Commit()
    FBDPCurrentContext.Logme()(
        'Create transition, create event %s from state %s to %s' \
            % (eventName, fromStateName, toStateName))

def CreateNewStates(stateChart, newStateNames):
    for state_name in newStateNames:
        FBDPCurrentContext.Logme()('Create new state: %s' % (state_name))
        stateChart.CreateState(state_name)
    stateChart.Commit()


def UpdateStateChart(chartName, definition):
    FBDPCurrentContext.Logme()(
        'Update the state chart %s' % (chartName))

    state_names = definition.keys()
    for all_transitions in definition.values():
        state_names.extend(
            [s for s in all_transitions.values()
                if s not in state_names])

    updatedStateNames = [s for s in state_names
                            if s not in ('Ready', 'Error')]

    stateC = acm.FStateChart[chartName]
    oldStateNames = [s for s in stateC.StatesByName()
                        if s not in ('Ready', 'Error')]

    newStateNames = [s for s in updatedStateNames
                        if s not in oldStateNames]
    CreateNewStates(stateC, newStateNames)
    states = stateC.StatesByName()

    #update the transition
    for state_name, transitions in definition.items():
        state = states.At(state_name)
        DeleteObsoleteTransitions(state, transitions)
        for event_name, to_state_name in transitions.items():
            if not TransitionExists(state, to_state_name, event_name):
                CreateStateTransition(stateC, state_name, to_state_name, event_name)

    return
