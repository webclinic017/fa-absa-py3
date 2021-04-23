import acm
import re
DEBUG_LEVEL = 1
'''================================================================================================
================================================================================================'''
class UsedDates():
    def __init__(self, currecny_pair):
        self._CURRENCYPAIR      = currecny_pair
        self._CALENDAR          = acm.FCalendar['ZAR Johannesburg']
        self._INCEPTION         = '1970-01-01'
        self._TODAY             = acm.Time.DateToday()
        self._TIMENOW           = acm.Time.TimeNow()
        self._FIRSTOFMONTH      = acm.Time.FirstDayOfMonth(self._TODAY)
        self._FIRSTOFYEAR       = acm.Time.FirstDayOfYear(self._TODAY)
        self._PREVBUSDAY        = self._CALENDAR.AdjustBankingDays(self._TODAY, -1)
        self._TWOBUSDAYSAGO     = self._CALENDAR.AdjustBankingDays(self._TODAY, -2)  
        self._TWODAYSAGO        = acm.Time.DateAddDelta(self._TODAY, 0, 0, -2)
        self._YESTERDAY         = acm.Time.DateAddDelta(self._TODAY, 0, 0, -1)
        self._SPOT              = self._CURRENCYPAIR.SpotDate(self._TODAY)
        self._TIMEONLY          = self.get_time_only()
       
        self._DATEDICT          =   {'CURRENCYPAIR':self._CURRENCYPAIR.Name(),\
                                    'CALENDAR':self._CALENDAR.Name(),\
                                    'INCEPTION':self._INCEPTION,\
                                    'TODAY':self._TODAY,\
                                    'TIMENOW':self._TIMENOW,\
                                    'FIRSTOFMONTH':self._FIRSTOFMONTH,\
                                    'FIRSTOFYEAR':self._FIRSTOFYEAR,\
                                    'PREVBUSDAY':self._PREVBUSDAY,\
                                    'TWOBUSDAYSAGO':self._TWOBUSDAYSAGO,\
                                    'TWODAYSAGO':self._TWODAYSAGO,\
                                    'YESTERDAY':self._YESTERDAY,\
                                    'SPOT':self._SPOT}

    def get_time_only(self):
        tuple = acm.Time.TimeOnlyMs().split(':')
        return tuple[0] + '-' + tuple[1]  + '-' + tuple[2]
    
        return acm.Time.DateAdjustPeriod(self._TODAY, period)  #this should really be currency pair...

    def add_period(self, period):
        return acm.Time.DateAdjustPeriod(self._TODAY, period)  #this should really be currency pair...
        
    def get_date_from_period(self, period):
        if period in self._DATEDICT.keys():
            return self._DATEDICT[period]
        else:
            try:
                return self.add_period(period)
            except Exception, e:
                return period
'''================================================================================================
================================================================================================'''
def get_value(m, object):
    node = m.mbf_find_object(object)
    if node != None:
        return node.mbf_get_value()
    return node
'''================================================================================================
Force a key, value pair into AMB Message, e.g set or replace. If empty value, remove key from message.
================================================================================================'''
def setOrReplace(mess, key, value):
    obj = mess.mbf_find_object(key, 'MBFE_BEGINNING')
    if obj:
        if value:
            mess.mbf_replace_string(key, value)
        else:
            mess.mbf_remove_object()
    elif value:
        mess.mbf_add_string(key, value)
'''================================================================================================
================================================================================================'''
def setDatePeriod(dates, mess, key):
    date = get_value(mess, key)
    date = dates.get_date_from_period(date)
    setOrReplace(mess, key, date)
'''================================================================================================
================================================================================================'''
def process_trade(trade_message,suggestid,testtype,dates,count,inside = True):

    setDatePeriod(dates, trade_message, 'TIME')
    setDatePeriod(dates, trade_message, 'VALUE_DAY')
    setDatePeriod(dates, trade_message, 'ACQUIRE_DAY')
    optkey = get_value(trade_message, 'OPTIONAL_KEY')
    trade_message.mbf_add_string('TEXT1', testtype)
    payment = trade_message.mbf_find_object('PAYMENT')

    if payment:
        setDatePeriod(dates, payment, 'VALID_FROM')
        setDatePeriod(dates, payment, 'PAYDAY')

    if inside == False:
        setOrReplace(trade_message, 'INSADDR.EXTERN_ID1', suggestid)
        setOrReplace(trade_message, 'CONTRACT_TRDNBR.OPTIONAL_KEY', suggestid)
        if 'CL' in testtype:        
            suggestid = suggestid + '_CL_' + str(count)
        if 'DD' in testtype:        
            suggestid = suggestid + '_DD_' + str(count)

        if 'EX' in testtype:        
            suggestid = suggestid + '_EX_' + str(count)

    setOrReplace(trade_message, 'OPTIONAL_KEY', suggestid)

'''================================================================================================
can use count rather then suggest1/2
================================================================================================'''
def process_instrument(insobj, testtype, dates, curr_pair, system):

    instype             = get_value(insobj, 'INSTYPE')
    message_insid       = get_value(insobj, 'INSID')

    if instype in ['INS_ODF', 'ODF']:
        exerciseev_message  = insobj.mbf_find_object('EXERCISEEVENT')
        underlying = get_value(insobj, 'UND_INSADDR.INSID')
        extenrid = dates._TIMEONLY + '|' + system + '|' + dates._TIMEONLY
        insid = curr_pair + '/' + underlying + '/' + dates._TIMEONLY   
        suggestno = re.sub("\D", "", insid)

        if 'SUGGEST1' == message_insid: 
            insid = '1_' + insid
            extenrid = '1_' + extenrid

        if 'SUGGEST2' == message_insid: 
            insid = '2_' + insid
            extenrid = '2_' + extenrid

        setDatePeriod(dates, exerciseev_message, 'END_DAY')
        setDatePeriod(dates, exerciseev_message, 'START_DAY')
        setOrReplace(insobj, 'INSID', insid)
        setOrReplace(insobj, 'EXTERN_ID1', extenrid)   

        trade_message  = insobj.mbf_find_object('TRADE') 
        process_trade(trade_message, extenrid, testtype, dates, 1)

    return extenrid
'''================================================================================================
--fail properly
================================================================================================'''
def receiver_modify(message):
    source = get_value(message, 'SOURCE')
    
    if source == 'TESTCASE':
        type        = get_value(message, 'TYPE')
        test        = get_value(message, 'TEST')
        curr_pair   = get_value(message, 'CURRENCY_PAIR')
        time        = get_value(message, 'TIME')
        system      = get_value(message, 'TRADESYSTEM')    
        dates       = None

        print '=' * 100
        if curr_pair != None:
            dates = UsedDates(acm.FCurrencyPair[curr_pair])
            
        setDatePeriod(dates, message, 'TIME')
        suggest_dictionary = {}

        if type == 'INSERT_INSTRUMENT':
            insobj = message.mbf_first_object()
            while insobj:
                if insobj.mbf_get_value() == 'INSTRUMENT':
                    message_insid = get_value(insobj, 'INSID')
                    suggestid = process_instrument(insobj, test, dates, curr_pair, system)
                    suggest_dictionary[message_insid] = suggestid
                    #(mklimke) get the trade out side of the instrument
                    #(mklimke) we could have checked the trade process here , that would have been better
                    if 'DD' in test or 'CL' in test: 
                        obj = message.mbf_first_object()
                        count = 0
                        while obj:
                            if obj.mbf_get_value() == 'TRADE': 
                                count = count + 1
                                process_trade(obj, suggestid, test, dates, count, False)  #What will the first suggest id be ?
                            obj = message.mbf_next_object()
                insobj = message.mbf_next_object()

            if 'EX' in test: #two instrument that why we had to move it out
                obj = message.mbf_first_object()
                count = 0
                while obj:
                    if obj.mbf_get_value() == 'TRADE': 
                        count = count + 1
                        process_trade(obj, suggest_dictionary['SUGGEST1'], test, dates, count, False)  #What will the first suggest id be ?
                    obj = message.mbf_next_object()
        

            #(mklimke) be very carfull of where the pointer is , look at the memeory address.
            if 'EX' in test: 
                obj = message.mbf_find_object('BUSINESSEVENT') #have to think about pointers
                first = obj.mbf_first_object()
                one = obj.mbf_next_object()
                event_type = one.mbf_find_object('TRADE_EVENT_TYPE').mbf_get_value()
                if 'TRADE_EVENT_TYPE_NEW':
                    setOrReplace(one, 'TRDNBR.OPTIONAL_KEY', suggest_dictionary['SUGGEST2'])
                else:
                    setOrReplace(one, 'TRDNBR.OPTIONAL_KEY', suggest_dictionary['SUGGEST1'])
                two = obj.mbf_next_object()
                event_type = two.mbf_find_object('TRADE_EVENT_TYPE').mbf_get_value()
                if 'TRADE_EVENT_TYPE_CANCEL':
                    setOrReplace(two, 'TRDNBR.OPTIONAL_KEY', suggest_dictionary['SUGGEST1'])
                else:
                    setOrReplace(two, 'TRDNBR.OPTIONAL_KEY', suggest_dictionary['SUGGEST2'])

    if DEBUG_LEVEL == 1:
        print message.mbf_object_to_string_xml()
    print '=' * 100
    return message
'''================================================================================================
acm.Time.DatePeriodCount('3d')    #returns 3
acm.Time.DatePeriodUnit('3d')     #returns "Days"
ModifyDate(cal2, cal3, date) 
acm.AMBAMessage.CreateSimulatedObject(message)
SuggestName()
value_day = None
if type == 'INSERT_TRADE':
    trade_message = message.mbf_find_object('TRADE','MBFE_BEGINNING')
    value_day = trade_message.mbf_find_object('VALUE_DAY','MBFE_BEGINNING').mbf_get_value()
================================================================================================'''
